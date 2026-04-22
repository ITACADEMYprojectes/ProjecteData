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
-- no hay valores null en apartment_id

-- column city
-- miro si hay valores null en city
SELECT *
FROM Tourist_Accommodation
WHERE city IS NULL;
-- no hay valores null en city

-- column room_type
-- miro si hay valores null en room_type
SELECT *
FROM Tourist_Accommodation
WHERE room_type IS NULL;
-- no hay valores null en room_type

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

-- ! Por analisi de experiencia de cliente: Hay que eliminar la filas con review_scores_rating = null

-- Creo una vista con solo la columnas que necesito
-- Si necesito borrar la vista: DROP VIEW vista_analisi
CREATE VIEW vista_analisi AS
SELECT
	apartment_id,
    name,
    room_type,
    city,
    price,
    review_scores_rating
FROM Tourist_Accommodation;

SELECT *
FROM vista_analisi;


-- Verifico que las columnas que necesito tengan valores coherentes:
-- La columna review_scores_rating presenta valores entre 600 y 1000, mientras que el rango esperado es 0-100.
-- Esto se debe a que los valores están escalados x10.
-- ! Para los análisis de experiencia de cliente, hay que dividir los valores entre 10

-- Creo copia de la tabla para hacer el cleaning:
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
-- todo correcto.

-- Borro las filas con id_apartment duplicado y tengo solo el mas reciente
-- Si necesito borrar la tabla: DROP TABLE copy_ta_latest
CREATE TABLE IF NOT EXISTS copy_ta_latest AS
SELECT *
FROM copy_ta t1
WHERE STR_TO_DATE(insert_date, '%d/%m/%Y') = (
   SELECT MAX(STR_TO_DATE(insert_date, '%d/%m/%Y')) -- mas reciente
   FROM copy_ta t2
   WHERE t1.apartment_id = t2.apartment_id
);

SELECT *
FROM copy_ta_latest
LIMIT 10;

SELECT COUNT(*) FROM copy_ta;
-- 7001 filas totales
-- 268 duplicados
-- Espero encontrar 6733 filas en la nueva tabla copy_ta_latest (7001-268)

SELECT COUNT(*) FROM copy_ta_latest;
-- 6733 filas, como esperado.

DROP TABLE copy_ta;
RENAME TABLE copy_ta_latest TO copy_ta;

SET SQL_SAFE_UPDATES = 1;

-- IMPUTACION
-- Imputacion del precio

-- Miro si el precio falta por algun motivo
SELECT *
FROM copy_ta
WHERE price IS NULL;
-- no hay nada raro, puedo continuar con la imputacion del precio.

-- miro tambien si la falta del precio es debida al ser alojamentos no activos (has_availability=null)
SELECT has_availability, COUNT(*) AS n
FROM copy_ta
WHERE price IS NULL
GROUP BY has_availability;
-- aqui tampoco: no hay nada raro, puedo continuar con la imputacion del precio.


SELECT city, COUNT(*) AS numero_apartment_id_null
FROM copy_ta
WHERE price IS NULL
GROUP BY city
ORDER BY numero_apartment_id_null DESC;
-- los apartment con precio null estan concentrados en Mallorca, BCN

SELECT room_type, COUNT(*) AS numero_apartment_id_null
FROM copy_ta
WHERE price IS NULL
GROUP BY room_type
ORDER BY numero_apartment_id_null DESC;
-- los apartment con precio null estan concentrados en la tipolojia de alojamento Entire home/apt

SELECT accommodates, COUNT(*) AS numero_apartment_id_null
FROM copy_ta
WHERE price IS NULL
GROUP BY accommodates
ORDER BY numero_apartment_id_null DESC;
-- los apartment con precio null estan mas distribuidos respecto el numero de accomodates

-- Imputacion basada en: tres variables para la imputación: city + room_type

-- Agrupo los alojamientos según: city, room_type
SELECT city, room_type, COUNT(*) AS numero_observaciones
FROM copy_ta
WHERE price IS NOT NULL
GROUP BY city, room_type
ORDER BY COUNT(*);
-- Algunos grupos tienen pocas observaciones, no tendría sentido tomar la media.
-- Hago una imputación por niveles.

-- Primero, creo nueva columna por el precio imputado
ALTER TABLE copy_ta
ADD COLUMN price_imputed DECIMAL(10,2);

-- copio los precios ya presentes
SET SQL_SAFE_UPDATES = 0;

UPDATE copy_ta
SET price_imputed = price
WHERE price IS NOT NULL;

SET SQL_SAFE_UPDATES = 1;


-- Imputación usando city + room_type
UPDATE copy_ta t1
JOIN (
    SELECT 
        city,
        room_type,
        ROUND(AVG(price), 2) AS avg_price
    FROM copy_ta
    WHERE price IS NOT NULL
    GROUP BY city, room_type
) t2
ON t1.city = t2.city
AND t1.room_type = t2.room_type
SET t1.price_imputed = t2.avg_price
WHERE t1.price IS NULL;

-- Imputamos los casos que siguen NULL usando solo la media por ciudad.
UPDATE copy_ta t1
JOIN (
    SELECT 
        city,
        ROUND(AVG(price), 2) AS avg_price
    FROM copy_ta
    WHERE price IS NOT NULL
    GROUP BY city
) t2
ON t1.city = t2.city
SET t1.price_imputed = t2.avg_price
WHERE t1.price IS NULL
  AND t1.price_imputed IS NULL;
  
-- Calculamos media global
SET @global_price = (
    SELECT ROUND(AVG(price), 2)
    FROM copy_ta
    WHERE price IS NOT NULL
);

-- Aplicamos fallback global
UPDATE copy_ta
SET price_imputed = @global_price
WHERE price IS NULL
  AND price_imputed IS NULL;
  
SELECT COUNT(*)
FROM copy_ta
WHERE price_imputed IS NULL;

SELECT *
FROM copy_ta
LIMIT 10;

-- Imputacion del review_score
-- Imputación de review_scores_rating_clean usando otras métricas
UPDATE copy_ta
SET review_scores_rating_clean =
(
    (
        IFNULL(review_scores_cleanliness, 0) +
        IFNULL(review_scores_accuracy, 0) +
        IFNULL(review_scores_checkin, 0) +
        IFNULL(review_scores_communication, 0) +
        IFNULL(review_scores_location, 0) +
        IFNULL(review_scores_value, 0)
    )
    /
    (
        (review_scores_cleanliness IS NOT NULL) +
        (review_scores_accuracy IS NOT NULL) +
        (review_scores_checkin IS NOT NULL) +
        (review_scores_communication IS NOT NULL) +
        (review_scores_location IS NOT NULL) +
        (review_scores_value IS NOT NULL)
    )
) * 10

WHERE review_scores_rating_clean IS NULL

-- Solo imputamos si al menos uno de los campos tiene valor
AND (
    review_scores_cleanliness IS NOT NULL OR
    review_scores_accuracy IS NOT NULL OR
    review_scores_checkin IS NOT NULL OR
    review_scores_communication IS NOT NULL OR
    review_scores_location IS NOT NULL OR
    review_scores_value IS NOT NULL
);

SELECT COUNT(*)
FROM copy_ta
WHERE review_scores_rating_clean IS NULL;

SELECT *
FROM copy_ta
LIMIT 10;
