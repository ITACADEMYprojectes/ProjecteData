# Data Carpeta para almacenar datos del proyecto.

Esta carpeta contiene los principales archivos de datos utilizados en el proyecto **StaySpain — 29/06/2026**.

El flujo de preparación de los datos ha seguido cuatro etapas:

1. **Data Understanding**
2. **Data Cleaning**
3. **Data Transformation**
4. **Data Reduction**

El resultado final de este proceso es el archivo:

`clean_dataset_29_06_2026.csv`

## Archivos incluidos

### `raw_dataset_29_06_2026.csv`

Dataset original utilizado como punto de partida del proyecto.

Contiene:

- 7.001 registros;
- 35 variables;
- información sobre alojamientos, precios, disponibilidad y valoraciones;
- varios registros repetidos por `apartment_id`, correspondientes a distintas actualizaciones temporales del mismo alojamiento.

Durante la fase de Data Understanding se identificaron duplicados no exactos, valores nulos estructurales en las variables de reseñas y posibles inconsistencias en las escalas de puntuación. :contentReference[oaicite:0]{index=0}

### `Data_Understanding_29_06_2026.pdf`

Documento de análisis inicial del dataset.

Incluye:

- contexto y origen de los datos;
- descripción de las variables;
- revisión de duplicados;
- análisis de valores nulos;
- limitaciones iniciales;
- áreas prioritarias para el análisis.

Los duplicados por `apartment_id` fueron interpretados como snapshots temporales del mismo alojamiento, por lo que se decidió conservar el registro más reciente para analizar el estado actual. :contentReference[oaicite:1]{index=1}

### `clean_dataset_29_06_2026.csv`

Dataset final utilizado por los notebooks de análisis departamental y por el dashboard de KPI.

Contiene:

- 6.733 alojamientos únicos;
- 18 variables seleccionadas;
- una única fila por `apartment_id`;
- variables transformadas y validadas;
- únicamente las columnas necesarias para responder a las preguntas de negocio y calcular los KPI del Sprint.

## Proceso de preparación

### 1. Data Cleaning

En esta fase se realizaron las principales tareas de limpieza:

- selección del registro más reciente por `apartment_id`;
- tratamiento de duplicados;
- revisión de valores nulos;
- validación de tipos de datos;
- corrección de formatos;
- comprobación de escalas y coherencia de las variables.

[Ver notebook de Data Cleaning](https://github.com/ITACADEMYprojectes/ProjecteData/blob/Equip_34/Equip_34/Scripts/Data_Cleaning_29_06_2026.ipynb)

### 2. Data Transformation

En esta fase se crearon y adaptaron variables necesarias para el análisis:

- conversión de variables booleanas;
- normalización de puntuaciones;
- creación de variables de ocupación;
- cálculo de tasas de ocupación;
- preparación de variables derivadas para los KPI.

[Ver notebook de Data Transformation](https://github.com/ITACADEMYprojectes/ProjecteData/blob/Equip_34/Equip_34/Scripts/data_transform_29_06_2026.ipynb)

### 3. Data Reduction

En esta fase se seleccionaron únicamente las variables necesarias para:

- Marketing y Estrategia Comercial;
- Operaciones y Gestión de Inventario;
- Experiencia del Cliente;
- cálculo de los KPI definidos por el equipo.

No se eliminaron los alojamientos sin reseñas, ya que siguen siendo válidos para otros análisis. Estos registros se excluyen únicamente en los cálculos que requieren una valoración válida.

[Ver notebook de Data Reduction](https://github.com/ITACADEMYprojectes/ProjecteData/blob/Equip_34/Equip_34/Scripts/data_reduction_29_06_2026.ipynb)

## Estructura del dataset final

Las variables finales son:

- `apartment_id`
- `city`
- `room_type`
- `price_€`
- `availability_30`
- `availability_60`
- `availability_90`
- `availability_365`
- `has_availability_numeric`
- `occupancy_30`
- `occupancy_rate_30`
- `review_scores_rating`
- `review_scores_accuracy`
- `review_scores_cleanliness`
- `review_scores_checkin`
- `review_scores_communication`
- `review_scores_location`
- `rating_above_80`

## Uso del dataset final

Todos los notebooks de análisis deben utilizar:

`Data/clean_dataset_29_06_2026.csv`

De esta forma se garantiza que los resultados de Marketing, Operaciones, Experiencia del Cliente y KPI se calculen sobre una única fuente de datos común, limpia y reproducible.
