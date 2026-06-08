# ======================
# Import libraries
# ======================

import pandas as pd
from datetime import date

import matplotlib.pyplot as plt


# ======================
# Control Registros
# ======================

def control_registros(df: pd.DataFrame) -> None:
    """
    Muestra un resumen de control de registros del DataFrame.

    Calcula e imprime la fecha actual, el número total de registros,
    el número de IDs únicos, los registros extra respecto a IDs únicos
    y el número de filas duplicadas exactas.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame que debe contener una columna llamada 'ID'.

    Returns
    -------
    None
    """

    fecha_actual = date.today()

    total_registros = df.shape[0]
    ID_unicos = df['ID'].nunique()
    ID_extra = total_registros - ID_unicos
    ID_duplicados_exactos = df[df.duplicated(keep=False)].drop_duplicates().shape[0]


    print('--------------------\nCONTROL DE REGISTROS\n--------------------')
    print(f'Fecha: {fecha_actual}\n--------------------')
    print(f'TOTAL REGISTROS: {total_registros}')
    print(f'ID ÚNICOS: {ID_unicos}')
    print(f'ID EXTRAS: {ID_extra}')
    print(f'ID DUPLICADOS EXACTOS: {ID_duplicados_exactos}')


# ======================
# Data cleaning
# ======================





# ======================
# EDA?
# ======================
def distr_hist(df: pd.DataFrame, column: str, bars: int) -> None:
    """
    Muestra un histograma para una columna del DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos.
    column : str
        Columna a visualizar.
    bars : int
        Número de barras del histograma.
    """
    plt.hist(df[column], bins=bars)
    plt.title(f'Distribución de la variable {column}')
    plt.show()



def distr_value(df: pd.DataFrame, column: str) -> None:
    """
    Muestra la distribución porcentual y los valores únicos de una columna.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos.
    column : str
        Columna a analizar.
    """
    value_count = df[column].value_counts(normalize=True)*100
    print(f'Value counts: {value_count}')
    val_unique = df[column].unique()
    print(f'----\nValores únicos:{val_unique}')
    
    print('----\nGráfico distribución valores únicos:')
    (df[column]
    .value_counts(normalize=True)
    .mul(100)
    .plot(kind='bar'))

    plt.ylabel('Porcentaje (%)')
    plt.xlabel('Hit_target')
    plt.title('Distribución de Hit_target')
    plt.show()

def distr_boxplot(df: pd.DataFrame, column: str) -> None:
    """
    Muestra un boxplot para una columna del DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos.
    column : str
        Columna a visualizar.
    """
    plt.boxplot(df[column])
    plt.title(f'Boxplot de la variable {column}')
    plt.show()    