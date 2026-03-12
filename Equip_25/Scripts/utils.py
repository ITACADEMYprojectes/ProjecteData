from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path.cwd()
while not (ROOT / "Data").exists():
    ROOT = ROOT.parent

# -----------------------------------------------------------
## GUARDAR GRÁFICOS
def guardar_grafico(fig, nombre_archivo, formato="png", dpi=300):
    '''Guarda un gráfico en la carpeta "Results/figures".
    Args:
        fig: Figura de Matplotlib a guardar.
        nombre_archivo: Nombre del archivo sin extensión.
        formato: Formato de la imagen (default: "png").
    '''
    ROOT = Path.cwd()

    while not (ROOT / "Data").exists():
        ROOT = ROOT.parent

    ruta_figures = ROOT / "Data" / "figures"
    ruta_figures.mkdir(parents=True, exist_ok=True)

    ruta_archivo = ruta_figures / f"{nombre_archivo}.{formato}"

    fig.savefig(ruta_archivo, bbox_inches="tight", dpi=dpi)
    plt.close(fig)

    print(f"Gráfico guardado en: {ruta_archivo}")