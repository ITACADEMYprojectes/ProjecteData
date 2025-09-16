import pandas as pd
import sys
import os
from pathlib import Path
import importlib.util

# Obtener la ruta absoluta al directorio del proyecto
project_root = Path(__file__).resolve().parent.parent.parent
utilities_path = project_root / "scripts" / "utilities"

# Ruta al archivo transformation_functions.py
transformation_functions_file = utilities_path / "transformation_functions.py"

# Verificar si el directorio utilities existe
if not utilities_path.exists() or not utilities_path.is_dir():
    print(f"ERROR: No se encuentra el directorio utilities en: {utilities_path}")
    print("Por favor, verifica la estructura de carpetas:")
    print("staySpain-analysis/")
    print("├── scripts/")
    print("│   ├── utilities/")
    print("│   │   ├── __init__.py")
    print("│   │   └── transformation_functions.py")
    print("│   └── week_01_2025-09-15/")
    print("│       └── 03_data_transformation.py")
    sys.exit(1)

# Verificar si el archivo existe
if not transformation_functions_file.exists():
    print(f"ERROR: No se encuentra el archivo {transformation_functions_file}")
    sys.exit(1)

# Cargar el módulo manualmente desde el archivo
spec = importlib.util.spec_from_file_location("transformation_functions", transformation_functions_file)
transformation_functions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transformation_functions)
print("Funciones de transformación cargadas correctamente")

# Asignar las funciones manteniendo sus nombres originales
create_new_variables = transformation_functions.create_new_variables
encode_categorical_variables = transformation_functions.encode_categorical_variables
extract_amenities_features = transformation_functions.extract_amenities_features
normalize_data = transformation_functions.normalize_data

def main():
    # Configurar rutas
    current_week = "week_01_2025-09-15"
    input_path = project_root / "data" / "processed" / current_week / "staySpain_cleaned.pkl"
    output_path = project_root / "data" / "processed" / current_week / "staySpain_transformed.pkl"
    
    # Verificar si el archivo de entrada existe
    if not input_path.exists():
        print(f"ERROR: No se encuentra el archivo de datos limpios: {input_path}")
        sys.exit(1)
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Cargar datos limpios
    print("Cargando datos limpios...")
    df_clean = pd.read_csv(input_path)
    print(f"Datos cargados: {df_clean.shape[0]} filas, {df_clean.shape[1]} columnas")
    
    # Aplicar funciones de transformación
    print("Aplicando transformación de datos...")
    df_transformed = create_new_variables(df_clean)
    df_transformed = encode_categorical_variables(df_transformed)
    df_transformed = extract_amenities_features(df_transformed)
    df_transformed = normalize_data(df_transformed)
    
    # Guardar datos transformados
    df_transformed.to_pickle(output_path, index=False)
    print(f"Datos transformados guardados en: {output_path}")
    print(f"Datos finales: {df_transformed.shape[0]} filas, {df_transformed.shape[1]} columnas")
    
    return df_transformed

if __name__ == "__main__":
    main()
