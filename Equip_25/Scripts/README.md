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
    · Un archivo .ipynb por departamento (ej: "marketing_analysis_w2.ipynb")
    · Markdowns/secciones estándar
    - # Librerias
    - # Carga de datos clean
    - # Análisis / Visualizaciones 
    - # Resultados/archivos generados 

## Nombre de archivos
Cambiar fecha segun semana y "dpt" según departamento (marketing,cliente,operaciones)
- ETL: etl_ddmmyy.ipynb 
- Análisis: "dpt"_analysis_ddmmyy.ipynb

## Buenas prácticas
- No modificar /Data/raw_data directamente. Siempre generar /data_cleaning.
- Usar versiones de scripts (_v2, _v3) para mantener trazabilidad.
