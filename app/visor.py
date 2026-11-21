"""Muestra un notebook ya ejecutado (explicaciones, resultados y gráficas) dentro de Streamlit, sin volver a ejecutarlo.

La aplicación no recalcula nada: lee las salidas que quedaron guardadas en el notebook, así lo que se ve aquí es
exactamente la evidencia del análisis.
"""
import base64
import re

import nbformat
import streamlit as st

LINEAS_MAXIMAS = 40   # las salidas de texto más largas se muestran dentro de un desplegable

ESTILO = """
<style>
.tabla-nb { overflow-x: auto; margin: 0.4rem 0 1.2rem 0; }
.tabla-nb table { border-collapse: collapse; font-size: 0.85rem; }
.tabla-nb th, .tabla-nb td { border: 1px solid #d9d9d9; padding: 4px 10px; text-align: right; white-space: nowrap; }
.tabla-nb th { background: #f2f2f2; }
</style>
"""


def estilo():
    """Estilo de las tablas de pandas; se llama una vez al inicio de la aplicación."""
    st.markdown(ESTILO, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def _leer(ruta, modificado):
    """Lee el notebook; 'modificado' hace que se vuelva a leer si el archivo cambió."""
    return nbformat.read(ruta, as_version=4)


def _tabla(html):
    """Tabla de pandas: se quita su bloque de estilo propio y se aplica el de la aplicación."""
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.S)
    html = "\n".join(linea.strip() for linea in html.splitlines() if linea.strip())   # sin sangrías ni líneas vacías
    st.markdown(f'<div class="tabla-nb">{html}</div>', unsafe_allow_html=True)


def _texto(texto):
    if len(texto.splitlines()) > LINEAS_MAXIMAS:
        with st.expander("Ver el resultado completo"):
            st.code(texto, language=None)
    else:
        st.code(texto, language=None)


def _salida(salida):
    tipo = salida.output_type
    if tipo == "stream":
        _texto(salida.text)
    elif tipo in ("execute_result", "display_data"):
        datos = salida.data
        if "image/png" in datos:
            st.image(base64.b64decode(datos["image/png"]), width="stretch")
        elif "text/html" in datos:
            _tabla(datos["text/html"])
        elif "text/plain" in datos:
            _texto(datos["text/plain"])
    elif tipo == "error":
        st.error(f"{salida.ename}: {salida.evalue}")


def mostrar(ruta, con_codigo=False):
    """Presenta el notebook celda por celda: el texto explicativo, el código (opcional) y sus resultados."""
    if not ruta.exists():
        st.warning(f"No se encontró {ruta.name}.")
        return
    nb = _leer(str(ruta), ruta.stat().st_mtime)
    celdas_codigo = [c for c in nb.cells if c.cell_type == "code"]
    if celdas_codigo and not any(c.get("outputs") for c in celdas_codigo):
        st.warning(f"{ruta.name} no tiene resultados guardados. Ejecute `python -m pipeline` para generarlos.")
    st.caption(f"Contenido de `notebooks/{ruta.name}`, tal como quedó ejecutado con los 24 meses de datos.")
    for celda in nb.cells:
        if celda.cell_type == "markdown":
            st.markdown(celda.source)
        elif celda.cell_type == "code":
            if con_codigo:
                st.code(celda.source, language="python")
            for salida in celda.get("outputs", []):
                _salida(salida)
