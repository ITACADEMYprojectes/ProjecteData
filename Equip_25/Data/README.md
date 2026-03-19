# Data Carpeta para almacenar datos del proyecto.

## Estructura
- /raw_data_"date" : datos extraídos del script SQL en .csv
    Con cada actualización de datos, nuevo csv de raw_data (ej: raw_data_ddmmyy)

- /clean_data_"date": datos procesados, listos para análisis (sin precios nulos)
- /cleand_data_nulos_"date": datos procesados, con los precios nulos

## Nombre de archivos
- Nombrar archivos según convención: clean_data_dd-mm-yy.csv (ddmmyy: cambiar según semana).

## Reglas de uso
- No modificar archivo /raw_data_date. Solo se actualizan al recibir nueva información desde la fuente de MySQL.


