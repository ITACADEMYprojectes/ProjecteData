```bash
staySpain-analysis/
│
├── data/
│   ├── raw/                           # Datos crudos (inmutables)
│   │   ├── week_01_2025-09-15/        # Semana 1 - datos originales
│   │   │   └── staySpain_raw.csv
│   │   ├── week_02_2025-09-22/        # Semana 2 - datos originales
│   │   │   └── staySpain_raw.csv
│   │   └── ...                        # Semanas posteriores
│   │
│   └── processed/                     # Datos procesados
│       ├── week_01_2025-09-15/        # Semana 1 - datos procesados
│       │   ├── staySpain_processed.pkl    
│       ├──  week_02_2025-09-22/        # Semana 2 - datos procesados
│       │   └── ... (misma estructura)
│       └── ...
│
├── results/                           # Todos los resultados generados
│   └── week_01_2025-09-15/            # Resultados de la semana 1
│   │   ├── eda/                       # Análisis exploratorio
│   │   │   ├── numerical_summary.txt
│   │   │   ├── categorical_summary.txt
│   │   │   ├── missing_values_plot.png
│   │   │   └── correlation_matrix.png
│   │   ├── marketing/                 # Análisis de marketing
│   │   │   ├── price_segmentation.png
│   │   │   ├── demand_analysis.png
│   │   │   ├── amenity_impact.csv
│   │   │   └── market_trends_report.pdf
│   │   ├── operations/                # Análisis de operaciones
│   │   │   ├── occupancy_rates.png
│   │   │   ├── availability_analysis.png
│   │   │   ├── optimal_pricing.csv
│   │   │   └── operations_report.pdf
│   │   ├── customer_experience/       # Análisis de experiencia
│   │   │   ├── rating_distribution.png
│   │   │   ├── review_analysis.png
│   │   │   ├── satisfaction_factors.csv
│   │   │   └── customer_report.pdf
│   │   └── consolidated_report/       # Reporte integrado
│   │       ├── executive_summary.pdf
│   │       └── dashboard.html
│   │
│   ├──  week_02_2025-09-22/            # Resultados de la semana 2
│   └── ...                            # Semanas posteriores
│
├── scripts/                           # Todos los scripts de análisis
│   ├── utilities/                     # Funciones y utilidades compartidas
│   │   ├── __init__.py               # Hace que utilities sea un paquete Python
│   │   ├── eda_utils.py               # Utilidades para EDA
│   │   ├── kpi_utils.py               # Utilidades para KPI
│   │   └── processing_functions.py      # Funciones de limpieza, transformación y reducción
│   │
│   └── week_01_2025-09-15/            # Scripts de la semana 1
│   │   ├── 01_data_understanding.ipynb  # Resultados del entendimiento de datos
│   │   ├── 02_eda.py                  # EDA
│   │   ├── 03_data_processing.py      # Limpieza, transformación y reducciónLimpieza de datos
│   │   ├── 04a_marketing_analysis.py  # Análisis de marketing
│   │   ├── 04b_operations_analysis.py # Análisis de operaciones
│   │   ├── 04c_customer_analysis.py   # Análisis de experiencia
│   │   └── 05_consolidated_report.py  # Reporte integrado
│   │
│   ├──  week_02_2025-09-22/            # Scripts de la semana 2
│   └── ...                            # Semanas posteriores
│
├── recursos/                          
│
│
├── tests/                             # Pruebas unitarias
│   ├── 
│   └── ...
│
└── README.md                          # Documentación principal
