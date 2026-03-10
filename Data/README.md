📊 Data Understanding — Rapid Express

Este proyecto analiza un conjunto de datos relacionado con el ausentismo laboral en la empresa Rapid Express. El objetivo es comprender los factores que pueden influir en las ausencias de los empleados y preparar los datos para análisis posteriores.

📁 Descripción del Dataset

El conjunto de datos contiene 740 registros y 21 variables.
Cada fila representa un episodio de ausencia laboral de un empleado, mientras que las columnas describen características relacionadas con el trabajador, su entorno laboral y su contexto personal.

Una ventaja importante del dataset es que no contiene valores faltantes, lo que facilita el proceso de análisis y modelado.

🧾 Tipos de Variables

Las variables del dataset se pueden agrupar en distintas categorías:

⏱️ Variables de Identificación y Contexto Temporal

Estas variables ayudan a identificar el momento y contexto en que ocurrió la ausencia:

Employee ID — Identificador único del empleado

Month of Absence — Mes en que ocurrió la ausencia

Day of the Week — Día de la semana

Seasons — Estación del año

🏢 Variables del Entorno Laboral

Describen características relacionadas con el trabajo dentro de Rapid Express:

Reason for Absence — Motivo de la ausencia

Service Time — Tiempo de servicio en la empresa

Workload Average per Day — Carga de trabajo promedio diaria

Hit Target — Indica si el empleado alcanzó el objetivo establecido

👤 Perfil Personal y de Salud

Incluyen información demográfica y condiciones de salud de los empleados:

Age — Edad

Weight — Peso

Height — Altura

Body Mass Index (BMI) — Índice de masa corporal

🧬 Hábitos y Estilo de Vida

Factores personales que pueden influir indirectamente en el ausentismo:

Social Drinker — Consumo de alcohol

Social Smoker — Tabaquismo

Pet — Número de mascotas

🎓 Información Socio-Demográfica

Variables relacionadas con el contexto familiar y educativo:

Education — Nivel educativo

Son — Número de hijos

🚗 Factores de Movilidad

Aspectos relacionados con el desplazamiento al trabajo:

Distance from Residence to Work — Distancia entre el hogar y el lugar de trabajo

Transportation Expense — Gasto en transporte

🎯 Variable Objetivo

La variable principal del análisis es:

Absenteeism Time in Hours

Esta variable mide el número de horas de ausencia registradas en cada incidencia.

Los valores presentan una distribución amplia, desde 0 horas hasta casos extremos de 40 horas, lo que sugiere la posible presencia de valores atípicos (outliers) que deberán analizarse en etapas posteriores del proyecto.

🔎 Calidad y Preparación de los Datos

Durante la inspección inicial del dataset se identificaron algunos aspectos relevantes:

✔️ No existen valores nulos en el conjunto de datos.
✔️ Se detectaron inconsistencias en el formato de algunas variables, que fueron corregidas.
✔️ Algunas variables codificadas como números representaban categorías sin orden jerárquico, por lo que se trataron como variables categóricas.

Estas correcciones se realizaron como parte de la fase de preprocesamiento, con el objetivo de garantizar la calidad, coherencia y fiabilidad de los datos antes de avanzar hacia análisis exploratorios y modelos predictivos.
