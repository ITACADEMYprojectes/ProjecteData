import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

def set_plot_style():
    """Configura el estilo de los gráficos"""
    plt.style.use('seaborn-v0_8')
    sns.set_palette("viridis")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12

def generate_summary_statistics(df, output_path):
    """Genera estadísticas descriptivas y las guarda en un archivo"""
    summary = {}
    
    # Estadísticas generales
    summary['shape'] = f"{df.shape[0]} filas, {df.shape[1]} columnas"
    summary['missing_values'] = int(df.isnull().sum().sum())
    summary['missing_percentage'] = f"{(df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100):.2f}%"
    
    # Estadísticas por tipo de dato
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    summary['numeric_columns'] = numeric_cols
    summary['categorical_columns'] = categorical_cols
    
    # Estadísticas numéricas detalladas
    numeric_stats = {}
    for col in numeric_cols:
        numeric_stats[col] = {
            'mean': df[col].mean(),
            'median': df[col].median(),
            'std': df[col].std(),
            'min': df[col].min(),
            'max': df[col].max(),
            'missing': df[col].isnull().sum()
        }
    
    summary['numeric_stats'] = numeric_stats
    
    # Guardar en archivo
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=4, default=str)
    
    return summary

def plot_numeric_distributions(df, output_folder):
    """Crea histogramas para variables numéricas"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    for col in numeric_cols:
        plt.figure(figsize=(10, 6))
        
        # Histograma con curva de densidad
        sns.histplot(df[col], kde=True, bins=30)
        plt.title(f'Distribución de {col}')
        plt.xlabel(col)
        plt.ylabel('Frecuencia')
        
        # Guardar figura
        plt.tight_layout()
        plt.savefig(f"{output_folder}/histogram_{col}.png", dpi=300, bbox_inches='tight')
        plt.close()

def plot_categorical_distributions(df, output_folder, top_n=10):
    """Crea gráficos de barras para variables categóricas"""
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    for col in categorical_cols:
        plt.figure(figsize=(12, 6))
        
        # Top N categorías
        top_categories = df[col].value_counts().head(top_n)
        
        # Gráfico de barras
        sns.barplot(x=top_categories.values, y=top_categories.index, palette="viridis")
        plt.title(f'Distribución de {col} (Top {top_n})')
        plt.xlabel('Frecuencia')
        plt.ylabel(col)
        
        # Guardar figura
        plt.tight_layout()
        plt.savefig(f"{output_folder}/barplot_{col}.png", dpi=300, bbox_inches='tight')
        plt.close()

def plot_correlation_matrix(df, output_folder):
    """Crea una matriz de correlación para variables numéricas"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) > 1:
        plt.figure(figsize=(14, 12))
        
        # Calcular matriz de correlación
        corr_matrix = df[numeric_cols].corr()
        
        # Crear heatmap
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", 
                   center=0, square=True, linewidths=.5, cbar_kws={"shrink": .8})
        
        plt.title('Matriz de Correlación de Variables Numéricas')
        
        # Guardar figura
        plt.tight_layout()
        plt.savefig(f"{output_folder}/correlation_matrix.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return corr_matrix
    else:
        print("No hay suficientes variables numéricas para la matriz de correlación")
        return None

def plot_boxplots_by_category(df, numeric_col, category_col, output_folder):
    """Crea boxplots de una variable numérica por categoría"""
    if numeric_col in df.columns and category_col in df.columns:
        plt.figure(figsize=(14, 8))
        
        # Ordenar por mediana para mejor visualización
        order = df.groupby(category_col)[numeric_col].median().sort_values(ascending=False).index
        
        # Boxplot
        sns.boxplot(x=category_col, y=numeric_col, data=df, order=order)
        plt.title(f'Distribución de {numeric_col} por {category_col}')
        plt.xticks(rotation=45)
        
        # Guardar figura
        plt.tight_layout()
        plt.savefig(f"{output_folder}/boxplot_{numeric_col}_by_{category_col}.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()

def plot_scatterplots(df, x_col, y_col, output_folder, hue_col=None):
    """Crea scatter plots entre variables numéricas"""
    if x_col in df.columns and y_col in df.columns:
        plt.figure(figsize=(10, 8))
        
        # Scatter plot
        if hue_col and hue_col in df.columns:
            sns.scatterplot(x=x_col, y=y_col, hue=hue_col, data=df, alpha=0.6, palette="viridis")
        else:
            sns.scatterplot(x=x_col, y=y_col, data=df, alpha=0.6)
        
        plt.title(f'Relación entre {x_col} y {y_col}')
        
        # Guardar figura
        plt.tight_layout()
        plt.savefig(f"{output_folder}/scatter_{x_col}_vs_{y_col}.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()

def plot_missing_values(df, output_folder):
    """Visualiza los valores faltantes en el dataset"""
    plt.figure(figsize=(14, 8))
    
    # Calcular porcentaje de valores faltantes por columna
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    missing_percentage = missing_percentage[missing_percentage > 0].sort_values(ascending=False)
    
    # Gráfico de barras
    sns.barplot(x=missing_percentage.values, y=missing_percentage.index, palette="rocket")
    plt.title('Porcentaje de Valores Faltantes por Columna')
    plt.xlabel('Porcentaje de Valores Faltantes')
    plt.ylabel('Columnas')
    
    # Guardar figura
    plt.tight_layout()
    plt.savefig(f"{output_folder}/missing_values.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    return missing_percentage

def analyze_price_relationships(df, output_folder):
    """Análisis específico de relaciones con el precio"""
    if 'price' in df.columns:
        # Precio vs accommodates
        if 'accommodates' in df.columns:
            plot_scatterplots(df, 'accommodates', 'price', output_folder)
        
        # Precio vs review_scores_rating
        if 'review_scores_rating' in df.columns:
            plot_scatterplots(df, 'review_scores_rating', 'price', output_folder)
        
        # Precio por tipo de habitación
        if 'room_type' in df.columns:
            plot_boxplots_by_category(df, 'price', 'room_type', output_folder)
        
        # Precio por ciudad
        if 'city' in df.columns:
            plot_boxplots_by_category(df, 'price', 'city', output_folder)

# Para probar las funciones directamente
if __name__ == "__main__":
    print("Módulo eda_utils cargado correctamente")