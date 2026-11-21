# Guion del video: estudio de caso ECOBICI CDMX

**Proyecto:** *De los datos a la toma de decisiones: el desbalance matutino de estaciones ECOBICI (corredor Buenavista → Reforma)*
**Duración objetivo:** 14 a 15 minutos
**Integrantes:** Juan (técnico) · Marcos (técnico) · Paulina Gallardo · Day

> Todas las cifras salen de la **versión final**
> (notebooks 03 y 04, bitácora D-12 a D-23). **No usen las cifras de `docs/propuesta_proyecto.md`**: son las iniciales y varias no se reprodujeron.

---

## 1. Reparto de roles

| Bloque | Fase | Quién presenta | Tiempo | Qué se ve en pantalla |
|---|---|---|---|---|
| 0 | Apertura | Los 4 (habla Paulina Gallardo) | 0:00–1:00 | Los 4 en cámara, luego la portada |
| 1 | **Ask** · Preguntar | Paulina Gallardo | 1:00–3:00 | Inicio de la aplicación, 5 porqués, brechas |
| 2 | **Prepare** · Preparar | Marcos | 3:00–5:15 | README, terminal, notebook 01 |
| 3 | **Process** · Procesar | Juan | 5:15–7:45 | Notebook 02, bitácora, `config/pipeline.toml` |
| 4 | **Analyze** · Analizar | Marcos (cómo) y Juan (qué cambió) | 7:45–10:45 | Notebook 03 |
| 5 | **Share** · Compartir | Day | 10:45–12:30 | Figuras 04 y explorador de la aplicación |
| 6 | **Act** · Actuar | Paulina Gallardo y Day | 12:30–14:15 | Tabla del plan de acción |
| 7 | Limitaciones y cierre | Los 4 | 14:15–15:00 | Los 4 en cámara |

**Por qué este reparto:** los dos perfiles técnicos explican el código y las decisiones de datos (Prepare, Process, Analyze), que es donde la rúbrica pide "mostrar y justificar procedimientos". Paulina y Day explican el problema, los hallazgos y las recomendaciones (Ask, Share, Act), que no requieren programar pero sí entender el caso. Cada persona habla al menos 2.5 minutos y aparece en cámara al inicio, durante su parte (recuadro pequeño) y al cierre.

---

## 2. Antes de grabar

### Preparar la pantalla
- [ ] Abrir la aplicación: `python -m pipeline --desde app` (o `streamlit run app/app.py`). Dejarla lista en la pestaña **Inicio**.
- [ ] En VS Code, subir el zoom a 150 % (`Cmd +` en macOS) y usar el tema claro. El texto del código debe leerse en una pantalla de laptop.
- [ ] Tener abiertas en pestañas: `README.md`, `config/pipeline.toml`, `docs/bitacora_decisiones.md` y los 4 notebooks **con sus salidas**.
- [ ] Tener las 9 figuras de `figuras/` abiertas en un visor de imágenes, en este orden: `04_mapa_saldo`, `04_perfil_horario_corredor`, `04_ranking_prioritarias`, `04_destinos_buenavista`, `04_linea_base_prioritarias`, `03_serie_014`.
- [ ] Cerrar notificaciones (Slack, correo, WhatsApp Web) y ocultar el escritorio.

### Grabación
- **Opción recomendada:** una reunión de Zoom o Teams con grabación en la nube; cada quien comparte pantalla en su bloque y deja la cámara encendida (aparece en recuadro). Así se cumple "todos aparecen".
- Audífonos con micrófono para todos (evitan eco). Grabar en un cuarto sin ruido.
- Hacer una **prueba de 30 segundos** y escucharla antes de grabar todo.
- Si alguien se equivoca, hagan una pausa de 3 segundos y repitan la frase: se corta después al editar.

### Ensayo
- Hacer al menos **un ensayo completo con cronómetro**.
- Cada integrante lee **todo** el guion, no solo su parte: la rúbrica califica que todos dominen el proyecto completo (sección 6 de este documento).

---

## 3. Guion

> **Formato:** 🎥 = qué se ve · 🗣️ = qué se dice. El texto es una guía: díganlo con sus palabras, pero conserven las cifras exactas.

### Bloque 0 · Apertura (0:00–1:00) — Los 4, habla Paulina Gallardo

🎥 Los cuatro en cámara (galería de Zoom). Al terminar la presentación, Paulina Gallardo comparte la pestaña **Inicio** de la aplicación.

🗣️ **Paulina Gallardo:** Hola, somos el equipo de Ciencia de Datos de la Maestría en Big Data e Inteligencia Artificial de la Universidad Anáhuac Puebla. Yo soy Paulina Gallardo…

🗣️ **Marcos:** …yo soy Marcos…

🗣️ **Juan:** …yo soy Juan…

🗣️ **Day:** …y yo soy Day.

🗣️ **Paulina Gallardo:** En este video les contamos cómo llevamos casi 40 millones de viajes de ECOBICI, el sistema de bicicletas compartidas de la Ciudad de México, a una recomendación concreta. Trabajamos como consultores de datos para la operación del sistema y seguimos las seis fases del análisis de datos: preguntar, preparar, procesar, analizar, compartir y actuar. Usamos 24 meses de datos abiertos, de noviembre de 2024 a octubre de 2026.

---

### Bloque 1 · ASK: el problema (1:00–3:00) — Paulina Gallardo

🎥 Pestaña **Inicio** de la aplicación (problema y cuatro cifras clave). Después, la figura `04_perfil_horario_corredor.png`.

🗣️ **Paulina Gallardo:** Primero teníamos que elegir **qué** problema investigar. Consideramos tres temas: la caída de la demanda, la brecha de género entre usuarios y el desbalance de estaciones. Elegimos el **desbalance** por dos razones: es un patrón que se repite casi todos los días laborables, y permite proponer acciones concretas y medibles. Los otros dos temas exigían explicar causas que los datos de viajes no muestran, y corríamos el riesgo de confundir correlación con causalidad. Esa decisión está registrada en nuestra bitácora como D-02.

🗣️ El problema es este: cada mañana de día laborable, las estaciones alrededor de **Buenavista**, donde llegan el Tren Suburbano y el Metro, se **vacían**, y muchas estaciones de **Paseo de la Reforma** se **llenan**. Para un usuario eso significa llegar y no encontrar bici, o llegar a su destino y no tener dónde dejarla.

🎥 Mostrar la gráfica del perfil horario.

🗣️ Lo delimitamos así: días laborables, de 7:00 a 10:59 de la mañana, de noviembre de 2024 a octubre de 2026.

🗣️ Usamos la técnica de los **cinco porqués**:
1. ¿Por qué faltan bicis en Buenavista? Porque salen muchas más de las que llegan.
2. ¿Por qué? Probablemente, quienes bajan del tren usan la bici para el último tramo hacia su trabajo. **Esto es una hipótesis**, no algo comprobado.
3. ¿Por qué no regresan? Sí regresan, pero en la tarde: hacia las 6 de la tarde Buenavista recibe muchas bicis.
4. ¿Por qué no alcanza? Porque la demanda de la mañana supera la capacidad de las estaciones.
5. ¿Por qué no se compensa? Pensamos que el rebalanceo del operador no está alineado con la hora pico; también es una **hipótesis**.

🗣️ Con eso planteamos cuatro preguntas de investigación: ¿qué estaciones y horarios concentran el desbalance y qué tan seguido se repite?, ¿qué tan grande es comparado con la capacidad de cada estación?, ¿qué rutas lo explican?, y ¿cambió entre el primer y el segundo año? Le paso la palabra a Marcos, que explica de dónde salieron los datos.

---

### Bloque 2 · PREPARE: las fuentes y su calidad (3:00–5:15) — Marcos

🎥 `README.md` (sección "Estructura del repositorio"), después `config/pipeline.toml`, después la terminal y el notebook `01_perfilado.ipynb`.

🗣️ **Marcos:** Usamos dos fuentes oficiales. La primera son los **viajes**, del portal de datos abiertos de ECOBICI: 24 archivos CSV, uno por mes, unos 2.4 GB y **39,235,386 viajes**. Cada fila es un viaje con la estación y la hora de salida, la estación y la hora de llegada, y la edad y el género del usuario. La segunda es el **catálogo de estaciones** (GBFS `station_information`), que nos da la **capacidad** y las coordenadas de las 677 estaciones. Sin la capacidad no podríamos decir si un desbalance es grande o pequeño.

🎥 `config/pipeline.toml`, sección `[ventana]`.

🗣️ El periodo no está escrito dentro del código, sino en este archivo de configuración: de 2024-11 a 2026-10. Elegimos una ventana **fija** de 24 meses para poder comparar dos años completos de 12 meses, y para que, si el profesor ejecuta el proyecto dentro de seis meses, obtenga los mismos números del documento.

🎥 `pipeline/descarga.py` y la terminal.

🗣️ La descarga es automática. Un detalle: los nombres de los archivos del portal no siguen un patrón, unos se llaman `2024-02.csv` y otros `public_data_web_2026-06.csv`. Por eso el script **lee la página del portal y extrae los enlaces**, en lugar de tener 24 direcciones escritas a mano. Además reintenta si la red falla y no vuelve a bajar lo que ya está completo.

🎥 Notebook 01, secciones 2 y 3 (tabla de calidad por mes).

🗣️ Organizamos los datos en tres capas, lo que se llama arquitectura **medallion**: *bronze* son los datos tal como vienen, pero en formato Parquet; *silver*, los datos limpios; y *gold*, las tablas resumidas para el análisis. En la capa bronze leemos **todo como texto**. ¿Por qué? Porque los códigos de estación llevan ceros a la izquierda, como `015`; si los convertimos a número se vuelven `15` y ya no coinciden con el catálogo.

🗣️ Aquí aprendimos una lección importante. En la exploración inicial leímos todos los CSV de una sola vez con DuckDB, y **se perdieron sin aviso dos meses completos**, unos 3.7 millones de viajes, porque esos archivos traían todos los campos entre comillas. Desde entonces leemos **mes por mes** y validamos que el número de filas del Parquet sea igual al del CSV original en cada mes. Está en la bitácora como D-03.

🗣️ En el perfilado medimos la calidad **sin corregir nada**: no hay celdas vacías ni duplicados; desde junio de 2026 la edad viene con decimal, "26.0" en vez de "26"; hay códigos dobles como `271-272`, que son estaciones contiguas; y hay edades imposibles, de más de 100 años. Juan explica cómo los tratamos.

---

### Bloque 3 · PROCESS: limpieza y reproducibilidad (5:15–7:45) — Juan

🎥 Notebook `02_limpieza.ipynb` (sección 1, reglas, y sección 2, conteos). Luego `docs/bitacora_decisiones.md` abierto en D-13. Luego la terminal.

🗣️ **Juan:** En la limpieza seguimos una regla: cada decisión tiene que estar **justificada, contada y registrada**. Aplicamos cinco reglas en orden, y un viaje se excluye en la primera que incumple: fecha u hora que no se puede leer; llegada anterior a la salida; duración menor a 1 minuto; duración mayor a 24 horas; y retiros demasiado antiguos para el archivo.

🎥 Tabla de conteos del notebook 02 (o `datos/perfil/limpieza_resumen.csv`).

🗣️ El resultado: conservamos **39,229,201 viajes, el 99.984 %**. Excluimos 5,027 viajes de menos de un minuto, que suelen ser alguien que saca la bici y la regresa de inmediato, y 1,158 de más de 24 horas, que son errores o bicis que no se devolvieron. Como es tan poco, la limpieza no cambia la forma del análisis, pero sí evita que esos casos distorsionen los conteos.

🗣️ Igual de importante es lo que **no** excluimos. No quitamos los viajes que regresan a la misma estación, porque son uso real. Tampoco corregimos las edades imposibles: la edad no interviene en el análisis de desbalance, así que solo dejamos constancia.

🎥 `config/pipeline.toml`, secciones `[limpieza]` y `[analisis]`; después la bitácora en D-13.

🗣️ Tuvimos que definir dos cosas que parecen obvias y no lo son. **La franja de la mañana**: de 7:00 a 10:59. Probamos de 7 a 9:59, pero con la franja hasta las 10:59 se reproduce la cifra de la exploración inicial para la estación 014. Y **el día laborable**: lunes a viernes, **sin los 14 días de descanso obligatorio** de la Ley Federal del Trabajo, porque esos días tienen entre 8 % y 50 % del tráfico normal y bajarían el promedio. Quedan 254 y 253 días laborables en cada año.

🗣️ Cada decisión está en la bitácora con la fecha, lo que decidimos, la alternativa que descartamos, por qué, y cuántos registros afecta. Hay 23 entradas.

🎥 Terminal: `python -m pipeline --hasta visualizaciones` (pueden mostrar una ejecución grabada antes y acelerada).

🗣️ Por último, la **reproducibilidad**. Todo el proyecto se reproduce con un solo comando: `python -m pipeline`. Descarga, crea las tres capas, ejecuta los cuatro notebooks y genera las gráficas. Lo probamos desde cero en una carpeta nueva. En esa prueba encontramos que una versión más nueva de DuckDB cambiaba tres valores en el último decimal, así que **fijamos las versiones exactas** de todas las librerías; con ellas, las 11 tablas resultantes salen idénticas al dígito. Marcos explica el análisis.

---

### Bloque 4 · ANALYZE: qué encontramos (7:45–10:45) — Marcos y Juan

#### 4a · Cómo medimos (Marcos, 7:45–9:15)

🎥 Notebook `03_analisis.ipynb`, secciones 2, 4 y 5.

🗣️ **Marcos:** Construimos cuatro medidas, una por pregunta de investigación.

🗣️ Primero, el **saldo**: llegadas menos salidas de cada estación entre las 7 y las 11 de la mañana. Si es positivo, la estación se llena; si es negativo, se vacía.

🗣️ Segundo, la **persistencia**: en qué porcentaje de los días laborables la estación gana o pierde al menos 5 bicis. Sirve para distinguir un problema crónico de uno ocasional.

🗣️ Tercero, la **presión**: el saldo dividido entre la capacidad. Una presión de 3 significa que cada mañana llegan, en neto, tres veces las bicis que caben en la estación.

🗣️ Cuarto, la **matriz origen-destino**: a dónde van quienes salen de Buenavista.

🗣️ Una decisión de método: solo contamos los días en que la estación tuvo actividad. Al principio rellenábamos con cero los días sin viajes, y eso subestimaba el desbalance (D-13).

🗣️ Los resultados del periodo más reciente, noviembre de 2025 a octubre de 2026: la estación **014, Reforma y Río de Plata**, con capacidad de 39 bicis, **gana en promedio 121 bicis cada mañana**: una presión de 3.1, la más alta del sistema. Recibe más de lo que sale el 100 % de los días laborables. En el lado contrario, la **271-272 de Buenavista**, con capacidad de 74, **pierde 151 bicis**. Y en todo el sistema, **34 estaciones** tienen un saldo mayor que su capacidad completa.

#### 4b · Lo que cambió y lo que corregimos (Juan, 9:15–10:45)

🎥 Notebook 03, sección 6 (tabla de comparación), luego `figuras/03_serie_014.png`, luego `figuras/04_destinos_buenavista.png`.

🗣️ **Juan:** La cuarta pregunta era si el desbalance cambió entre los dos años. Sí cambió: el saldo de la estación 014 **bajó a la mitad**, de 247 a 121 bicis por mañana. Las salidas del núcleo de Buenavista bajaron de 565 a 453 diarias.

🎥 Serie mensual de 014.

🗣️ Quisimos saber por qué, y aquí hay que ser honestos. Revisamos tres cosas: la serie mes a mes, las estaciones vecinas y de dónde vienen las bicis que llegan a 014. Las llegadas a 014 cayeron **44 %**, mientras que el sistema completo cayó **8 %**, y las vecinas no absorbieron esa demanda. **Los datos de viajes no nos permiten saber por qué**: puede ser una obra, una oficina que cerró o un cambio operativo. Lo declaramos así, sin inventar una causa.

🎥 Gráfica de destinos desde Buenavista.

🗣️ El hallazgo más importante para el caso es que **la historia inicial era una simplificación**. Solo **25 %** de las bicis que salen de Buenavista termina en Reforma; el resto se reparte entre muchísimos destinos. Y solo cerca del **9 %** de las bicis que llegan a 014 viene de Buenavista. Hay un movimiento de Buenavista a Reforma, pero el desbalance es un problema **de muchas estaciones**, no de un solo corredor.

🗣️ Esto también nos sirvió para **verificar el trabajo inicial hecho con inteligencia artificial**. Recalculamos las cifras de la propuesta: el +243 de la estación 014 sí se reprodujo; pero el −250 de Buenavista no salió con ninguna definición, y los "580 viajes diarios hacia Reforma" en realidad eran las salidas **totales** de Buenavista. Todo el uso de IA y lo que verificamos está registrado en `docs/uso_ia.md`.

---

### Bloque 5 · SHARE: cómo lo comunicamos (10:45–12:30) — Day

🎥 `figuras/04_mapa_saldo.png`, luego `04_ranking_prioritarias.png`, luego `04_linea_base_prioritarias.png`, y al final la aplicación (pestaña **04 · Visualizaciones**, explorador de estaciones).

🗣️ **Day:** Para comunicar los resultados hicimos cinco gráficas con una sola regla de color: **rojo** significa que la estación **se llena** y **azul** que **se vacía**. Cada gráfica tiene como título la idea que muestra.

🎥 Mapa.

🗣️ En el mapa, cada punto es una estación: el color indica su saldo de la mañana y el tamaño, su capacidad. El primer panel muestra que ECOBICI cubre solo la zona central de la ciudad. En el acercamiento se ve Buenavista en azul y Reforma en rojo, pero también hay puntos rojos lejos de esa zona: **el desbalance no se limita al corredor**.

🎥 Ranking de prioritarias.

🗣️ Con estos datos elegimos **15 estaciones prioritarias**: las de mayor presión en las que el desbalance se repite en al menos el 80 % de los días. **Doce se llenan y solo tres se vacían.** Cuatro son de Reforma y dos de Buenavista, pero la mayoría de las demás está en otras zonas, sobre todo en Polanco.

🎥 Línea base.

🗣️ Esta gráfica es la **línea base**: en las 15 prioritarias, el saldo de la mañana supera la capacidad de la estación en el **87 % de los días laborables**, y el año anterior era 89 %. Es decir, casi nueve de cada diez días. No es algo ocasional.

🎥 Aplicación: elegir la estación 014 en el explorador y mostrar su serie y su perfil por hora.

🗣️ Además, hicimos una **aplicación** que muestra el proyecto etapa por etapa, con los notebooks ya ejecutados, y un explorador donde se elige cualquier estación y se ven sus indicadores. Por ejemplo, aquí está la 014: llegadas en rojo, concentradas entre las 8 y las 9 de la mañana.

---

### Bloque 6 · ACT: recomendaciones (12:30–14:15) — Paulina Gallardo y Day

🎥 Tabla del plan de acción (pueden ponerla en una diapositiva o en el documento).

| # | Acción | Indicador (KPI) | Línea base (2025-11 a 2026-10) | Meta propuesta* | Responsable / frecuencia |
|---|---|---|---|---|---|
| 1 | Rebalanceo programado en las 15 prioritarias: llenar las que se vacían antes de las 7:00 y vaciar las que se llenan entre 9:00 y 10:00 | % de días con saldo mayor que la capacidad | 87 % | [definir] | Operador / semanal |
| 2 | Más capacidad o resguardo temporal en 014 y en 271-272 / 273-274 | Bicis o espacios que faltan por mañana (medida indirecta) | 014: 121 · 271-272: 152 · 273-274: 128 | [definir] | SEMOVI y operador / mensual |
| 3 | Medir el inventario real con `station_status` (cada 5 min) antes y después de las acciones 1 y 2 | Minutos con la estación vacía o llena entre 7:00 y 10:59 | No existe hoy | Línea base en el primer mes | Operador / continuo |

\* Las metas las propone el equipo (están pendientes en el checklist). El impacto es **esperado, no comprobado**.

🗣️ **Paulina Gallardo:** Con base en lo que encontramos, proponemos tres acciones. Cada una tiene un indicador, una línea base que ya medimos, un responsable y una frecuencia.

🗣️ La **primera** es un **rebalanceo programado** en las 15 estaciones prioritarias: llevar bicis a las que se vacían antes de las 7 de la mañana y retirar bicis de las que se llenan entre las 9 y las 10. Se mide con el porcentaje de días en que el saldo supera la capacidad; hoy es 87 %.

🗣️ La **segunda** es **más capacidad**, o un servicio de resguardo temporal, en las estaciones con el desbalance más grande: la 014 necesitaría en promedio 121 espacios más cada mañana, y la 271-272 de Buenavista, 152 bicis más.

🗣️ **Day:** La **tercera** es **medir el inventario real**. Nuestros datos muestran viajes, no cuántas bicis había en cada estación. El catálogo de ECOBICI publica el estado de cada estación en tiempo real; si el operador lo registra cada 5 minutos, puede saber cuántos minutos pasa una estación vacía o llena, y comprobar si las acciones 1 y 2 funcionan.

🗣️ También **descartamos** una idea que parecía buena: dar incentivos a quien viaje en sentido contrario, de Reforma a Buenavista. Los datos muestran que ese contraflujo es de apenas **6 viajes al día**, contra **112** en el sentido principal. Aunque se duplicara, no compensaría el flujo. Así los datos nos ayudaron a descartar una acción, no solo a proponerlas.

🗣️ Importante: todas las mejoras son **esperadas, no comprobadas**. Por eso cada acción trae su línea base, para medir antes y después.

---

### Bloque 7 · Limitaciones y cierre (14:15–15:00) — Los 4

🎥 Los cuatro en cámara.

🗣️ **Marcos:** Tenemos tres limitaciones. No hay datos de inventario, así que vemos flujos y no estaciones vacías. La capacidad es la actual del catálogo, aunque comprobamos con una captura de 2024 que solo cambió en 9 de 677 estaciones, y en ninguna prioritaria.

🗣️ **Juan:** Y la más importante: **correlación no es causalidad**. El patrón coincide con la hipótesis del tren en Buenavista, pero no la demuestra. Todo el proyecto se puede reproducir con un solo comando y cada decisión está en la bitácora.

🗣️ **Day:** En resumen: el desbalance de ECOBICI es **crónico**, se repite casi nueve de cada diez días en las estaciones prioritarias, y **está en muchas estaciones**, no solo en un corredor.

🗣️ **Paulina Gallardo:** Por eso recomendamos actuar sobre 15 estaciones concretas y medir el resultado. Gracias.

---

## 4. Cómo cumple el guion con la checklist de la tarea

| Requisito | Dónde se cumple |
|---|---|
| Todos los integrantes aparecen y participan | Bloques 0 y 7 con los cuatro en cámara; cada persona presenta 2.5 a 4 minutos con la cámara en recuadro |
| Explican el desarrollo de las seis fases | Bloques 1 a 6, uno por fase |
| Muestran y justifican los procedimientos utilizados | Bloques 2 a 4: código, configuración, notebooks y bitácora en pantalla, con la alternativa descartada de cada decisión (lectura como texto, mes por mes, reglas de limpieza, franja, festivos, versiones fijas) |
| Explican hallazgos y recomendaciones | Bloque 4 (hallazgos), 5 (gráficas) y 6 (plan de acción con KPI) |
| Audio claro y recursos visuales legibles | Sección 2: audífonos, prueba de audio, zoom 150 % en VS Code, figuras en pantalla completa |
| Video disponible en la plataforma educativa | Sección 5 |

---

## 5. Después de grabar

- [ ] Ver el video completo antes de subirlo: que se escuche a todos y que las gráficas se lean.
- [ ] Cortar errores y silencios largos (Clipchamp, iMovie o el editor de Zoom).
- [ ] Exportar en MP4, 1080p.
- [ ] Subirlo a la plataforma educativa (si pesa mucho, a YouTube como "no listado" o a OneDrive y pegar el enlace, si el profesor lo permite).
- [ ] Abrir el enlace desde otra cuenta o en una ventana de incógnito para confirmar que se reproduce.
- [ ] Marcar "Video del estudio de caso" en `docs/checklist_proyecto.md`.

---

## 6. Preparación para preguntas (todos deben poder responder)

La rúbrica califica el **dominio** de todo el proyecto, no solo de la parte de cada quien. Repasen estas respuestas en equipo.

| Pregunta posible | Respuesta corta |
|---|---|
| ¿Qué es el saldo de una estación? | Llegadas menos salidas en la mañana. Positivo = se llena; negativo = se vacía. |
| ¿Qué es la presión? | El saldo dividido entre la capacidad. La 014 tiene 3.1: llegan 3 veces más bicis de las que caben. |
| ¿Qué son bronze, silver y gold? | Tres capas: datos originales en Parquet, datos limpios y tablas resumidas para el análisis. |
| ¿Por qué leer los datos como texto? | Para no perder los ceros a la izquierda de los códigos de estación (`015`). |
| ¿Por qué validar mes por mes? | Porque al leer todo junto con DuckDB se perdieron dos meses sin aviso. |
| ¿Cuántos datos eliminaron? | 6,185 viajes de 39.2 millones (0.016 %): los de menos de 1 minuto y los de más de 24 horas. |
| ¿Por qué quitaron los festivos? | Tienen entre 8 % y 50 % del tráfico normal y bajarían el promedio. |
| ¿Por qué bajó la estación 014? | No lo sabemos. Los viajes no lo explican; haría falta información externa. |
| ¿Es cierto que el problema es Buenavista → Reforma? | En parte: solo 25 % de las salidas de Buenavista va a Reforma. El desbalance está en muchas estaciones. |
| ¿Por qué no recomiendan incentivos a contraflujo? | Son 6 viajes al día contra 112; aunque se duplicaran, no compensan. |
| ¿El tren causa el desbalance? | Es una hipótesis compatible con el horario, pero correlación no es causalidad. |
| ¿Cómo se reproduce el proyecto? | `pip install -r requirements.txt` y `python -m pipeline`. |
| ¿Usaron IA? | Sí, para código y documentos. Está registrado en `docs/uso_ia.md`, y verificamos las cifras: algunas de la propuesta inicial no se reprodujeron y las corregimos. |

### Mini glosario para Paulina y Day
- **Pipeline:** la serie de pasos automáticos que convierte los datos originales en resultados.
- **Parquet:** un formato de archivo más rápido y ligero que el CSV.
- **DuckDB:** el programa con el que consultamos millones de filas en una laptop.
- **Notebook:** documento que mezcla explicación, código y resultados; es nuestra evidencia.
- **GBFS:** el formato estándar en que los sistemas de bicicletas publican sus estaciones.
- **Línea base:** el valor de hoy, contra el que se medirá si una acción funcionó.
