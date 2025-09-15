import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

def select_relevant_variables(df):
    """Selección de variables relevantes para el análisis"""
    df_reduced = df.copy()
    
    # Lista de columnas a mantener (ajusta según tus necesidades)
    columns_to_keep = [
        'apartment_id', 'city', 'accommodates', 'bedrooms', 'bathrooms',
        'price', 'price_per_person', 'review_scores_rating', 'has_high_rating',
        'availability_30', 'number_of_reviews', 'days_since_last_review'
    ]
    
    # Agregar columnas de room_type (si existen)
    room_type_cols = [col for col in df.columns if col.startswith('room_type_')]
    columns_to_keep.extend(room_type_cols)
    
    # Agregar columnas de amenities (si existen)
    amenities_cols = [col for col in df.columns if col.startswith('has_')]
    columns_to_keep.extend(amenities_cols)
    
    # Mantener solo las columnas existentes en el DataFrame
    existing_columns = [col for col in columns_to_keep if col in df.columns]
    
    # Si hay pocas columnas, mantener todas
    if len(existing_columns) < 5:
        print("Advertencia: Pocas columnas seleccionadas. Manteniendo todas las columnas.")
        return df_reduced
    
    return df_reduced[existing_columns]

def filter_records(df):
    """Filtrado de registros"""
    df_reduced = df.copy()
    
    # Filtrar propiedades sin reviews
    if 'number_of_reviews' in df_reduced.columns:
        df_reduced = df_reduced[df_reduced['number_of_reviews'] > 0]
    
    # Filtrar propiedades sin precio
    if 'price' in df_reduced.columns:
        df_reduced = df_reduced[df_reduced['price'] > 0]
    
    return df_reduced

def aggregate_data(df):
    """Agregación de datos (opcional, según necesidades)"""
    # Esta función es opcional y depende de tus necesidades de análisis
    # Por ejemplo, podrías agregar datos por ciudad o tipo de propiedad
    
    # Por ahora, simplemente devolvemos el DataFrame sin cambios
    return df

def reduce_dimensionality(df):
    """Reducción de dimensionalidad para variables numéricas"""
    df_reduced = df.copy()
    
    # Seleccionar solo columnas numéricas
    numerical_columns = df_reduced.select_dtypes(include=[np.number]).columns.tolist()
    
    # Eliminar columnas que no son relevantes para PCA
    cols_to_exclude = ['apartment_id', 'has_high_rating']  # Ajustar según necesidades
    numerical_columns = [col for col in numerical_columns if col not in cols_to_exclude]
    
    # Aplicar PCA si hay suficientes columnas numéricas
    if len(numerical_columns) > 5:
        print(f"Aplicando PCA a {len(numerical_columns)} variables numéricas")
        
        # Estandarizar datos
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df_reduced[numerical_columns])
        
        # Aplicar PCA
        pca = PCA(n_components=0.95)  # Mantener el 95% de varianza
        pca_data = pca.fit_transform(scaled_data)
        
        # Crear nombres para los componentes
        pca_columns = [f'pca_component_{i+1}' for i in range(pca_data.shape[1])]
        
        # Crear DataFrame con los componentes
        pca_df = pd.DataFrame(pca_data, columns=pca_columns, index=df_reduced.index)
        
        # Eliminar las columnas numéricas originales y agregar los componentes
        df_reduced = df_reduced.drop(columns=numerical_columns)
        df_reduced = pd.concat([df_reduced, pca_df], axis=1)
        
        print(f"Reducción de {len(numerical_columns)} variables a {pca_data.shape[1]} componentes")
    
    return df_reduced

# Para probar las funciones directamente
if __name__ == "__main__":
    print("Módulo reduction_functions cargado correctamente")