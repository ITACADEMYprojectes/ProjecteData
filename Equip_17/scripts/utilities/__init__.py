"""
Módulo utilities para el proyecto StaySpain - Análisis de Datos

Este paquete contiene funciones auxiliares para el procesamiento y análisis
de datos de la plataforma de alojamientos turísticos.

Módulos incluidos:
- cleaning_functions: Funciones para limpieza de datos
- transformation_functions: Funciones para transformación de datos  
- reduction_functions: Funciones para reducción de datos
- eda_utils: Utilidades para análisis exploratorio de datos (EDA)
- visualization_utils: Utilidades para visualización
- marketing_utils: Utilidades para análisis de marketing
- operations_utils: Utilidades para análisis de operaciones
- customer_experience_utils: Utilidades para análisis de experiencia del cliente
"""

# Importaciones principales de cada módulo
from .cleaning_functions import (
    handle_missing_values,
    correct_data_types,
    remove_duplicates,
    handle_outliers,
    standardize_amenities_format
)

from .transformation_functions import (
    create_new_variables,
    encode_categorical_variables,
    extract_amenities_features,
    normalize_data,
    create_property_segments
)

from .reduction_functions import (
    select_relevant_variables,
    filter_records,
    aggregate_data,
    reduce_dimensionality,
    optimize_memory_usage
)

# Importar funciones de EDA
from .eda_utils import (
    set_plot_style,
    generate_summary_statistics,
    plot_numeric_distributions,
    plot_categorical_distributions,
    plot_correlation_matrix,
    plot_boxplots_by_category,
    plot_scatterplots,
    plot_missing_values,
    analyze_price_relationships
)

# from .visualization_utils import (
#     set_plot_style,
#     save_plot,
#     create_custom_palette,
#     plot_correlation_matrix,
#     plot_distribution,
#     plot_geographical_data
# )

# from .marketing_utils import (
#     analyze_price_segmentation,
#     calculate_demand_indicators,
#     identify_amenity_impact,
#     generate_market_trends
# )

# from .operations_utils import (
#     calculate_occupancy_rates,
#     analyze_availability_patterns,
#     optimize_minimum_nights,
#     forecast_demand
# )

# from .customer_experience_utils import (
#     analyze_rating_patterns,
#     calculate_satisfaction_scores,
#     identify_review_trends,
#     extract_keywords_from_reviews
# )

# Lista de lo que se exporta con "from utilities import *"
__all__ = [
    # Funciones de limpieza
    'handle_missing_values',
    'correct_data_types',
    'remove_duplicates',
    'handle_outliers',
    'standardize_amenities_format',
    
    # Funciones de transformación
    'create_new_variables',
    'encode_categorical_variables',
    'extract_amenities_features',
    'normalize_data',
    'create_property_segments',
    
    # Funciones de reducción
    'select_relevant_variables',
    'filter_records',
    'aggregate_data',
    'reduce_dimensionality',
    'optimize_memory_usage',
    
    # Funciones de EDA
    'set_plot_style',
    'generate_summary_statistics',
    'plot_numeric_distributions',
    'plot_categorical_distributions',
    'plot_correlation_matrix',
    'plot_boxplots_by_category',
    'plot_scatterplots',
    'plot_missing_values',
    'analyze_price_relationships',
    
    # # Funciones de visualización
    # 'set_plot_style',
    # 'save_plot',
    # 'create_custom_palette',
    # 'plot_correlation_matrix',
    # 'plot_distribution',
    # 'plot_geographical_data',
    
    # # Funciones de marketing
    # 'analyze_price_segmentation',
    # 'calculate_demand_indicators',
    # 'identify_amenity_impact',
    # 'generate_market_trends',
    
    # # Funciones de operaciones
    # 'calculate_occupancy_rates',
    # 'analyze_availability_patterns',
    # 'optimize_minimum_nights',
    # 'forecast_demand',
    
    # # Funciones de experiencia del cliente
    # 'analyze_rating_patterns',
    # 'calculate_satisfaction_scores',
    # 'identify_review_trends',
    # 'extract_keywords_from_reviews'
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