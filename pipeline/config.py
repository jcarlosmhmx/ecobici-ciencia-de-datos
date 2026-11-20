"""Lee config/pipeline.toml y define las rutas del proyecto (todas relativas a la raíz del repo)."""
import tomllib
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "datos" / "raw"
BRONZE = RAIZ / "datos" / "bronze"
SILVER = RAIZ / "datos" / "silver"
GOLD = RAIZ / "datos" / "gold"
CATALOGO = RAIZ / "datos" / "catalogo"
PERFIL = RAIZ / "datos" / "perfil"
FIGURAS = RAIZ / "figuras"


def cargar(ruta=None):
    """Devuelve la configuración como diccionario."""
    with open(ruta or RAIZ / "config" / "pipeline.toml", "rb") as f:
        return tomllib.load(f)


def meses(cfg):
    """Lista de meses 'AAAA-MM' de la ventana, ambos extremos incluidos."""
    a, m = map(int, cfg["ventana"]["desde"].split("-"))
    a2, m2 = map(int, cfg["ventana"]["hasta"].split("-"))
    salida = []
    while (a, m) <= (a2, m2):
        salida.append(f"{a:04d}-{m:02d}")
        a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    return salida
