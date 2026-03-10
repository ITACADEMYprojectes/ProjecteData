from importlib.resources import path
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Raíz del código 
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "Data" / "data_cleaning"

## GUARDAR DF
def guardar_pickle(df, archivo="df.pkl"):
    ''' Guarda el dataframe en formato pickle en la carpeta "Data/data_cleaning".
    Args:
        df: DataFrame a guardar.
        archivo: Nombre del archivo (ej. "df.pkl").
    '''
    if not archivo.endswith(".pkl"):
        archivo += ".pkl"
    
    path.mkdir(parents=True, exist_ok=True)
    ruta = path / archivo
    
    df.to_pickle(ruta)
    print(f"DataFrame guardado en: {ruta}")

# -----------------------------------------------------------
## CARGAR DF
def cargar_pickle(archivo):
    '''
    Carga un DataFrame desde pickle en Data/data_cleaning.
    Args:
        archivo: nombre del archivo (con o sin .pkl)
        subcarpeta: carpeta dentro de data_cleaning donde está el archivo
    '''
    if not archivo.endswith(".pkl"):
        archivo += ".pkl"
     
    ruta = path / archivo
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")
    
    return pd.read_pickle(ruta)

# -----------------------------------------------------------
## GUARDAR GRÁFICOS
def guardar_grafico(fig, nombre_dpt, tipo, info, formato="png", dpi=300):
    '''Guarda un gráfico en la carpeta "Results/figures".
    Args:
        fig: Figura de Matplotlib a guardar.
        nombre_dpt: Nombre del departamento (ej. "mkt"). 
        tipo: Tipo de gráfico (ej. "boxplot").
        info: Información adicional para el nombre del archivo (ej. "precio").   
    '''
    actual = Path.cwd()
    ROOT = Path(__file__).resolve().parent.parent

    for parent in [actual] + list(actual.parents):
        if parent.name == "src":
            ROOT = parent.parent
            break

    if ROOT is None:
        raise FileNotFoundError(
            "No se pudo detectar la raíz del proyecto"
        )

    ruta_figures = ROOT / "Results" / "figures"
    ruta_figures.mkdir(parents=True, exist_ok=True)

    ruta_archivo = ruta_figures / f"fig_{nombre_dpt}_{tipo}_{info}.{formato}"
    fig.savefig(ruta_archivo, bbox_inches="tight", dpi=dpi)
    plt.close(fig)

    print(f"Gráfico guardado en: {ruta_archivo}")