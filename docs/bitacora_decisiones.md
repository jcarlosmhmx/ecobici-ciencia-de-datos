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

### D-06 · Ventana de datos fija: 2024-11 a 2026-10 (24 meses)
- **Fecha:** 2026-11-20
- **Fase / notebook:** Prepare — archivo de configuración del pipeline (por construir)
- **Decisión:** el periodo de análisis es **fijo**: del **2024-11** al **2026-10**, ambos meses incluidos (24 meses). Se interpreta
  "hasta el 2026-10-01" como el último archivo mensual publicado (2026-10). Resuelve P-01 y concreta D-05: el periodo sigue
  viviendo en la configuración, pero con estos valores. La comparación entre periodos se hace entre **dos ventanas de 12 meses**:
  2024-11 a 2025-10 contra 2025-11 a 2026-10.
- **Alternativa(s) descartada(s):** ventana móvil ("últimos 24 meses"), porque los números del PDF no coincidirían si el profesor
  ejecuta el pipeline meses después; 2025-01 a 2026-10 (22 meses), que deja la comparación anual desigual; solo los últimos 12 meses,
  que impide comparar periodos.
- **Justificación:** el documento, el pipeline y las cifras coinciden siempre. Mantiene el tamaño explorado (~2.7 GB, ~24 archivos) y
  permite comparar 12 contra 12 meses, lo que evita comparar un año completo con uno parcial.
- **Registros afectados:** se descartan del análisis los archivos 2024-01 a 2024-10 usados en la exploración. Cantidad de viajes por
  mes y total: se miden en `02_limpieza.ipynb`.
- **Validación:** pendiente: que el pipeline descargue exactamente los 24 archivos y que el conteo por mes coincida con cada CSV.
  Falta revisar el esquema de los archivos de 2026 (ver D-05).
- **Responsable:** _por completar por el equipo_

### D-07 · Revisión del esquema de los 24 archivos de la ventana (2024-11 a 2026-10)
- **Fecha:** 2026-11-20
- **Fase / notebook:** Prepare — comprobación previa a la descarga completa (se repite dentro del pipeline)
- **Decisión:** antes de descargar todo se leyeron **solo el encabezado y las primeras filas** (primeros ~1.5 KB) y el tamaño de cada
  uno de los 24 archivos, tomados de los enlaces del portal. Resultado:
  - Los 24 encabezados son **idénticos**: `Genero_Usuario, Edad_Usuario, Bici, Ciclo_Estacion_Retiro, Fecha_Retiro, Hora_Retiro,
    Ciclo_EstacionArribo, Fecha_Arribo, Hora_Arribo`. Ninguno lleva comillas ni la variante `Fecha Arribo`; el cambio de nombre
    de archivo desde 2026-06 (`public_data_web_...`) **no cambió las columnas**.
  - Fechas `dd/mm/aaaa` y horas `HH:MM:SS` en todos. Códigos de estación como texto con ceros (`096`) y dobles (`107-108`).
  - **Cambio de formato:** desde **2026-06** la edad viene con decimal (`26.0`) en lugar de entero (`26`). Hay que leerla como
    texto y convertirla con una regla única, o se mezclarán dos formatos en la misma columna.
  - Tamaño total de la ventana: 2.43 GB (88–119 MB por archivo). Todos los archivos terminan con salto de línea tipo Windows (CRLF).
  - Cada archivo empieza con retiros del mes anterior (p. ej. `2026-10` abre con viajes del 30/09), como ya se sabía.
- **Alternativa(s) descartada(s):** descargar los 2.4 GB para revisar el esquema; para ver encabezados no hace falta.
- **Justificación:** confirma que el mismo código de lectura sirve para toda la ventana, salvo el formato de edad.
- **Registros afectados:** 0 (solo lectura).
- **Validación:** limitada. Se revisaron únicamente las primeras filas de cada archivo, así que **no** descarta problemas más
  adelante en el archivo (p. ej. comillas en 2024-08 y 2024-09, que no están en la ventana). El pipeline debe validar cada archivo completo
  (columnas, número de campos por fila y conteo de filas).
- **Responsable:** _por completar por el equipo_

### D-08 · Prueba del diseño con un prototipo desechable (3 meses)
- **Fecha:** 2026-11-20
- **Fase / notebook:** Prepare / Process / Analyze — prueba previa, no forma parte del repo (se hizo en una carpeta temporal)
- **Decisión:** antes de escribir el pipeline se probaron sus partes más riesgosas con 2026-06, 2026-10 y 2025-05 (DuckDB, lectura como
  texto, `strict_mode`). Resultados:
  - **Bronze:** filas del Parquet = filas del CSV en los 2 meses probados (1,494,265 y 1,599,384). La validación por mes funciona.
  - **Edad:** en 2026-06 y 2026-10 todas las edades traen decimal (`26.0`) y no hay otros formatos; unas 30–36 por mes vienen vacías.
  - **Calidad (2026-06 + 2026-10, 3,093,649 viajes):** 406 viajes de menos de 1 min, 102 de más de 24 h, 0 fechas inválidas.
    Hay retiros de noviembre de 2025 dentro de archivos de 2026 (regla de retiros fuera de ventana, por decidir).
  - **Catálogo:** los 677 códigos del catálogo coinciden **directamente** con los de los viajes (incluidos los dobles como `271-272`);
    no hace falta normalizar ceros. Quedan sin catálogo 5 códigos: `Temporal 1` a `Temporal 4` y `1000` (≈570 viajes).
  - **Las cifras de la propuesta no se reproducen igual.** Saldo medio por día laboral entre 7 y 10 h:

    | Estación | 2025-05 (h 7–9) | 2025-05 (h 7–10) | 2026-10 (h 7–9) | 2026-10 (h 7–10) | Propuesta |
    |---|---|---|---|---|---|
    | 014 Reforma – Río de Plata | +220.8 | **+243.0** | +75.1 | +86.7 | +243 |
    | 271-272 Buenavista | −57.9 | −68.1 | −124.6 | −136.0 | −250 |

    1. La cifra de 014 de la propuesta (+243) **solo sale si la franja incluye la hora 10** (07:00 a 10:59). Entonces "entre 7 y 10 h"
       es ambiguo y hay que definirlo (P-10).
    2. La de 271-272 (−250) no coincide en ninguno de los dos meses; puede tratarse de otra definición (p. ej. suma del clúster
       de Buenavista o promedio de otro periodo). **No se sabe**: hay que revisar de dónde salió.
    3. **El patrón cambió entre meses:** 014 pasó de +221/+243 (2025-05) a +75/+87 (2026-10), y 271-272 se hizo más negativa. La dirección y la
       persistencia se mantienen (en 2026-10, 014 gana ≥5 bicis el 100 % de los días laborales y 271-272 pierde ≥5 el 100 %),
       pero **la afirmación "6 veces su capacidad" no se sostiene con 2026-10** (75 ÷ 39 ≈ 1.9). Es una observación de un solo mes
       y puede ser estacional; se resuelve con la ventana completa.
- **Alternativa(s) descartada(s):** construir todo el pipeline sin probarlo antes.
- **Justificación:** detecta temprano que la franja horaria no está bien definida y que las cifras de la propuesta no son estables entre periodos.
- **Registros afectados:** 0 (se leyó una copia temporal; no se guardó nada en el repo).
- **Validación:** el prototipo está en la carpeta temporal de la sesión y no se versiona. Las cifras deben recalcularse en `03_analisis.ipynb`.
- **Responsable:** _por completar por el equipo_

### D-09 · Alcance de la prueba preliminar (revisión interna del equipo, sábado 2026-11-21)
- **Fecha:** 2026-11-20
- **Fase / notebook:** Process / Analyze — pipeline mínimo y notebooks 01 a 03
- **Decisión:** la prueba preliminar la revisa **el equipo** (no el profesor) el 2026-11-21 y debe poder entenderse sin perfil técnico.
  Alcance: pipeline mínimo (descarga → bronze → silver → gold) y notebooks 01 a 03 con salidas, sobre una **ventana parcial
  (2026-06 a 2026-10)** y no sobre los 24 meses de D-06, que sigue siendo la ventana final. No se recolecta `station_status`
  (no alcanza el tiempo: se necesitan varias mañanas laborales); la acción 1 usará un indicador indirecto calculado con los viajes
  (saldo acumulado desde las 7:00 frente a la capacidad), que **no mide estaciones vacías** y se declara como limitación.
  Valores **provisionales** que se confirman después: franja de la mañana = horas 7 a 10 (07:00–10:59, P-10) y día laborable = lunes a viernes sin excluir
  festivos (P-08). Cualquier cifra de la prueba es preliminar y no se copia a documentos finales.
- **Alternativa(s) descartada(s):** recolectar `station_status` hasta el sábado (solo habría 1 o 2 mañanas, no una muestra útil);
  procesar los 24 meses (2.43 GB, horas de descarga y procesamiento, riesgo para la entrega).
- **Justificación:** es lo que se puede validar de punta a punta en el plazo. La franja 7–10 h es la única con la que se reproduce
  la cifra de la propuesta para la estación 014 (D-08), lo que permite comparar con la exploración.
- **Registros afectados:** 0 (decisión de alcance). La ventana parcial son ≈3.1 M de viajes de 5 meses.
- **Validación:** pendiente: al terminar, comprobar que los conteos por mes coinciden con los CSV y que el pipeline corre desde cero.
- **Responsable:** _por completar por el equipo_

### D-10 · Reglas de limpieza provisionales y primeros resultados de la prueba preliminar
- **Fecha:** 2026-11-20
- **Fase / notebook:** Process / Analyze — `notebooks/02_limpieza.ipynb`, `notebooks/03_analisis.ipynb`
- **Decisión:** en la capa silver se excluye un viaje si incumple la **primera** de estas reglas (en este orden): fecha u hora no interpretable;
  arribo anterior al retiro; duración menor a 60 s; duración mayor a 24 h; retiro anterior al mes previo al del archivo. **No se excluyen**
  viajes con estaciones sin catálogo (`Temporal 1` a `4`, `1000`; ≈610 viajes) ni se corrige la edad o el género (no intervienen en el análisis).
  Los umbrales viven en `config/pipeline.toml`. Son **provisionales** hasta que el equipo los confirme.
- **Alternativa(s) descartada(s):** (a) no excluir nada (los viajes de segundos o de días distorsionan los conteos); (b) excluir también los viajes
  que regresan a la misma estación (~3 %, son uso real); (c) excluir las estaciones `Temporal` (sus movimientos son reales, solo carecen de capacidad).
- **Justificación:** son reglas simples, de efecto muy pequeño y fáciles de explicar. Se cuenta cuántos viajes se excluye por cada motivo.
- **Registros afectados:** ventana 2026-06 a 2026-10: 7,558,447 viajes conservados (99.983 %); excluidos 1,049 por durar menos de 1 min (0.014 %)
  y 254 por durar más de 24 h (0.003 %). Las demás reglas no excluyen ninguno (los retiros muy antiguos caen antes en la regla de las 24 h).
- **Validación:** el pipeline comprueba que bronze = conservados + excluidos en cada mes, y que los totales de gold coinciden con un
  recuento directo de silver (1,545,362 salidas y 1,539,497 llegadas en la franja de la mañana).
- **Responsable:** _por completar por el equipo_
- **Resultados preliminares (ventana 2026-06 a 2026-10, 110 días laborables, franja 7–10 h, día laborable = lunes a viernes).**
  Ya NO coinciden con las de la propuesta, que son de 2024–2025 y salieron de una exploración con IA:

  | Medida | Propuesta | Recalculado (preliminar) |
  |---|---|---|
  | Saldo medio de la mañana, estación 014 | +243 | +111.6 (gana ≥5 bicis el 100 % de los días) |
  | Saldo medio de la mañana, estación 271-272 | −250 | −186.4 (pierde ≥5 bicis el 97.3 % de los días) |
  | Estaciones con |saldo| > capacidad | 36 | 29 (de 677 con capacidad conocida) |
  | Estaciones con |saldo| > mitad de la capacidad | 167 | 150 |
  | Peso de las 100 estaciones con mayor desbalance | 42 % | 47 % |
  | Viajes del corredor Buenavista → Reforma por la mañana | "~580 diarios" | 271-272 → 014: 585 viajes **en total** (≈5 al día); los 10 destinos principales desde las 4 estaciones de Buenavista suman ≈9,000 en 110 días (≈80 al día) |

  El patrón de fondo se mantiene (Buenavista se vacía, Reforma se llena, y por la tarde se invierte: ver `figuras/03_perfil_horario.png`).
  La cifra de "~580 viajes diarios" de la propuesta **no se reproduce** con ninguna definición probada; hay que revisar de dónde salió antes de usarla.
  La medida indirecta "bicis necesarias a las 7:00" de 271-272 es de 187 en promedio (máximo 359) frente a una capacidad de 74 (ver limitaciones en el notebook 03).

### D-11 · La prueba preliminar usa la ventana completa de 24 meses (revisa D-09)
- **Fecha:** 2026-11-20
- **Fase / notebook:** Prepare / Process / Analyze — `config/pipeline.toml`, notebooks 01 a 03
- **Decisión:** por indicación del equipo, la prueba preliminar **descarga y procesa los 24 meses** (2024-11 a 2026-10, D-06) y no la ventana
  parcial de 5 meses de D-09. El resto de D-09 sigue igual (revisión interna el 2026-11-21, sin `station_status`, franja y día laborable provisionales).
  La configuración define dos periodos de 12 meses (2024-11 a 2025-10 y 2025-11 a 2026-10) para responder la pregunta 4. Para no cargar ~42 M de
  filas en memoria, silver y gold usan vistas de DuckDB en lugar de tablas intermedias, y silver lee solo los archivos bronze de los meses de la ventana.
- **Alternativa(s) descartada(s):** mantener la ventana de 5 meses de D-09 (más rápida, pero sin comparación entre periodos).
- **Justificación:** el equipo quiere ver el pipeline y los resultados sobre los datos reales completos, y la comparación entre dos años de 12 meses
  es una de las cuatro preguntas de investigación.
- **Registros afectados:** los de la ventana completa; los conteos exactos se registran en el notebook 02 y en `datos/perfil/limpieza_resumen.csv`.
- **Validación:** el pipeline valida cada mes contra su CSV y gold contra silver. Las cifras de D-10 (ventana de 5 meses) quedan **sustituidas** por las del notebook 03.
- **Responsable:** _por completar por el equipo_

### D-12 · Resultados preliminares con la ventana completa de 24 meses (sustituyen a los de D-10)
- **Fecha:** 2026-11-20
- **Fase / notebook:** Process / Analyze — `notebooks/02_limpieza.ipynb`, `notebooks/03_analisis.ipynb`
- **Decisión:** se registran las cifras obtenidas al ejecutar el pipeline completo (descarga, bronze, silver y gold en ≈2 min con los archivos
  ya descargados; ≈1.5 min más la primera vez) con la configuración de D-11. Son **preliminares**: dependen de las reglas provisionales (D-10),
  de la franja 7–10 h (P-10) y de día laborable = lunes a viernes (P-08).
- **Alternativa(s) descartada(s):** no aplica (registro de resultados).
- **Justificación:** deja constancia de qué cifras salieron de los datos y cuáles de la propuesta no se reproducen.
- **Registros afectados:** bronze 39,235,386 viajes (= suma de los 24 CSV validada mes por mes); silver 39,229,201 conservados (99.984 %);
  excluidos 5,027 por durar menos de 1 min (0.013 %) y 1,158 por más de 24 h (0.003 %). 2,521 viajes (0.006 %) tienen una estación sin catálogo
  (`Temporal …`, `1000`, algunos con comillas dobles dentro del código). 261 y 260 días laborables en cada periodo.
- **Validación:** conteo por mes bronze = CSV; conservados + excluidos = bronze; gold = recuento directo de silver
  (7,694,762 salidas y 7,659,576 llegadas en la franja de la mañana).
- **Responsable:** _por completar por el equipo_
- **Resultados:**

  | Medida (día laborable, 7–10 h) | Propuesta (2024-2025, exploración IA) | 2024-11 a 2025-10 | 2025-11 a 2026-10 |
  |---|---|---|---|
  | Saldo medio, estación 014 Reforma | +243 | **+240.9** | +117.5 |
  | Saldo medio, estación 271-272 Buenavista | −250 | −178.7 | −138.9 |
  | Estaciones con \|saldo\| > capacidad | 36 | 44 | 32 |
  | Estaciones con \|saldo\| > mitad de la capacidad | 167 | 160 | 155 |
  | Peso de las 100 estaciones con mayor desbalance | 42 % | 49 % | 46 % |
  | Viajes/día de los 10 destinos principales desde Buenavista (mañana) | "~580 diarios" | ≈103 | ≈75 |

  Lectura (sin explicar causas): (1) el +243 de la propuesta para 014 **sí se reproduce** con el primer periodo (+241), lo que respalda que se usó la
  franja 7–10 h; (2) el saldo de 014 **se redujo a la mitad** en el segundo periodo, y el de las estaciones de Buenavista bajó en magnitud, aunque la dirección
  y la persistencia (≥ 88 % de los días en Buenavista, ≥ 94 % en 014) se mantienen; (3) el −250 de 271-272 y los "~580 viajes diarios" **no se reproducen** con
  ninguna definición probada; hay que ubicar su origen antes de usarlos; (4) por qué cambió 014 entre periodos **no se sabe**: puede ser demanda, capacidad, estaciones
  nuevas o cambios operativos, y los datos de viajes no lo distinguen.

## Decisiones pendientes (no tomadas)

| # | Pregunta | Opciones | Nota |
|---|---|---|---|
| P-02 | Alcance de Streamlit | Extra que lee solo gold, o requisito del pipeline | La rúbrica no pide aplicación. Si bloquea el arranque, el pipeline debe correr aparte con progreso visible. |
| P-03 | ¿Se descarta formalmente la nube (Databricks / warehouse)? | Sí (D-04) o mantener como opcional | Debe confirmarlo el equipo. |
| P-04 | Gold en git | Añadir excepción en `.gitignore` o guardar como CSV | `.gitignore` excluye hoy `*.parquet`. |
| P-05 | Recolectar `station_status` (~7 días) | **No se hace para la prueba preliminar** (D-09); queda opcional para después | La línea base de la acción 1 usará el indicador indirecto de los viajes. |
| P-06 | Aprobar la estructura de `docs/arquitectura_pipeline.md` | Aprobar o ajustar | Propuesta del 2026-11-20 (capas, carpetas, configuración, validaciones). |
| P-07 | Versión mínima de Python | 3.11 (`tomllib`) o mantener 3.10 con otro formato de configuración | El pipeline ya usa `tomllib` y el README pide 3.11; confirmar. |
| P-08 | Definición de "día laboral" | Lunes a viernes, o también excluir festivos oficiales | Cambia las cifras del análisis. |
| P-10 | Definición de la franja "mañana" | 07:00–09:59 (horas 7, 8, 9) o 07:00–10:59 (horas 7 a 10) | La cifra +243 de la estación 014 en la propuesta solo sale con la hora 10 incluida (D-08). |
| P-09 | Copia fechada del catálogo de estaciones en git | Sí (reproducible) o descargar siempre la versión vigente | La capacidad es la actual, no la de 2024–2026: limitación a declarar. |
