# Checklist del proyecto

Estado al **2026-11-20** (prueba preliminar con la ventana completa de 24 meses para revisión interna del equipo el sábado 2026-11-21, D-09 y D-11). Se actualiza cada vez que cambie algo (con la fecha en la columna de notas).

**Leyenda:** ✅ hecho · 🔄 en progreso · ⬜ pendiente · ⏸ bloqueado por una decisión (ver sección 8)

Las asignaciones de responsable están sin llenar a propósito: las define el equipo.

## 1. Entregables (lo que se califica)

| Entregable | Valor | Estado | Notas |
|---|---|---|---|
| Documento del caso (PDF, 10–15 págs., sin contar anexos) | 60 pts | ⬜ | No hay borrador. Se escribe cuando estén recalculadas las cifras (3, 4 y 5 abajo). |
| Video del estudio de caso | 25 pts | ⬜ | Todos aparecen y participan; se sube a la plataforma educativa. |
| Elevator pitch (máx. 3 min) | 15 pts | ⬜ | Todos presentes en la proyección y listos para responder preguntas. |

## 2. Fase 0 · Decisiones y preparación del trabajo

| Tarea | Estado | Notas |
|---|---|---|
| Elegir el tema (desbalance de estaciones) | ✅ | D-02. Condicionado a la cobertura de datos, que la prueba D-08 confirmó. |
| Definir la ventana de datos (2024-11 a 2026-10) | ✅ | D-06. |
| Revisar el esquema de los 24 archivos de la ventana | ✅ | D-07. Cambia solo el formato de la edad desde 2026-06. |
| Probar el diseño con un prototipo | ✅ | D-08. Detectó que las cifras de la propuesta no se reproducen igual. |
| Actualizar `CLAUDE.md` y la cabecera de la propuesta | ✅ | |
| Actualizar el `README.md` (tema, estructura, entregables, Ask y Act, validación, reglas) | 🔄 | Solo se cambió el problema. Falta lo listado en la revisión del README. |
| Aprobar la arquitectura del pipeline (`docs/arquitectura_pipeline.md`) | ⏸ | P-06. |
| Hacer commit de D-08, la arquitectura y este checklist | ⬜ | Los cambios siguen sin commit. |
| Recolectar `station_status` (~7 días, cada 5 min) | ⬜ | Descartado para la prueba preliminar (D-09, P-05): no alcanza el tiempo. Opcional más adelante. |

## 3. Ask · Preguntar (10 pts)

| Tarea | Estado | Notas |
|---|---|---|
| Problema delimitado (corredor, horario, periodo) | 🔄 | Está en la propuesta. La franja horaria no está definida (P-10). |
| Cinco porqués y análisis de brechas | 🔄 | Borrador en la propuesta. Los porqués 2 y 5 son hipótesis. |
| Cuatro preguntas de investigación y unidad de análisis | ✅ | En la propuesta; revisar si el periodo cambia su redacción. |
| Reemplazar las cifras preliminares por las recalculadas | ⬜ | Depende de `03_analisis.ipynb`. No usar las cifras actuales (D-08). |

## 4. Prepare · Preparar (10 pts)

| Tarea | Estado | Notas |
|---|---|---|
| Perfilado de calidad de los datos | 🔄 | `01_perfilado.ipynb` regenerado y ejecutado con los 24 meses. Retirados los archivos exploratorios de 2024–2025 (JSON de `datos/perfil/`, figuras `01_*` viejas, `01_perfilado.py`). |
| Diccionario de datos | 🔄 | Existe; falta el formato de edad con decimal y los códigos `Temporal` (D-07, D-08). |
| Script de descarga que lee el portal | 🔄 | `pipeline/descarga.py` hecho y probado con los 24 meses; `descargar_ecobici.sh` eliminado. |
| Descarga y copia fechada del catálogo de estaciones | 🔄 | Copia en `datos/catalogo/` (2026-11-20). Falta confirmar si se versiona (P-09). |
| Evaluar calidad, pertinencia y confiabilidad de las fuentes | ⬜ | Se redacta en el PDF. |
| Fuente opcional: afluencia Tren Suburbano / Metro Buenavista | ⬜ | Opcional; ayuda a cumplir "múltiples fuentes". |

## 5. Process · Procesar (10 pts: justificado, validado y reproducible)

| Tarea | Estado | Notas |
|---|---|---|
| `config/pipeline.toml` y paquete `pipeline/` | ✅ | Versión mínima (descarga, bronze, silver, gold). Comando: `python -m pipeline`. |
| Bronze: CSV → Parquet por mes, validado contra el CSV | ✅ | 24 meses, 39,235,386 viajes validados mes por mes. |
| Decidir las reglas de limpieza (< 1 min, > 24 h, retiros anteriores a la ventana, códigos raros, edad) | 🔄 | Reglas provisionales aplicadas y registradas en D-10. El equipo debe confirmarlas. |
| Silver: limpieza, conteos antes y después, unión con el catálogo | ✅ | `02_limpieza.ipynb` ejecutado con los 24 meses. |
| Definir "día laborable" y la franja de la mañana | 🔄 | Provisionales: lunes a viernes y horas 7–10 (D-09). Confirmar P-08 y P-10. |
| Gold: tablas agregadas validadas contra silver | ✅ | 5 tablas, validadas contra un recuento directo de silver. |
| Ejecutar el pipeline en una máquina limpia siguiendo solo el README | ⬜ | Prueba de reproducibilidad final. |

## 6. Analyze · Analizar (15 pts)

| Tarea | Estado | Notas |
|---|---|---|
| Saldo neto por estación, hora y día | ✅ | `03_analisis.ipynb` (24 meses, dos periodos). |
| Persistencia (% de días laborales con saldo ≥ umbral) | ✅ | |
| Presión relativa (saldo ÷ capacidad) | ✅ | La capacidad del catálogo es la actual. Incluye el indicador indirecto "bicis necesarias". |
| Matriz origen-destino del corredor Buenavista → Reforma | 🔄 | Tabla de destinos hecha. Falta confirmar las 4 estaciones de Buenavista y la cifra "~580 diarios" de la propuesta (no se reproduce, D-10). |
| Comparación 2024-11→2025-10 contra 2025-11→2026-10 | 🔄 | Hecha en el notebook 03 (D-12). Falta entender y explicar por qué baja el saldo de 014 (los viajes no lo explican). |
| Línea base con `station_status` | ⬜ | No se hace en la prueba preliminar; se usa el indicador indirecto. |
| Redactar limitaciones y no confundir correlación con causalidad | ⬜ | |

## 7. Share (5 pts), Act (10 pts) y documentos de apoyo

| Tarea | Estado | Notas |
|---|---|---|
| Mapa de estaciones por saldo matutino | ⬜ | `04_visualizaciones.ipynb` (no existe todavía). |
| Perfil horario Buenavista contra 014 Reforma | 🔄 | Versión preliminar en `figuras/03_perfil_horario.png`. |
| Ranking de saldo ÷ capacidad | 🔄 | Versión preliminar en `figuras/03_ranking_presion.png`. |
| Diagrama o tabla de flujos desde Buenavista | ⬜ | |
| Tres acciones con KPI, línea base, meta, responsable y plazo | 🔄 | Borrador en la propuesta; las líneas base dependen del análisis. Impacto = esperado, no comprobado. |
| Aplicación Streamlit | ⏸ | P-02. Extra, no se pide en la rúbrica. |
| `docs/documento_caso.md` (texto fuente del PDF, con portada y resumen ejecutivo ≤ 250 palabras) | ⬜ | |
| `docs/referencias.md` (APA 7) | ⬜ | |
| `docs/reflexion_equipo.md` | ⬜ | La escribe el equipo, al final. |
| `docs/guion_video.md` con el reparto de fases entre los 4 integrantes | ⬜ | |
| `docs/guion_pitch.md` cronometrado (≤ 3 min) | ⬜ | |
| Repaso del proyecto completo en equipo antes de grabar | ⬜ | Pesa en "participación y dominio" (10 pts). |
| Completar `uso_ia.md` y los responsables de la bitácora | 🔄 | Las comprobaciones a mano están "por completar". |

## 8. Decisiones pendientes (detalle en la bitácora)

| # | Decisión | Estado |
|---|---|---|
| P-02 | Alcance de Streamlit (extra o requisito) | ⬜ |
| P-03 | Descartar formalmente la nube (Databricks / warehouse) | ⬜ |
| P-04 | Cómo versionar gold (`.gitignore` excluye `*.parquet`) | ⬜ |
| P-05 | Recolectar `station_status` | ✅ No para la preliminar (D-09) |
| P-06 | Aprobar la arquitectura del pipeline | ⬜ |
| P-07 | Versión mínima de Python (3.11 o 3.10) | ⬜ |
| P-08 | Definición de "día laborable" (¿festivos?) | ⬜ |
| P-09 | Versionar la copia fechada del catálogo | ⬜ |
| P-10 | Franja de la mañana (¿incluye la hora 10?) | ⬜ |

## 9. Ruta crítica

1. **Revisión de la prueba preliminar** con el equipo (sábado 2026-11-21).
2. Decidir P-06, P-08 y P-10, confirmar las reglas de limpieza (D-10) y las estaciones de Buenavista.
3. Visualizaciones finales (`04_visualizaciones.ipynb`) → documento, video y pitch con las cifras de D-12 (no las de la propuesta).
