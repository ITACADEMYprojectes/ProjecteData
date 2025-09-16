import pandas as pd
import sys
import os
from pathlib import Path
import importlib.util


def main():
    # Obtener la ruta absoluta al directorio del proyecto
    project_root = Path(__file__).resolve().parent.parent.parent
    
    # Configurar rutas
    current_week = "week_01_2025-09-15"
    input_path = project_root / "data" / "processed" / current_week / "staySpain_cleaned.pkl"
    
    print(f"Buscando archivo en: {input_path}")
    
    if not input_path.exists():
        print("❌ Archivo no encontrado. Verifica:")
        print(f"   - Que la carpeta 'data/processed/{current_week}' existe")
        print(f"   - Que el archivo 'staySpain_cleaned.pkl' está en esa carpeta")
        return None
    
    try:
        df = pd.read_pickle(input_path)
        print(f"✅ DataFrame cargado: {df.shape}")
        return df
    except Exception as e:
        print(f"❌ Error al leer el archivo Pickle: {e}")
        return None

if __name__ == "__main__":
    df = main()
    
    # Verificar si se cargó correctamente el DataFrame
    if df is not None:
        print("DataFrame cargado exitosamente")
        # Aquí puedes continuar procesando tu DataFrame
        print(df.head())
    else:
        print("No se pudo cargar el DataFrame")