"""
Módulo utilities para el proyecto StaySpain - Análisis de Datos

Este paquete contiene funciones auxiliares para el procesamiento y análisis
de datos de la plataforma de alojamientos turísticos.

Módulos incluidos:
- eda_utils: Utilidades para análisis exploratorio de datos (EDA)
- data_processing_functions: Funciones para limpieza, transformación y reducción
"""

# Importar funciones de EDA
# from .eda_utils import (
#     set_plot_style,
#     generate_summary_statistics,
#     plot_numeric_distributions,
#     plot_categorical_distributions,
#     plot_correlation_matrix,
#     plot_boxplots_by_category,
#     plot_scatterplots,
#     plot_missing_values,
#     analyze_price_relationships
# )


# Importaciones principales de cada módulo
from .data_processing_functions import (
    #Data Cleaning Functions
    handle_duplicates,
    input_price,
    correct_data_types_str_to_date,
    correct_data_types_str_to_int,
    fill_name,
    fill_descriptions,

    #Data Transformation Functions
    extract_amenities_features,

    #Data Reduction Functions
)

# Lista de lo que se exporta con "from utilities import *"
__all__ = [

    # Funciones de EDA
    # 'set_plot_style',
    # 'generate_summary_statistics',
    # 'plot_numeric_distributions',
    # 'plot_categorical_distributions',
    # 'plot_correlation_matrix',
    # 'plot_boxplots_by_category',
    # 'plot_scatterplots',
    # 'plot_missing_values',
    # 'analyze_price_relationships'


    #Data Cleaning Functions
    'handle_duplicates',
    'input_price',
    'correct_data_types_str_to_date',
    'correct_data_types_str_to_int',
    'fill_name',
    'fill_descriptions',
    
    #Data Transformation Functions
   'extract_amenities_features'

    #Data Reduction Functions

]

# Configuración inicial (opcional)
import matplotlib.pyplot as plt
import warnings

# Configurar estilo de plots por defecto
plt.style.use('seaborn-v0_8')

# Filtrar advertencias irrelevantes
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Mensaje de confirmación de carga
print(f"Paquete utilities cargado correctamente. {len(__all__)} funciones disponibles.")