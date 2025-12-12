import pandas   as pd
from sqlalchemy import create_engine
from helpers    import is_defined
import mysql.connector

# Definir la cadena de conexión URI
DATABASE_URI = 'mysql+mysqlconnector://Equipo20:E1q2u3i4p5o20@212.227.90.6:3306/Equip_20'

"""
Creamos la conexión con MySQL a partir de las credenciales proporcionadas
"""
def get_engine():
    """
    Crea y devuelve un objeto Engine de SQLAlchemy para la base de datos.
    """
    return create_engine(DATABASE_URI)

def load_tables(tablas=None) -> dict:
    """
    Carga las tablas especificadas en la base de datos y devuelve un diccionario
    con los DataFrames.

    Parámetros:
    tablas (list): Lista de nombres de tablas a cargar.

    Retorna:
    dict: Diccionario con los DataFrames de las tablas cargadas.
    """
    # Verificar si 'tablas_db' está definido
    if tablas is None:
        tablas_db = ['ausentismo']
    else:
        tablas_db = tablas

    df = {}

    engine = get_engine()

    for tabla in tablas_db:
        print(f"Cargando los datos de la tabla {tabla}")

        query = f'SELECT * FROM {tabla}'
        df[tabla] = pd.read_sql(query, engine)

    engine.dispose() # es buena práctica cerrar la pool de conexiones si no se va a usar más

    return df

def categorizar_ausentismo(df):
    """
    Convierte en `Categorical` las columnas `Cay_of_week`, `Month_absence`
    y `Season`. Además, segmenta la edad en tramos de aproximadamente 10 años.

    Prameters:
    df       df_ausentismo

    Returns:
    df       DataFrame categorizado
    """
    # Categorizar las columnas Month_absence, Day_of_week y Season.
    weekdays = ['Monday','Tuesday', 'Wednesday','Thursday','Friday']
    seasons  = ['Spring', 'Summer', 'Autumn','Winter']
    months   = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    # Categorías al revés, para los gráficos de barra horizontal
    rseasons  = seasons.copy()
    rmonths   = months.copy()
    rweekdays = weekdays.copy()

    rseasons.reverse()
    rmonths.reverse()
    rweekdays.reverse()

    df['Day_of_week']   = pd.Categorical(df['Day_of_week'],   weekdays, ordered=True)
    df['Month_absence'] = pd.Categorical(df['Month_absence'], months,   ordered=True)
    df['Season']        = pd.Categorical(df['Season'],        seasons,  ordered=True)

    # Crear grupos de edad a partir de la columna 'Age' mediante la función cut()
    age_ranges  = (18, 26, 36, 46, 55, 66, 101)
    ages_labels = ["{0}-{1}".format(age_ranges[i], age_ranges[i+1]-1) for i in range(0, len(age_ranges)-1)]
    df['Group'] = pd.cut(df['Age'], age_ranges, right=False, labels=ages_labels)

    # Asignar las variables al ámbito global del módulo principal
    import sys
    main_module = sys.modules['__main__']
    main_module.__dict__['rweekdays'] = rweekdays
    main_module.__dict__['rmonths']   = rmonths
    main_module.__dict__['rseasons']  = rseasons

    return df

def categorizar_ausencias(df):
    import numpy as np

    df['Absence_type'] = np.where(
        df['reason_id'].isin([0, 26]),
        'Unjustified',
        'Justified'
    )

    return df

def categorizar_distancias(df):
    # Clasificar las distancias al trabajo, en franjas de kms.
    def clasificar(distancias):
        rangos = [
            (0, 10, 'menos de 10 km'),
            (10, 21, 'entre 10 y 20 km'),
            (21, 31, 'entre 21 y 30 km'),
            (31, 41, 'entre 31 y 40 km'),
            (41, 51, 'entre 41 y 50 km')
        ]

        for min_val, max_val, descripcion in rangos:
            if min_val <= distancias < max_val:
                return descripcion

        return 'más de 50 km'

    df['distance_categories'] = df['dist2work'].apply(clasificar)
    return df