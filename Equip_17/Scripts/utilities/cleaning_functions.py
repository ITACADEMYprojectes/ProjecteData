import pandas as pd
import numpy as np

def handle_missing_values(df):
    """Manejo de valores faltantes"""
    df_clean = df.copy()
    
    # Ejemplo: Imputar precios faltantes con la mediana por ciudad
    df_clean['price'] = df_clean.groupby('city')['price'].transform(
        lambda x: x.fillna(x.median())
    )
    
    # Otras imputaciones...
    return df_clean

def correct_data_types(df):
    """Corrección de tipos de datos"""
    df_clean = df.copy()
    
    # Conversión de tipos
    df_clean['price'] = df_clean['price'].astype(float)
    df_clean['last_review_date'] = pd.to_datetime(df_clean['last_review_date'])
    
    return df_clean

def remove_duplicates(df):
    """Eliminación de duplicados"""
    return df.drop_duplicates(subset=['apartment_id'])

def handle_outliers(df):
    """Manejo de valores atípicos"""
    df_clean = df.copy()
    
    # Ejemplo: Eliminar precios extremos
    Q1 = df_clean['price'].quantile(0.05)
    Q3 = df_clean['price'].quantile(0.95)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    df_clean = df_clean[
        (df_clean['price'] >= lower_bound) & 
        (df_clean['price'] <= upper_bound)
    ]
    
    return df_clean