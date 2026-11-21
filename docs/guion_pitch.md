# Elevator pitch: guion del video ejecutivo

**Proyecto:** *De los datos a la toma de decisiones: el desbalance matutino de estaciones ECOBICI (corredor Buenavista → Reforma)*
**Duración máxima:** 3:00 · **Objetivo de grabación:** 2:40 a 2:50 (deja margen para que no se pase)
**Integrantes:** Juan (técnico) · Marcos (técnico) · Paulina Gallardo · Day

> Todas las cifras salen de la **versión final** (notebooks 03 y 04, bitácora D-12 a D-23), igual que en `docs/guion_video.md`.
> **Mensaje central (si solo recuerdan una frase):** *"Cada mañana, 15 estaciones de ECOBICI reciben o pierden más bicis de las que caben, casi nueve de cada diez días; proponemos un rebalanceo programado y medirlo contra esa línea base."*

---

## 1. Reparto de roles

| Bloque | Qué cubre | Quién | Tiempo | En pantalla |
|---|---|---|---|---|
| 1 | Problema y su importancia | Paulina Gallardo | 0:00–0:40 | Los 4 en cámara → `04_perfil_horario_corredor.png` |
| 2 | Metodología | Marcos | 0:40–1:15 | Diagrama de las 6 fases y las capas (o el README) |
| 3 | Hallazgos | Juan | 1:15–2:00 | `04_ranking_prioritarias.png` → `04_destinos_buenavista.png` |
| 4 | Recomendación e impacto esperado | Day | 2:00–2:45 | `04_linea_base_prioritarias.png` → tabla de la recomendación |
| 5 | Cierre | Paulina Gallardo | 2:45–2:55 | Los 4 en cámara |

**Por qué así:** el pitch es para convencer, no para enseñar el código. Por eso Paulina y Day llevan el problema y la propuesta de valor (el inicio y el final, que es lo que más se recuerda), y Marcos y Juan dan el respaldo técnico en pocas frases. Hablan los cuatro, aunque la consigna solo exige que estén presentes en la proyección.

---

## 2. Guion

> 🎥 = qué se ve · 🗣️ = qué se dice. Aquí **sí conviene decirlo casi palabra por palabra**: cada bloque está medido en segundos (unas 150 palabras por minuto).

### Bloque 1 · Problema e importancia (0:00–0:40) — Paulina Gallardo · ≈95 palabras

🎥 Los cuatro en cámara durante 3 segundos; después, el perfil horario a pantalla completa.

🗣️ **Paulina Gallardo:** Imagina que bajas del tren en Buenavista, vas por una ECOBICI para llegar a tu oficina… y la estación está vacía. O llegas a Reforma y no hay lugar para dejarla. Esto pasa casi todos los días laborables. Cada mañana, las estaciones de Buenavista se vacían y muchas de Reforma se saturan.

🗣️ Importa porque un usuario que no encuentra bici o lugar deja de confiar en el sistema, y el operador gasta recursos sin saber dónde y cuándo actuar. Somos Paulina, Marcos, Juan y Day, y analizamos 39 millones de viajes para responder a eso.

### Bloque 2 · Metodología (0:40–1:15) — Marcos · ≈85 palabras

🎥 Diagrama simple: *Ask → Prepare → Process → Analyze → Share → Act* y, debajo, *raw → bronze → silver → gold*.

🗣️ **Marcos:** Seguimos las seis fases del análisis de datos con fuentes oficiales: 24 meses de viajes de los datos abiertos de ECOBICI, de noviembre de 2024 a octubre de 2026, y el catálogo de estaciones, que nos da la capacidad. Validamos cada mes contra su archivo original y limpiamos solo lo indispensable: conservamos el 99.98 % de los viajes. Medimos el saldo de cada estación entre las 7 y las 11 de la mañana y lo comparamos con su capacidad. Todo se reproduce con un solo comando.

### Bloque 3 · Hallazgos (1:15–2:00) — Juan · ≈105 palabras

🎥 Ranking de las 15 prioritarias; a los 25 segundos, cambiar a los destinos desde Buenavista. *Alternativa:* la pestaña **Inicio** de la aplicación, cuyas cuatro tarjetas (+121 bicis en 014, 25 % a Reforma, 12 / 3 prioritarias, 87 % de los días) son exactamente las cifras de este bloque.

🗣️ **Juan:** Tres hallazgos. Primero: el problema es enorme. La estación 014, en Reforma y Río de Plata, tiene lugar para 39 bicis y cada mañana recibe en promedio 121 más de las que salen: tres veces su capacidad. Pasa el 100 % de los días laborables.

🗣️ Segundo: es crónico. En las 15 estaciones con más presión, el saldo de la mañana supera la capacidad en el 87 % de los días.

🗣️ Tercero, y nos sorprendió: no es un solo corredor. Solo una de cada cuatro bicis que salen de Buenavista termina en Reforma, y 9 de las 15 estaciones prioritarias están en otras zonas de la ciudad.

### Bloque 4 · Recomendación e impacto esperado (2:00–2:45) — Day · ≈100 palabras

🎥 Línea base de las prioritarias; después, la tabla de abajo en una diapositiva.

🗣️ **Day:** Nuestra recomendación: un **rebalanceo programado** en esas 15 estaciones. Llevar bicis a las que se vacían antes de las 7 de la mañana y retirarlas de las que se llenan entre las 9 y las 10. Y en la 014 y en Buenavista, sumar capacidad o un resguardo temporal.

🗣️ El impacto **esperado** es que menos usuarios se queden sin bici o sin lugar. Es una hipótesis, no un resultado: por eso dejamos medida la línea base, el 87 % de los días. Con el estado de las estaciones en tiempo real, el operador puede comprobar con datos si funciona.

| Acción | Indicador | Línea base | Responsable |
|---|---|---|---|
| Rebalanceo programado en 15 estaciones | % de días con saldo mayor que la capacidad | 87 % | Operador, revisión semanal |
| Capacidad o resguardo en 014 y Buenavista | Bicis o espacios que faltan por mañana (indicador indirecto) | 014: 121 · 271-272: 152 | SEMOVI y operador, mensual |

### Bloque 5 · Cierre (2:45–2:55) — Paulina Gallardo · ≈20 palabras

🎥 Los cuatro en cámara.

🗣️ **Paulina Gallardo:** Los datos ya nos dicen dónde y cuándo. Lo que falta es actuar ahí y medirlo. Gracias.

---

## 3. Cómo cumple el guion con la checklist

| Requisito | Dónde se cumple |
|---|---|
| Presentan el problema y su importancia | Bloque 1: la escena del usuario sin bici y por qué afecta a usuarios y operador |
| Explican brevemente la metodología | Bloque 2: seis fases, dos fuentes oficiales, validación, limpieza y medida de saldo contra capacidad, en 35 segundos |
| Comunican los hallazgos más relevantes | Bloque 3: tamaño (014, 3 veces su capacidad), frecuencia (87 % de los días) y alcance (no es un solo corredor) |
| Presentan su recomendación y el impacto esperado | Bloque 4: rebalanceo programado y capacidad, con el impacto como **esperado** y su indicador para medirlo |
| El video no supera los tres minutos | Unas 420 palabras habladas ≈ 2:48; cada bloque lleva su tiempo |

---

## 4. Grabación y control del tiempo

- [ ] **Ensayar con cronómetro** cada bloque por separado. Si alguien se pasa más de 5 segundos de su tiempo, recorte una frase, no hable más rápido.
- [ ] Grabar igual que el video del caso (Zoom o Teams, cámara encendida, audífonos), pero **sin mostrar código**: solo gráficas grandes y la tabla de la recomendación.
- [ ] Preparar antes una diapositiva con el diagrama de las 6 fases (bloque 2) y otra con la tabla de la recomendación (bloque 4).
- [ ] Al editar, revisar que la duración final sea **2:55 o menos**.
- [ ] Probar el video en la computadora del salón o llevarlo en una memoria USB además del enlace.

---

## 5. Preguntas en clase (los cuatro deben estar presentes y poder responder)

Respuestas en una o dos frases. Reparto sugerido de quién contesta primero, aunque cualquiera debe poder hacerlo.

| Pregunta posible | Quién contesta primero | Respuesta corta |
|---|---|---|
| ¿Por qué eligieron este problema? | Paulina | Se repite casi todos los días y permite acciones medibles. La caída de la demanda o la brecha de género exigían explicar causas que los datos no muestran. |
| ¿Cómo saben que una estación está vacía? | Marcos | No lo sabemos directamente: los viajes muestran flujos, no inventario. Por eso proponemos medir con el estado en tiempo real. |
| ¿Qué significa "tres veces su capacidad"? | Juan | Que el saldo neto de la mañana (llegadas menos salidas) es de 121 bicis en una estación de 39 lugares. |
| ¿Cuántos datos limpiaron? | Juan | Quitamos 6,185 de 39.2 millones de viajes (0.016 %): los de menos de 1 minuto o más de 24 horas. |
| ¿El tren causa el desbalance? | Marcos | Es una hipótesis que coincide con el horario, pero correlación no es causalidad. |
| ¿Por qué no incentivar viajes en sentido contrario? | Day | El contraflujo es de 6 viajes al día contra 112; aunque se duplicara, no compensaría. |
| ¿Cuánto mejoraría con su propuesta? | Day | No lo prometemos: es un impacto esperado. Dejamos la línea base (87 %) para medirlo antes y después. |
| ¿Cambió el problema entre los dos años? | Juan | Sí: el saldo de la 014 bajó de 247 a 121 bicis por mañana, pero el problema sigue presente casi todos los días. No sabemos por qué bajó. |
| ¿Por qué no usaron machine learning? | Marcos | No hacía falta: la pregunta era describir y medir un patrón, y la sencillez hace el análisis más fácil de verificar. |
| ¿Usaron IA? | Paulina | Sí, para código y documentos. Lo registramos en `docs/uso_ia.md` y verificamos las cifras; algunas de la propuesta inicial no se reprodujeron y las corregimos. |

Para el detalle de cualquier respuesta, ver la sección 6 de `docs/guion_video.md`.
