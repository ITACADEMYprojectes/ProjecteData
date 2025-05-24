# Carpeta `data/`

Esta carpeta contiene los conjuntos de datos usados para el análisis.
Aquí se almacenan tanto los archivos originales como aquellos que han sido preprocesados para su análisis posterior.


## Nomenclatura de archivos

Todos los archivos siguen una convención basada en la fecha de inicio del dataset, en formato `aammdd`, y comienzan con el prefijo `df`:

- `df_original_aammdd.csv`: versión original sin modificaciones ni limpieza, extracción directa de MySQL Workbench.
- `df_aammdd.csv`: versión procesada y lista para análisis.


## Flexibilidad en la estructura

Aunque esta es la estructura base definida para cada sprint o semana de trabajo, queda abierta la posibilidad de añadir otros archivos según lo requiera el análisis.
Todos ellos deberán seguir la misma convención:

- Comenzar con el prefijo `df`
- Terminar con la fecha de inicio del dataset en formato `aammdd`

De este modo se asegura consistencia en la organización de los datos y se facilita su trazabilidad.


## Archivos actuales

- `df_original_250512.csv`
- `df_250512.csv`
- `df_original_250519.csv`