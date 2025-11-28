/**
 * Limpieza y adecuación de los datos de la tabla RRHH
 * ---
 */

/**
 * Tablas adicionales, para datos normalizados como
 * la estación del año (Season), el día de la semana o el mes.
 *
 * También incluye una VIEW para mostrar los datos desnormalizados
 * sin necesidad de estar haciendo JOINs cada vez.
 */

-- Estaciones (COLUMN `RRHH.Season`)
CREATE TABLE seasons (
    season TINYINT PRIMARY KEY,
    name   VARCHAR(10) NOT NULL,
    nombre VARCHAR(10) NOT NULL DEFAULT ''
);

INSERT INTO seasons
VALUES (1, 'Summer', 'Verano')
     , (2, 'Autumn', 'Otoño')
     , (3, 'Winter', 'Invierno')
     , (4, 'Spring', 'Primavera')
;

-- Meses del año (RRHH.Month_absence)
CREATE TABLE months (
    month_id  TINYINT     PRIMARY KEY,
    name      VARCHAR(16) NOT NULL,
    name_es   VARCHAR(16) NOT NULL
);

INSERT INTO months
VALUES (1,  'January',   'Enero')
     , (2,  'February',  'Febrero')
     , (3,  'March',     'Marzo')
     , (4,  'April',     'Abril')
     , (5,  'May',       'Mayo')
     , (6,  'June',      'Junio')
     , (7,  'July',      'Julio')
     , (8,  'August',    'Agosto')
     , (9,  'September', 'Septiembre')
     , (10, 'October',   'Octubre')
     , (11, 'November',  'Noviembre')
     , (12, 'December',  'Diciembre')
;

-- Días de la semana
CREATE TABLE day_of_week (
    dow_id    TINYINT     PRIMARY KEY,
    name      VARCHAR(10) NOT NULL,
    name_es   VARCHAR(10) NOT NULL DEFAULT ''
);

INSERT INTO day_of_week (dow_id, name)
VALUES
      (1, 'Sunday')
    , (2, 'Monday')
    , (3, 'Tuesday')
    , (4, 'Wednesday')
    , (5, 'Thursday')
    , (6, 'Friday')
    , (7, 'Saturday')
;

-- Motivos de ausencia (Absenteeism_reason)
CREATE TABLE ab_reason (
    reason_id   TINYINT  PRIMARY KEY,
    description TEXT
);

INSERT INTO ab_reason
VALUES ( 0, 'Unknown')
     , ( 1, 'Certain infectious and parasitic diseases')
     , ( 2, 'Neoplasms')
     , ( 3, 'Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism')
     , ( 4, 'Endocrine, nutritional and metabolic diseases')
     , ( 5, 'Mental and behavioural disorders')
     , ( 6, 'Diseases of the nervous system')
     , ( 7, 'Diseases of the eye and adnexa')
     , ( 8, 'Diseases of the ear and mastoid process')
     , ( 9, 'Diseases of the circulatory system')
     , (10, 'Diseases of the respiratory system')
     , (11, 'Diseases of the digestive system')
     , (12, 'Diseases of the skin and subcutaneous tissue')
     , (13, 'Diseases of the musculoskeletal system and connective tissue')
     , (14, 'Diseases of the genitourinary system')
     , (15, 'Pregnancy, childbirth and the puerperium')
     , (16, 'Certain conditions originating in the perinatal period')
     , (17, 'Congenital malformations, deformations and chromosomal abnormalities')
     , (18, 'Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified')
     , (19, 'Injury, poisoning and certain other consequences of external causes')
     , (20, 'External causes of morbidity and mortality')
     , (21, 'Factors influencing health status and contact with health services.')
     , (22, 'Patient fol-up')
     , (23, 'medical consultation')
     , (24, 'blood, donation')
     , (25, 'laboratory examination')
     , (26, 'unjustified absence')
     , (27, 'physiotherapy')
     , (28, 'dental consultation')
  ;

