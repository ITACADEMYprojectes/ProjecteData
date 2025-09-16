import pandas as pd
import sys
import os
from pathlib import Path
import importlib.util

# Obtener la ruta absoluta al directorio del proyecto
project_root = Path(__file__).resolve().parent.parent.parent
utilities_path = project_root / "scripts" / "utilities"

# Ruta al archivo cleaning_functions.py
cleaning_functions_file = utilities_path / "cleaning_functions.py"

# Verificar si el archivo existe
if not cleaning_functions_file.exists():
    print(f"ERROR: No se encuentra el archivo {cleaning_functions_file}")
    sys.exit(1)

# Cargar el módulo manualmente
spec = importlib.util.spec_from_file_location("cleaning_functions", cleaning_functions_file)
cleaning_functions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleaning_functions)

# Ahora puedes usar las funciones del módulo
handle_duplicates = cleaning_functions.handle_duplicates
correct_data_types_str_to_date = cleaning_functions.correct_data_types_str_to_date
correct_data_types_str_to_int = cleaning_functions.correct_data_types_str_to_int

def main():
    # Configurar rutas
    current_week = "week_01_2025-09-15"
    input_path = project_root / "data" / "raw" / current_week / "staySpain_raw.csv"
    output_path = project_root / "data" / "processed" / current_week / "staySpain_cleaned.csv"
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Cargar datos
    print("Cargando datos crudos...")
    df = pd.read_csv(input_path)
    
    # Aplicar funciones de limpieza
    print("Aplicando limpieza de datos...")
    df_clean = handle_duplicates(df)
    df_clean = correct_data_types_str_to_date(df_clean)
    df_clean = correct_data_types_str_to_int(df_clean)
    
    # Guardar datos limpios
    df_clean.to_csv(output_path, index=False)
    print(f"Datos limpios guardados en: {output_path}")
    
    return df_clean

if __name__ == "__main__":
    main()