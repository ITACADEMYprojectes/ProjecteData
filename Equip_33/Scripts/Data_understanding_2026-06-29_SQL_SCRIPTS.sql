-- DATA UNDERSTANDING — Taula RRHH (Absentisme)

-- 0. ESTRUCTURA
DESCRIBE RRHH;

-- 1.LLISTA DUPLICATS
SELECT COUNT(*) AS veces_q_aparece, COUNT(*)-1 AS veces_duplicado, ID, Reason_absence, Month_absence, Day_week, Seasons,
    Transportation_expense, Distance_Residence_Work, Service_time,
    Age, Work_load_Average_day, Hit_target, Disciplinary_failure,
    Education, Son, Social_drinker, Social_smoker, Pet,
    Weight, Height, Body_mass_index, Absenteeism_hours
FROM RRHH
GROUP BY ID, Reason_absence, Month_absence, Day_week, Seasons,
    Transportation_expense, Distance_Residence_Work, Service_time,
    Age, Work_load_Average_day, Hit_target, Disciplinary_failure,
    Education, Son, Social_drinker, Social_smoker, Pet,
    Weight, Height, Body_mass_index, Absenteeism_hours
HAVING COUNT(*) > 1
ORDER BY ID;

-- TOTAL DUPLICATS
SELECT 
    COUNT(*) AS files_uniques_duplicades,
    SUM(repeticions) - COUNT(*) AS files_extres_a_borrar
FROM (
    SELECT 
        ID, Reason_absence, Month_absence, Day_week, Seasons,
        Transportation_expense, Distance_Residence_Work, Service_time,
        Age, Work_load_Average_day, Hit_target, Disciplinary_failure,
        Education, Son, Social_drinker, Social_smoker, Pet,
        Weight, Height, Body_mass_index, Absenteeism_hours,
        COUNT(*) AS repeticions
    FROM RRHH
    GROUP BY 
        ID, Reason_absence, Month_absence, Day_week, Seasons,
        Transportation_expense, Distance_Residence_Work, Service_time,
        Age, Work_load_Average_day, Hit_target, Disciplinary_failure,
        Education, Son, Social_drinker, Social_smoker, Pet,
        Weight, Height, Body_mass_index, Absenteeism_hours
    HAVING COUNT(*) > 1
) AS sub;

-- 2. ANÀLISI DE NULLS
SELECT 'ID' AS columna, COUNT(*) - COUNT(ID) AS nulls FROM RRHH UNION ALL
SELECT 'Reason_absence', COUNT(*) - COUNT(Reason_absence) FROM RRHH UNION ALL
SELECT 'Month_absence', COUNT(*) - COUNT(Month_absence) FROM RRHH UNION ALL
SELECT 'Day_week', COUNT(*) - COUNT(Day_week) FROM RRHH UNION ALL
SELECT 'Seasons', COUNT(*) - COUNT(Seasons) FROM RRHH UNION ALL
SELECT 'Transportation_expense', COUNT(*) - COUNT(Transportation_expense) FROM RRHH UNION ALL
SELECT 'Distance_Residence_Work', COUNT(*) - COUNT(Distance_Residence_Work) FROM RRHH UNION ALL
SELECT 'Service_time', COUNT(*) - COUNT(Service_time) FROM RRHH UNION ALL
SELECT 'Age', COUNT(*) - COUNT(Age) FROM RRHH UNION ALL
SELECT 'Work_load_Average_day', COUNT(*) - COUNT(Work_load_Average_day) FROM RRHH UNION ALL
SELECT 'Hit_target', COUNT(*) - COUNT(Hit_target) FROM RRHH UNION ALL
SELECT 'Disciplinary_failure', COUNT(*) - COUNT(Disciplinary_failure) FROM RRHH UNION ALL
SELECT 'Education', COUNT(*) - COUNT(Education) FROM RRHH UNION ALL
SELECT 'Son', COUNT(*) - COUNT(Son) FROM RRHH UNION ALL
SELECT 'Social_drinker', COUNT(*) - COUNT(Social_drinker) FROM RRHH UNION ALL
SELECT 'Social_smoker', COUNT(*) - COUNT(Social_smoker) FROM RRHH UNION ALL
SELECT 'Pet', COUNT(*) - COUNT(Pet) FROM RRHH UNION ALL
SELECT 'Weight', COUNT(*) - COUNT(Weight) FROM RRHH UNION ALL
SELECT 'Height', COUNT(*) - COUNT(Height) FROM RRHH UNION ALL
SELECT 'Body_mass_index', COUNT(*) - COUNT(Body_mass_index) FROM RRHH UNION ALL
SELECT 'Absenteeism_hours', COUNT(*) - COUNT(Absenteeism_hours) FROM RRHH;

-- 3. NULLS -BUITS-ESPAIS de falsos varchar
SELECT 'Disciplinary_failure' AS columna,
       SUM(CASE WHEN Disciplinary_failure IS NULL THEN 1 ELSE 0 END) AS nulls,
       SUM(CASE WHEN TRIM(Disciplinary_failure) = '' THEN 1 ELSE 0 END) AS buits_o_espais
FROM RRHH
UNION ALL
SELECT 'Social_drinker',
       SUM(CASE WHEN Social_drinker IS NULL THEN 1 ELSE 0 END),
       SUM(CASE WHEN TRIM(Social_drinker) = '' THEN 1 ELSE 0 END)
FROM RRHH
UNION ALL
SELECT 'Social_smoker',
       SUM(CASE WHEN Social_smoker IS NULL THEN 1 ELSE 0 END),
       SUM(CASE WHEN TRIM(Social_smoker) = '' THEN 1 ELSE 0 END)
FROM RRHH
UNION ALL
SELECT 'Son',
       SUM(CASE WHEN Son IS NULL THEN 1 ELSE 0 END),
       SUM(CASE WHEN TRIM(Son) = '' THEN 1 ELSE 0 END)
FROM RRHH
UNION ALL
SELECT 'Pet',
       SUM(CASE WHEN Pet IS NULL THEN 1 ELSE 0 END),
       SUM(CASE WHEN TRIM(Pet) = '' THEN 1 ELSE 0 END)
FROM RRHH
UNION ALL
SELECT 'Education',
       SUM(CASE WHEN Education IS NULL THEN 1 ELSE 0 END),
       SUM(CASE WHEN TRIM(Education) = '' THEN 1 ELSE 0 END)
FROM RRHH
UNION ALL
SELECT 'Work_load_Average_day',
       SUM(CASE WHEN Work_load_Average_day IS NULL THEN 1 ELSE 0 END),
       SUM(CASE WHEN TRIM(Work_load_Average_day) = '' THEN 1 ELSE 0 END)
FROM RRHH;

-- 4. RANGS MIN/MAX — REVISIÓ VALORS RARS
SELECT MIN(Service_time), MAX(Service_time), ROUND(AVG(Service_time),2) FROM RRHH;
SELECT MIN(Age), MAX(Age) FROM RRHH;
SELECT MIN(Work_load_Average_day), MAX(Work_load_Average_day) FROM RRHH;
SELECT MIN(Weight), MAX(Weight) FROM RRHH;
SELECT MIN(Height), MAX(Height) FROM RRHH;
SELECT MIN(Body_mass_index), MAX(Body_mass_index) FROM RRHH;
SELECT MIN(ID), MAX(ID) FROM RRHH;
SELECT MIN(Distance_Residence_Work), MAX(Distance_Residence_Work) FROM RRHH;
SELECT MIN(Transportation_expense), MAX(Transportation_expense) FROM RRHH;
SELECT MIN(Absenteeism_hours), MAX(Absenteeism_hours) FROM RRHH;
SELECT MIN(Hit_target), MAX(Hit_target) FROM RRHH;

-- 5. VALORS ÚNICS ("FALSOS VARCHAR")
SELECT DISTINCT Disciplinary_failure FROM RRHH;
SELECT DISTINCT Social_drinker FROM RRHH;
SELECT DISTINCT Social_smoker FROM RRHH;
SELECT DISTINCT Education FROM RRHH;
SELECT DISTINCT Son FROM RRHH;
SELECT DISTINCT Pet FROM RRHH;
SELECT DISTINCT Seasons FROM RRHH;

-- 6. NOMBRE D'ABSÈNCIES PER EMPLEAT
SELECT ID, COUNT(*) AS num_absencies
FROM RRHH
GROUP BY ID
ORDER BY num_absencies DESC;

-- 7. ATRIBUTS FIXES EMPLEAT (valors diferents, son error??)
SELECT ID,
    COUNT(DISTINCT Age) AS valors_Age,
    COUNT(DISTINCT Education) AS valors_Education,
    COUNT(DISTINCT Son) AS valors_Son,
    COUNT(DISTINCT Social_drinker) AS valors_Social_drinker,
    COUNT(DISTINCT Social_smoker) AS valors_Social_smoker,
    COUNT(DISTINCT Pet) AS valors_Pet,
    COUNT(DISTINCT Weight) AS valors_Weight,
    COUNT(DISTINCT Height) AS valors_Height,
    COUNT(DISTINCT Body_mass_index) AS valors_BMI
FROM RRHH
GROUP BY ID
ORDER BY ID;

-- 8. DISTRIBUCIÓ DE Reason_absence
SELECT Reason_absence, COUNT(*) AS num_registres
FROM RRHH
GROUP BY Reason_absence
ORDER BY Reason_absence;

-- 9. REVISIÓ Month_absence (valor 0 detectat)
SELECT DISTINCT Month_absence FROM RRHH ORDER BY Month_absence;
SELECT * FROM RRHH WHERE Month_absence = 0;

-- 10. QUADRA Body_mass_index vs Weight/Height
SELECT ID, Weight, Height, Body_mass_index,
       ROUND(Weight / POWER(Height/100, 2), 0) AS BMI_calculat
FROM RRHH
LIMIT 14;