SELECT  ID, sum(Absenteeism_hours) FROM Equip_15.RRHH_22092025 group by 1 order by 2 desc limit 10;

SELECT sum(Absenteeism_hours) FROM Equip_15.RRHH_22092025;


SELECT  ID, count(Absenteeism_hours) FROM Equip_15.RRHH_22092025 group by 1 order by  2 desc limit 10;
 
SELECT count(Absenteeism_hours) FROM Equip_15.RRHH_22092025;

SELECT ID, 
       SUM(Absenteeism_hours) as total_hours,
       COUNT(Absenteeism_hours) as absence_count
FROM Equip_15.RRHH_22092025 
GROUP BY ID 
ORDER BY total_hours DESC 
LIMIT 10;

SELECT ID, 
       SUM(Absenteeism_hours) as total_hours,
       COUNT(Absenteeism_hours) as absence_count
FROM Equip_15.RRHH_22092025 
GROUP BY ID 
ORDER BY absence_count DESC 
LIMIT 10;

SELECT ID, Social_drinker,
       SUM(Absenteeism_hours) as total_hours,
       COUNT(Absenteeism_hours) as absence_count
FROM Equip_15.RRHH_22092025 
GROUP BY 1,2
ORDER BY absence_count DESC 
LIMIT 10;

SELECT ID,
       SUM(Absenteeism_hours) as total_hours,
       COUNT(Absenteeism_hours) as absence_count
FROM Equip_15.RRHH_22092025 
GROUP BY ID, Social_drinker,Reason_absence
ORDER BY absence_count DESC 
LIMIT 20;
