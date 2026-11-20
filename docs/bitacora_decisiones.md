# Bitácora de decisiones

Registro de **cada** decisión de preparación, limpieza o transformación de datos. Sirve para que cualquier
persona pueda entender, revisar y reproducir el proceso (rúbrica: *Process* justificado, validado y reproducible).

**Cómo agregar una entrada:** copia la plantilla, numérala en orden y llénala *en el momento* de tomar la decisión.
Si una decisión se revierte, no la borres: agrega una entrada nueva que lo explique.

## Plantilla

```markdown
### D-XX · <título corto>
- **Fecha:** AAAA-MM-DD
- **Fase / notebook:** Prepare | Process | Analyze — `notebooks/0X_....ipynb`
- **Decisión:** qué se hizo exactamente (regla concreta, p. ej. "se excluyen viajes con duración < 1 min").
- **Alternativa(s) descartada(s):** qué otra opción se consideró.
- **Justificación:** por qué esta opción es la mejor para nuestra pregunta.
- **Registros afectados:** cuántos viajes y qué % del total (cifra tomada del notebook).
- **Validación:** cómo comprobamos que se aplicó bien (conteo antes/después, gráfica, etc.).
- **Responsable:** nombre de quien la propuso y quien la revisó.
```

---

## Entradas

### D-01 · Leer todos los datos como texto y no modificar nada en la fase Prepare
- **Fecha:** 2026-11-18
- **Fase / notebook:** Prepare — `notebooks/01_perfilado.ipynb`
- **Decisión:** los 24 CSV se leen mes por mes, con todas las columnas como texto (`dtype=str`, sin convertir
  "NULL" ni celdas vacías a valores faltantes). Los nombres de columna se homologan a 9 nombres cortos
  (`genero`, `edad`, `bici`, `est_retiro`, `fecha_retiro`, `hora_retiro`, `est_arribo`, `fecha_arribo`, `hora_arribo`)
  después de comprobar que, quitando comillas y espacios, todos los meses traen las mismas columnas en el mismo orden.
  En esta fase **no se elimina, corrige ni imputa ningún registro**: solo se mide.
- **Alternativa(s) descartada(s):** (a) dejar que pandas infiera los tipos, que convierte "015" en 15 y esconde
  las edades no numéricas; (b) limpiar al mismo tiempo que se perfila, lo que mezcla diagnóstico y decisión y
  hace más difícil justificar cada cambio; (c) cargar los 42 M de filas de una vez, que necesita demasiada memoria
  para las laptops del equipo.
- **Justificación:** para diagnosticar hay que ver los datos tal como vienen. Los códigos de estación llevan ceros
  a la izquierda, y si los convertimos a número se pierden. Separar el diagnóstico (01) de la limpieza (02) deja
  cada decisión trazable.
- **Registros afectados:** 0 (no se modifica nada).
- **Validación:** la celda de la sección 2 del notebook verifica con `assert` que los encabezados coinciden en los 24 meses.
- **Responsable:** _por completar por el equipo_

### D-02 · Elegir el tema: desbalance de estaciones (corredor Buenavista → Reforma)
- **Fecha:** 2026-11-20
- **Fase / notebook:** Ask — `docs/propuesta_proyecto.md`
- **Decisión:** el estudio de caso será el **desbalance de estaciones** de ECOBICI en el corredor Buenavista → Reforma
  (días laborales, 7–10 h, 2024–2025). La decisión es **condicional a contar con la información necesaria**. Criterio de
  viabilidad, comprobado el 2026-11-20:
  - Viajes 2024-01 a 2025-12 (42,377,769): disponibles y perfilados. **Cumple.**
  - Catálogo de estaciones con capacidad (GBFS `station_information`): responde y trae 677 estaciones. **Cumple.**
  - Estado en vivo (GBFS `station_status`): responde y trae 677 estaciones; es opcional y sirve como línea base. **Disponible, por recolectar.**
  Si al unir viajes con catálogo la cobertura de códigos fuera insuficiente para calcular saldo ÷ capacidad, se reabre la decisión.
- **Alternativa(s) descartada(s):** evolución de la demanda (explicar el *por qué* exige datos externos y el riesgo de confundir
  correlación con causalidad es alto; se usa solo como contexto) y brecha de género (los viajes no permiten explicar causas y el
  valor "?" de género crece hasta 3 % del mes).
- **Justificación:** patrón muy estable (96–99 % de los días laborales), acciones concretas y medibles. Ver sección 1 de la propuesta.
- **Registros afectados:** 0 (decisión de diseño). Las cifras de la propuesta son preliminares y se recalculan en `03_analisis.ipynb`.
- **Validación:** pendiente: recalcular la cobertura de códigos viajes ↔ catálogo en `02_limpieza.ipynb` (la propuesta indica 677 de 680).
- **Responsable:** _por completar por el equipo_

### D-03 · Cargar los CSV mes por mes y validar el total, no con un comodín de DuckDB
- **Fecha:** 2026-11-20
- **Fase / notebook:** Process — `notebooks/02_limpieza.ipynb`
- **Decisión:** los 24 CSV se leen **uno por uno** y el total se valida contra el perfilado (**42,377,769** viajes). No se usa
  `read_csv('datos/raw/*.csv')` en una sola lectura.
- **Alternativa(s) descartada(s):** leer todos los archivos con un comodín en DuckDB, que es más corto pero omitió sin aviso
  los meses 2024-08 y 2024-09 (≈3.7 M de viajes), cuyos campos vienen todos entre comillas.
- **Justificación:** una carga que pierde datos sin avisar invalida todo lo demás. Validar el conteo de cada mes y el total
  después de cada carga es la comprobación que hace reproducible el proceso.
- **Registros afectados:** 0 con el método elegido; ≈3.7 M de viajes (≈8.7 % del total) se habrían perdido con el comodín.
- **Validación:** `assert` del total y de cada mes contra `datos/perfil/calidad_por_mes.csv`.
- **Responsable:** _por completar por el equipo_
- **Nota (2026-11-20):** la validación con el total fijo se ajusta en D-05, porque el periodo puede cambiar.

### D-04 · Arquitectura: medallion local (bronze → silver → gold) que se ejecuta al inicializar el proyecto
- **Fecha:** 2026-11-20
- **Fase / notebook:** Prepare / Process — pipeline de datos (por construir)
- **Decisión:** el proyecto se reproduce desde cero con un pipeline que, al inicializarse, ejecuta en orden:
  1. descarga de los datos, 2. ingesta a **bronze** (Parquet por mes, sin cambios), 3. **silver** (datos limpios según esta bitácora,
  con el catálogo de estaciones unido), 4. **gold** (agregados del análisis), 5. notebooks con salidas y visualizaciones,
  6. aplicación Streamlit. Todo corre en la máquina de quien reproduce (DuckDB + Parquet + Jupyter), sin servicios en la nube.
  Por decisión del equipo, el periodo de datos **no es fijo**: se define como parámetro (ver D-05).
- **Alternativa(s) descartada(s):** (a) **Databricks Free Edition**: solo cómputo serverless con cuota diaria, subir ~2.7 GB por la
  interfaz es incómodo y quien califique necesitaría una cuenta; (b) **warehouse en la nube con API key**: depende de que la cuenta,
  la cuota y la red sigan disponibles al calificar, exige compartir una credencial fuera de git y no muestra la carga ni la limpieza,
  que es lo que evalúa *Process*; (c) quedarse con `datos/procesados/` sin capas.
  _Nota: (a) y (b) fueron evaluadas con la IA; el equipo debe confirmar que las descarta._
- **Justificación:** la rúbrica pide un procesamiento "justificado, validado y reproducible" y dice que la complejidad tecnológica
  no da más puntos. 42 M de filas caben en una laptop con DuckDB. El medallion deja clara la historia de los datos para el documento.
- **Registros afectados:** 0 (decisión de diseño).
- **Validación:** pendiente. Una persona del equipo debe ejecutar el pipeline en una máquina limpia siguiendo solo el README.
- **Responsable:** _por completar por el equipo_

### D-05 · El periodo de análisis pasa a ser un parámetro; los artefactos del periodo 2024–2025 son provisionales
- **Fecha:** 2026-11-20
- **Fase / notebook:** Prepare — configuración del pipeline (por construir)
- **Decisión:** el trabajo hecho hasta ahora fue **exploratorio** y se hizo sobre 2024-01 a 2025-12. El equipo quiere poder usar datos más
  recientes (p. ej. 2025–2026). El portal publica hasta 2026-10 (comprobado el 2026-11-20). Por eso: (1) el periodo (mes inicial y final)
  vive en un archivo de configuración; (2) la descarga **lee el portal y extrae los enlaces**, porque los nombres de archivo son
  inconsistentes (`2024-02.csv`, `datos_abiertos_2024_03-1-1.csv`, `2025-10-1.csv`, `public_data_web_2026-06.csv`); (3) la validación de la
  carga compara **cada mes contra el conteo de filas de su CSV**, sin totales escritos a mano (sustituye la cifra fija 42,377,769 de D-03).
  Se consideran **provisionales** y se regenerarán: `datos/perfil/*`, `figuras/01_*`, `01_perfilado.ipynb`, y todas las cifras de
  `docs/propuesta_proyecto.md` (250 y 243 bicis, 36 estaciones, 42 %, 3,900 netas, comparación 2024 vs 2025).
- **Alternativa(s) descartada(s):** mantener 2024–2025 fijo con las 24 URL escritas a mano en `descargar_ecobici.sh`.
- **Justificación:** datos más actuales hacen más útil la recomendación, y la configuración evita rehacer el código cada vez que cambie la ventana.
- **Registros afectados:** 0 por ahora. Falta comprobar que los archivos de 2026 traen el mismo esquema (el cambio de nombre desde 2026-06 sugiere que puede haber diferencias).
- **Validación:** pendiente: revisar encabezados de los archivos de 2026 antes de definir la ventana.
- **Responsable:** _por completar por el equipo_

## Decisiones pendientes (no tomadas)

| # | Pregunta | Opciones | Nota |
|---|---|---|---|
| P-01 | ¿Ventana fija o móvil? | Fija (p. ej. 2025-01 a 2026-10, en la configuración) o "últimos 24 meses" | La IA recomienda fija: el PDF y el pipeline coinciden aunque se ejecute meses después. |
| P-02 | Alcance de Streamlit | Extra que lee solo gold, o requisito del pipeline | La rúbrica no pide aplicación. Si bloquea el arranque, el pipeline debe correr aparte con progreso visible. |
| P-03 | ¿Se descarta formalmente la nube (Databricks / warehouse)? | Sí (D-04) o mantener como opcional | Debe confirmarlo el equipo. |
| P-04 | Gold en git | Añadir excepción en `.gitignore` o guardar como CSV | `.gitignore` excluye hoy `*.parquet`. |
| P-05 | Máquina para recolectar `station_status` (~7 días) | Por definir | Es lo que más tarda. Falta el script. |
