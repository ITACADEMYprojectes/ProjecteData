-- DATA CLEANING 260126

-- 1. Tratamiento de valores faltantes
-- 1.a NULLS
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

-- Detalle NULLS en age
SELECT *
FROM BANK_marketing
WHERE age IS NULL;

-- 1.b UNKNOWN
SELECT
  SUM(job = 'unknown') AS job_unknown,
  SUM(marital = 'unknown') AS marital_unknown,
  SUM(education = 'unknown') AS education_unknown,
  SUM(contact = 'unknown') AS contact_unknown,
  SUM(month = 'unknown') AS month_unknown,
  SUM(poutcome = 'unknown') AS poutcome_unknown
FROM BANK_marketing;

-- Detalle poutcome = 'unknown' y  previous (COUNT) 
SELECT previous, poutcome, COUNT(*) AS num_contactos
FROM BANK_marketing
GROUP BY previous, poutcome
HAVING poutcome = 'unknown';

-- Detalle contact = 'unknown' y  previous (COUNT) 
SELECT previous, contact, COUNT(*) AS num_contactos
FROM BANK_marketing
GROUP BY previous, contact
HAVING contact = 'unknown';
 
-- Se ha detectado que previous, pdays y poutcome tienen ambos el mismo número de registros 
SELECT previous, pdays, poutcome, COUNT(*) AS num_contactos
FROM BANK_marketing
GROUP BY previous, poutcome,pdays
HAVING poutcome = 'unknown'
AND pdays = -1 ;

-- 1.c Transformación de NULLs y UNKNOWNS
-- AGE --> A los NULLS imputamos la mediana para que no dé error al hacer clustering
SET SQL_SAFE_UPDATES = 0; 
UPDATE BANK_marketing
SET age = (
    SELECT AVG(age)
    FROM (
        SELECT 
            age,
            ROW_NUMBER() OVER (ORDER BY age) AS rn,
            COUNT(*) OVER () AS cnt
        FROM BANK_marketing
        WHERE age IS NOT NULL
    ) t
    WHERE rn IN (FLOOR((cnt + 1) / 2), FLOOR((cnt + 2) / 2))
)
WHERE age IS NULL;
SET SQL_SAFE_UPDATES = 1;

--  JOB --> Los UNKNOWNS aplicamos las probabilidades ponderadas de cada categoría
SET SQL_SAFE_UPDATES = 0; 

UPDATE BANK_marketing AS b
JOIN (
    SELECT 
        job,
        SUM(prob) OVER (ORDER BY prob DESC) AS cum_prob
    FROM (
        SELECT 
            job,
            COUNT(*) / SUM(COUNT(*)) OVER () AS prob
        FROM BANK_marketing
        WHERE job <> 'unknown'
        GROUP BY job
    ) AS dist
) AS d
ON RAND() <= d.cum_prob
SET b.job = d.job
WHERE b.job = 'unknown';

SET SQL_SAFE_UPDATES = 1;

--  MARITAL --> Los UNKNOWNS aplicamos las probabilidades ponderadas de cada categoría
SET SQL_SAFE_UPDATES = 0;

UPDATE BANK_marketing AS b
JOIN (
    SELECT 
        marital,
        SUM(prob) OVER (ORDER BY prob DESC) AS cum_prob
    FROM (
        SELECT 
            marital,
            COUNT(*) / SUM(COUNT(*)) OVER () AS prob
        FROM BANK_marketing
        WHERE marital <> 'unknown'
        GROUP BY marital
    ) AS dist
) AS d
ON RAND() <= d.cum_prob
SET b.marital = d.marital
WHERE b.marital = 'unknown';

SET SQL_SAFE_UPDATES = 1;

--  EDUCATION --> Los UNKNOWNS aplicamos las probabilidades ponderadas de cada categoría
SET SQL_SAFE_UPDATES = 0;

UPDATE BANK_marketing AS b
JOIN (
    SELECT 
        education,
        SUM(prob) OVER (ORDER BY prob DESC) AS cum_prob
    FROM (
        SELECT 
            education,
            COUNT(*) / SUM(COUNT(*)) OVER () AS prob
        FROM BANK_marketing
        WHERE education <> 'unknown'
        GROUP BY education
    ) AS dist
) AS d
ON RAND() <= d.cum_prob
SET b.education = d.education
WHERE b.education = 'unknown';

SET SQL_SAFE_UPDATES = 1;

-- CONTACT --> Traspasamos a marketing la gestión de los UNKNOWNS
SET SQL_SAFE_UPDATES = 0;

ALTER TABLE BANK_marketing
MODIFY contact varchar(20);

UPDATE BANK_marketing
SET contact = 'low_quality'
WHERE contact = 'unknown';

SET SQL_SAFE_UPDATES = 1;

-- POUTCOME --> Traspasamos a marketing la gestión de los UNKNOWNS

-- 2. Eliminación o corrección de duplicados
-- 2.1. Id duplicados exactos 
SELECT id, age, job, marital, education, balance, housing, loan, contact, day, month, duration, campaign, pdays, previous, poutcome, deposit, COUNT(*) AS cuenta
FROM Equip_21.BANK_marketing
GROUP BY id, age, job, marital, education,balance, housing, loan, contact, day, month, duration, campaign, pdays, previous, poutcome, deposit
HAVING COUNT(*) > 1;

-- 2.2. Creamos una columna id unico Y Eliminamos duplicados perfectos, conserva el id más pequeño de los duplicados
-------- SET SQL_SAFE_UPDATES = 0;

-------- ALTER TABLE Equip_21.BANK_marketing
ADD COLUMN uniq_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY;

-- 2.3. Eliminamos duplicados perfectos, conserva el id más pequeño de los duplicados
-------- DELETE t1
FROM Equip_21.BANK_marketing t1
JOIN Equip_21.BANK_marketing t2
ON t1.age = t2.age
AND t1.job = t2.job
AND t1.marital = t2.marital
AND t1.education = t2.education
AND t1.balance = t2.balance
AND t1.housing = t2.housing
AND t1.loan = t2.loan
AND t1.contact = t2.contact
AND t1.day = t2.day
AND t1.month = t2.month
AND t1.duration = t2.duration
AND t1.campaign = t2.campaign
AND t1.pdays = t2.pdays
AND t1.previous = t2.previous
AND t1.poutcome = t2.poutcome
AND t1.deposit = t2.deposit
AND t1.uniq_id > t2.uniq_id;

-- 2.4. Eliminamos columna temporal de id unico 
-------- ALTER TABLE Equip_21.BANK_marketing
DROP COLUMN uniq_id;

-------- SET SQL_SAFE_UPDATES = 1;

-- 3. Validación y corrección de valores atípicos

-- AGE --> No vemos valores atípicos
SELECT MIN(age), MAX(age)
FROM BANK_marketing;

-- BALANCE --> No vemos valores atípicos
SELECT
  MIN(balance),
  MAX(balance),
  AVG(balance)
FROM BANK_marketing;

-- 4. Estandarización de formatos
-- 4.1. Creamos la columna pcontact (boolean) para saber si se ha contactado antes o no

-------- SET SQL_SAFE_UPDATES = 0;

-------- ALTER TABLE BANK_marketing
ADD COLUMN pcontact BOOLEAN;

-------- SET
  pcontact = CASE
    WHEN pdays < '0' THEN 0
    WHEN pdays >= '0' THEN 1
    ELSE NULL
  END;
  
-------- SET SQL_SAFE_UPDATES = 1;


-- 4.2. LO TRASPASAMOS A MARKETING: modificamos la columna pdays para que no haya negativos y solo contabilice los dias desde la ultima llamada (los -1 pasaran a ser 1? o 0?)

-- 5. Corrección de tipos de datos
-- 5.1. Canvio de tipo de valor de las columna age

SET SQL_SAFE_UPDATES = 0;

ALTER TABLE BANK_marketing
MODIFY age INT;

SET SQL_SAFE_UPDATES = 1;

-- 6. Exportar base de datos sin duplicados exacto a traves de VIEW 

CREATE OR REPLACE VIEW Equip_21.BANK_marketing_deduplicated AS
SELECT
    id,
    age,
    job,
    marital,
    education,
    credit_default,
    balance,
    housing,
    loan,
    contact,
    day,
    month,
    duration,
    campaign,
    pdays,
    previous,
    poutcome,
    deposit
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY
                id,
                age,
                job,
                marital,
                education,
                credit_default,
                balance,
                housing,
                loan,
                contact,
                day,
                month,
                duration,
                campaign,
                pdays,
                previous,
                poutcome,
                deposit
            ORDER BY id
        ) AS rn
    FROM Equip_21.BANK_marketing
) t
WHERE rn = 1;

-- check num de rows
SELECT COUNT(*) FROM Equip_21.BANK_marketing;
SELECT COUNT(*) FROM Equip_21.BANK_marketing_deduplicated;


-- select para exportar la tabla view de-duplicated
SELECT * FROM Equip_21.BANK_marketing_dedup;