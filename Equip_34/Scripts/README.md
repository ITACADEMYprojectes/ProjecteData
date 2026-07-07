# Scripts Carpeta para almacenar los scripts

Esta carpeta contiene los notebooks utilizados durante el Sprint 1 del proyecto **StaySpain**.

El flujo de trabajo se divide en dos bloques principales:

1. preparación y validación de los datos;
2. Análisis por área de negocio.

Todos los análisis finales utilizan como fuente común el archivo:

`Data/clean_dataset_29_06_2026.csv`

De esta forma, Marketing, Operaciones, Experiencia del Cliente y los KPI trabajan sobre un dataset único, limpio y reproducible.

---

## Flujo de preparación de los datos

El proceso seguido por el equipo fue:

`EDA → Data Cleaning → Data Transformation → Data Reduction → Dataset final`

### 1. EDA

[Ver notebook EDA](https://github.com/ITACADEMYprojectes/ProjecteData/blob/Equip_34/Equip_34/Scripts/EDA_29_06_2026.ipynb)

Este notebook realiza la exploración inicial del dataset y permite identificar:

- dimensiones y estructura de los datos;
- tipos de variables;
- valores nulos;
- duplicados;
- distribuciones;
- valores atípicos;
- posibles inconsistencias;
- relaciones entre variables.

Su objetivo es comprender la calidad y el comportamiento general de los datos antes de iniciar las fases de preparación.

### 2. Data Cleaning

[Ver notebook Data Cleaning](https://github.com/ITACADEMYprojectes/ProjecteData/blob/Equip_34/Equip_34/Scripts/Data_Cleaning_29_06_2026.ipynb)

En esta fase se realizan las tareas principales de limpieza:

- tratamiento de duplicados;
- selección del registro más reciente por `apartment_id`;
- revisión de valores nulos;
- corrección de formatos;
- validación de tipos de datos;
- comprobación de escalas;
- control de coherencia entre variables.

El objetivo es obtener una base fiable para las siguientes fases del proyecto.

### 3. Data Transformation

[Ver notebook Data Transformation](https://github.com/ITACADEMYprojectes/ProjecteData/blob/Equip_34/Equip_34/Scripts/data_transform_29_06_2026.ipynb)

En este notebook se crean y adaptan las variables necesarias para los análisis y los KPI.

Entre las principales transformaciones se incluyen:

- conversión de variables booleanas;
- normalización de puntuaciones;
- creación de variables derivadas;
- cálculo de ocupación;
- cálculo de tasas de ocupación;
- preparación de indicadores de satisfacción.

### 4. Data Reduction

[Ver notebook Data Reduction](https://github.com/ITACADEMYprojectes/ProjecteData/blob/Equip_34/Equip_34/Scripts/data_reduction_29_06_2026.ipynb)

En esta fase se seleccionan únicamente las variables necesarias para responder a las preguntas de negocio del Sprint.

La reducción permite:

- eliminar columnas que no aportan información a los análisis finales;
- mantener las variables necesarias para los KPI;
- simplificar el dataset;
- mejorar la claridad y eficiencia de los notebooks analíticos.

El resultado final es:

`Data/clean_dataset_29_06_2026.csv`

---

## Análisis por área de negocio

### 5. Marketing y Estrategia Comercial

[Ver notebook de Marketing](https://github.com/ITACADEMYprojectes/ProjecteData/blob/Equip_34/Equip_34/Scripts/analisis_marketing_29_06_2026.ipynb)

Pregunta de negocio:

**¿Cuál es el precio medio de los alojamientos por tipo de alojamiento en cada ciudad?**

Este análisis estudia:

- precio medio y mediano;
- diferencias entre ciudades;
- diferencias entre tipos de alojamiento;
- segmentación entre alojamientos de coste alto y bajo;
- interacción entre ciudad y tipo de alojamiento;
- validación estadística de las diferencias observadas.

### 6. Operaciones y Gestión de Inventario

[Ver notebook de Operaciones](https://github.com/ITACADEMYprojectes/ProjecteData/blob/Equip_34/Equip_34/Scripts/an%C3%A1lisis_operaciones_gesti%C3%B3n_inventario_29_06_2026.ipynb)

Pregunta de negocio:

**¿Cuál es la disponibilidad media de los alojamientos turísticos en los distintos plazos de 30, 60, 90 y 365 días en cada ciudad?**

Este análisis estudia:

- disponibilidad media por ciudad;
- disponibilidad según el horizonte temporal;
- diferencias entre ciudades;
- relación entre volumen de alojamientos y disponibilidad;
- oportunidades para mejorar la ocupación.

### 7. Experiencia del Cliente

[Ver notebook de Experiencia del Cliente](https://github.com/ITACADEMYprojectes/ProjecteData/blob/Equip_34/Equip_34/Scripts/analisis_experiencia_cliente_29_06_2026.ipynb)

Pregunta de negocio:

**¿Cuál es la puntuación media dada por los usuarios a los alojamientos turísticos y qué porcentaje de alojamientos tienen una evaluación general superior a 80 en cada ciudad?**

Este análisis incluye:

- puntuación media por ciudad;
- número y porcentaje de alojamientos con puntuación superior a 80;
- cobertura de valoraciones;
- distribución de puntuaciones;
- comparación de componentes de satisfacción;
- identificación de fortalezas y oportunidades de mejora;
- validación estadística de las diferencias entre ciudades.

---

## Criterios comunes del proyecto

Todos los notebooks analíticos siguen los mismos criterios:

- uso del dataset final limpio;
- una fila por `apartment_id`;
- exclusión de valores nulos únicamente cuando el cálculo lo requiere;
- conservación del dataset original sin modificaciones dentro de los análisis;
- uso de DataFrames auxiliares;
- visualizaciones coherentes con la paleta del equipo;
- separación entre KPI, EDA y análisis departamental;
- código reproducible y documentado;
- conclusiones basadas en los resultados obtenidos.

---

## Orden recomendado de ejecución

Para reproducir el flujo completo del proyecto:

1. `EDA_29_06_2026.ipynb`
2. `Data_Cleaning_29_06_2026.ipynb`
3. `data_transform_29_06_2026.ipynb`
4. `data_reduction_29_06_2026.ipynb`
5. `analisis_marketing_29_06_2026.ipynb`
6. `análisis_operaciones_gestión_inventario_29_06_2026.ipynb`
7. `analisis_experiencia_cliente_29_06_2026.ipynb`

---

## Estructura del proyecto

```text
Equip_34/
├── Data/
│   ├── raw_dataset_29_06_2026.csv
│   ├── clean_dataset_29_06_2026.csv
│   └── README.md
│
├── Scripts/
│   ├── EDA_29_06_2026.ipynb
│   ├── Data_Cleaning_29_06_2026.ipynb
│   ├── data_transform_29_06_2026.ipynb
│   ├── data_reduction_29_06_2026.ipynb
│   ├── analisis_marketing_29_06_2026.ipynb
│   ├── análisis_operaciones_gestión_inventario_29_06_2026.ipynb
│   ├── analisis_experiencia_cliente_29_06_2026.ipynb
│   └── README.md
│
└── Results/
