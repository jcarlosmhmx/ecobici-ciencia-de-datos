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
├── descargar_ecobici.sh      # descarga los 24 CSV originales a datos/raw/
├── requirements.txt          # librerías de Python necesarias
├── datos/
│   ├── raw/                  # CSV originales, uno por mes (NO se suben a git, ~2.7 GB)
│   ├── procesados/           # datos limpios en Parquet (se regeneran con los notebooks)
│   └── perfil/               # tablas de diagnóstico de calidad (pequeñas, sí se suben)
├── notebooks/
│   ├── 01_perfilado.ipynb    # Prepare: diagnóstico de calidad (sin limpiar nada)
│   ├── 02_limpieza.ipynb     # Process: limpieza y transformación (pendiente)
│   ├── 03_analisis.ipynb     # Analyze (pendiente)
│   └── 04_visualizaciones.ipynb  # Share (pendiente)
├── figuras/                  # gráficas exportadas para el documento y la presentación
└── docs/
    ├── diccionario_datos.md   # qué significa cada columna y qué problemas tiene
    ├── bitacora_decisiones.md # registro de cada decisión de limpieza/transformación
    └── uso_ia.md              # registro del uso de herramientas de IA
```

## Instalación del entorno (una sola vez)

Requisitos: **Python 3.10 o superior**, **VS Code** con las extensiones *Python* y *Jupyter*, y unos 4 GB libres en disco.
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

1. **Descargar los datos** (unos 2.7 GB; tarda según la conexión):
   ```bash
   bash descargar_ecobici.sh
   ```
   Quedan 24 archivos `datos/raw/2024-01.csv` … `datos/raw/2025-12.csv`. Si un archivo ya existe, no se vuelve a descargar.
   En Windows, ejecútalo desde *Git Bash*, o descarga los archivos a mano con los enlaces del script y guárdalos con el nombre `AAAA-MM.csv`.

2. **Ejecutar los notebooks en orden** desde VS Code (botón *Run All*), o desde la terminal con el entorno activado:
   ```bash
   cd notebooks
   jupyter nbconvert --to notebook --execute --inplace 01_perfilado.ipynb
   ```
   | Notebook | Qué produce | Tiempo aprox. |
   |---|---|---|
   | `01_perfilado.ipynb` | `datos/perfil/calidad_por_mes.csv`, `datos/perfil/problemas_calidad.csv`, `figuras/01_*.png` | 5–10 min |
   | `02_limpieza.ipynb` | Parquet limpio en `datos/procesados/` | pendiente |
   | `03_analisis.ipynb` | tablas y resultados del análisis | pendiente |
   | `04_visualizaciones.ipynb` | gráficas finales en `figuras/` | pendiente |

3. **Guardar los notebooks con sus salidas.** Las salidas son la evidencia del trabajo, así que no hay que borrarlas antes de subirlos.

## Reglas de trabajo del equipo

- Cada paso de código lleva antes una celda de texto en español que explica **qué** se hace y **por qué**.
- Toda decisión de limpieza se anota en `docs/bitacora_decisiones.md`.
- Todo uso de IA se anota en `docs/uso_ia.md`, junto con lo que el equipo verificó a mano.
- En el código solo se usan rutas relativas a la carpeta del proyecto.
- No confundimos correlación con causalidad, y no presentamos un impacto esperado como si fuera un resultado comprobado.

## Entregables

Documento PDF de 10 a 15 páginas, video del estudio de caso y *elevator pitch* de 3 minutos o menos.
