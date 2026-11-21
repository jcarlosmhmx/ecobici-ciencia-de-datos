"""Ejecuta el pipeline completo:  python -m pipeline [--desde ETAPA] [--hasta ETAPA]

Etapas: descarga → bronze (01_perfilado) → silver (02_limpieza) → gold (03_analisis) → visualizaciones (04_visualizaciones) → app.
Cada etapa de datos se ejecuta a través de su notebook, para que las salidas queden guardadas como evidencia.
La última etapa abre la aplicación Streamlit y se queda esperando hasta cerrarla con Ctrl+C; para procesar sin abrirla:
    python -m pipeline --hasta visualizaciones
Para abrir solo la aplicación:  python -m pipeline --desde app   (o  streamlit run app/app.py)
"""
import argparse
import importlib.util
import subprocess
import sys
import time

from . import catalogo, config, descarga

ETAPAS = ["descarga", "bronze", "silver", "gold", "visualizaciones", "app"]
NOTEBOOKS = {"bronze": "01_perfilado.ipynb", "silver": "02_limpieza.ipynb", "gold": "03_analisis.ipynb",
             "visualizaciones": "04_visualizaciones.ipynb"}


def ejecutar_notebook(nombre):
    ruta = config.RAIZ / "notebooks" / nombre
    subprocess.run(
        [sys.executable, "-m", "nbconvert", "--to", "notebook", "--execute", "--inplace",
         "--ExecutePreprocessor.timeout=3600", "--ExecutePreprocessor.kernel_name=python3", str(ruta)],
        check=True, cwd=ruta.parent,
    )


def abrir_app():
    """Abre la aplicación Streamlit y espera hasta que se cierre (Ctrl+C)."""
    if importlib.util.find_spec("streamlit") is None:
        raise SystemExit("Streamlit no está instalado. Ejecute: pip install -r requirements.txt")
    print("  Se abrirá en el navegador (por lo general en http://localhost:8501). Para cerrarla, presione Ctrl+C.")
    try:
        codigo = subprocess.run([sys.executable, "-m", "streamlit", "run", str(config.RAIZ / "app" / "app.py")],
                                cwd=config.RAIZ).returncode
    except KeyboardInterrupt:
        codigo = 0
    if codigo not in (0, 130, -2, 3221225786):   # salidas normales al cerrar con Ctrl+C (Linux, macOS y Windows)
        raise SystemExit(f"Streamlit terminó con un error (código {codigo}).")
    print("\n  Aplicación cerrada.")


def main():
    parser = argparse.ArgumentParser(description="Pipeline de datos ECOBICI")
    parser.add_argument("--desde", choices=ETAPAS, default="descarga")
    parser.add_argument("--hasta", choices=ETAPAS, default=ETAPAS[-1])
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
        elif etapa == "app":
            abrir_app()
            continue
        else:
            ejecutar_notebook(NOTEBOOKS[etapa])
        print(f"  listo en {time.time() - inicio:.0f} s")


if __name__ == "__main__":
    main()
