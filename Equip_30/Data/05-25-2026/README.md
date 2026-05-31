# Data Carpeta para almacenar datos del proyecto.

## Estructura
results/ 
    ├── 05-25-2026/ # Los datos de la semana del 25/05/2026


## Descripción del archivo
1. **Bank_Marketing_Raw-25_May.csv** 
    - *Origen:* Exportación desde la base de datos "Equip_30", fecha de descarga: 26 de mayo de 2026.
    - *Descripción:* Los datos están relacionados con campañas de marketing directo (llamadas telefónicas) de una entidad bancaria portuguesa.

2. **Bank_Marketing_Clean-25_May.csv**
    - *Cómo se obtuvo:* Salida del script 'Scripts/05-25-2026/Bank_Marketing_clean_data-25_May.ipynb'.
    - *Uso:* Cargado directamente en:
            - 'Scripts/05-25-2026/Bank_Marketing_Report_M&C-25_May.ipynb'
            - 'Scripts/05-25-2026/Bank_Marketing_Report_Perfil_usuario-25_May.ipynb'.
            - 'Scripts/05-25-2026/Bank_Marketing_Report_Finance_credit_risk_analysis-25_May.ipynb'.