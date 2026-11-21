# De los datos a la toma de decisiones: ECOBICI CDMX 2024–2025

Proyecto final de **Ciencia de Datos**, Maestría en Big Data e Inteligencia Artificial, Universidad Anáhuac Puebla.

Estudio de caso que sigue las seis fases del análisis de datos (**Ask, Prepare, Process, Analyze, Share, Act**)
con los datos abiertos de viajes del sistema de bicicletas compartidas **ECOBICI** de la Ciudad de México:
24 meses (enero 2024 a diciembre 2025), unos **42 millones de viajes**.

- Fuente de datos: <https://ecobici.cdmx.gob.mx/datos-abiertos/>
- Problema a investigar: **desbalance de estaciones en el corredor Buenavista → Reforma** (cada mañana las estaciones
  de Buenavista se vacían y las de Reforma se saturan). Detalle en [`docs/propuesta_proyecto.md`](docs/propuesta_proyecto.md);
  la decisión de tema está en la bitácora (D-02).

## Estructura del repositorio

```
├── requirements.txt          # librerías de Python necesarias
├── config/pipeline.toml      # ventana de datos, franja de la mañana, reglas de limpieza
├── pipeline/                 # código del pipeline: descarga, bronze, silver, gold (python -m pipeline)
├── app/                      # aplicación Streamlit que presenta el proyecto por etapas (streamlit run app/app.py)
├── datos/
│   ├── raw/                  # CSV originales, uno por mes (NO se suben a git, ~2.4 GB)
│   ├── bronze/               # los mismos datos en Parquet, sin cambios (se regenera; no va a git)
│   ├── silver/               # viajes limpios en Parquet (se regenera; no va a git)
│   ├── gold/                 # tablas agregadas para el análisis (se regenera)
│   ├── catalogo/             # copias fechadas del catálogo de estaciones (capacidad actual y una captura de 2024-11)
│   ├── mapa/                 # contorno de la Ciudad de México para los mapas (capa del SIEG CDMX, D-18)
│   └── perfil/               # tablas de diagnóstico de calidad (pequeñas, sí se suben)
├── notebooks/
│   ├── 01_perfilado.ipynb    # Prepare: descarga, bronze y diagnóstico de calidad (sin limpiar nada)
│   ├── 02_limpieza.ipynb     # Process: silver, limpieza y transformación
│   ├── 03_analisis.ipynb     # Analyze: gold y análisis del desbalance
│   └── 04_visualizaciones.ipynb  # Share: gráficas finales para el documento y el video
├── figuras/                  # gráficas exportadas para el documento y la presentación
└── docs/
    ├── propuesta_proyecto.md  # el caso: problema, fuentes, análisis y acciones propuestas (cifras iniciales de la propuesta; las vigentes están en los notebooks 03 y 04)
    ├── arquitectura_pipeline.md # diseño del pipeline (medallion local)
    ├── capas_medallion.md     # qué contiene cada capa (bronze, silver, gold) y cada tabla gold, con diagrama
    ├── checklist_proyecto.md  # estado de tareas y entregables
    ├── diccionario_datos.md   # qué significa cada columna y qué problemas tiene
    ├── bitacora_decisiones.md # registro de cada decisión de limpieza/transformación
    └── uso_ia.md              # registro del uso de herramientas de IA
```

## Instalación del entorno (una sola vez)

Requisitos: **Python 3.12** (versión con la que se obtuvieron y reprodujeron los resultados, D-20 y D-23; el pipeline lee su configuración con `tomllib`, que exige 3.11 o más), **VS Code** con las extensiones *Python* y *Jupyter*, y unos 4 GB libres en disco.
Recomendado: 8 GB de RAM o más.

Abre una terminal en la carpeta del proyecto y ejecuta:

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Después, en VS Code abre cualquier notebook y en la esquina superior derecha (**Select Kernel**) elige el
intérprete de `.venv`.

## Cómo reproducir todo, paso a paso

**Atajo:** con el entorno activado, desde la carpeta del proyecto:

```bash
python -m pipeline                              # todo: descarga + bronze + silver + gold + gráficas, y al final abre la aplicación
python -m pipeline --hasta visualizaciones      # solo procesa (notebooks 01 a 04), sin abrir la aplicación
python -m pipeline --desde silver               # repite desde una etapa (descarga, bronze, silver, gold, visualizaciones o app)
python -m pipeline --desde app                  # solo abre la aplicación (igual que streamlit run app/app.py)
```

El periodo de datos se define en `config/pipeline.toml`: la ventana fija **2024-11 a 2026-10** (24 meses, bitácora D-06 y D-11).
La primera vez descarga ~2.4 GB y tarda unos 2 minutos con buena conexión; después, con los archivos ya descargados, unos 45 segundos.
Si un archivo ya está descargado y completo, no se vuelve a bajar. Los archivos se descargan leyendo los enlaces de la
página de datos abiertos (los nombres de archivo del portal no siguen un patrón).

Cada etapa de datos se ejecuta a través de su notebook (desde VS Code también se pueden abrir y correr con *Run All*):

| Notebook | Qué produce | Tiempo aprox. |
|---|---|---|
| `01_perfilado.ipynb` | descarga, `datos/bronze/`, `datos/perfil/calidad_por_mes.csv`, `figuras/01_viajes_por_mes.png` | ~30 s |
| `02_limpieza.ipynb` | `datos/silver/viajes.parquet`, `datos/perfil/limpieza_resumen.csv` | ~10 s |
| `03_analisis.ipynb` | `datos/gold/*.parquet`, `figuras/03_*.png` | ~10 s |
| `04_visualizaciones.ipynb` | `figuras/04_*.png` (5 gráficas) | ~5 s |

**Guardar los notebooks con sus salidas.** Las salidas son la evidencia del trabajo, así que no hay que borrarlas antes de subirlos.

## Ver el proyecto en una aplicación

Con el entorno activado, desde la carpeta del proyecto:

```bash
streamlit run app/app.py
```

(También se abre sola al final de `python -m pipeline`; para cerrarla, `Ctrl+C` en la terminal.) Se abre en el navegador, con una pestaña por cada etapa (**Inicio** y los notebooks **01 a 04**) y un explorador de estaciones. La aplicación muestra los notebooks ya ejecutados, así que no hace falta volver a procesar los datos; las cifras de *Inicio* y el explorador usan `datos/gold`, que se genera con `python -m pipeline`.

## Reglas de trabajo del equipo

- Cada paso de código lleva antes una celda de texto en español que explica **qué** se hace y **por qué**.
- Toda decisión de limpieza se anota en `docs/bitacora_decisiones.md`.
- Todo uso de IA se anota en `docs/uso_ia.md`, junto con lo que el equipo verificó a mano.
- En el código solo se usan rutas relativas a la carpeta del proyecto.
- No confundimos correlación con causalidad, y no presentamos un impacto esperado como si fuera un resultado comprobado.

## Entregables

Documento PDF de 10 a 15 páginas, video del estudio de caso y *elevator pitch* de 3 minutos o menos.
