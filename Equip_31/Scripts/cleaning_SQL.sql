USE Equip_31;

-- ID DUPLICADOS EXACTOS
SELECT
  ID, Reason_absence, Month_absence, Day_week, Seasons,
  Transportation_expense, Distance_Residence_Work, Service_time,
  Age, Work_load_Average_day, Hit_target, Disciplinary_failure,
  Education, Son, Social_drinker, Social_smoker, Pet, Weight,
  Height, Body_mass_index, Absenteeism_hours,
  COUNT(*) AS times_repeated
FROM RRHH
GROUP BY
  ID, Reason_absence, Month_absence, Day_week, Seasons,
  Transportation_expense, Distance_Residence_Work, Service_time,
  Age, Work_load_Average_day, Hit_target, Disciplinary_failure,
  Education, Son, Social_drinker, Social_smoker, Pet, Weight,
  Height, Body_mass_index, Absenteeism_hours
HAVING COUNT(*) > 1;

-- SEPARATE TABLES

-- Demographics
SELECT
	DISTINCT (ID), Transportation_expense, Distance_Residence_Work, Service_time, # only ID from this line?
	Age, Education, Son, Social_drinker, Social_smoker, Pet, Weight,
	Height, Body_mass_index
FROM RRHH
ORDER BY ID;

-- Absentism

SELECT
	ID, Reason_absence, Month_absence, Day_week, Seasons,
	Work_load_Average_day, Hit_target, Disciplinary_failure, # separate disciplinary failure? separate work load and hit target?
	Absenteeism_hours
FROM RRHH
ORDER BY ID, Seasons, Month_absence;

-- ONLY ABSENCES
SELECT
	ID, Reason_absence, Month_absence, Day_week, Seasons,
	Work_load_Average_day, Hit_target
	Absenteeism_hours
FROM RRHH
WHERE Disciplinary_failure != 1
ORDER BY ID;

-- ONLY DISCIPLINARY

SELECT
	ID, Month_absence, Day_week, Seasons,
	Disciplinary_failure
FROM RRHH
WHERE Disciplinary_failure = 1
ORDER BY ID;

-- SEPARATE WORK LOAD
-- Not finished
SELECT
	ID, Month_absence, Seasons,
	Work_load_Average_day, Hit_target
FROM RRHH
ORDER BY ID;

-- TRANSPORTATION EXPENSE - DISTANCE - SERVICE TIME

SELECT
	DISTINCT (ID), Transportation_expense, Distance_Residence_Work, Service_time
FROM RRHH
ORDER BY ID;






