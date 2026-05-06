SELECT * 
FROM copy_ta04052026;

/*
Limpieza de datos

Variables analizadas:
city
neighbourhood_name
number_of_reviews
reviews_per_month
review_scores_rating
review_scores_location
availability_30
availability_60
availability_90
availability_365
minimum_nights
maximum_nights
*/

/*DATA QUALITY CHECK

Objetivo:
detectar posibles problemas antes de limpiar los datos.
*/

/*
1. Comprobar datatype de las variables
*/

DESCRIBE copy_ta04052026;

SELECT
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'copy_ta04052026'
AND COLUMN_NAME IN (
    'city',
    'neighbourhood_name',
    'number_of_reviews',
    'reviews_per_month',
    'review_scores_rating',
    'review_scores_location',
    'availability_30',
    'availability_60',
    'availability_90',
    'availability_365',
    'minimum_nights',
    'maximum_nights'
);

/*
2. Comprobar valores NULL
*/

SELECT
    SUM(CASE WHEN city IS NULL THEN 1 ELSE 0 END) AS null_city,
    SUM(CASE WHEN neighbourhood_name IS NULL THEN 1 ELSE 0 END) AS null_neighbourhood_name,
    SUM(CASE WHEN number_of_reviews IS NULL THEN 1 ELSE 0 END) AS null_number_of_reviews,
    SUM(CASE WHEN reviews_per_month IS NULL THEN 1 ELSE 0 END) AS null_reviews_per_month,
    SUM(CASE WHEN review_scores_rating_clean IS NULL THEN 1 ELSE 0 END) AS null_review_scores_rating_clean,
    SUM(CASE WHEN review_scores_location IS NULL THEN 1 ELSE 0 END) AS null_review_scores_location,
    SUM(CASE WHEN availability_30 IS NULL THEN 1 ELSE 0 END) AS null_availability_30,
    SUM(CASE WHEN availability_60 IS NULL THEN 1 ELSE 0 END) AS null_availability_60,
    SUM(CASE WHEN availability_90 IS NULL THEN 1 ELSE 0 END) AS null_availability_90,
    SUM(CASE WHEN availability_365 IS NULL THEN 1 ELSE 0 END) AS null_availability_365,
    SUM(CASE WHEN minimum_nights IS NULL THEN 1 ELSE 0 END) AS null_minimum_nights,
    SUM(CASE WHEN maximum_nights IS NULL THEN 1 ELSE 0 END) AS null_maximum_nights
FROM copy_ta04052026;

/*
Comprobar si los NULL de review_scores_rating_clean
también son NULL en review_scores_location
*/

SELECT
    review_scores_rating_clean,
    review_scores_location
FROM copy_ta04052026
WHERE review_scores_rating_clean IS NULL;

-- Todos los NULL de review_scores_rating_clean también son NULL en review_scores_location

/*
Comprobar si los NULL de review_scores_location 
también son NULL en review_scores_rating_clean
*/

SELECT
    review_scores_rating_clean,
    review_scores_location
FROM copy_ta04052026
WHERE review_scores_location IS NULL;

-- !Hay algun (15 casos) NULL de review_scores_location que NO son NULL en review_scores_rating_clean
-- Los registros con review_scores_location NULL serán excluidos del dataset final utilizado para el cálculo de la distancia euclidiana.

/*
3. Comprobar valores vacíos o con espacios en variables categóricas
city
neighbourhood_name
*/

SELECT *
FROM copy_ta04052026
WHERE city = ''
   OR TRIM(city) = ''
   OR neighbourhood_name = ''
   OR TRIM(neighbourhood_name) = '';

-- no hay nada

/*
4. Comprobar posibles espacios extra en variables categóricas
*/

SELECT
    city,
    TRIM(city) AS city_trimmed
FROM copy_ta04052026
WHERE city <> TRIM(city);

-- no hay nada

SELECT
    neighbourhood_name,
    TRIM(neighbourhood_name) AS neighbourhood_name_trimmed
FROM copy_ta04052026
WHERE neighbourhood_name <> TRIM(neighbourhood_name);

-- no hay nada

/*
5. Comprobar ciudades escritas de forma diferente
*/

SELECT
    city,
    COUNT(*) AS total_copy_ta04052026
FROM copy_ta04052026
GROUP BY city
ORDER BY city ASC;

-- todo ok

/*
6. Comprobar barrios escritos de forma diferente o demasiado raros
Los barrios con muy pocas apariciones pueden indicar errores de escritura.

Check de valores raros (con COUNT=1)
*/

SELECT city, neighbourhood_name, COUNT(*)
FROM copy_ta04052026
GROUP BY city, neighbourhood_name
HAVING COUNT(*) = 1
ORDER BY city, neighbourhood_name;

-- todo ok

-- Uniformar mayúsculas/minúsculas

-- Contro si existen duplicados debidos únicamente a mayúsculas/minúsculas:
SELECT
    LOWER(TRIM(neighbourhood_name)) AS neighbourhood_name_lower,
    COUNT(DISTINCT neighbourhood_name) AS n_variants,
    GROUP_CONCAT(DISTINCT neighbourhood_name ORDER BY neighbourhood_name SEPARATOR ' | ') AS variants
FROM copy_ta04052026
WHERE neighbourhood_name IS NOT NULL
  AND TRIM(neighbourhood_name) <> ''
GROUP BY LOWER(TRIM(neighbourhood_name))
HAVING COUNT(DISTINCT neighbourhood_name) > 1
ORDER BY n_variants DESC;

-- Check: si hay valores duplicados debidos a minuscola/maiuscola
-- No hay valores duplicados

/* Aunque no se hayan encontrados valores duplicados,
Se estandardiza neighbourhood_name en minúsculas utilizando LOWER(TRIM())
para garantizar consistencia y facilitar futuros análisis y agrupaciones.
*/

ALTER TABLE copy_ta04052026
ADD neighbourhood_name_clean VARCHAR(255);

SET SQL_SAFE_UPDATES = 0;

UPDATE copy_ta04052026
SET neighbourhood_name_clean = LOWER(TRIM(neighbourhood_name));

SET SQL_SAFE_UPDATES = 1;

-- Check resultado:
SELECT DISTINCT neighbourhood_name_clean
FROM copy_ta04052026
ORDER BY neighbourhood_name_clean;

-- check: comprueba si son todos lower case.
-- son todos lower case

SELECT COUNT(DISTINCT neighbourhood_name) AS number_distinct_neighbourhood_name
FROM copy_ta04052026;

SELECT COUNT(DISTINCT neighbourhood_name_clean) AS number_distinct_neighbourhood_name_clean
FROM copy_ta04052026;

-- me doy cuenta que hay un caso raro de 'ciudad universitaria' vs 'ciutad universitaria' >> compruebo que sean de ciutades diferentes
SELECT city, neighbourhood_name_clean, COUNT(*)
FROM copy_ta04052026
WHERE neighbourhood_name_clean LIKE '%universitaria%'
GROUP BY city, neighbourhood_name_clean;

-- check: sono de ciutades diferentes?
-- si lo son

-- me doy cuenta que hay un caso raro de 'ciudad jardin' vs 'ciudad jard�n' >> compruebo que sean de ciutades diferentes
SELECT city, neighbourhood_name_clean, COUNT(*)
FROM copy_ta04052026
WHERE neighbourhood_name_clean LIKE '%ciudad jar%'
GROUP BY city, neighbourhood_name_clean;

-- filtro solo los casos sospechos:

-- Busco los barrios que aparecen solo una vez dentro de cada ciudad para identificar posibles errores de escritura.
SELECT
    city,
    neighbourhood_name_clean,
    COUNT(*) AS n_rows
FROM copy_ta04052026
GROUP BY city, neighbourhood_name_clean
HAVING COUNT(*) = 1
ORDER BY city, neighbourhood_name_clean;

-- Check: Busco posibles variantes del mismo neighbourhood_name dentro de la misma ciudad.
-- No hay

-- Busco posibles errores de encoding que aparecen solo una vez dentro de cada ciudad.
SELECT
    city,
    neighbourhood_name_clean,
    COUNT(*) AS n_rows
FROM copy_ta04052026
WHERE neighbourhood_name_clean LIKE '%�%'
GROUP BY city, neighbourhood_name_clean
HAVING COUNT(*) = 1
ORDER BY city, neighbourhood_name_clean;

-- Check: Debo comprobar si estos valores son errores aislados o variantes incorrectas de otros neighbourhood_name.
-- todo ok

-- Aunque no tengo problema de duplicados debidos a �, cuento cuántos neighbourhood_name contienen caracteres corruptos de encoding (con �)
SELECT
    COUNT(DISTINCT neighbourhood_name_clean) AS corrupted_values
FROM copy_ta04052026
WHERE neighbourhood_name_clean LIKE '%�%';

-- Busco todos los neighbourhood_name con caracteres corruptos (�) y los agrupo por ciudad.
SELECT
    city,
    neighbourhood_name_clean,
    COUNT(*) AS n_rows
FROM copy_ta04052026
WHERE neighbourhood_name_clean LIKE '%�%'
GROUP BY city, neighbourhood_name_clean
ORDER BY city, neighbourhood_name_clean;

-- Check: hay que decidir si quiero hacer una corrección manual de los caracteres corruptos (�)
-- Por el momento: Decido de dajarlos asì porqué no sabria como cambiarlos y porqué no afectan la analisi,
-- ya que no sono variantes incorrectas del mismo neighbourhood_name de la misma ciudad.

-- Busco posibles variantes del mismo neighbourhood_name dentro de la misma ciudad causadas por diferencias de acentos.
SELECT
    city,
    neighbourhood_name_clean COLLATE utf8mb4_0900_ai_ci AS normalized_name,
    COUNT(DISTINCT neighbourhood_name_clean) AS n_variants,
    GROUP_CONCAT(DISTINCT neighbourhood_name_clean ORDER BY neighbourhood_name_clean SEPARATOR ' | ') AS variants
FROM copy_ta04052026
GROUP BY city, normalized_name
HAVING COUNT(DISTINCT neighbourhood_name_clean) > 1
ORDER BY city, n_variants DESC;

-- Check: Debo comprobar si las variantes corresponden realmente al mismo barrio y si conviene unificarlas en una única versión normalizada.
-- no hay nada


/*
7. Resumen estadístico de variables numéricas

Aquí NO miramos todos los valores distintos.
Miramos mínimos, máximos y medias para detectar valores sospechosos.
*/

SELECT
    MIN(number_of_reviews) AS min_number_of_reviews,
    MAX(number_of_reviews) AS max_number_of_reviews,
    AVG(number_of_reviews) AS avg_number_of_reviews,

    MIN(reviews_per_month) AS min_reviews_per_month,
    MAX(reviews_per_month) AS max_reviews_per_month,
    AVG(reviews_per_month) AS avg_reviews_per_month,

    MIN(review_scores_rating_clean) AS min_review_scores_rating_clean,
    MAX(review_scores_rating_clean) AS max_review_scores_rating_clean,
    AVG(review_scores_rating_clean) AS avg_review_scores_rating_clean,

    MIN(review_scores_location) AS min_review_scores_location,
    MAX(review_scores_location) AS max_review_scores_location,
    AVG(review_scores_location) AS avg_review_scores_location,

    MIN(availability_30) AS min_availability_30,
    MAX(availability_30) AS max_availability_30,
    AVG(availability_30) AS avg_availability_30,

    MIN(availability_60) AS min_availability_60,
    MAX(availability_60) AS max_availability_60,
    AVG(availability_60) AS avg_availability_60,

    MIN(availability_90) AS min_availability_90,
    MAX(availability_90) AS max_availability_90,
    AVG(availability_90) AS avg_availability_90,

    MIN(availability_365) AS min_availability_365,
    MAX(availability_365) AS max_availability_365,
    AVG(availability_365) AS avg_availability_365,

    MIN(minimum_nights) AS min_minimum_nights,
    MAX(minimum_nights) AS max_minimum_nights,
    AVG(minimum_nights) AS avg_minimum_nights,

    MIN(maximum_nights) AS min_maximum_nights,
    MAX(maximum_nights) AS max_maximum_nights,
    AVG(maximum_nights) AS avg_maximum_nights
FROM copy_ta04052026;

-- todo ok


/*
8. Comprobar valores imposibles en variables numéricas

availability_30 debe estar entre 0 y 30
availability_60 debe estar entre 0 y 60
availability_90 debe estar entre 0 y 90
availability_365 debe estar entre 0 y 365

minimum_nights no debería ser menor que 1
maximum_nights no debería ser menor que minimum_nights

Las puntuaciones no deberían estar fuera de su escala.
En Airbnb normalmente review_scores_rating puede estar entre 0 y 100
y review_scores_location entre 0 y 10.
*/

/*
Compruebo si availability_30 tiene valores fuera del rango válido entre 0 y 30.
*/

SELECT *
FROM copy_ta04052026
WHERE availability_30 < 0
   OR availability_30 > 30;
   
-- Check: Debo comprobar si aparecen disponibilidades negativas o superiores a 30 días.
-- No hay

/*
Compruebo si availability_60 tiene valores fuera del rango válido entre 0 y 60.
*/

SELECT *
FROM copy_ta04052026
WHERE availability_60 < 0
   OR availability_60 > 60;
   
-- Debo comprobar si aparecen disponibilidades negativas o superiores a 60 días.
-- no hay

/*
Compruebo si availability_90 tiene valores fuera del rango válido entre 0 y 90.
*/

SELECT *
FROM copy_ta04052026
WHERE availability_90 < 0
   OR availability_90 > 90;

-- Debo comprobar si aparecen disponibilidades negativas o superiores a 90 días.
-- no hay

/*
Compruebo si availability_365 tiene valores fuera del rango válido entre 0 y 365.
*/

SELECT *
FROM copy_ta04052026
WHERE availability_365 < 0
   OR availability_365 > 365;
   
-- Debo comprobar si aparecen disponibilidades negativas o superiores a 365 días.
-- No hay

/*
Compruebo si minimum_nights tiene valores menores que 1.
*/

SELECT *
FROM copy_ta04052026
WHERE minimum_nights < 1;

-- Debo comprobar si existen alojamientos con noches mínimas inválidas.
-- No hay

/*
Compruebo si maximum_nights es menor que minimum_nights.
*/

SELECT *
FROM copy_ta04052026
WHERE maximum_nights < minimum_nights;

-- Debo comprobar si existen incoherencias entre noches mínimas y máximas.
-- no hay

/*
Compruebo si number_of_reviews tiene valores negativos.
*/

SELECT *
FROM copy_ta04052026
WHERE number_of_reviews < 0;

-- Debo comprobar si existen cantidades de reseñas imposibles.
-- no hay

/*
Compruebo si reviews_per_month tiene valores negativos.
*/

SELECT *
FROM copy_ta04052026
WHERE reviews_per_month < 0;

-- Debo comprobar si existen valores imposibles en las reseñas mensuales.
-- no hay

/*
Compruebo si review_scores_rating_clean tiene valores fuera de la escala esperada entre 0 y 100.
*/

SELECT *
FROM copy_ta04052026
WHERE review_scores_rating_clean < 0
   OR review_scores_rating_clean > 100;

-- Debo comprobar si existen puntuaciones inválidas o errores en los datos.
-- no hay

/*
Compruebo si review_scores_location tiene valores fuera de la escala esperada entre 0 y 10.
*/

SELECT *
FROM copy_ta04052026
WHERE review_scores_location < 0
   OR review_scores_location > 10;

-- Debo comprobar si existen puntuaciones inválidas o errores en los datos.
-- ! Todos los valores son fuera de la escala 0-10!
-- La documentación indicaba una escala de 0 a 10 para review_scores_location.
-- Hacemos una verificacion:

/*
Compruebo la escala real de todas las variables de review para verificar
si coinciden con la documentación del dataset.
Debo observar mínimos, máximos y medias para entender si las puntuaciones están en escala 0-10 o 0-100.
*/

SELECT
    MIN(review_scores_rating_clean) AS min_review_scores_rating_clean,
    MAX(review_scores_rating_clean) AS max_review_scores_rating_clean,
    AVG(review_scores_rating_clean) AS avg_review_scores_rating_clean,

    MIN(review_scores_accuracy) AS min_review_scores_accuracy,
    MAX(review_scores_accuracy) AS max_review_scores_accuracy,
    AVG(review_scores_accuracy) AS avg_review_scores_accuracy,

    MIN(review_scores_cleanliness) AS min_review_scores_cleanliness,
    MAX(review_scores_cleanliness) AS max_review_scores_cleanliness,
    AVG(review_scores_cleanliness) AS avg_review_scores_cleanliness,

    MIN(review_scores_checkin) AS min_review_scores_checkin,
    MAX(review_scores_checkin) AS max_review_scores_checkin,
    AVG(review_scores_checkin) AS avg_review_scores_checkin,

    MIN(review_scores_communication) AS min_review_scores_communication,
    MAX(review_scores_communication) AS max_review_scores_communication,
    AVG(review_scores_communication) AS avg_review_scores_communication,

    MIN(review_scores_location) AS min_review_scores_location,
    MAX(review_scores_location) AS max_review_scores_location,
    AVG(review_scores_location) AS avg_review_scores_location,

    MIN(review_scores_value) AS min_review_scores_value,
    MAX(review_scores_value) AS max_review_scores_value,
    AVG(review_scores_value) AS avg_review_scores_value

FROM copy_ta04052026;

/* Según la documentación, las métricas de valoración deberían estar representadas en una escala de 0 a 10, 
pero en los datos todas las variables de review aparecen en una escala de 0 a 100.

Como todas las métricas son consistentes entre sí, 
pensamos que probablemente la documentación no está actualizada o contiene un error, 
por lo que vamos a mantener las variables en escala 0-100 para el análisis.
*/


/*
9. Compruebo si existe coherencia entre el número total de reseñas y las reseñas mensuales.

Si un alojamiento tiene number_of_reviews = 0, no debería tener reviews_per_month mayores que 0,
porque no puede recibir reseñas mensuales si nunca ha tenido reseñas.

También compruebo si existen alojamientos con reseñas totales mayores que 0
pero con reviews_per_month en NULL, ya que podría indicar valores faltantes o problemas de actualización de datos.
*/

SELECT *
FROM copy_ta04052026
WHERE number_of_reviews = 0
  AND reviews_per_month > 0;

SELECT *
FROM copy_ta04052026
WHERE number_of_reviews > 0
  AND reviews_per_month IS NULL;
  
/*
El primer control no devuelve resultados, por lo que no hay alojamientos con 0 reseñas totales
pero reviews_per_month positivo.

El segundo control devuelve solo 3 casos: alojamientos con 1 reseña total pero reviews_per_month NULL.
Como son pocos registros y tienen muy poca actividad, considero que reviews_per_month es un valor faltante
y no una incoherencia grave del dataset.

Para el análisis, debo decidir si excluir estos registros en los cálculos que usan reviews_per_month
o mantenerlos utilizando number_of_reviews como referencia histórica.
*/


/*
10. Comprobar incoherencias entre availability

La disponibilidad en 60 días no debería ser menor que la de 30 días.
La disponibilidad en 90 días no debería ser menor que la de 60 días.
La disponibilidad en 365 días no debería ser menor que la de 90 días.
*/

SELECT *
FROM copy_ta04052026
WHERE availability_60 < availability_30;
   
SELECT *
FROM copy_ta04052026
WHERE availability_90 < availability_60;
   
SELECT *
FROM copy_ta04052026
WHERE availability_365 < availability_90;

-- no hay nada: todo ok.

/*
Busco valores extremadamente altos o bajos en minimum_nights.
Debo comprobar si existen outliers que puedan distorsionar el análisis.
*/

SELECT
    minimum_nights,
    COUNT(*) AS n_rows
FROM copy_ta04052026
GROUP BY minimum_nights
ORDER BY minimum_nights DESC;

/*
Detecto valores extremadamente altos en minimum_nights.
Aunque no parecen errores técnicos, estos valores representan alojamientos
orientados a estancias largas y pueden distorsionar el análisis turístico.

! Hay que decedir que hacer con esos.
*/



/*
Calculo el porcentaje de valores NULL en reviews_per_month.
Debo comprobar si la cantidad de valores faltantes es relevante para el análisis.
*/

SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN reviews_per_month IS NULL THEN 1 ELSE 0 END) AS null_reviews_per_month,
    ROUND(
        SUM(CASE WHEN reviews_per_month IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS pct_null_reviews_per_month
FROM copy_ta04052026;


