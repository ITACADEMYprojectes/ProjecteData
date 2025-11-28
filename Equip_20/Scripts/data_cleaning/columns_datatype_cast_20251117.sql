/**
 * Limpieza y adecuación de los datos de la tabla RRHH
 * ---
 */

/**
 * Alterar los tipos de las columnas  que están como VARCHAR() per que contienen
 * valores de otros tipos.
 */

-- Work_load_average_day no se puede modificar a FLOAT por la coma, así que la
-- cambiamos por un punto antes:
UPDATE RRHH
   SET `Work_load_Average_day` = REPLACE(`Work_load_Average_day`, ',', '.');

-- Modificamos algunos campos de VARCHAR() a un tipo más adecuado al dato que
-- contienen. TINYINT es un valor de 0 a 255 (si es UNSIGNED)
ALTER TABLE `RRHH`
     MODIFY COLUMN Work_load_Average_day FLOAT UNSIGNED
   , MODIFY COLUMN Disciplinary_failure  BOOL
   , MODIFY COLUMN Social_drinker        BOOL
   , MODIFY COLUMN Social_smoker         BOOL
   , MODIFY COLUMN Pet                   TINYINT UNSIGNED
   , MODIFY COLUMN Son                   TINYINT UNSIGNED
   , MODIFY COLUMN Education             TINYINT UNSIGNED;

/**
 *                  Pasando de:           A:
 * Field                    Type (antes)  Type
 * -----------------------  ------------  ----------
 * ID                       int           int
 * Reason_absence           int           int
 * Month_absence            int           int
 * Day_week                 int           int
 * Seasons                  int           int
 * Transportation_expense   int           int
 * Distance_Residence_Work  int           int
 * Service_time             int           int
 * Age                      int           int
 * Work_load_Average_day    varchar(512)  float
 * Hit_target               int           int
 * Disciplinary_failure     varchar(512)  bool
 * Education                varchar(512)  tinyint
 * Son                      varchar(512)  tinyint
 * Social_drinker           varchar(512)  bool
 * Social_smoker            varchar(512)  bool
 * Pet                      varchar(512)  tinyint
 * Weight                   int           int
 * Height                   int           int
 * Body_mass_index          int           int
 * Absenteeism_hours        int           int
 */
