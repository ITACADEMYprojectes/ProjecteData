-- Tratamiento de valores faltantes: Se han analizado los NULL detectándose en los campos “age”, “marital” y “education”.

-- También se han encontrado registros UNKNOWN en los campos “job”, “education”, “contact”, “poutcome”.

-- Eliminación o corrección de duplicados: Se ha revisado la existencia de registros duplicados y la existencia de “id” extras y no se han detectado.

-- Validación y corrección de valores atípicos: Se ha revisado en rango de “age” (18-95) siendo los valores normales. 
-- En “balance” se ha considerado también normal la existencia de valores negativos y 0. No se han detectado valores atípicos en los campos
-- “day”, “duration”, “campaign” ni “previous”. En refercia al campo “pdays” se ha acordado desagregarlo en dos columnas (boolean e int)
-- para eliminar el signo negativo en la fase de Data Transformation.

-- Estandarización de formatos: Hemos considerado UNKNOWN como una categoria propia y válida por lo que se han mantenido como están. 
-- Con respecto a los NULL, si se trata de una variable categórica ("marital" y "education"), se han convertido en UNKNOWN, y si la variable es numérica, 
-- no se han realizado cambios para evitar incompatibilidades con el literal y/o errores en consultas futuras. 

-- Se ha revisado también que no hubiera errores tipográficos en las variables categóricas que generaran “falsas categorias”, no encontrándose ninguno.

-- Corrección de tipos de datos. Se ha transformado los campos “default”, “housing”, “loan” y “deposit” al literal boolean. 

-- Adicionalmente, dado que "default" es una palabra reservada, le hemos cambiado el nombre al campo por "credit_default".


SELECT * FROM  BANK_marketing;

-- Cuantificar los NULL
SELECT
  SUM(age IS NULL) AS age_nulls,
  SUM(job IS NULL) AS job_nulls,
  SUM(marital IS NULL) AS marital_nulls,
  SUM(education IS NULL) AS education_nulls,
  SUM(balance IS NULL) AS balance_nulls,
  SUM(housing IS NULL) AS housing_nulls,
  SUM(loan IS NULL) AS loan_nulls
FROM BANK_marketing;

-- Cuantificar los unknown
SELECT
  SUM(job = 'unknown') AS job_unknown,
  SUM(education = 'unknown') AS education_unknown,
  SUM(contact = 'unknown') AS contact_unknown,
  SUM(poutcome = 'unknown') AS poutcome_unknown
FROM BANK_marketing;

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

