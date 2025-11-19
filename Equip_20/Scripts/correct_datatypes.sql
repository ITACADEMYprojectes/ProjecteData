/**
 * Algunos campos están como VARCHAR siendo que son BOOLEAN.
 * Ya de paso, revisamos todos los campos.
 */

-- Es un valor FLOAT, pero está como VARCHAR por la coma, así que la cambiamos.
UPDATE RRHH
   SET `Work_load_Average_day` = REPLACE(`Work_load_Average_day`, ',', '.');

ALTER TABLE `RRHH`
     MODIFY COLUMN Work_load_Average_day FLOAT
   , MODIFY COLUMN Disciplinary_failure  BOOL
   , MODIFY COLUMN Social_drinker        BOOL
   , MODIFY COLUMN Social_smoker         BOOL
   , MODIFY COLUMN Pet                   TINYINT
   , MODIFY COLUMN Son                   TINYINT
   , MODIFY COLUMN Education             TINYINT;

/*
                 Pasando de:           A:
Field                    Type (antes)  Type
-----------------------  ------------  ----------
ID                       int           int
Reason_absence           int           int
Month_absence            int           int
Day_week                 int           int
Seasons                  int           int
Transportation_expense   int           int
Distance_Residence_Work  int           int
Service_time             int           int
Age                      int           int
Work_load_Average_day    varchar(512)  float
Hit_target               int           int
Disciplinary_failure     varchar(512)  tinyint(1)
Education                varchar(512)  tinyint
Son                      varchar(512)  tinyint
Social_drinker           varchar(512)  tinyint(1)
Social_smoker            varchar(512)  tinyint(1)
Pet                      varchar(512)  tinyint
Weight                   int           int
Height                   int           int
Body_mass_index          int           int
Absenteeism_hours        int           int
























a:


