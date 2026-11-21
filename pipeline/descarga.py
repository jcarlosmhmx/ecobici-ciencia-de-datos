"""Descarga los CSV mensuales leyendo los enlaces de la página de datos abiertos de ECOBICI.

Los nombres de archivo no siguen un patrón (2024-02.csv, datos_abiertos_2024_03-1-1.csv,
public_data_web_2026-06.csv...), por eso se leen los enlaces del portal en vez de construirlos.
"""
import re
import time
import urllib.error
import urllib.request
from urllib.parse import urljoin

from tqdm import tqdm

from . import config

ENLACE = re.compile(r"""(?:https?://[^"'\s<>]+)?/wp-content/uploads/\d{4}/\d{2}/[^"'\s<>]+\.csv""", re.I)
MES = re.compile(r"(20\d{2})[-_](\d{2})")
CABECERAS = {"User-Agent": "Mozilla/5.0 (proyecto academico ecobici)"}
ESPERAS = (5, 15, 45)   # segundos de espera antes de cada reintento; en total 4 intentos


def _abrir(url, metodo="GET"):
    return urllib.request.urlopen(urllib.request.Request(url, headers=CABECERAS, method=metodo), timeout=60)


def con_reintentos(accion, descripcion):
    """Ejecuta accion(); si falla por la red (tiempo de espera, conexión cortada, tamaño incompleto) reintenta con espera creciente."""
    for intento, espera in enumerate((*ESPERAS, None), start=1):
        try:
            return accion()
        except (OSError, urllib.error.URLError, RuntimeError) as error:
            if espera is None:
                raise RuntimeError(f"{descripcion}: no se pudo después de {intento} intentos ({error}). "
                                   "Revise su conexión y vuelva a ejecutar python -m pipeline: retoma donde se quedó.") from error
            print(f"  {descripcion}: falló ({error}); reintento {intento} de {len(ESPERAS)} en {espera} s")
            time.sleep(espera)


def enlaces_portal(pagina):
    """Devuelve {'AAAA-MM': url}. Falla si un mes tiene más de un enlace (no se adivina cuál es)."""
    html = _abrir(pagina).read().decode("utf8", "ignore")
    por_mes = {}
    for coincidencia in ENLACE.finditer(html):
        url = urljoin(pagina, coincidencia.group(0))
        mes = MES.search(url.rsplit("/", 1)[-1])
        if mes:
            por_mes.setdefault(f"{mes.group(1)}-{mes.group(2)}", set()).add(url)
    repetidos = {m: sorted(u) for m, u in por_mes.items() if len(u) > 1}
    if repetidos:
        raise RuntimeError(f"Hay más de un enlace para estos meses, hay que elegir a mano: {repetidos}")
    return {m: next(iter(u)) for m, u in por_mes.items()}


def descargar_mes(mes, url, destino):
    """Baja un CSV si no existe completo. Devuelve 'descargado' u 'omitido'."""
    esperado = _abrir(url, "HEAD").headers.get("Content-Length")
    esperado = int(esperado) if esperado else None
    if destino.exists() and (esperado is None or destino.stat().st_size == esperado):
        return "omitido"
    parcial = destino.with_suffix(".part")
    with _abrir(url) as r, open(parcial, "wb") as f, tqdm(
        total=esperado, unit="B", unit_scale=True, desc=mes, leave=False, mininterval=2
    ) as barra:
        while bloque := r.read(1 << 20):
            f.write(bloque)
            barra.update(len(bloque))
    if esperado is not None and parcial.stat().st_size != esperado:
        raise RuntimeError(f"{mes}: se descargaron {parcial.stat().st_size} bytes y se esperaban {esperado}")
    parcial.replace(destino)
    return "descargado"


def descargar_ventana(cfg):
    """Descarga todos los meses de la ventana. Devuelve una lista de (mes, estado, bytes)."""
    config.RAW.mkdir(parents=True, exist_ok=True)
    enlaces = con_reintentos(lambda: enlaces_portal(cfg["portal"]["pagina"]), "Página del portal")
    faltan = [m for m in config.meses(cfg) if m not in enlaces]
    if faltan:
        raise RuntimeError(f"El portal no publica estos meses de la ventana: {faltan}")
    resultado = []
    for mes in config.meses(cfg):
        destino = config.RAW / f"{mes}.csv"
        estado = con_reintentos(lambda: descargar_mes(mes, enlaces[mes], destino), mes)
        resultado.append((mes, estado, destino.stat().st_size))
    return resultado
