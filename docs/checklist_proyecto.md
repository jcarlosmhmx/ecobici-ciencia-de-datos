# Checklist del proyecto

Estado al **2026-11-21** (versión final del análisis con la ventana completa de 24 meses, D-06). Se actualiza cada vez que cambie algo (con la fecha en la columna de notas).

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
| Recolectar `station_status` (~7 días, cada 5 min) | ⬜ | Descartado (D-09, P-05): no alcanza el tiempo. Opcional más adelante. |

## 3. Ask · Preguntar (10 pts)

| Tarea | Estado | Notas |
|---|---|---|
| Problema delimitado (corredor, horario, periodo) | 🔄 | Está en la propuesta. La franja quedó definida en D-13 (7:00 a 10:59); el texto de la propuesta aún no la refleja. |
| Cinco porqués y análisis de brechas | 🔄 | Borrador en la propuesta. Los porqués 2 y 5 son hipótesis. |
| Cuatro preguntas de investigación y unidad de análisis | ✅ | En la propuesta; revisar si el periodo cambia su redacción. |
| Reemplazar las cifras de la propuesta por las recalculadas | ⬜ | Depende de `03_analisis.ipynb`. No usar las cifras actuales (D-08). |

## 4. Prepare · Preparar (10 pts)

| Tarea | Estado | Notas |
|---|---|---|
| Perfilado de calidad de los datos | 🔄 | `01_perfilado.ipynb` regenerado y ejecutado con los 24 meses. Retirados los archivos exploratorios de 2024–2025 (JSON de `datos/perfil/`, figuras `01_*` viejas, `01_perfilado.py`). |
| Diccionario de datos | 🔄 | Existe; falta el formato de edad con decimal y los códigos `Temporal` (D-07, D-08). |
| Script de descarga que lee el portal | 🔄 | `pipeline/descarga.py` hecho y probado con los 24 meses; `descargar_ecobici.sh` eliminado. |
| Descarga y copia fechada del catálogo de estaciones | 🔄 | Copias en `datos/catalogo/` (2026-11-20 y captura histórica 2024-11-07, D-16). Falta confirmar si se versionan (P-09). |
| Evaluar calidad, pertinencia y confiabilidad de las fuentes | ⬜ | Se redacta en el PDF. |
| Fuente opcional: afluencia Tren Suburbano / Metro Buenavista | ⬜ | Opcional; ayuda a cumplir "múltiples fuentes". |

## 5. Process · Procesar (10 pts: justificado, validado y reproducible)

| Tarea | Estado | Notas |
|---|---|---|
| `config/pipeline.toml` y paquete `pipeline/` | ✅ | Versión mínima (descarga, bronze, silver, gold). Comando: `python -m pipeline` (`--hasta visualizaciones` para no abrir la app). |
| Bronze: CSV → Parquet por mes, validado contra el CSV | ✅ | 24 meses, 39,235,386 viajes validados mes por mes. |
| Decidir las reglas de limpieza (< 1 min, > 24 h, retiros anteriores a la ventana, códigos raros, edad) | ✅ | Reglas de D-10 confirmadas como definitivas en D-13. |
| Silver: limpieza, conteos antes y después, unión con el catálogo | ✅ | `02_limpieza.ipynb` ejecutado con los 24 meses. |
| Definir "día laborable" y la franja de la mañana | ✅ | D-13: lunes a viernes sin festivos oficiales; horas 7 a 10. |
| Gold: tablas agregadas validadas contra silver | ✅ | 5 tablas, validadas contra un recuento directo de silver. |
| Ejecutar el pipeline en una máquina limpia siguiendo solo el README | 🔄 | Probado por la IA en un clon limpio, en Windows y con Python 3.12 y 3.15 (D-20): resultados idénticos. Falta que el equipo lo repita en otra computadora, de preferencia macOS o Linux. |

## 6. Analyze · Analizar (15 pts)

| Tarea | Estado | Notas |
|---|---|---|
| Saldo neto por estación, hora y día | ✅ | `03_analisis.ipynb` (24 meses, dos periodos). |
| Persistencia (% de días laborales con saldo ≥ umbral) | ✅ | |
| Presión relativa (saldo ÷ capacidad) | ✅ | La capacidad del catálogo es la actual. Incluye el indicador indirecto "bicis necesarias". |
| Matriz origen-destino del corredor Buenavista → Reforma | ✅ | "Reforma" definida por regla (24 estaciones, D-14). Solo ≈25 % de las salidas de Buenavista va a Reforma. Falta confirmar en el mapa el grupo de Buenavista (D-13). |
| Comparación 2024-11→2025-10 contra 2025-11→2026-10 | ✅ | Notebook 03 (D-12, D-13). La caída de 014 se describe pero **no se explica** (D-14); explicarla requiere datos externos. |
| Línea base con `station_status` | ⬜ | No se hace; se usa el indicador indirecto (D-09, P-05). |
| Redactar limitaciones y no confundir correlación con causalidad | ⬜ | |

## 7. Share (5 pts), Act (10 pts) y documentos de apoyo

| Tarea | Estado | Notas |
|---|---|---|
| Mapa de estaciones por saldo matutino | ✅ | `figuras/04_mapa_saldo.png` (D-17). Mapa por coordenadas con el contorno de la CDMX de fondo, sin calles (D-17, D-18). Falta citar la fuente en `docs/referencias.md`. |
| Perfil horario Buenavista contra 014 Reforma | ✅ | `figuras/04_perfil_horario_corredor.png`, con los dos periodos (D-17). |
| Ranking de saldo ÷ capacidad | ✅ | `figuras/04_ranking_prioritarias.png` (las 15 prioritarias) y `04_linea_base_prioritarias.png` (D-15, D-17). |
| Diagrama o tabla de flujos desde Buenavista | ✅ | `figuras/04_destinos_buenavista.png`: destinos más frecuentes (D-17). |
| Tres acciones con KPI, línea base, meta, responsable y plazo | 🔄 | Líneas base medidas (D-15, notebook 03 sección 9). Faltan metas, responsables y plazos, que propone el equipo. Impacto = esperado, no comprobado. |
| Aplicación Streamlit | ✅ | `app/app.py` (D-21): pestañas Inicio y notebooks 01 a 04, más explorador de estaciones. Extra, no se pide en la rúbrica. Se abre al final de `python -m pipeline` (etapa `app`) o sola con `streamlit run app/app.py`. |
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
| P-02 | Alcance de Streamlit | ✅ D-21 |
| P-03 | Descartar formalmente la nube (Databricks / warehouse) | ⬜ |
| P-04 | Cómo versionar gold (`.gitignore` excluye `*.parquet`) | ⬜ |
| P-05 | Recolectar `station_status` | ✅ No se hace (D-09) |
| P-06 | Aprobar la arquitectura del pipeline | ⬜ |
| P-07 | Versión mínima de Python (3.11 o 3.10) | ⬜ |
| P-08 | Definición de "día laborable" | ✅ D-13 |
| P-09 | Versionar la copia fechada del catálogo | ⬜ |
| P-10 | Franja de la mañana | ✅ D-13 |

## 9. Ruta crítica

1. **Revisión de la versión final** con el equipo (sábado 2026-11-21).
2. Decidir P-06 y confirmar en el mapa el grupo de Buenavista (D-13).
3. Revisar las figuras `figuras/04_*.png` y usarlas en el documento, el video y el pitch con las cifras de D-12 a D-16 (no las de la propuesta).
