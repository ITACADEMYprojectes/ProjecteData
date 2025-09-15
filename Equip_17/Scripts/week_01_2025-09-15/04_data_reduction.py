import pandas as pd
import sys
import os
from pathlib import Path
import importlib.util

# Obtener la ruta absoluta al directorio del proyecto
project_root = Path(__file__).resolve().parent.parent.parent
utilities_path = project_root / "scripts" / "utilities"

# Verificar si el directorio utilities existe
if not utilities_path.exists() or not utilities_path.is_dir():
    print(f"ERROR: No se encuentra el directorio utilities en: {utilities_path}")
    print("Por favor, verifica la estructura de carpetas:")
    print("staySpain-analysis/")
    print("├── scripts/")
    print("│   ├── utilities/")
    print("│   │   ├── __init__.py")
    print("│   │   └── reduction_functions.py")
    print("│   └── week_01_2025-09-15/")
    print("│       └── 04_data_reduction.py")
    sys.exit(1)

# Ruta al archivo reduction_functions.py
reduction_functions_file = utilities_path / "reduction_functions.py"

# Verificar si el archivo existe
if not reduction_functions_file.exists():
    print(f"ERROR: No se encuentra el archivo {reduction_functions_file}")
    sys.exit(1)

# Cargar el módulo manualmente desde el archivo
spec = importlib.util.spec_from_file_location("reduction_functions", reduction_functions_file)
reduction_functions = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(reduction_functions)
except Exception as e:
    print(f"ERROR al cargar el módulo reduction_functions: {e}")
    sys.exit(1)

print("Funciones de reducción cargadas correctamente")

# Asignar las funciones manteniendo sus nombres originales
select_relevant_variables = reduction_functions.select_relevant_variables
filter_records = reduction_functions.filter_records
aggregate_data = reduction_functions.aggregate_data
reduce_dimensionality = reduction_functions.reduce_dimensionality

def main():
    # Configurar rutas
    current_week = "week_01_2025-09-15"
    input_path = project_root / "data" / "processed" / current_week / "staySpain_transformed.csv"
    output_path = project_root / "data" / "processed" / current_week / "staySpain_reduced.csv"
    
    # Verificar si el archivo de entrada existe
    if not input_path.exists():
        print(f"ERROR: No se encuentra el archivo de datos transformados: {input_path}")
        sys.exit(1)
    
    # Crear directorio de salida si no existe
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Cargar datos transformados
    print("Cargando datos transformados...")
    df_transformed = pd.read_csv(input_path)
    print(f"Datos cargados: {df_transformed.shape[0]} filas, {df_transformed.shape[1]} columnas")
    
    # Aplicar funciones de reducción
    print("Aplicando reducción de datos...")
    df_reduced = select_relevant_variables(df_transformed)
    df_reduced = filter_records(df_reduced)
    df_reduced = aggregate_data(df_reduced)
    df_reduced = reduce_dimensionality(df_reduced)
    
    # Guardar datos reducidos
    df_reduced.to_csv(output_path, index=False)
    print(f"Datos reducidos guardados en: {output_path}")
    print(f"Datos finales: {df_reduced.shape[0]} filas, {df_reduced.shape[1]} columnas")
    
    return df_reduced

if __name__ == "__main__":
    main()
