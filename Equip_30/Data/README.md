# Data Carpeta para almacenar datos del proyecto.

## Estructura del proyecto
El proyecto se divide en módulos que siguen la lógica de CRISP-DM:

Data/ 

    ├── 05-25-2026/ # Los datos de la semana del 25/05/2026

    ├── 06-01-2026/ # Los datos de la semana del 01/06/2026

    ├── 06-08-2026/ # Los datos de la semana del 08/06/2026

    ├── 06-15-2026/ # Los datos de la semana del 15/06/2026
    
    README.md


## Descripción del archivo
### ├── 05-25-2026/ 
    1. **05-25-2026_Raw.csv** 
    
        - *Origen:* Exportación desde la base de datos "Equip_30", fecha de descarga: 26 de mayo de 2026.

        - *Descripción:* Los datos están relacionados con campañas de marketing directo (llamadas telefónicas) de una entidad bancaria.

    2. **05-25-2026_Clean.csv**
        - *Cómo se obtuvo:* Salida del script 'Scripts/05-25-2026/05-25-2026_Clean-Data.ipynb'.
        - *Uso:* Cargado directamente en:
                - 'Scripts/05-25-2026/05-25-2026_Analysis-Marketing.ipynb'
                - 'Scripts/05-25-2026/05-25-2026_Analysis-Client-Profile.ipynb'.
                - 'Scripts/05-25-2026/05-25-2026_Analysis-Finance-Credit-Risk.ipynb'.


### ├── 06-01-2026/ 
    1. **06-01-2026_Raw.csv**

        - *Origen:* Exportación desde la base de datos "Equip_30", fecha de descarga: 01 de junio de 2026.

        - *Descripción:* Los datos están relacionados con campañas de marketing directo (llamadas telefónicas) de una entidad bancaria.

    2. **06-01-2026_Clean.csv**

        - *Cómo se obtuvo:* Salida del script 'Scripts/06-01-2026/06-01-2026_Clean-Data.ipynb'.

        - *Uso:* Cargado directamente en:
                - 'Scripts/06-01-2026/06-01-2026_Analysis-Marketing.ipynb'
                - 'Scripts/06-01-2026/06-01-2026_Analysis-Client-Profile.ipynb'.
                - 'Scripts/06-01-2026/06-01-2026_Analysis-Finance-Credit-Risk.ipynb'.

    3. **06-01-2026_Marketing_Analysis.csv**

        - *Cómo se obtuvo:* Salida del script 'Scripts/06-01-2026/06-01-2026_Marketing_Analysis.ipynb'.

        - *Uso:* Cargado directamente en:
                - 'Scripts/06-01-2026/06-01-2026_Analysis-Marketing.ipynb'

    4. **06-01-2026_Clusters_clients.csv**

        - *Cómo se obtuvo:* Salida del script 'Scripts/05-25-2026/05-25-2026_Analysis-Client-Profile.ipynb' con los datos del archivo 'Scripts/05-25-2026/05-25-2026_Clean-Data.ipynb'.
    
        - *Uso:* Cargado directamente en:
                - 'Scripts/06-01-2026/06-01-2026_Analysis-Finance-Credit-Risk.ipynb'


### ├── 06-08-2026/ 
    1. **06-08-2026_Raw.csv** 

        - *Origen:* Exportación desde la base de datos "Equip_30", fecha de descarga: 08 de junio de 2026.

        - *Descripción:* Los datos están relacionados con campañas de marketing directo (llamadas telefónicas) de una entidad bancaria.

    2. **06-08-2026_Clean.csv**

        - *Cómo se obtuvo:* Salida del script 'Scripts/06-01-2026/06-01-2026_Clean-Data.ipynb'.

        - *Uso:* Cargado directamente en:
                - 'Scripts/06-08-2026/06-08-2026_Analysis-Marketing.ipynb'
                - 'Scripts/06-08-2026/06-08-2026_Analysis-Client-Profile.ipynb'.
                - 'Scripts/06-08-2026/06-08-2026_Analysis-Finance.ipynb'.


### ├── 06-15-2026/ 
        ├── EFC_2021

        1. **06-15-2026_raw_ecf_2021.csv.zip** 

        - *Origen:* Página web del Banco de España https://app.bde.es/efs_ecf/, fecha de descarga: 15 de junio de 2026.

        - *Descripción:* Los datos de la Encuesta de competencias financieras de 2021

        - *Uso:* Cargado directamente en:
                - 'Scripts/06-15-2026/06-15-2026_Analisis-comportamiento-financiero.ipynb'
                - 'Scripts/06-15-2026/06-15-2026_Analisis-competencias-financieras.ipynb'

        2. **06-15-2026_ecf_2021_imp.csv**

        - *Origen:* Página web del Banco de España https://app.bde.es/efs_ecf/, fecha de descarga: 15 de junio de 2026.

        - *Descripción:* Los datos de la Encuesta de competencias financieras de 2021, contiene las variables imputadas.
        
        - *Uso:* Cargado directamente en:
                - 'Scripts/06-15-2026/06-15-2026_Analisis-comportamiento-financiero.ipynb'


        ├── INE_2026_2030

        1. **06-15-2026_poblacion_2024-2074.csv** 

        2. **06-15-2026_indice_envejecimiento.csv** 

        3. **06-15-2026_edad_media_2024-2039.csv** 

        4. **06-15-2026_tasa_dependencia_poblacion_mayor.csv**

        - *Origen:* Página web del Instituto Nacional de Estadística 
        https://www.ine.es/dyngs/INEbase/es/categoria.htm?c=Estadistica_P&cid=1254734710984, fecha de descarga: 15 de junio de 2026.

        - *Descripción:* Los datos de las operaciones estadísticas que el INE elabora de forma periódica

        - *Uso:* Cargado directamente en:
                - 'Scripts/06-15-2026/06-15-2026_Analisis-comportamiento-financiero.ipynb'
                - 'Scripts/06-15-2026/06-15-2026_Analisis-competencias-financieras.ipynb'

        5. **06-08-2026_Clean.csv**

        - *Cómo se obtuvo:* Salida del script 'Scripts/06-15-2026/06-15-2026_Analisis-proyeccion-poblacional-Espana_(2026-2036).ipynb'.

