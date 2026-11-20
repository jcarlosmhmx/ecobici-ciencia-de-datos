# Registro de uso de inteligencia artificial

En este archivo documentamos **cuándo y para qué** usamos herramientas de IA, y **qué verificamos a mano**.
La IA puede ayudarnos a escribir código o texto, pero el equipo es responsable de entenderlo y comprobarlo.
Cualquier integrante debe poder explicar cualquier celda del proyecto.

## Plantilla

```markdown
### IA-XX · <tarea>
- **Fecha:** AAAA-MM-DD
- **Herramienta:** (p. ej. Claude Code, ChatGPT, Copilot)
- **Qué se pidió:** resumen de la instrucción.
- **Qué produjo:** archivos o celdas generados o modificados.
- **Qué verificamos a mano:** comprobaciones concretas hechas por el equipo (abrir el CSV y comparar, recalcular
  un número, revisar una gráfica, leer el código línea por línea…).
- **Qué cambiamos o rechazamos:** correcciones a lo que propuso la IA.
- **Verificado por:** nombre(s).
```

---

## Entradas

### IA-01 · Preparación del repositorio y perfilado de calidad (fase Prepare)
- **Fecha:** 2026-11-18
- **Herramienta:** Claude Code (modelo Claude Opus 5.5), ejecutado localmente en la carpeta del proyecto.
- **Qué se pidió:** crear la estructura del repositorio (carpetas, `.gitignore`, `requirements.txt`, `README.md`);
  convertir el script exploratorio `notebooks/01_perfilado.py` (también generado con IA) en el notebook
  `notebooks/01_perfilado.ipynb` con una tabla de calidad por mes, 4 gráficas y explicaciones en español;
  crear `docs/diccionario_datos.md`, esta bitácora y este registro; ejecutar el notebook sin limpiar datos.
- **Qué produjo:** los archivos anteriores, `datos/perfil/calidad_por_mes.csv`, `datos/perfil/problemas_calidad.csv`
  y `figuras/01_*.png`.
- **Qué verificamos a mano:** _por completar por el equipo_. Sugerencias:
  - [ ] Abrir 2 o 3 CSV (por ejemplo `2024-08.csv`, con encabezados entre comillas) y confirmar que las columnas son las que dice el notebook.
  - [ ] Contar las filas de un mes con otra herramienta (Excel no sirve, pasa del límite de ~1 M de filas; usar `wc -l` o DuckDB) y compararlas con la tabla.
  - [ ] Buscar a mano en un CSV un caso de edad > 100 y uno de duración > 24 h para confirmar que existen.
  - [ ] Revisar que las cifras de "Problemas de calidad encontrados" coinciden con las tablas del notebook.
  - [ ] Que cada integrante lea las celdas de explicación y pueda contar con sus palabras qué hace cada bloque.
- **Qué cambiamos o rechazamos:** _por completar_
- **Verificado por:** _por completar_

### IA-02 · Creación del repositorio en GitHub
- **Fecha:** 2026-11-18
- **Herramienta:** Claude Code (modelo Claude Opus 5.5).
- **Qué se pidió:** verificar que la CLI `gh` estuviera autenticada (el login lo hace la persona, no la IA); revisar el
  `.gitignore`; inicializar git en la rama `main`; confirmar que no se suba ningún CSV crudo ni archivo de más de 5 MB;
  hacer el primer commit; crear el repositorio **público** `ecobici-ciencia-de-datos` y subirlo; explicar cómo invitar
  a los colaboradores.
- **Qué produjo:** cambios en el `.gitignore`, aprobados antes de aplicarlos: se agregaron `.env`, `*.parquet` en todo el repo
  y extensiones de video. Además, el commit inicial y el repositorio remoto.
  Por decisión del equipo **sí se suben** dos CSV pequeños de diagnóstico: `datos/perfil/calidad_por_mes.csv` y
  `datos/perfil/problemas_calidad.csv`, de pocos KB y sin datos personales.
- **Qué verificamos a mano:** _por completar por el equipo_. Sugerencias:
  - [ ] Abrir el repo en GitHub y confirmar que no aparece la carpeta `datos/raw/` ni ningún archivo pesado.
  - [ ] Clonar el repo en otra computadora y seguir el README desde cero para comprobar que es reproducible.
- **Qué cambiamos o rechazamos:** _por completar_
- **Verificado por:** _por completar_

### IA-03 · Análisis exploratorio y propuesta de proyecto
- **Fecha:** 2026-11-18
- **Herramienta:** Claude Code (modelo Claude Opus 5.5).
- **Qué se pidió:** con base en el PDF del proyecto final y en las pautas de estudio de caso del BID, analizar los CSV
  y proponer un proyecto que cumpla la rúbrica.
- **Qué produjo:** `docs/propuesta_proyecto.md`. Para generarlo se hicieron consultas exploratorias con DuckDB sobre una copia
  temporal (no guardada en el repo), comparando los tres temas candidatos, y se consultó el catálogo público de estaciones (GBFS).
  Durante el trabajo detectó que leer los 24 CSV juntos con DuckDB omitía sin aviso 2024-08 y 2024-09; lo corrigió leyendo
  mes por mes y validando el total (42,377,769).
- **Qué verificamos a mano:** _por completar por el equipo_. Sugerencias:
  - [ ] Recalcular en `03_analisis.ipynb` las cifras clave (saldo matutino de 271-272 y de 014, 36 estaciones con saldo > capacidad).
  - [ ] Confirmar en el mapa de ECOBICI que 266-267, 268-269, 271-272 y 273-274 están junto a Buenavista.
  - [ ] Revisar que las metas del plan de acción estén redactadas como propuestas y no como resultados.
- **Qué cambiamos o rechazamos:** _por completar_
- **Verificado por:** _por completar_

### IA-04 · Fase 0: decisión del tema y actualización de documentos
- **Fecha:** 2026-11-20
- **Herramienta:** Claude Code (modelo Claude Sonnet 5.5).
- **Qué se pidió:** analizar la propuesta y armar un plan de trabajo; revisar el README contra el PDF del proyecto y las pautas
  del BID; comprobar que el catálogo de estaciones y `station_status` estén disponibles; registrar la decisión del tema.
- **Qué produjo:** entradas D-02 a D-05 y la lista de decisiones pendientes en la bitácora, esta entrada, y cambios en `CLAUDE.md`, `README.md` y la cabecera de
  `docs/propuesta_proyecto.md`. Las consultas a los dos endpoints GBFS solo leyeron los datos (no se guardaron).
- **Qué verificamos a mano:** _por completar por el equipo_. Sugerencias:
  - [ ] Abrir las dos URL de GBFS en el navegador y confirmar que traen 677 estaciones y el campo `capacity`.
  - [ ] Que cada integrante lea la propuesta y esté de acuerdo con el tema (la decisión D-02 es del equipo, no de la IA).
- **Qué cambiamos o rechazamos:** _por completar_
- **Verificado por:** _por completar_
