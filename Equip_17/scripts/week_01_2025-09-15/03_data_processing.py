import pandas as pd
import sys
import os
from pathlib import Path
import importlib.util

# Obtener la ruta absoluta al directorio del proyecto
project_root = Path(__file__).resolve().parent.parent.parent
utilities_path = project_root / "scripts" / "utilities"

# Ruta al archivo data_processing_functions.py
data_processing_functions_file = utilities_path / "data_processing_functions.py"

# Verificar si el archivo existe
if not data_processing_functions_file.exists():
    print(f"ERROR: No se encuentra el archivo {data_processing_functions_file}")
    sys.exit(1)

# Cargar el módulo manualmente
spec = importlib.util.spec_from_file_location("data_processing_functions", data_processing_functions_file)
data_processing_functions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_processing_functions)

# Ahora puedes usar las funciones del módulo
handle_duplicates = data_processing_functions.handle_duplicates
input_price = data_processing_functions.input_price
correct_data_types_str_to_date = data_processing_functions.correct_data_types_str_to_date
correct_data_types_str_to_int = data_processing_functions.correct_data_types_str_to_int
fill_name = data_processing_functions.fill_name
fill_descriptions = data_processing_functions.fill_descriptions
reviews_format = data_processing_functions.reviews_format
extract_amenities_features = data_processing_functions.extract_amenities_features


def main():
    # Configurar rutas
    current_week = "week_01_2025-09-15"
    input_path = project_root / "data" / "raw" / current_week / "staySpain_raw.csv"
    output_path = project_root / "data" / "processed" / current_week / "staySpain_cleaned.pkl"
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Cargar datos
    print("Cargando datos crudos...")
    df = pd.read_csv(input_path)
    
    # Aplicar funciones de limpieza
    print("Aplicando limpieza de datos...")
    df_clean = handle_duplicates(df, 'apartment_id', 'insert_date')
    df_clean = correct_data_types_str_to_date(df_clean)
    df_clean = correct_data_types_str_to_int(df_clean)
    df_clean = correct_data_types_str_to_int(df_clean)

    # Aplicar funciones de transformación
    print("Aplicando transformación de datos...")
    df_clean = reviews_format(df)

    # Aplicar funciones de reducción
    print("Aplicando reducción de datos...")



    
    # Guardar datos limpios
    df_clean.to_pickle(output_path)
    print(f"Datos limpios guardados en: {output_path}")
    
    return df_clean

if __name__ == "__main__":
    main()