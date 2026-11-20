# Proyecto final – Ciencia de Datos (Maestría Big Data e IA, Anáhuac Puebla)

## Contexto
Equipo de 4 (2 con perfil técnico, 2 sin experiencia en programación). Proyecto "De los datos a la toma de
decisiones": estudio de caso con las 6 fases (Ask, Prepare, Process, Analyze, Share, Act) sobre los datos
abiertos de viajes de ECOBICI CDMX (https://ecobici.cdmx.gob.mx/datos-abiertos/).
Entregables: documento PDF 10–15 págs (60 pts), video del caso (25 pts), elevator pitch ≤3 min (15 pts).
Rúbrica documento: Ask 10, Prepare 10, Process 10 (justificado, validado y REPRODUCIBLE), Analyze 15, Share 5, Act 10.
Problema a investigar: DESBALANCE DE ESTACIONES, corredor Buenavista → Reforma (decisión D-02, 2026-11-20; detalle en
`docs/propuesta_proyecto.md`). Evolución de la demanda solo como contexto. Las cifras de la propuesta son preliminares:
recalcular en `03_analisis.ipynb`. Fuentes extra: catálogo GBFS `station_information` (capacidad) y `station_status` (opcional).

## Reglas de trabajo (importantes para la calificación)
- Todo el trabajo se hace en notebooks Jupyter (.ipynb) que el equipo ejecuta localmente en VS Code; se guardan
  CON salidas, porque son la evidencia. Cada paso lleva una celda markdown en español que explica QUÉ se hace y POR QUÉ,
  en lenguaje que entienda alguien sin formación técnica.
- Cada decisión de limpieza/transformación se registra también en `docs/bitacora_decisiones.md`
  (fecha, decisión, alternativa descartada, justificación, registros afectados).
- El uso de IA se documenta en `docs/uso_ia.md` (qué se pidió, qué se verificó a mano). El equipo debe entender todo.
- No confundir correlación con causalidad. No presentar impacto esperado como resultado comprobado.
- Sencillez > complejidad: la complejidad tecnológica no da más puntos. No se requiere machine learning.
- Rutas relativas a la raíz del repo; nada de rutas absolutas de una máquina.
- Los CSV crudos NO van a git (son ~2.7 GB); se reproducen con `descargar_ecobici.sh`.

## Datos
- `datos/raw/AAAA-MM.csv`: 24 meses (2024-01 a 2025-12), ~42.4 M viajes, 1.4–2.1 M filas por mes, ~100 MB c/u.
- Columnas: Genero_Usuario, Edad_Usuario, Bici, Ciclo_Estacion_Retiro, Fecha_Retiro, Hora_Retiro,
  Ciclo_EstacionArribo, Fecha_Arribo (en algunos meses "Fecha Arribo" con espacio), Hora_Arribo.
  Algunos meses (2024-08, 2024-09) traen encabezados entre comillas. Fechas dd/mm/aaaa, horas HH:MM:SS.
- Leer códigos de estación como texto (tienen ceros a la izquierda: "015").
- Los archivos están organizados por fecha de ARRIBO (hay retiros del mes anterior).
- Para procesar 42 M filas: procesar mes por mes o usar DuckDB; guardar intermedios en Parquet (`datos/procesados/`).

## Hallazgos del perfilado preliminar (verificar al re-ejecutar)
- Sin vacíos ni duplicados exactos.
- Género: M ~69%, F ~28%, O ~2%; valor "?" crece de ~10/mes (2024) a ~50 mil/mes (fin 2025); algunos "NULL".
- Edad: mínimo 16, máximos absurdos (124, 143, 160); 200–700 registros/mes con >80 años; algunos no numéricos.
- Duración: mediana ~12 min; 85–270 viajes/mes <1 min; 35–95/mes >24 h; retiros fechados hasta 2022 en archivos de 2024.
- ~678 estaciones; códigos dobles tipo "271-272" (estaciones contiguas); ~3% de viajes regresan a la misma estación.
- Existe un script preliminar `notebooks/01_perfilado.py` (lo generó la IA para explorar); debe migrarse a notebook.

## Estructura del repo
datos/raw (ignorado) · datos/procesados (ignorado si pesa) · datos/perfil · notebooks/ (01_perfilado, 02_limpieza,
03_analisis, 04_visualizaciones) · figuras/ · docs/ (bitacora_decisiones.md, uso_ia.md, diccionario_datos.md) · README.md
