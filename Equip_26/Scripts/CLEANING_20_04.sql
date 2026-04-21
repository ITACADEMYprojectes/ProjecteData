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

-- ! Por analisi de review clientes: Hay que eliminar la filas con review_scores_rating = null

-- Creo una vista con solo la columnas que necesito
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
-- Los datos de review_scores_rating





