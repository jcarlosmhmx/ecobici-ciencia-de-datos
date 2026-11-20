"""Ejecuta el pipeline completo:  python -m pipeline [--desde ETAPA] [--hasta ETAPA]

Etapas: descarga → bronze (01_perfilado) → silver (02_limpieza) → gold (03_analisis).
Cada etapa de datos se ejecuta a través de su notebook, para que las salidas queden guardadas como evidencia.
"""
import argparse
import subprocess
import sys
import time

from . import catalogo, config, descarga

ETAPAS = ["descarga", "bronze", "silver", "gold"]
NOTEBOOKS = {"bronze": "01_perfilado.ipynb", "silver": "02_limpieza.ipynb", "gold": "03_analisis.ipynb"}


def ejecutar_notebook(nombre):
    ruta = config.RAIZ / "notebooks" / nombre
    subprocess.run(
        [sys.executable, "-m", "nbconvert", "--to", "notebook", "--execute", "--inplace",
         "--ExecutePreprocessor.timeout=3600", "--ExecutePreprocessor.kernel_name=python3", str(ruta)],
        check=True, cwd=ruta.parent,
    )


def main():
    parser = argparse.ArgumentParser(description="Pipeline de datos ECOBICI")
    parser.add_argument("--desde", choices=ETAPAS, default="descarga")
    parser.add_argument("--hasta", choices=ETAPAS, default="gold")
    args = parser.parse_args()
    primera, ultima = ETAPAS.index(args.desde), ETAPAS.index(args.hasta)
    if primera > ultima:
        parser.error("--desde no puede ir después de --hasta")
    cfg = config.cargar()
    print(f"Ventana: {cfg['ventana']['desde']} a {cfg['ventana']['hasta']}  ({len(config.meses(cfg))} meses)")
    for etapa in ETAPAS[primera:ultima + 1]:
        inicio = time.time()
        print(f"\n=== {etapa} ===")
        if etapa == "descarga":
            _, ruta = catalogo.obtener_catalogo(cfg)
            print(f"Catálogo de estaciones: {ruta.name}")
            for mes, estado, tamano in descarga.descargar_ventana(cfg):
                print(f"  {mes}: {estado} ({tamano / 1e6:.0f} MB)")
        else:
            ejecutar_notebook(NOTEBOOKS[etapa])
        print(f"  listo en {time.time() - inicio:.0f} s")


if __name__ == "__main__":
    main()
