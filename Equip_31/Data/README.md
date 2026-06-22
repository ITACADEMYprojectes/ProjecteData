# Data Carpeta para almacenar datos del proyecto

# Estructura de la carpeta Data

Esta carpeta contiene los datasets utilizados en el proyecto.

Históricamente, la mayoría de datasets del proyecto seguían una estructura simple:

```text
raw data → clean data
```

Donde:

- `raw/` contiene los datasets fuente.
- `clean/` contiene los datasets limpios utilizados para el análisis.

Para los datos de la **[EAL](https://www.mites.gob.es/es/estadisticas/mercado_trabajo/EAL/welcome.htm)**, el flujo de trabajo es más detallado porque los archivos Excel originales contienen múltiples tablas con estructuras diferentes. Por este motivo, el proceso de extracción de la EAL incluye fases intermedias y procesadas:

```text
raw/EAL_15062026 → pre_processed_2020_2024/EAL_15062026 → Processed_2020_2024/EAL_15062026 → clean/EAL_15062026
```

## raw/

Contiene los archivos originales o fuente, sin modificaciones manuales.

## pre_processed/

Contiene archivos intermedios generados durante el proceso de extracción o transformación.

En el caso de la EAL, esta carpeta contiene archivos CSV extraídos de las tablas originales de Excel. Estos archivos son útiles para revisar el proceso de extracción, pero no necesariamente están listos para el análisis final.

## processed/

Contiene archivos estructurados y procesados.

En el caso de la EAL, esta carpeta contiene tablas limpias y transformadas, una para cada año y tabla, así como un documento con todo unificado. Tiene datos de 2020 a 2024.

## clean/

Contiene los datasets finales utilizados para el análisis.

En el caso de la EAL, esta carpeta contiene datasets filtrados y unidos por temática, creados a partir de los archivos procesados para responder a la pregunta de negocio final. Actualmente solo está disponible con datos de 2024.

## Notas

El uso de las carpetas puede variar ligeramente según el dataset o la fase del proyecto. Los datasets anteriores pueden utilizar únicamente `raw/` y `clean/`, mientras que la EAL utiliza un flujo más detallado debido a la complejidad de los archivos originales.
