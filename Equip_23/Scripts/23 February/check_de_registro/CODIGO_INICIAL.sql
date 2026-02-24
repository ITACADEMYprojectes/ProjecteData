# TOTAL REGISTROS
SELECT COUNT(*) AS total_registros
FROM BANK_marketing;

# ID UNICOS
SELECT COUNT(DISTINCT id) AS id_unicos
FROM BANK_marketing;

# ID EXTRAS
SELECT COUNT(*) - COUNT(DISTINCT id) AS id_extras
FROM BANK_marketing;

# ID DUPLICADOS EXACTOS
SELECT COUNT(*)
FROM (
    SELECT id
    FROM BANK_marketing
    GROUP BY id
    HAVING COUNT(*) > 1
) AS duplicados;