# Arquitectura del pipeline (medallion local)

> **Estado:** propuesta de estructura (2026-11-20), desarrolla las decisiones D-04, D-05 y D-06 de la bitácora.
> Todavía no hay código. Las preguntas abiertas están en la sección 8.

## 1. Idea general

Un solo comando descarga los datos oficiales y los transforma en tres capas. Cada capa es una carpeta de Parquet y cada
paso deja evidencia en un notebook explicado en español.

```
portal ECOBICI ──► raw ──► BRONZE ──► SILVER ──► GOLD ──► notebooks 01 a 04 ──► Streamlit
(CSV mensuales)  (CSV)   (Parquet,   (limpio +   (agregados  (análisis y      (solo lee
                         sin cambios) catálogo)   pequeños)   gráficas)        gold)
GBFS station_information ───────────────► SILVER (capacidad y coordenadas)
```

| Capa | Qué contiene | Quién la produce | ¿Va a git? |
|---|---|---|---|
| `raw` | CSV tal como los publica el portal | `pipeline/descarga.py` | No (~2.4 GB) |
| `bronze` | Los mismos datos en Parquet, todo como texto, un archivo por mes, con el mes de origen | `01_perfilado.ipynb` | No |
| `silver` | Viajes limpios, tipos correctos, códigos de estación normalizados, capacidad unida | `02_limpieza.ipynb` | No |
| `gold` | Tablas agregadas que usan el análisis y la aplicación (≈ 3 MB) | `03_analisis.ipynb` | No (D-23) |

Las capas mantienen los nombres de notebook que ya tiene el repo, y así cada fase de la rúbrica (Prepare, Process, Analyze,
Share) sigue teniendo su evidencia en un notebook con salidas.

## 2. Estructura de carpetas

```
├── config/
│   └── pipeline.toml          # ventana de datos, URL del portal, rutas, reglas de validación
├── pipeline/                  # código reutilizable; los notebooks lo importan
│   ├── config.py              # lee pipeline.toml y define las rutas
│   ├── descarga.py            # lee el portal, baja solo lo que falta, verifica tamaño y reintenta
│   ├── catalogo.py            # catálogo GBFS station_information (usa la copia fechada)
│   ├── lectura.py             # lectura de un CSV mensual como texto
│   ├── bronze.py              # CSV → Parquet sin cambios, valida filas contra el CSV
│   ├── silver.py              # reglas de limpieza y tipos; cuenta lo que excluye
│   ├── gold.py                # las 11 tablas resumidas (ver docs/capas_medallion.md)
│   └── __main__.py            # python -m pipeline [--desde etapa] [--hasta etapa] (la etapa final abre la app)
├── app/
│   ├── app.py                 # Streamlit: pestañas Inicio y notebooks 01 a 04 (D-21)
│   └── visor.py               # muestra un notebook ya ejecutado dentro de Streamlit
├── notebooks/                 # 01_perfilado, 02_limpieza, 03_analisis, 04_visualizaciones
├── datos/
│   ├── raw/                   # CSV (ignorado)
│   ├── bronze/AAAA-MM.parquet # (ignorado)
│   ├── silver/                # (ignorado)
│   ├── gold/                  # tablas pequeñas (ignorado; se regenera, D-23)
│   ├── catalogo/station_information_AAAA-MM-DD.json   # copia fechada (se versiona)
│   ├── perfil/                # diagnósticos de calidad (se versionan)
│   └── mapa/                  # contorno de la CDMX para los mapas (se versiona)
├── figuras/  ·  docs/
```

`descargar_ecobici.sh` se sustituye por `pipeline/descarga.py`. Así el pipeline es Python puro y funciona igual en Windows,
macOS y Linux, sin depender de Git Bash.

## 3. Configuración (`config/pipeline.toml`)

```toml
[ventana]
desde = "2024-11"     # D-06
hasta = "2026-10"

[portal]
pagina = "https://ecobici.cdmx.gob.mx/datos-abiertos/"

[catalogo]
url = "https://gbfs.mex.lyftbikes.com/gbfs/es/station_information.json"
usar_copia_versionada = true      # reproduce con la copia fechada; false = descargar la de hoy

[analisis]
franja_manana = ["07:00", "10:59"]   # horas 7 a 10 incluidas (D-13)
umbral_persistencia_bicis = 5     # "gana o pierde >= 5 bicis" (propuesta, sección 2.4)
```

Todo lo que cambie el resultado (ventana, franja, umbrales) vive aquí, no escrito dentro del código.

## 4. Etapas y validaciones

| # | Etapa | Entrada → salida | Validaciones que detienen el pipeline si fallan |
|---|---|---|---|
| 1 | **Descarga** | portal → `raw/` | Hay exactamente un archivo por mes de la ventana; el tamaño descargado coincide con `Content-Length`; se omiten los ya completos |
| 2 | **Bronze** | `raw/` → `bronze/` | Encabezados = los 9 esperados; mismo número de campos en cada fila; **filas del Parquet = filas del CSV (por mes)** |
| 3 | **Silver** | `bronze/` → `silver/` | Conteo antes/después de cada regla de limpieza (cada una con su entrada en la bitácora); ningún mes queda con 0 filas; cobertura de códigos de estación contra el catálogo |
| 4 | **Gold** | `silver/` → `gold/` | Las sumas de los agregados cuadran con silver (p. ej. la suma de salidas por hora = viajes del periodo) |
| 5 | **Notebooks** | `gold/` → figuras | Ejecución sin errores; las salidas quedan guardadas |
| 6 | **App** | `gold/` | Si falta `gold/`, muestra qué comando ejecutar en vez de fallar |

Las validaciones comparan cada mes contra su propio archivo. No se escribe ningún total a mano (D-05).

## 5. Reglas conocidas que el código debe contemplar

- Leer todo como **texto**; los códigos de estación llevan ceros a la izquierda (`096`) y hay códigos dobles (`107-108`).
  El catálogo GBFS usa los mismos códigos (con ceros y dobles), así que la unión es directa (prueba en D-08). Quedan sin
  catálogo `Temporal 1`–`Temporal 4` y `1000`.
- La **edad** trae decimal desde 2026-06 (`26.0`); se convierte con una regla única en silver (D-07).
- Los archivos se organizan por fecha de **arribo**; cada mes abre con retiros del mes anterior.
- Tolerar variaciones ya vistas en otros meses: encabezados entre comillas y `Fecha Arribo` con espacio. Aunque no aparecen en la
  ventana, el lector debe fallar con un mensaje claro si encuentra algo inesperado.
- Cada regla de limpieza (viajes < 1 min o > 24 h, retiros anteriores a la ventana, códigos raros) se registra en la bitácora
  antes de programarse.

## 6. Tablas de cada capa

El detalle de cada capa y de las **11 tablas de gold** (grano, columnas, cómo se calculan, qué resultado dieron y dónde se usan) está en
[`capas_medallion.md`](capas_medallion.md), con un diagrama de cómo se relacionan.

## 7. Cómo se usa (objetivo del README)

```bash
pip install -r requirements.txt
python -m pipeline              # descarga + bronze + silver + gold + notebooks, y al final abre la aplicación
streamlit run app/app.py        # abre solo la aplicación (no procesa nada)
```

Etapas: `descarga`, `bronze`, `silver`, `gold`, `visualizaciones` (notebook 04, que solo lee `gold/`) y `app` (abre Streamlit y queda esperando hasta `Ctrl+C`).
Opciones: `--desde silver` para repetir desde una capa; `--hasta visualizaciones` para procesar sin abrir la aplicación (úsese en ejecuciones desatendidas); `--desde app` para abrir solo la aplicación. La primera ejecución
descarga ~2.4 GB, por lo que el comando muestra el avance por etapa y por mes. Las siguientes omiten lo que ya está listo.

## 8. Preguntas abiertas (también en la bitácora)

1. **Versión de Python:** resuelta en D-23: Python 3.12 (`tomllib` viene desde 3.11).
2. **Días laborales:** ¿se excluyen solo sábados y domingos, o también festivos oficiales? Cambia el resultado y debe quedar en la bitácora.
3. **Librerías nuevas:** `streamlit`, `folium` o `plotly` (mapa) y `tqdm` (avance). Hay que añadirlas a `requirements.txt` con versiones fijas.
4. **Copia del catálogo:** resuelta en D-23: se versiona el JSON fechado para que el resultado no cambie si el feed cambia (el catálogo trae la
   capacidad *actual*, no la de la ventana: limitación a declarar; medida en D-16, diferencia pequeña).
