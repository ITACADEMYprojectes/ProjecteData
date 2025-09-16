import pandas as pd
import numpy as np

def handle_duplicates(df, apartment_id, insert_date):
    """Eliminación de duplicados según insert_date"""
    df_clean = df.copy()
    
    # Encontrar duplicados
    duplicados = df_clean[df_clean.duplicated(apartment_id, keep=False)]
    
    if duplicados.empty:
        print("No se encontraron registros duplicados.")
        return None
    
    # Ordenar duplicados por fecha (más reciente primero)
    duplicados_ordenados = duplicados.sort_values(by=[apartment_id, insert_date], ascending=[True, False])
    
    # Mantener solo el registro más reciente de cada duplicado
    df_clean = df_clean.sort_values(insert_date, ascending=False)\
                     .drop_duplicates(apartment_id, keep='first')\
                     .sort_index()
       
    return df_clean

def impute_price(df, price, room_type, accommodates, neighbourhood_name):
    """Imputación de precios"""
    df_clean = df.copy()
    
    # Calcular la media según alojamiento, capacidad y localización
    avgs = df_clean.groupby([room_type, accommodates, neighbourhood_name])[price].transform('mean')
    df_clean[price] = df_clean[price].fillna(avgs)
    
    return df_clean

def correct_data_types_str_to_date(df):
    """Corrección de tipos de datos de str a date"""
    df_clean = df.copy()
    
    # Conversión de tipos
    df_clean['first_review_date'] = pd.to_datetime(df_clean['first_review_date'], errors='coerce', format='%d/%m/%Y')
    df_clean['last_review_date'] = pd.to_datetime(df_clean['last_review_date'], errors='coerce', format='%d/%m/%Y')
    df_clean['insert_date'] = pd.to_datetime(df_clean['insert_date'], errors='coerce', format='%d/%m/%Y')

    return df_clean

def correct_data_types_str_to_int(df):
    """Corrección de tipos de datos de str a int"""
    df_clean = df.copy()
    
    # Conversión de tipos
    df_clean['bedrooms'] = pd.to_numeric(df_clean['bedrooms'], errors='coerce').astype('Int64')
    df_clean['bathrooms'] = pd.to_numeric(df_clean['bathrooms'], errors='coerce').astype('Int64')
    
    return df_clean

def fill_name(df):
    """Gestión de registros sin datos en 'name'"""
    df_clean = df.copy()
    
    df_clean['name'] = df_clean['name'].fillna(df_clean['room_type'] + ' ' + df_clean['neighbourhood_name'])
    
    return df_clean

def fill_descriptions(df):
    """Gestión de registros sin datos en 'descriptions'"""
    df_clean = df.copy()
    
    df_clean['description'] = df_clean['description'].fillna(df_clean['name'])
    
    return df_clean

def reviews_format(df):
    """Formatear las variables de review'"""
    df_clean = df.copy()
    
    df_clean['review_scores_rating'] = df_clean['review_scores_rating'] / 10
    df_clean['review_scores_accuracy'] = df_clean['review_scores_accuracy'] / 10
    df_clean['review_scores_cleanliness'] = df_clean['review_scores_cleanliness'] / 10
    df_clean['review_scores_checkin'] = df_clean['review_scores_checkin'] / 10
    df_clean['review_scores_communication'] = df_clean['review_scores_communication'] / 10
    df_clean['review_scores_location'] = df_clean['review_scores_location'] / 10
    df_clean['review_scores_value'] = df_clean['review_scores_value'] / 10

    return df_clean
