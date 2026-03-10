# Scripts Carpeta para almacenar los scripts y código fuente.

## Estructura
- /utils : archivo .py con funciones comunes reutilizables para uso tanto en ETL como en análisis 
    · Importar funciones concretas: from utils import "funcion_especifica","otra_funcion"...
    · Comentar/indicar qué scripts dependen de cada función.

- /etl : scripts de extracción, limpieza y transformación de datos. Salida --> /Data/data_cleaning
    Markdowns/secciones estándar: 
    - # Librerias
    - # Carga de datos raw
    - # Limpieza
    - # Transformación
    - # Creación de variables

- /analysis : notebooks de análisis por departamento
    · Un archivo .ipynb por departamento (ej: "mkt_analysis_w2.ipynb")
    · Markdowns/secciones estándar
    - # Librerias
    - # Carga de datos clean
    - # Análisis / Visualizaciones 
    - # Resultados/archivos generados 

## Nombre de archivos
Cambiar "w2" segun semana y "dept" según departamento (mkt,client,opt)
- ETL: etl_"w2".ipynb 
- Análisis: "dept"_analysis_"w2".ipynb

## Buenas prácticas
- No modificar /Data/raw_data directamente. Siempre generar /data_cleaning.
- Usar versiones de scripts (_w2, _w3) para mantener trazabilidad.
