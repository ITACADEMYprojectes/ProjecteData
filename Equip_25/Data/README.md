# Data Carpeta para almacenar datos del proyecto.

## Estructura
- /data_understanding : resumen de los datos raw para comprensión inicial del dataset.
- /raw_data_"date" : datos extraídos del script SQL en .csv
    Con cada actualización de datos, nuevo csv de raw_data (ej: raw_data_ddmmyy)
- /KPI_TA : resumen de los KPI por departamento y generales.

- /data_cleaning: datos procesados, listos para análisis.
- /figures : Gráficos para uso en reportes

## Nombre de archivos
- Nombrar archivos según convención: clean_data_ddmmyy.csv (ddmmyy: cambiar según semana).
- Gráficos: fig_"dpt"_"tipo"_"info".png (ej: fig_operaciones_lineplot_reservas.png)

## Reglas de uso
- No modificar archivo /raw_data_date. Solo se actualizan al recibir nueva información desde la fuente de MySQL.
- Archivos limpios deben estar guardados en data_cleaning.
- Documentar cualquier transformación hecha en los scripts correspondientes.

