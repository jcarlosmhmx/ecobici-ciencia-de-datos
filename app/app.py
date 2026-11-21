"""Presenta el proyecto etapa por etapa (notebooks 01 a 04).   Uso:  streamlit run app/app.py

La aplicación no procesa datos: muestra los notebooks ya ejecutados y consulta las tablas pequeñas de datos/gold.
Si faltan, se generan con:  python -m pipeline
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(Path(__file__).resolve().parent))   # para importar visor.py

import pandas as pd
import streamlit as st

import visor
from pipeline import config

st.set_page_config(page_title="ECOBICI CDMX: desbalance de estaciones", layout="wide")
visor.estilo()

cfg = config.cargar()
a = cfg["analisis"]
periodos = [x["nombre"] for x in cfg["periodos"]]
anterior, reciente = periodos[0], periodos[-1]
foco = a["estaciones_reforma"][0]
ROJO, AZUL = "#b2182b", "#2166ac"   # rojo: la estación se llena; azul: se vacía (bitácora D-19)
NOTEBOOKS = config.RAIZ / "notebooks"
COMANDO = "python -m pipeline"


@st.cache_data(show_spinner=False)
def gold(nombre):
    """Lee una tabla de datos/gold; devuelve None si todavía no se ha generado."""
    ruta = config.GOLD / f"{nombre}.parquet"
    return pd.read_parquet(ruta) if ruta.exists() else None


def corto(nombre):
    """Quita el prefijo 'CE-123' del nombre de la estación."""
    partes = str(nombre).split(" ", 1)
    return partes[1].strip() if len(partes) > 1 else str(nombre)


# ───────────────────────────── barra lateral ─────────────────────────────
with st.sidebar:
    st.title("ECOBICI CDMX")
    st.write("Desbalance de estaciones en el corredor **Buenavista → Reforma**.")
    st.write(f"Datos: **{cfg['ventana']['desde']} a {cfg['ventana']['hasta']}** (24 meses de viajes).")
    codigo = st.checkbox("Mostrar el código de cada paso", value=False)
    st.divider()
    st.caption("Prueba preliminar: las cifras deben revisarse antes de copiarse a los documentos finales.")
    st.caption("Fuente de los viajes: datos abiertos de ECOBICI.")


# ───────────────────────────── explorador de estaciones ─────────────────────────────
def explorador():
    st.subheader("Explora una estación")
    pers, serie, perfil = gold("persistencia_estacion"), gold("serie_mensual_estacion"), gold("perfil_horario_estacion")
    if pers is None or serie is None or perfil is None:
        st.info(f"Todavía no existen las tablas de `datos/gold`. Ejecute `{COMANDO}` y recargue la página.")
        return
    actual = pers[pers["periodo"] == reciente].sort_values("est")
    nombres = dict(zip(actual["est"], actual["nombre"].map(corto)))
    codigos = list(nombres)
    estacion = st.selectbox("Estación", codigos, index=codigos.index(foco) if foco in codigos else 0,
                            format_func=lambda c: f"{c} · {nombres[c]}")
    st.caption(f"Franja de la mañana: de {a['hora_inicio']}:00 a {a['hora_fin']}:59, solo días laborables. "
               "Saldo = llegadas menos salidas: positivo, la estación se llena; negativo, se vacía. "
               f"**% días gana / pierde:** porcentaje de días laborables en que gana o pierde al menos {a['umbral_persistencia_bicis']} bicis en la franja. "
               "**Presión:** saldo medio entre capacidad. **Bicis necesarias:** medida indirecta (media por día).")

    resumen = pers[pers["est"] == estacion].sort_values("periodo")[
        ["periodo", "capacidad", "dias_laborables", "dias_sin_actividad", "saldo_medio", "pct_dias_gana", "pct_dias_pierde",
         "presion", "bicis_necesarias_media"]]
    resumen.columns = ["Periodo", "Capacidad", "Días laborables", "Días sin actividad", "Saldo medio",
                       "% días gana", "% días pierde", "Presión", "Bicis necesarias"]
    st.dataframe(resumen, hide_index=True, width="stretch")

    izquierda, derecha = st.columns(2)
    with izquierda:
        st.markdown("**Llegadas y salidas por mes** (por día laborable, en la franja de la mañana)")
        mensual = serie[serie["est"] == estacion].sort_values("mes").set_index("mes")[["llegadas_por_dia", "salidas_por_dia"]]
        mensual.columns = ["llegadas", "salidas"]
        st.line_chart(mensual, color=[ROJO, AZUL])
    with derecha:
        periodo = st.radio("Periodo del perfil horario", periodos, index=len(periodos) - 1, horizontal=True)
        st.markdown("**Llegadas y salidas por hora** (por día laborable)")
        horas = (perfil[(perfil["est"] == estacion) & (perfil["periodo"] == periodo)].set_index("hora")
                 [["llegadas_por_dia", "salidas_por_dia"]].reindex(range(24), fill_value=0))
        horas.columns = ["llegadas", "salidas"]
        st.line_chart(horas, color=[ROJO, AZUL])


# ───────────────────────────── inicio ─────────────────────────────
def inicio():
    st.title("De los datos a la toma de decisiones: ECOBICI CDMX")
    st.markdown(
        "ECOBICI es el sistema de bicicletas compartidas de la Ciudad de México. Por la mañana, en días laborables, "
        "algunas estaciones **se vacían** (salen más bicis de las que llegan) y otras **se llenan** o saturan. "
        "Este estudio mide ese desbalance con **24 meses de viajes** y revisa en particular el corredor **Buenavista → Reforma**.")

    pers, cor, prior, kpi = gold("persistencia_estacion"), gold("corredor_buenavista_reforma"), gold("estaciones_prioritarias"), gold("kpi_prioritarias")
    if pers is None or cor is None or prior is None or kpi is None:
        st.info(f"Las cifras clave se calculan desde `datos/gold`, que todavía no existe. Ejecute `{COMANDO}` y recargue la página.")
    else:
        p = pers[pers["periodo"] == reciente].set_index("est")
        nucleo = cor[(cor["periodo"] == reciente) & (cor["grupo"] == "núcleo")].iloc[0]
        llenan, vacian = int((prior["tipo"] == "se llena").sum()), int((prior["tipo"] == "se vacía").sum())
        pct = kpi[kpi["periodo"] == reciente]["pct_dias_saldo_mayor_capacidad"].mean()
        st.subheader(f"Cifras clave ({reciente})")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(f"Estación {foco} (Reforma)", f"{p.loc[foco, 'saldo_medio']:+.0f} bicis", help="Saldo medio por mañana laborable: llegadas menos salidas.")
        c2.metric("Salidas de Buenavista a Reforma", f"{nucleo['pct_a_reforma']:.0f} %",
                  help="De las salidas matutinas de las 4 estaciones de Buenavista del análisis.")
        c3.metric("Prioritarias: se llenan / se vacían", f"{llenan} / {vacian}", help="Las 15 estaciones con mayor presión (saldo medio entre capacidad).")
        c4.metric("Saldo mayor que la capacidad", f"{pct:.0f} % de los días", help="Promedio de las 15 prioritarias, en días laborables.")

    st.subheader("Cómo recorrer esta aplicación")
    st.markdown(
        "Cada pestaña muestra uno de los notebooks del proyecto, con sus explicaciones, tablas y gráficas:\n\n"
        "- **01 · Perfilado (*Prepare*):** se obtienen los datos y se mide su calidad, sin modificarlos.\n"
        "- **02 · Limpieza (*Process*):** reglas de limpieza, con cuántos registros afecta cada una.\n"
        "- **03 · Análisis (*Analyze*):** saldo, persistencia y presión por estación; el corredor; la comparación entre los dos años; "
        "y la línea base del plan de acción (*Act*).\n"
        "- **04 · Visualizaciones (*Share*):** las gráficas finales y un explorador para consultar cualquier estación.\n\n"
        "En la barra lateral se puede activar la muestra del código de cada paso.")

    st.subheader("Qué hay que tener presente")
    st.markdown(
        "- **Prueba preliminar:** las cifras deben revisarse antes de usarse en el documento final.\n"
        "- **Se describe qué ocurre, no por qué.** Que dos cosas coincidan en el tiempo no demuestra que una cause la otra.\n"
        "- **No hay inventario:** los viajes muestran movimientos, no cuántas bicis había en cada estación ni la demanda que se quedó sin atender.\n"
        "- **Capacidad:** se usa la capacidad actual del catálogo de estaciones; se comparó con una captura de 2024 y la diferencia es pequeña.\n"
        "- Las mejoras que se propongan en el plan de acción son **hipótesis por medir**, no resultados.")


pestanas = st.tabs(["Inicio", "01 · Perfilado", "02 · Limpieza", "03 · Análisis", "04 · Visualizaciones"])
with pestanas[0]:
    inicio()
with pestanas[1]:
    visor.mostrar(NOTEBOOKS / "01_perfilado.ipynb", codigo)
with pestanas[2]:
    visor.mostrar(NOTEBOOKS / "02_limpieza.ipynb", codigo)
with pestanas[3]:
    visor.mostrar(NOTEBOOKS / "03_analisis.ipynb", codigo)
with pestanas[4]:
    visor.mostrar(NOTEBOOKS / "04_visualizaciones.ipynb", codigo)
    st.divider()
    explorador()
