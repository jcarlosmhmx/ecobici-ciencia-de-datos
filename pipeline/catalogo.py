"""Catálogo de estaciones (GBFS station_information): nombre, coordenadas y capacidad ACTUAL."""
import json
import urllib.request
from datetime import date

from . import config


def obtener_catalogo(cfg):
    """Devuelve (lista de estaciones, ruta del JSON). Reutiliza la copia fechada si la configuración lo pide."""
    config.CATALOGO.mkdir(parents=True, exist_ok=True)
    copias = sorted(config.CATALOGO.glob("station_information_*.json"))
    if cfg["catalogo"]["usar_copia_versionada"] and copias:
        ruta = copias[-1]
    else:
        ruta = config.CATALOGO / f"station_information_{date.today().isoformat()}.json"
        peticion = urllib.request.Request(cfg["catalogo"]["url"], headers={"User-Agent": "Mozilla/5.0"})
        ruta.write_bytes(urllib.request.urlopen(peticion, timeout=60).read())
    with open(ruta, encoding="utf8") as f:
        return json.load(f)["data"]["stations"], ruta
