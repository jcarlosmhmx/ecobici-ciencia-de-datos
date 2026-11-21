# Propuesta de proyecto: desbalance de estaciones ECOBICI (corredor Buenavista → Reforma)

> **Estado:** tema **adoptado** el 2026-11-20 (bitácora D-02), condicionado a la cobertura de datos (ver D-02). Las cifras
> de este documento son las **iniciales** de la propuesta del 2026-11-18; las vigentes están en los notebooks 03 y 04.
> **Base:** *Proyecto final: De los datos a la toma de decisiones* (Anáhuac Puebla) y *Pautas para la elaboración
> de Estudios de Caso* (BID, 2011).
>
> **Importante:** las cifras de este documento salen de un **análisis exploratorio inicial** hecho con IA (ver
> `docs/uso_ia.md`, IA-03). Antes de usarlas en el documento final hay que **recalcularlas en
> `notebooks/03_analisis.ipynb`** con los datos ya limpios. Pueden cambiar un poco según las reglas de limpieza.

---

## 1. Por qué este tema y no los otros dos

| Candidato | Lo que muestran los datos | Veredicto |
|---|---|---|
| **Desbalance de estaciones** | Patrón enorme y muy estable: el 96–99 % de los días laborales se repite. Las acciones posibles son concretas y medibles. | **Elegido** |
| Evolución de la demanda | 2025 tuvo 9.5 % menos viajes que 2024 (22.2 M → 20.1 M); la caída empieza en abril de 2025 y es mayor en el grupo de 16 a 24 años (−17 %). | Explicar el *por qué* exige datos externos (tarifas, competencia), así que el riesgo de confundir correlación con causalidad es alto. **Lo usamos como contexto.** |
| Brecha de género | Las mujeres son el 28 % de los viajes, una proporción estable. Ellas son el 32 % entre 25 y 34 años y el 17 % entre los mayores de 60. Por estación varía de 19 % a 40 %. | Los datos de viajes no permiten explicar las causas (por ejemplo, seguridad) y el valor "?" crece hasta 3 % del mes. El plan de acción quedaría débil. |

## 2. La propuesta

**Título tentativo:** *Bicis donde se necesitan: el desbalance matutino Buenavista–Reforma en ECOBICI (2024–2025)*

**Rol del equipo:** consultores en ciencia de datos para la operación de ECOBICI (SEMOVI y el operador del sistema).

### 2.1 Ask: el problema

Cada día laboral, las estaciones alrededor de **Buenavista** (salida del Tren Suburbano y del Metro) se vacían, y las de
**Paseo de la Reforma** se saturan. Los usuarios pueden llegar a una estación sin bicis o sin lugar para dejarla.

**Evidencia inicial (cifras de la propuesta, no las vigentes):**
- En la estación **271-272** de Buenavista (capacidad 74), entre las 7 y las 10 h de un día laboral **salen en promedio 250 bicis
  más de las que llegan**.
- En la **014 Reforma – Río de Plata** (capacidad 39) **llegan 243 bicis más de las que salen**: más de **6 veces su capacidad**.
  El 99 % de los días laborales pasa lo mismo.
- Por la tarde el flujo se invierte: Buenavista recibe 371 bicis entre las 18 y las 19 h.
- En **36 estaciones**, el saldo matutino promedio supera su capacidad completa, y en **167** supera la mitad.
- Las 100 estaciones con mayor desbalance concentran el **42 %** del problema, así que la acción se puede focalizar.
- El desbalance diario equivale a unas **3,900 bicis netas por día laboral** (5.9 % de los viajes). Esa proporción
  subió de 5.8 % a 6.1 % entre 2024 y 2025, aunque la demanda total cayó.

**Cinco porqués (borrador):**
1. Faltan bicis en Buenavista por la mañana → salen muchas más de las que llegan.
2. ¿Por qué? → quienes bajan del tren las usan para la "última milla" hacia sus oficinas en Reforma.
3. ¿Por qué no regresan? → regresan, pero hasta la tarde: el flujo es de ida y vuelta, desfasado.
4. ¿Por qué no alcanza el inventario? → la capacidad instalada es menor que el pico de demanda.
5. ¿Por qué no se compensa? → *(hipótesis por validar)* el rebalanceo no está alineado con los horarios pico.

> La parte del transporte (porqués 2 y 5) se presenta como **hipótesis apoyada por el patrón horario**, no como causa comprobada.

**Análisis de brechas:**

| | Estado actual (datos) | Estado deseado (meta propuesta) |
|---|---|---|
| Estaciones con saldo matutino mayor a su capacidad | 36 | 0 en las 15 estaciones prioritarias |
| Desbalance neto diario | ~3,900 bicis (5.9 % de los viajes) | Meta por definir con la línea base |
| Estaciones clave vacías o llenas entre 7 y 10 h | Desconocido (se mide con `station_status`) | Ninguna estación clave vacía entre 7 y 10 h |

Las metas son **propuestas del equipo**, no resultados.

**Preguntas de investigación:**
1. ¿Qué estaciones y horarios concentran el desbalance, y qué tan persistente es (% de días en que se repite)?
2. ¿Qué tan grande es la presión comparada con la capacidad de cada estación?
3. ¿Qué rutas origen-destino lo explican? (El corredor Buenavista → Reforma suma ~580 viajes diarios por la mañana).
4. ¿Cambió el desbalance entre 2024 y 2025, con la caída de la demanda?

**Unidad de análisis** (término de las pautas del BID): la estación (y el par origen-destino) en días laborales, 2024–2025.

### 2.2 Prepare: fuentes de datos

| Fuente | Qué aporta | Estado |
|---|---|---|
| Viajes ECOBICI 2024-01 a 2025-12 (24 CSV, 42,377,769 viajes): <https://ecobici.cdmx.gob.mx/datos-abiertos/> | Origen, destino, fecha y hora de cada viaje | Perfilado en `01_perfilado.ipynb` |
| Catálogo de estaciones (GBFS `station_information`): <https://gbfs.mex.lyftbikes.com/gbfs/es/station_information.json> | Nombre, coordenadas y **capacidad**. Coinciden 677 de los 680 códigos | Por descargar y documentar |
| *(Opcional, recomendado)* estado en vivo de las estaciones (GBFS `station_status`, cada 5 min durante ~7 días) | Minutos reales que cada estación pasa vacía o llena: **línea base de los indicadores** | Por recolectar |
| *(Opcional)* afluencia del Tren Suburbano o del Metro Buenavista (datos abiertos) | Refuerza (sin probar causalidad) la hipótesis del transbordo | Por buscar |

Las pautas del BID piden **múltiples fuentes de evidencia**; las opcionales ayudan a cumplirlo.

### 2.3 Process: puntos ya identificados

- Reglas de limpieza por decidir (cada una va a `docs/bitacora_decisiones.md`): viajes de menos de 1 min o de más de 24 h,
  retiros anteriores a 2024, edades imposibles (no afectan este análisis), códigos dobles (`271-272`) y códigos raros (`tag 2`, `Temporal…`).
- **Hallazgo de validación:** al leer los 24 CSV de una sola vez con DuckDB (`read_csv('datos/raw/*.csv')`), **se perdieron sin
  aviso los meses 2024-08 y 2024-09** (3.7 M de viajes), que traen todos los campos entre comillas. Se resolvió leyendo mes por mes
  y validando el total contra el perfilado (42,377,769). Esto debe quedar en la bitácora y en `02_limpieza.ipynb`, porque es un
  ejemplo concreto de por qué hay que **validar cada carga**.

### 2.4 Analyze

- Saldo neto (llegadas − salidas) por estación, por hora y por tipo de día.
- Persistencia: % de días laborales en que la estación pierde o gana ≥ 5 bicis entre 7 y 10 h.
- Presión relativa: saldo matutino ÷ capacidad.
- Matriz origen-destino del corredor Buenavista → Reforma.
- Comparación 2024 contra 2025.
- **Limitaciones que hay que declarar:** no hay historial de inventario, así que vemos flujos y no la demanda que se quedó sin
  atender; la capacidad del catálogo es la actual, no necesariamente la de 2024–2025; no hay identificador de usuario; correlación ≠ causalidad.

### 2.5 Share: visualizaciones propuestas

1. Mapa de estaciones coloreado por saldo matutino (las que se vacían contra las que se llenan).
2. Perfil horario de salidas y llegadas: Buenavista contra 014 Reforma (muestra la ida por la mañana y la vuelta por la tarde).
3. Ranking de las 15 estaciones con mayor saldo ÷ capacidad.
4. Diagrama de flujo (o tabla) de los principales destinos desde Buenavista.

### 2.6 Act: recomendaciones con indicadores

| # | Acción | Indicador (KPI) | Línea base | Meta propuesta | Responsable / frecuencia |
|---|---|---|---|---|---|
| 1 | **Ventanas de rebalanceo programadas** en las 15 estaciones de mayor presión: llenar Buenavista antes de las 7 h y vaciar Reforma entre 9 y 10 h; lo inverso por la tarde | % de minutos vacía o llena entre 7 y 10 h | Medición con `station_status` | Por definir | Operador / semanal |
| 2 | **Más capacidad o un servicio de resguardo** en 014 y en el clúster de Buenavista | Días con saldo matutino > capacidad | 99 % de los días (014) | Por definir | SEMOVI / mensual |
| 3 | **Incentivo para viajes "a contraflujo"** (puntos o minutos gratis por dejar la bici en Buenavista por la mañana) | Viajes Reforma → Buenavista entre 7 y 10 h | Por calcular | Por definir | Operador / mensual |

> El impacto se presenta como **esperado**, no como comprobado. La propuesta incluye cómo medirlo: comparar antes y después
> contra la línea base.

## 3. Verificación contra la rúbrica

| Criterio | Pts | Cómo se cumple "Sobresaliente" | Evidencia |
|---|---|---|---|
| Ask | 10 | Problema delimitado (corredor + horario + periodo), contexto, 5 porqués, brechas y 4 preguntas | Sección del documento |
| Prepare | 10 | Fuentes oficiales documentadas, calidad evaluada | `01_perfilado.ipynb`, `diccionario_datos.md` (ya hechos) |
| Process | 10 | Reglas de limpieza justificadas, conteos de validación antes y después, ejecución completa | `02_limpieza.ipynb`, bitácora, validación del total |
| Analyze | 15 | Cifras verificables, persistencia (% de días), comparación con capacidad, limitaciones explícitas | `03_analisis.ipynb` |
| Share | 5 | Mapa, perfil horario, ranking de saldo contra capacidad, interpretación en texto | `04_visualizaciones.ipynb`, `figuras/` |
| Act | 10 | 3 acciones, cada una con KPI, línea base, meta, responsable y plazo | Tabla del plan de acción |
| Video: participación y dominio | 10 | Cada integrante presenta 1–2 fases y todos pueden responder sobre todo el proyecto | Reparto de roles |
| Video: explicación del proceso | 10 | Mostrar notebooks y bitácora; justificar decisiones (por ejemplo, el fallo de DuckDB) | Grabación de pantalla |
| Video: comunicación audiovisual | 5 | Guion, buen audio y gráficas legibles | — |
| Pitch: síntesis y tiempo | 5 | Máximo 3 minutos, un solo mensaje central | Guion cronometrado |
| Pitch: hallazgos y evidencia | 5 | "Cada mañana llegan a la estación 014 más de 6 veces su capacidad" | Cifra del notebook |
| Pitch: propuesta de valor | 5 | Recomendación concreta y medible (acción 1 con su KPI) | Tabla del plan de acción |

**Checklist del documento PDF:** portada con los 4 integrantes · resumen ejecutivo ≤ 250 palabras · las 6 fases ·
hallazgos y visualizaciones · recomendaciones, plan de acción e indicadores · conclusiones, limitaciones y referencias APA 7 ·
anexos técnicos, bitácora de decisiones y reflexión del equipo.

**Estructura sugerida por las pautas del BID:** introducción (propósito y antecedentes) → preguntas de reflexión → narración
del caso (momentos críticos: la mañana en Buenavista y la saturación en Reforma) → lecciones y recomendaciones → anexos.

## 4. Riesgos y cómo mitigarlos

| Riesgo | Mitigación |
|---|---|
| No hay historial de inventario: no sabemos si la estación estaba realmente vacía | Recolectar `station_status` unos 7 días y declararlo como limitación |
| La capacidad del catálogo es la de hoy | Declararla como limitación; comparar con los máximos observados |
| El vínculo con el tren es una hipótesis | Presentarlo como hipótesis; reforzarlo con datos de afluencia sin afirmar causalidad |
| Que los integrantes sin perfil técnico no dominen el proyecto (pesa 10 pts en el video) | Celdas explicativas en cada notebook y repaso del proyecto completo en equipo antes de grabar |

## 5. Próximos pasos

1. Discutir y aprobar la propuesta en equipo, y actualizar el "problema a investigar" en `CLAUDE.md` y en el `README.md`.
2. Registrar en la bitácora la decisión del tema y el hallazgo de DuckDB.
3. `02_limpieza.ipynb`: aplicar las reglas de limpieza y guardar el Parquet limpio validado.
4. Descargar el catálogo de estaciones (y opcionalmente iniciar la recolección de `station_status`).
5. `03_analisis.ipynb` y `04_visualizaciones.ipynb`: recalcular las cifras de este documento.
6. Documento PDF, video y pitch.
