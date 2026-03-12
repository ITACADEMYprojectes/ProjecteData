from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------------------------------------
## GUARDAR GRÁFICOS
def guardar_grafico(fig, nombre_archivo, formato="png", dpi=300):
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

    ruta_archivo = ruta_figures / f"{nombre_archivo}.{formato}"
    fig.savefig(ruta_archivo, bbox_inches="tight", dpi=dpi)
    plt.close(fig)

    print(f"Gráfico guardado en: {ruta_archivo}")