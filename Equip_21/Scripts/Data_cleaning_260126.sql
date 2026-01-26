
-- 1. tratiamento de valores faltantes (NULLs and unknown )

-- 1.a Cuantificar los NULL
SELECT
  SUM(age IS NULL) AS age_nulls,
  SUM(job IS NULL) AS job_nulls,
  SUM(marital IS NULL) AS marital_nulls,
  SUM(education IS NULL) AS education_nulls,
  SUM(credit_default IS NULL) AS credit_default_nulls,
  SUM(balance IS NULL) AS balance_nulls,
  SUM(housing IS NULL) AS housing_nulls,
  SUM(loan IS NULL) AS loan_nulls,
  SUM(contact IS NULL) AS contact_nulls,
  SUM(day IS NULL) AS day_nulls,
  SUM(month IS NULL) AS month_nulls,
  SUM(duration IS NULL) AS duration_nulls,
  SUM(campaign IS NULL) AS campaign_nulls,
  SUM(pdays IS NULL) AS pdays_nulls,
  SUM(previous IS NULL) AS previous_nulls,
  SUM(deposit IS NULL) AS deposit_nulls
FROM BANK_marketing;


-- detalle NULL en age
SELECT *
FROM BANK_marketing
WHERE age IS NULL;


-- 1.b Cuantificar los unknown
SELECT
  SUM(job = 'unknown') AS job_unknown,
  SUM(marital = 'unknown') AS marital_unknown,
  SUM(education = 'unknown') AS education_unknown,
  SUM(contact = 'unknown') AS contact_unknown,
  SUM(month = 'unknown') AS month_unknown,
  SUM(poutcome = 'unknown') AS poutcome_unknown
FROM BANK_marketing;

-- detalle poutcome = 'unknown y  previous (COUNT) 
SELECT previous, poutcome, COUNT(*) AS num_contactos
FROM BANK_marketing
GROUP BY previous, poutcome
HAVING poutcome = 'unknown';

-- detalle contact = 'unknown y  previous (COUNT) 
SELECT previous, contact, COUNT(*) AS num_contactos
FROM BANK_marketing
GROUP BY previous, contact
HAVING contact = 'unknown';

------------------------------------------------------------------
-- 1.c clasificacion de NULLs y unknown

-- age --> media?mediana?moda?
---- UPDATE BANK_marketing
SET age = (
    SELECT AVG(age) ------- DECIDIR media? mediana? otra cosa?
    FROM BANK_marketing
    WHERE age IS NOT NULL
)
WHERE age IS NULL;

--  job --> ponderada
---- WITH job_dist AS (
    SELECT
        job,
        COUNT(*)::float / SUM(COUNT(*)) OVER () AS prob
    FROM BANK_marketing
    WHERE job IS NOT NULL
      AND job <> 'unknown'
    GROUP BY job
)
SELECT * FROM job_dist;

--  marital --> ponderada
---- UPDATE BANK_marketing
SET marital = (
    SELECT -- FORMULA AQUI
    FROM BANK_marketing
    WHERE marital IS NOT NULL
)
WHERE age IS NULL;

-- contact unknown AND previous == 0
UPDATE BANK_marketing
SET contact = 'inbound'
WHERE contact = 'unknown' AND previous = 0;

-- contact unknown (  AND previous != 0)
UPDATE BANK_marketing
SET contact = -- TRATAR SEGUN TENDECIA PONDERADA
WHERE contact = 'unknown' AND previous != 0;
------------------------------------------------------------------
-- 2. 

------------------------------------------------------------------
-- Encontrar valores atípicos en la edad
SELECT MIN(age), MAX(age)
FROM BANK_marketing;

-- Encontrar valores atípicos en el balance
SELECT
  MIN(balance),
  MAX(balance),
  AVG(balance)
FROM BANK_marketing;

-- Selección de los Null en edad
SELECT *
FROM BANK_marketing
WHERE age IS NULL;

-- Selección de los Null en marital
SELECT *
FROM BANK_marketing
WHERE marital IS NULL;

-- Selección de los Null en education
SELECT *
FROM BANK_marketing
WHERE education IS NULL;

-- Selección de unknown en job
SELECT *
FROM BANK_marketing
WHERE job = "unknown";

-- Selección de los unknown en contact
SELECT *
FROM BANK_marketing
WHERE contact = "unknown";

-- Modificación de los valores categóricos null por unknown de marital
UPDATE BANK_marketing
SET marital = 'unknown'
WHERE marital IS NULL;

-- Modificación de los valores categóricos null por unknown de education
UPDATE BANK_marketing
SET education = 'unknown'
WHERE education IS NULL;

-- Descripción de la tabla
DESCRIBE BANK_marketing;

-- Mofificación del nombre de columna default
ALTER TABLE BANK_marketing
CHANGE `default` credit_default VARCHAR(3);

-- Verificación de datos booleanos en las columnas
SELECT DISTINCT credit_default FROM BANK_marketing;
SELECT DISTINCT housing FROM BANK_marketing;
SELECT DISTINCT loan FROM BANK_marketing;
SELECT DISTINCT deposit FROM BANK_marketing;

-- Conversión de los valores de las columnas a booleano
UPDATE BANK_marketing
SET
  credit_default = CASE
    WHEN credit_default = 'yes' THEN 1
    WHEN credit_default = 'no' THEN 0
    ELSE NULL
  END,
  housing = CASE
    WHEN housing = 'yes' THEN 1
    WHEN housing = 'no' THEN 0
    ELSE NULL
  END,
  loan = CASE
    WHEN loan = 'yes' THEN 1
    WHEN loan = 'no' THEN 0
    ELSE NULL
  END,
  deposit = CASE
    WHEN deposit = 'yes' THEN 1
    WHEN deposit = 'no' THEN 0
    ELSE NULL
  END;
  
  -- Canvio de tipo de valor de las columnas en tabla
ALTER TABLE BANK_marketing
MODIFY credit_default BOOLEAN,
MODIFY housing BOOLEAN,
MODIFY loan BOOLEAN,
MODIFY deposit BOOLEAN;

