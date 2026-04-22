/*
Registros totales: 7001
ID Unico: 6733
ID extra: 268
ID Duplicado: 0 
*/

-- Miro el dataset
SELECT *
FROM Tourist_Accommodation
LIMIT 10;

DESCRIBE Tourist_Accommodation;

-- Miro la columna apartment_id
-- Cuantas sonos las filas? Quantos apartment_id unicos? Cuantos apartment_id duplicados? (Ya sé que no tengo filas duplicadas)
SELECT 
    COUNT(*) AS filas_tot, -- filas totales
    COUNT(DISTINCT apartment_id) AS unicos_id_apartments, -- apartment_id unicos
    COUNT(*) - COUNT(DISTINCT apartment_id) AS duplicados_id_apartments -- apartment_id duplicados
FROM Tourist_Accommodation;
-- tengo algunos apartment_id que se repiten (entonces hay mas filas que hablan del mismo alojamento)

-- Cuantas veces se repiten los apartment_id duplicados?
SELECT apartment_id, COUNT(*) AS id_apartment_duplicados
FROM Tourist_Accommodation
GROUP BY apartment_id
HAVING COUNT(*) > 1;

-- voy a ver en que son distintas las filas con mismo apartment_id
SELECT *
FROM Tourist_Accommodation
WHERE apartment_id IN (
    SELECT apartment_id
    FROM Tourist_Accommodation
    GROUP BY apartment_id
    HAVING COUNT(*) > 1
)
ORDER BY apartment_id;
-- parece sea la fecha. Tengo que comprobarlo.
-- La fecha es en formato VARCHAR
-- ! Hay que transformar la fecha en datatype

-- compruebo que la cosa que cambia es la fecha
SELECT apartment_id, insert_date
FROM Tourist_Accommodation
WHERE apartment_id IN (
    SELECT apartment_id
    FROM Tourist_Accommodation
    GROUP BY apartment_id
    HAVING COUNT(*) > 1
)
ORDER BY apartment_id, STR_TO_DATE(insert_date, '%d/%m/%Y'); -- cambio momentáneamente el formato a fecha para ordenarlo correctamente.
-- lo que cambia es la insert_date: hay apartment_id duplicados porqué son snapshot del mismo alojamento a lo largo del tiempo.

-- ! Por analisi de marketing y analisi de clientes: Hay que eliminar las filas con apartment_id duplicados
-- y quedarse solo con las filas con insert_date mas reciente.
                      

-- CUANTAS VARIABLES CATEGORIALES TENGO? (city y room_type)                        
-- Miro cuantas distintas tipolojia de alojamento hay
SELECT DISTINCT(room_type)
FROM Tourist_Accommodation;

-- Miro cuantas distintas ciutades hay
SELECT COUNT(DISTINCT city)
FROM Tourist_Accommodation;

-- y cuales
SELECT DISTINCT city
FROM Tourist_Accommodation;

-- DATA CLEANING

-- VALORES NULL

-- column apartment_id
-- miro si hay valores null en apartment_id
SELECT *
FROM Tourist_Accommodation
WHERE apartment_id IS NULL;
-- NO hay valores null en apartment_id

-- column city
-- miro si hay valores null en city
SELECT *
FROM Tourist_Accommodation
WHERE city IS NULL;
-- NO hay valores null en city

-- column room_type
-- miro si hay valores null en room_type
SELECT *
FROM Tourist_Accommodation
WHERE room_type IS NULL;
-- NO hay valores null en room_type

-- column price
-- miro si hay valores null en price
SELECT *
FROM Tourist_Accommodation
WHERE price IS NULL;
-- HAY valores null en price

SELECT COUNT(*)
FROM Tourist_Accommodation
WHERE price IS NULL;
-- Hay 131 valores null en price

-- ! Por analisi de Marketing: Hay que eliminar la filas con price = null

-- column review_scores_rating
-- miro si hay valores null en review_scores_rating
SELECT *
FROM Tourist_Accommodation
WHERE review_scores_rating IS NULL;
-- HAY valores null en review_scores_rating

SELECT COUNT(*)
FROM Tourist_Accommodation
WHERE review_scores_rating IS NULL;
-- Hay 1.327 valores null en review_scores_rating

-- Quantas de la filas con review_scores_rating=null tienen también las otras metricas de rating=null?
SELECT
    COUNT(*) AS total_review_null,
    SUM(CASE WHEN review_scores_cleanliness IS NULL THEN 1 ELSE 0 END) AS null_cleanliness,
    SUM(CASE WHEN review_scores_accuracy IS NULL THEN 1 ELSE 0 END) AS null_accuracy,
    SUM(CASE WHEN review_scores_checkin IS NULL THEN 1 ELSE 0 END) AS null_checkin,
    SUM(CASE WHEN review_scores_communication IS NULL THEN 1 ELSE 0 END) AS null_communication,
    SUM(CASE WHEN review_scores_location IS NULL THEN 1 ELSE 0 END) AS null_location,
    SUM(CASE WHEN review_scores_value IS NULL THEN 1 ELSE 0 END) AS null_value
FROM Tourist_Accommodation
WHERE review_scores_rating IS NULL;
-- Las filas con review_scores_rating=null tienen también las otras metricas de rating nulas.
/*Los valores nulos en review_scores_rating no representan datos faltantes, sino la ausencia de reseñas. 
Esto se confirma porque todas las métricas de review están simultáneamente vacías en estos casos. 
*/

-- VALORES COHERENTES

-- Verifico que las columnas que necesito tengan valores coherentes:
SELECT
	apartment_id,
    name,
    room_type,
    city,
    price,
    review_scores_rating
FROM Tourist_Accommodation;
-- La columna review_scores_rating presenta valores entre 600 y 1000, mientras que el rango esperado es 0-100.
-- Esto se debe a que los valores están escalados x10.
-- ! Para los análisis de experiencia de cliente, hay que dividir los valores entre 10

-- CLEANING

-- Creo copia de la tabla para hacer el cleaning.
-- Si necesito borrar la tabla: DROP TABLE copy_ta
CREATE TABLE IF NOT EXISTS copy_ta AS
SELECT *
FROM Tourist_Accommodation;

SELECT *
FROM copy_ta
LIMIT 10;

DESCRIBE copy_ta;

SET SQL_SAFE_UPDATES = 0;

ALTER TABLE copy_ta
ADD COLUMN review_scores_rating_clean INT;

UPDATE copy_ta
SET review_scores_rating_clean = review_scores_rating/10
WHERE review_scores_rating IS NOT NULL;

SELECT *
FROM copy_ta
LIMIT 10;

-- compruebo que la transformación se ha realizado correctamente (o sea: que no se han creado nuevos nulls):
SELECT COUNT(*)
FROM copy_ta
WHERE review_scores_rating_clean IS NULL;

SELECT COUNT(*)
FROM copy_ta
WHERE review_scores_rating IS NULL;
-- El numero de nulls entre las 2 columnas es igual. Todo correcto.

-- Borro las filas con id_apartment duplicado y tengo solo el mas reciente. Lo hago su una nueva tabla (que después borreré).
-- Si necesito borrar la tabla: DROP TABLE copy_ta_latest
CREATE TABLE IF NOT EXISTS copy_ta_latest AS
SELECT *
FROM copy_ta t1
WHERE STR_TO_DATE(insert_date, '%d/%m/%Y') = (
   SELECT MAX(STR_TO_DATE(insert_date, '%d/%m/%Y')) -- mas reciente
   FROM copy_ta t2
   WHERE t1.apartment_id = t2.apartment_id
);

-- Miro el output:
SELECT *
FROM copy_ta_latest
LIMIT 10;

-- Compruebo que el numero de filas borradas sea justo:
SELECT COUNT(*) FROM copy_ta;
-- 7001 filas totales
-- 268 duplicados
-- Espero encontrar 6733 filas en la nueva tabla copy_ta_latest (7001-268)

SELECT COUNT(*) FROM copy_ta_latest;
-- 6733 filas, como esperado. Todo correcto.

-- Tengo solo la ultima tabla con las filas borradas (ahora tenemos un id_apartment unico y no nulo)
DROP TABLE copy_ta;
RENAME TABLE copy_ta_latest TO copy_ta;

SET SQL_SAFE_UPDATES = 1;

-- IMPUTACION
-- Imputacion del precio

-- Cuantos son los precios null?
SELECT 
    COUNT(*) AS total_rows,
    SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS price_null,
    ROUND(
        SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS percentuale_null
FROM copy_ta;
-- los precios null son el 1.8% del total.

-- Busco pattern:

-- Miro si el precio falta por algun motivo
SELECT *
FROM copy_ta
WHERE price IS NULL;
-- no veo nada raro, continuo con la busqueda de pattern.

-- miro tambien si la falta del precio es debida al ser alojamentos no activos (has_availability=null)
SELECT has_availability, COUNT(*) AS n
FROM copy_ta
WHERE price IS NULL
GROUP BY has_availability;
-- aqui tampoco: no hay nada raro: los alojamentos con precio null no es porqué no son activos.

-- Hay una correlacion entre precio nulos i fecha?
SELECT 
    insert_date,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS price_nulls
FROM copy_ta
GROUP BY insert_date
ORDER BY STR_TO_DATE(insert_date, '%d/%m/%Y');
-- Los valores nulos NO aumentan con el tiempo

-- distribución de los precios nulos por numero de accommodates:
SELECT
    accommodates,
    COUNT(*) AS total_anuncios,
    SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS anuncios_con_price_null,
    ROUND(
        SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS pct_price_null
FROM copy_ta
GROUP BY accommodates
ORDER BY accommodates;
-- Esto sugiere que los valores nulos en el precio se concentran en alojamientos de gran tamaño.


-- distribución de los precios nulos por tipo de alojamiento (room_type):
SELECT
    room_type,
    COUNT(*) AS total_anuncios,
    SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS anuncios_sin_precio,
    ROUND(
        SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS pct_price_null
FROM copy_ta
GROUP BY room_type
ORDER BY pct_price_null DESC;
-- aquì no veo ningun pattern que destaca

-- distribución de los precios nulos por ciutad:
SELECT
    city,
    COUNT(*) AS total_anuncios,
    SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS anuncios_sin_precio,
    ROUND(
        SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS pct_sin_precio
FROM copy_ta
GROUP BY city
ORDER BY pct_sin_precio DESC;
-- Mallorca tiene el 5.57% de alojamentos con precio null.

-- Para cada variable de review, calculo cuántos valores son NULL:
SELECT
    COUNT(*) AS total_price_null,
    -- Rating
    SUM(CASE WHEN review_scores_rating IS NULL THEN 1 ELSE 0 END) AS null_rating,
    ROUND(SUM(CASE WHEN review_scores_rating IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_null_rating,
    -- Cleanliness
    SUM(CASE WHEN review_scores_cleanliness IS NULL THEN 1 ELSE 0 END) AS null_cleanliness,
    ROUND(SUM(CASE WHEN review_scores_cleanliness IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_null_cleanliness,
    -- Accuracy
    SUM(CASE WHEN review_scores_accuracy IS NULL THEN 1 ELSE 0 END) AS null_accuracy,
    ROUND(SUM(CASE WHEN review_scores_accuracy IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_null_accuracy,
    -- Checkin
    SUM(CASE WHEN review_scores_checkin IS NULL THEN 1 ELSE 0 END) AS null_checkin,
    ROUND(SUM(CASE WHEN review_scores_checkin IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_null_checkin,
    -- Communication
    SUM(CASE WHEN review_scores_communication IS NULL THEN 1 ELSE 0 END) AS null_communication,
    ROUND(SUM(CASE WHEN review_scores_communication IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_null_communication,
    -- Location
    SUM(CASE WHEN review_scores_location IS NULL THEN 1 ELSE 0 END) AS null_location,
    ROUND(SUM(CASE WHEN review_scores_location IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_null_location,
    -- Value
    SUM(CASE WHEN review_scores_value IS NULL THEN 1 ELSE 0 END) AS null_value,
    ROUND(SUM(CASE WHEN review_scores_value IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_null_value
FROM copy_ta
WHERE price IS NULL;
-- Todos los apartamentos con precio nulo que no tienen un review_scores_rating tampoco tienen ninguna de las métricas de reseñas completadas.
-- Un 36% de los apartamentos sin precio no tienen completada la información de reseñas.

-- Imputacion precio
-- Imputacion basada en: 2 variables para la imputación: city+room_type

-- Agrupo los alojamientos según: city, room_type, accomodates
SELECT city, room_type, accommodates, COUNT(*) AS numero_observaciones
FROM copy_ta
WHERE price IS NOT NULL
GROUP BY city, room_type, accommodates
ORDER BY COUNT(*);
-- Algunos grupos tienen pocas observaciones, no tendría sentido tomar la media.

-- Agrupo los alojamientos según: city, room_type
SELECT city, room_type, COUNT(*) AS numero_observaciones
FROM copy_ta
WHERE price IS NOT NULL
GROUP BY city, room_type
ORDER BY COUNT(*);
-- Algunos grupos tienen pocas observaciones, no tendría sentido tomar la media.

-- Cómo se distribuyen los precios dentro de cada grupo de city+room_type?
SELECT
    city,
    room_type,
    COUNT(*) AS numero_observaciones,
    MIN(price) AS precio_minimo,
    MAX(price) AS precio_maximo,
    ROUND(AVG(price), 2) AS precio_medio,
    ROUND(MAX(price) - MIN(price), 2) AS rango_precios
FROM copy_ta
WHERE price IS NOT NULL
GROUP BY city, room_type
ORDER BY numero_observaciones ASC;
/*Algunos grupos presentan muy pocas observaciones, lo que limita la posibilidad de estimar precios representativos. 
Además, en varios casos se observa una alta dispersión en los precios (rangos amplios entre el mínimo y el máximo), 
lo que indica una gran variabilidad dentro del grupo. 
Esto sugiere que el uso de la media podría no ser adecuado para la imputación en estos casos.*/

-- Que hemos decidido sobre la imputacion:
-- Hago imputacion por city y room_type (no accommodates)
-- Dejo los precios con valor nulo si el grupo de pertenencia (city + room_type) tiene demasiadas pocas observaciones
-- Por la imputacion tomamos la mediana (no la media)

-- Primero, creo nueva columna por el precio imputado
ALTER TABLE copy_ta
ADD COLUMN price_imputed DECIMAL(10,2);

-- copio los precios ya presentes
SET SQL_SAFE_UPDATES = 0;

UPDATE copy_ta
SET price_imputed = price
WHERE price IS NOT NULL;

SET SQL_SAFE_UPDATES = 1;

-- creo tabla con el numero de observaciones por cada grupo city+room_type
CREATE TABLE group_counts AS
SELECT 
    city,
    room_type,
    COUNT(*) AS n_observaciones
FROM copy_ta
WHERE price IS NOT NULL
GROUP BY city, room_type;

-- creo tabla con la mediana por cada grupo city+room_type
CREATE TABLE group_medians AS
WITH ordered_prices AS (
    SELECT
        city,
        room_type,
        price,
        ROW_NUMBER() OVER (
            PARTITION BY city, room_type
            ORDER BY price
        ) AS rn,
        COUNT(*) OVER (
            PARTITION BY city, room_type
        ) AS cnt
    FROM copy_ta
    WHERE price IS NOT NULL
)
SELECT
    city,
    room_type,
    ROUND(AVG(price), 2) AS median_price
FROM ordered_prices
WHERE rn IN (
    FLOOR((cnt + 1) / 2),
    FLOOR((cnt + 2) / 2)
)
GROUP BY city, room_type;

-- check del output:
SELECT * 
FROM group_medians;

-- creo tabla con la mediana de cada grupo city+room_type
CREATE TABLE median_price_by_group AS
SELECT 
    c.city,
    c.room_type,
    c.n_observaciones,
    m.median_price
FROM group_counts c
JOIN group_medians m
    ON c.city = m.city
   AND c.room_type = m.room_type;
   
SELECT *
FROM median_price_by_group;

-- creo la tabla filtrada: tengo solo los grupos city + room_type con un numero de observaciones > 10.
CREATE TABLE median_price_valid_groups AS
SELECT *
FROM median_price_by_group
WHERE n_observaciones >= 10;

-- Check del output:
SELECT *
FROM median_price_valid_groups
ORDER BY n_observaciones ASC, city, room_type;

-- hago la imputacion de los precios:
SET SQL_SAFE_UPDATES = 0;

UPDATE copy_ta AS t
JOIN median_price_valid_groups AS m
    ON t.city = m.city
   AND t.room_type = m.room_type
SET t.price_imputed = m.median_price
WHERE t.price IS NULL;

SET SQL_SAFE_UPDATES = 1;

-- Miro el output:
SELECT
    COUNT(*) AS total_price_null_original,
    SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS original_null,
    SUM(CASE WHEN price IS NULL AND price_imputed IS NOT NULL THEN 1 ELSE 0 END) AS imputados,
    SUM(CASE WHEN price IS NULL AND price_imputed IS NULL THEN 1 ELSE 0 END) AS no_imputados
FROM copy_ta;
-- la columna price_imputed ahora tiene los precios imputados.


-- Imputacion del review_score

-- Cuantos sonos los review_scores_rating nulos? ATTENCION! Trabajo con la nueva columna review_scores_rating_clean (con review escala 100)
SELECT 
    COUNT(*) AS total_rows,
    SUM(CASE WHEN review_scores_rating_clean IS NULL THEN 1 ELSE 0 END) AS review_null_clean,
    ROUND(
        SUM(CASE WHEN review_scores_rating_clean IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS pct_null_clean
FROM copy_ta;
-- Los review_scores_rating son el 19% del total.

SELECT
    COUNT(*) AS total_review_null,
    SUM(CASE WHEN number_of_reviews = 0 THEN 1 ELSE 0 END) AS n_reviews
FROM copy_ta
WHERE review_scores_rating_clean IS NULL;


SELECT
    COUNT(*) AS total_review_scores_rating_clean_null,
    SUM(CASE WHEN review_scores_cleanliness IS NULL THEN 1 ELSE 0 END) AS null_cleanliness,
    SUM(CASE WHEN review_scores_accuracy IS NULL THEN 1 ELSE 0 END) AS null_accuracy,
    SUM(CASE WHEN review_scores_checkin IS NULL THEN 1 ELSE 0 END) AS null_checkin,
    SUM(CASE WHEN review_scores_communication IS NULL THEN 1 ELSE 0 END) AS null_communication,
    SUM(CASE WHEN review_scores_location IS NULL THEN 1 ELSE 0 END) AS null_location,
    SUM(CASE WHEN review_scores_value IS NULL THEN 1 ELSE 0 END) AS null_value
FROM copy_ta
WHERE review_scores_rating_clean IS NULL;
/*Los valores nulos en review_scores_rating no representan datos faltantes, sino la ausencia de reseñas. 
Esto se confirma porque todas las métricas de review están simultáneamente vacías en estos casos. 
Por lo tanto, no se ha realizado imputación sobre estas variables.*/
