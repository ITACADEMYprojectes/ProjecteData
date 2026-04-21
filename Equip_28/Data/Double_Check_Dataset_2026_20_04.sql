-- Nº de registros totales: 

SELECT COUNT(*) AS registros_totales
FROM RRHH;

-- ID únicos: 
SELECT COUNT(DISTINCT ID) AS id_unicos
FROM RRHH;

-- ID extras:

SELECT 
    COUNT(*) AS registros_totales, 
    COUNT(DISTINCT ID) AS ids_unicos,
    (COUNT(*) - COUNT(DISTINCT ID)) AS id_extras
FROM RRHH;

-- ID duplicados exactos: 

SELECT *, COUNT(*) as repeticiones
FROM RRHH
GROUP BY ID, Reason_absence, Month_absence, Day_week, Seasons, Transportation_expense, 
         Distance_Residence_Work, Service_time, Age, Work_load_Average_day, Hit_target, 
         Disciplinary_failure, Education, Son, Social_drinker, Social_smoker, Pet, 
         Weight, Height, Body_mass_index, Absenteeism_hours
HAVING COUNT(*) > 1;