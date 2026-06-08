# Data Carpeta para almacenar datos del proyecto.

## Estructura del proyecto
El proyecto se divide en módulos que siguen la lógica de CRISP-DM:

Data/ 
    ├── 05-25-2026/ # Los datos de la semana del 25/05/2026
    ├── 06-01-2026/ # Los datos de la semana del 01/06/2026
    README.md


## Descripción del archivo
├── 05-25-2026/ 
    1. **05-25-2026_Raw.csv** 
        - *Origen:* Exportación desde la base de datos "Equip_30", fecha de descarga: 26 de mayo de 2026.
        - *Descripción:* Los datos están relacionados con campañas de marketing directo (llamadas telefónicas) de una entidad bancaria.

    2. **05-25-2026_Clean.csv**
        - *Cómo se obtuvo:* Salida del script 'Scripts/05-25-2026/05-25-2026_Clean-Data.ipynb'.
        - *Uso:* Cargado directamente en:
                - 'Scripts/05-25-2026/05-25-2026_Analysis-Marketing.ipynb'
                - 'Scripts/05-25-2026/05-25-2026_Analysis-Client-Profile.ipynb'.
                - 'Scripts/05-25-2026/05-25-2026_Analysis-Finance-Credit-Risk.ipynb'.


├── 06-01-2026/ 
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