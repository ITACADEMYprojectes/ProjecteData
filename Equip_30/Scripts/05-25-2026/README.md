# Scripts Carpeta para almacenar los scripts

## Estructura del proyecto
El proyecto se divide en módulos que siguen la lógica de CRISP-DM:

Scripts/ 
    ├── 05-25-2026/ # Scripts de la semana del 25/05/2026

## Ejecutación
Los scripts se ejecutan uno por uno:
1. Bank_Marketing_load_data-25_May.ipynb
2. Bank_Marketing_eda-25_May.ipynb
3. Bank_Marketing_clean_data-25_May.ipynb
4. Bank_Marketing_Report_M&C-25_May.ipynb
5. Bank_Marketing_Report_Perfil_usuario-25_May.ipynb
6. Bank_Marketing_Report_Finance_credit_risk_analysis-25_May.ipynb


# Descripción
1. **Bank_Marketing_load_data-25_May.ipynb**
- *Función:* Carga los datos sin procesar, verifica su integridad y los guarda en `Data/05-25-2026`. Usa el archivo 'Bank_Marketing_config-25_May.json' para connectar a la base de datos.

    1.1. **Bank_Marketing_config-25_May.json**
    - *Función:* Contiene los datos para connectar a la base de datos.


2. **Bank_Marketing_eda-25_May.ipynb**
- *Función:* Exploración Inicial de los Datos (Exploratory Data Analysis - EDA).


3. **Bank_Marketing_clean_data-25_May.ipynb**
- *Función:* Procesa los datos faltantes, los valores atípicos y las categorías de códigos. Guarda los datos limpios en `Data/05-25-2026`.


4. **Bank_Marketing_Report_M&C-25_May.ipynb**
- *Función:* El análisis de Marketing y Comunicación. 


5. **Bank_Marketing_Report_Perfil_usuario-25_May.ipynb**
- *Función:* El análisis del Perfil del Cliente.


6. **Bank_Marketing_Report_Finance_credit_risk_analysis-25_May.ipynb**
- *Función:* El análisis de Finanzas y Riesgo Crediticio.


