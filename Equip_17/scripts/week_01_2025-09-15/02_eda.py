import pandas as pd
import sys
import os
from pathlib import Path
import importlib.util

# Obtener la ruta absoluta al directorio del proyecto
project_root = Path(__file__).resolve().parent.parent.parent
utilities_path = project_root / "scripts" / "utilities"

# Ruta al archivo eda_utils.py
eda_utils_file = utilities_path / "eda_utils.py"

# Verificar si el archivo existe
if not eda_utils_file.exists():
    print(f"ERROR: No se encuentra el archivo {eda_utils_file}")
    sys.exit(1)

# Cargar el módulo manualmente
spec = importlib.util.spec_from_file_location("eda_utils", eda_utils_file)
eda_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eda_utils)

# Ahora puedes usar las funciones del módulo
EDA = eda_utils.EDA


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
    
 
    # EDA
    print("Aplicando EDA...")
    EDA(df)


    
    # # Guardar datos limpios
    # df_clean.to_pickle(output_path)
    # print(f"Datos limpios guardados en: {output_path}")
    
    # return df_clean

if __name__ == "__main__":
    main()