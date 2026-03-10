# Data Carpeta para almacenar datos del proyecto.

## Estructura
- /data_understanding : resumen de los datos raw para comprensión inicial del dataset.
- /raw_data : datos extraídos del script SQL en .csv
    Con cada actualización de datos, nuevo csv de raw_data (ej: raw_data_*w2*)
- /KPI_TA : resumen de los KPI por departamento y generales.

- /data_cleaning: datos procesados, listos para análisis.

## Reglas de uso
- No modificar archivo /raw_data. Solo se actualizan al recibir nueva información desde la fuente de MySQL.
- Archivos limpios deben estar guardados en data_cleaning.
- Nombrar archivos según convención: clean_data_*w2*.csv (w2: cambiar según semana).
- Documentar cualquier transformación hecha en los scripts correspondientes.