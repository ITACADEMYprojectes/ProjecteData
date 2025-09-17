import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

def EDA(df, show_plots=True):
    # Estadísticas por columna numérica
    columnas_num = df.select_dtypes(include=[np.number]).columns
    if len(columnas_num) == 0:
        print("\n No se encontraron columnas numéricas.")
    else:
        for col in columnas_num:
            serie = df[col].dropna()
            modos = serie.mode()
            modos_list = modos.tolist() if not modos.empty else []
            print(f"\n🔎 Estadísticas para la columna: {col}")
            print(f"  ▸ Media: {serie.mean():.4f}" if not serie.empty else "  ▸ Media: n/a")
            print(f"  ▸ Mediana: {serie.median():.4f}" if not serie.empty else "  ▸ Mediana: n/a")
            print(f"  ▸ Desviación estándar: {serie.std():.4f}" if not serie.empty else "  ▸ Desv. estándar: n/a")
            print(f"  ▸ Mínimo: {serie.min() if not serie.empty else 'n/a'}")
            print(f"  ▸ Máximo: {serie.max() if not serie.empty else 'n/a'}")
            print(f"  ▸ Moda(s): {modos_list if modos_list else 'n/a'}")

    # Visualizaciones
    if show_plots and len(columnas_num) > 0:
        # Boxplots
        for col in columnas_num:
            plt.figure()
            df.boxplot(column=col)
            plt.title(f"Boxplot de {col}")
            plt.tight_layout()
            plt.show()

        # Histogramas
        plt.figure()
        df[columnas_num].hist(figsize=(20, 15))
        plt.tight_layout()
        plt.show()

        # Matriz de correlación
        correlaciones = df.corr(numeric_only=True)
        if correlaciones.shape[0] >= 2:
            plt.figure(figsize=(14, 10))
            annot_flag = correlaciones.shape[0] <= 12
            sns.heatmap(correlaciones, cmap="coolwarm", annot=annot_flag, fmt=".2f",
                        linewidths=0.5)
            plt.title(" Matriz de correlación entre variables numéricas")
            plt.xticks(rotation=45, ha="right")
            plt.yticks(rotation=0)
            plt.tight_layout()
            plt.show()
        else:
            print("\n No se puede calcular una matriz de correlación útil (muy pocas columnas numéricas).")
            