import pandas as pd
import numpy as np

def create_new_variables(df):
    """Creación de nuevas variables"""
    df_transformed = df.copy()
    
    # Precio por persona
    if 'price' in df_transformed.columns and 'accommodates' in df_transformed.columns:
        df_transformed['price_per_person'] = df_transformed['price'] / df_transformed['accommodates']
    
    # Indicador de alta calificación
    if 'review_scores_rating' in df_transformed.columns:
        df_transformed['has_high_rating'] = (df_transformed['review_scores_rating'] >= 4.5).astype(int)
    
    # Días desde última revisión (si hay fecha)
    if 'last_review_date' in df_transformed.columns:
        df_transformed['last_review_date'] = pd.to_datetime(df_transformed['last_review_date'])
        df_transformed['days_since_last_review'] = (pd.Timestamp.now() - df_transformed['last_review_date']).dt.days
    
    return df_transformed

def encode_categorical_variables(df):
    """Codificación de variables categóricas"""
    df_transformed = df.copy()
    
    # Codificar room_type si existe
    if 'room_type' in df_transformed.columns:
        df_transformed = pd.get_dummies(df_transformed, columns=['room_type'], prefix='room_type')
    
    # Codificar city si existe
    if 'city' in df_transformed.columns:
        df_transformed = pd.get_dummies(df_transformed, columns=['city'], prefix='city')
    
    return df_transformed

def extract_amenities_features(df):
    """Extracción de características de amenities"""
    df_transformed = df.copy()
    
    # Lista de amenities comunes a buscar
    amenities_to_check = ['WiFi', 'Air Conditioning', 'Pool', 'Kitchen', 'Washer', 'TV', 'Parking', 'Elevator']
    
    # Crear variables dummy para cada amenity
    if 'amenities_list' in df_transformed.columns:
        for amenity in amenities_to_check:
            col_name = f'has_{amenity.lower().replace(" ", "_")}'
            df_transformed[col_name] = df_transformed['amenities_list'].str.contains(amenity, na=False).astype(int)
    
    return df_transformed

def normalize_data(df):
    """Normalización de datos numéricos"""
    df_transformed = df.copy()
    
    # Normalizar precios si existen
    if 'price' in df_transformed.columns:
        df_transformed['price_normalized'] = (df_transformed['price'] - df_transformed['price'].mean()) / df_transformed['price'].std()
    
    # Normalizar número de reviews si existe
    if 'number_of_reviews' in df_transformed.columns:
        df_transformed['reviews_normalized'] = (df_transformed['number_of_reviews'] - df_transformed['number_of_reviews'].mean()) / df_transformed['number_of_reviews'].std()
    
    return df_transformed

# Para probar las funciones directamente
if __name__ == "__main__":
    print("Módulo transformation_functions cargado correctamente")