-- =========================================
-- Familiarización inicial del dataset
-- Autor: Fede
-- Objetivo: entender estructura, volumen,
-- variable objetivo y relación inicial
-- entre contactos y éxito de campaña
-- =========================================

-- 1. Ver estructura de la tabla
DESCRIBE BANK_marketing;

-- 2. Contar registros totales
SELECT COUNT(*) AS total_registros
FROM BANK_marketing;

-- 3. Vista rápida de los datos
SELECT *
FROM BANK_marketing
LIMIT 10;

-- 4. Distribución de la variable objetivo
SELECT deposit, COUNT(*) AS total
FROM BANK_marketing
GROUP BY deposit;

-- 5. Distribución del número de contactos
SELECT campaign, COUNT(*) AS total
FROM BANK_marketing
GROUP BY campaign
ORDER BY campaign;

-- 6. Relación entre número de contactos y tasa de éxito
SELECT 
    campaign AS num_contactos,
    COUNT(*) AS total_clientes,
    SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) AS exitos,
    ROUND(
        SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) / COUNT(*) * 100,
        2
    ) AS tasa_exito_pct
FROM BANK_marketing
GROUP BY campaign
ORDER BY campaign;

-- 7. Revisión de valores nulos
SELECT 
    SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) AS age_nulls,
    SUM(CASE WHEN balance IS NULL THEN 1 ELSE 0 END) AS balance_nulls,
    SUM(CASE WHEN campaign IS NULL THEN 1 ELSE 0 END) AS campaign_nulls,
    SUM(CASE WHEN deposit IS NULL THEN 1 ELSE 0 END) AS deposit_nulls
FROM BANK_marketing;

-- 8. Estadísticas básicas
SELECT 
    MIN(age) AS edad_min,
    MAX(age) AS edad_max,
    AVG(age) AS edad_media,
    
    MIN(balance) AS balance_min,
    MAX(balance) AS balance_max,
    AVG(balance) AS balance_media
FROM BANK_marketing;
