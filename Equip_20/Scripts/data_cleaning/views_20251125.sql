/**
 * Limpieza y adecuación de los datos de la tabla RRHH
 * ---
 */

-- VIEW que combina estos datos.
-- ** SUSTITUIDA ** --
CREATE OR REPLACE VIEW ausentismo AS
    SELECT ID as id
         , Reason_absence          AS reason_id
         , ab_reason.description   AS absence_reason
         , Absenteeism_hours
         , Month_absence, Day_week
         , downames.dayname AS Day_of_week
         , seasons.name     AS Season
         , Transportation_expense  AS tr_expense
         , Distance_Residence_Work AS dist2work
         , Service_time
         , Work_load_Average_day   AS work_load_avg
         , Hit_target
         , Disciplinary_failure    AS disciplined
         , Age, Education, Social_drinker, Social_smoker
         , Son AS children
         , Pet as pets
         , weight, height, CAST(ROUND((Weight / (Height * Height))*1e4, 0) as unsigned integer) AS bmi
      FROM `RRHH`
      JOIN ab_reason ON reason_id=Reason_absence
      JOIN seasons   ON Seasons=season
      JOIN (VALUES
             ROW (1, 'Sunday'),
             ROW (2, 'Monday'),
             ROW (3, 'Tuesday'),
             ROW (4, 'Wednesday'),
             ROW (5, 'Thursday'),
             ROW (6, 'Friday'),
             ROW (7, 'Saturday')
          ) AS downames(Day_week, dayname)
          USING (Day_week)
      JOIN (VALUES
             ROW( 1, 'January'),
             ROW( 2, 'February'),
             ROW( 3, 'March'),
             ROW( 4, 'April'),
             ROW( 5, 'May'),
             ROW( 6, 'June'),
             ROW( 7, 'July'),
             ROW( 8, 'August'),
             ROW( 9, 'September'),
             ROW(10, 'October'),
             ROW(11, 'November'),
             ROW(12, 'December')
         ) AS months(month_id, name)
           ON month_id = Month_absence
    ;

-- Ya que tenemos los valores normalizados en tablas, sustituyo el VALUES ROW()
-- por la tabla correspondiente en el JOIN.
-- History
--   - 20251117 Versión inicial
--   - 20251125 Añade nuevas columnas:
--     - `justified` (registros con ID <> 0 o 26)
--     - categorización de la distancia al trabajo (1 a 4)
CREATE OR REPLACE VIEW ausentismo AS
    SELECT ID AS id
         , Reason_absence          AS reason_id
         , ab_reason.description   AS absence_reason
         , reason_id NOT IN(0,26)  AS justified
         , Absenteeism_hours
         , RRHH.Month_absence      AS Month_absence_num
         , months.name             AS Month_absence, Day_week
         , day_of_week.name        AS Day_of_week
         , seasons.name            AS Season
         , Transportation_expense  AS tr_expense
         , Distance_Residence_Work AS distance_to_work
         , CASE WHEN Distance_Residence_Work < 16 THEN 1
                WHEN Distance_Residence_Work < 31 THEN 2
                WHEN Distance_Residence_Work < 46 THEN 3
                ELSE 4
            END AS cat_distance_to_work
         , Service_time
         , Work_load_Average_day   AS work_load_avg
         , Hit_target
         , Disciplinary_failure    AS disciplined
         , Age, Education, Social_drinker, Social_smoker
         , Son AS children
         , Pet AS pets
         , weight, height
         , CAST(ROUND((Weight/(Height * Height))*1e4, 0) AS UNSIGNED INTEGER) AS bmi
      FROM `RRHH`
      JOIN ab_reason   ON reason_id = Reason_absence
      JOIN seasons     ON season    = Seasons
      JOIN day_of_week ON dow_id    = Day_week
      JOIN months      ON month_id  = RRHH.`Month_absence`;

-- Vista de niveles de ausentismo
CREATE OR REPLACE VIEW long_absence AS
   SELECT ID
        , ROUND(SUM(Absenteeism_hours)/8, 2) AS work_days_absent
        , CASE WHEN SUM(Absenteeism_hours)/8 < 8  THEN 1
               WHEN SUM(Absenteeism_hours)/8 < 22 THEN 2
               WHEN SUM(Absenteeism_hours)/8 < 43 THEN 3
               ELSE 4
          END  AS `ab_level`
        , CASE WHEN SUM(Absenteeism_hours)/8 < 8  THEN "Bajo"
               WHEN SUM(Absenteeism_hours)/8 < 22 THEN "Medio"
               WHEN SUM(Absenteeism_hours)/8 < 43 THEN "Alto"
               ELSE "Muy alto"
          END  AS `level`
     FROM ausentismo GROUP BY ID HAVING SUM(Absenteeism_hours) > 7;

-- Vista de niveles de ausentismo dos categorías con todos los empleados
CREATE OR REPLACE VIEW long_absence AS
   SELECT ID
        , ROUND(SUM(Absenteeism_hours)/8, 2) AS work_days_absent
        , CASE WHEN SUM(Absenteeism_hours)/8 < 22 THEN 0
               ELSE 1
          END  AS `ab_level`
        , CASE WHEN SUM(Absenteeism_hours)/8 < 22 THEN "Bajo"
               ELSE THEN "Medio-Alto"
          END  AS `level`
     FROM ausentismo GROUP BY ID;
