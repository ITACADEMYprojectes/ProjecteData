import pandas as pd
import sys
import os
from pathlib import Path
import importlib.util
import numpy as np

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
set_plot_style = eda_utils.set_plot_style
generate_summary_statistics = eda_utils.generate_summary_statistics
plot_numeric_distributions = eda_utils.plot_numeric_distributions
plot_categorical_distributions = eda_utils.plot_categorical_distributions
plot_correlation_matrix = eda_utils.plot_correlation_matrix
plot_boxplots_by_category = eda_utils.plot_boxplots_by_category
plot_scatterplots = eda_utils.plot_scatterplots
plot_missing_values = eda_utils.plot_missing_values
analyze_price_relationships = eda_utils.analyze_price_relationships

def main():
    # Configurar rutas
    current_week = "week_01_2025-09-15"
    input_path = project_root / "data" / "processed" / current_week / "staySpain_reduced.csv"
    output_folder = project_root / "results" / current_week / "eda"
    
    # Verificar si el archivo de entrada existe
    if not input_path.exists():
        print(f"ERROR: No se encuentra el archivo de datos procesados: {input_path}")
        sys.exit(1)
    
    # Crear directorios de salida si no existen
    os.makedirs(output_folder, exist_ok=True)
    
    # Cargar datos procesados
    print("Cargando datos procesados...")
    df = pd.read_csv(input_path)
    print(f"Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
    
    # Configurar estilo de gráficos
    set_plot_style()
    
    # 1. Generar estadísticas descriptivas
    print("Generando estadísticas descriptivas...")
    summary_path = output_folder / "summary_statistics.json"
    summary = generate_summary_statistics(df, summary_path)
    print(f"Estadísticas guardadas en: {summary_path}")
    
    # 2. Visualizar distribuciones numéricas
    print("Generando gráficos de distribuciones numéricas...")
    plot_numeric_distributions(df, output_folder)
    print("Gráficos de distribuciones numéricas guardados")
    
    # 3. Visualizar distribuciones categóricas
    print("Generando gráficos de distribuciones categóricas...")
    plot_categorical_distributions(df, output_folder, top_n=15)
    print("Gráficos de distribuciones categóricas guardados")
    
    # 4. Matriz de correlación
    print("Generando matriz de correlación...")
    corr_matrix = plot_correlation_matrix(df, output_folder)
    if corr_matrix is not None:
        # Guardar matriz de correlación como CSV
        corr_matrix.to_csv(output_folder / "correlation_matrix.csv")
        print("Matriz de correlación guardada")
    
    # 5. Visualizar valores faltantes
    print("Analizando valores faltantes...")
    missing_values = plot_missing_values(df, output_folder)
    if len(missing_values) > 0:
        missing_values.to_csv(output_folder / "missing_values_summary.csv")
        print("Análisis de valores faltantes guardado")
    
    # 6. Análisis específico de precios
    print("Analizando relaciones con el precio...")
    analyze_price_relationships(df, output_folder)
    print("Análisis de precios guardado")
    
    # 7. Análisis adicionales específicos para StaySpain
    print("Realizando análisis adicionales...")
    
    # Relación entre precio y número de reviews
    if 'price' in df.columns and 'number_of_reviews' in df.columns:
        plot_scatterplots(df, 'number_of_reviews', 'price', output_folder)
    
    # Relación entre precio y disponibilidad
    if 'price' in df.columns and 'availability_30' in df.columns:
        plot_scatterplots(df, 'availability_30', 'price', output_folder)
    
    # Distribución de precios por número de habitaciones
    if 'price' in df.columns and 'bedrooms' in df.columns:
        plot_boxplots_by_category(df, 'price', 'bedrooms', output_folder)
    
    print("Análisis adicionales guardados")
    
    # 8. Generar reporte resumen
    print("Generando reporte resumen...")
    with open(output_folder / "eda_report.txt", "w") as report_file:
        report_file.write("REPORTE DE ANÁLISIS EXPLORATORIO DE DATOS - STAYSPAIN\n")
        report_file.write("==========================================================\n\n")
        report_file.write(f"Fecha del análisis: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n")
        report_file.write(f"Dataset: {input_path.name}\n")
        report_file.write(f"Dimensiones: {df.shape[0]} filas, {df.shape[1]} columnas\n\n")
        
        report_file.write("PRINCIPALES HALLAZGOS:\n")
        report_file.write("---------------------\n")
        
        # Resumen de variables numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        report_file.write(f"Variables numéricas: {len(numeric_cols)}\n")
        for col in numeric_cols[:5]:  # Primeras 5 variables
            report_file.write(f"  - {col}: media={df[col].mean():.2f}, mediana={df[col].median():.2f}\n")
        
        # Resumen de variables categóricas
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        report_file.write(f"\nVariables categóricas: {len(categorical_cols)}\n")
        for col in categorical_cols[:3]:  # Primeras 3 variables
            report_file.write(f"  - {col}: {df[col].nunique()} categorías únicas\n")
        
        # Valores faltantes
        total_missing = df.isnull().sum().sum()
        report_file.write(f"\nValores faltantes totales: {total_missing}\n")
        report_file.write(f"Porcentaje de valores faltantes: {(total_missing / (df.shape[0] * df.shape[1]) * 100):.2f}%\n")
        
        # Correlaciones fuertes (si hay matriz de correlación)
        if corr_matrix is not None:
            report_file.write("\nCORRELACIONES FUERTES (|r| > 0.5):\n")
            strong_correlations = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.5:
                        strong_correlations.append(
                            f"  - {corr_matrix.columns[i]} & {corr_matrix.columns[j]}: {corr_matrix.iloc[i, j]:.2f}"
                        )
            
            if strong_correlations:
                for correlation in strong_correlations:
                    report_file.write(f"{correlation}\n")
            else:
                report_file.write("  No se encontraron correlaciones fuertes\n")
    
    print(f"Reporte de EDA guardado en: {output_folder / 'eda_report.txt'}")
    print("Análisis exploratorio de datos completado exitosamente!")

if __name__ == "__main__":
    main()