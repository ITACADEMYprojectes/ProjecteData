# Scripts

Carpeta para almacenar notebooks y scripts del equipo.

## Notebooks EAL 2020-2024

Los notebooks de la Encuesta Anual Laboral (EAL) estan numerados segun el orden recomendado de ejecucion:

1. `01_eal_2020_2024_extract_excel_to_csv.ipynb`
   Extrae los Excel originales de EAL desde `Data/raw/EAL_15062026/` y genera CSV preprocesados en `Data/pre_processed_2020_2024/EAL_15062026/`.

2. `02_eal_2020_2024_transform_csv_to_processed_outputs.ipynb`
   Transforma los CSV preprocesados y genera salidas estructuradas en `Data/Processed_2020_2024/EAL_15062026/`.

3. `03_eal_2020_2024_clean_complete_outputs.ipynb`
   Prepara salidas limpias a partir de los datos procesados.

4. `04_eal_2020_2024_clean_grouped_outputs.ipynb`
   Agrupa y normaliza salidas para el analisis posterior.

5. `05_eal_2020_2024_analyze_competencies.ipynb`
   Analiza competencias a partir de los datos EAL.

6. `06_eal_2020_2024_analyze_training_barriers.ipynb`
   Analiza barreras y necesidades de formacion.

El resto de notebooks corresponden a analisis historicos del proyecto: absentismo, perfil, EDA y KPIs.
