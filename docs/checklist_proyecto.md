# Checklist del proyecto

Estado al **2026-11-20**. Se actualiza cada vez que cambie algo (con la fecha en la columna de notas).

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
| Recolectar `station_status` (~7 días, cada 5 min) | ⏸ | P-05. Es lo que más tarda: cada día sin iniciar lo retrasa. |

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
| Perfilado de calidad de los datos | 🔄 | `01_perfilado.ipynb` existe pero es de 2024–2025: se regenera con la ventana nueva. |
| Diccionario de datos | 🔄 | Existe; falta el formato de edad con decimal y los códigos `Temporal` (D-07, D-08). |
| Script de descarga que lee el portal | ⬜ | Sustituye a `descargar_ecobici.sh` (URLs de 2024–2025 escritas a mano). |
| Descarga y copia fechada del catálogo de estaciones | ⏸ | P-09. Solo se probó en un prototipo temporal. |
| Evaluar calidad, pertinencia y confiabilidad de las fuentes | ⬜ | Se redacta en el PDF. |
| Fuente opcional: afluencia Tren Suburbano / Metro Buenavista | ⬜ | Opcional; ayuda a cumplir "múltiples fuentes". |

## 5. Process · Procesar (10 pts: justificado, validado y reproducible)

| Tarea | Estado | Notas |
|---|---|---|
| `config/pipeline.toml` y paquete `pipeline/` | ⬜ | Estructura definida en la arquitectura. |
| Bronze: CSV → Parquet por mes, validado contra el CSV | ⬜ | Funcionó en el prototipo (D-08). |
| Decidir las reglas de limpieza (< 1 min, > 24 h, retiros anteriores a la ventana, códigos raros, edad) | ⬜ | Cada una va a la bitácora antes de programarse. |
| Silver: limpieza, conteos antes y después, unión con el catálogo | ⬜ | `02_limpieza.ipynb`. |
| Definir "día laborable" y la franja de la mañana | ⏸ | P-08 y P-10. |
| Gold: tablas agregadas validadas contra silver | ⬜ | |
| Ejecutar el pipeline en una máquina limpia siguiendo solo el README | ⬜ | Prueba de reproducibilidad final. |

## 6. Analyze · Analizar (15 pts)

| Tarea | Estado | Notas |
|---|---|---|
| Saldo neto por estación, hora y día | ⬜ | `03_analisis.ipynb`. |
| Persistencia (% de días laborales con saldo ≥ umbral) | ⬜ | |
| Presión relativa (saldo ÷ capacidad) | ⬜ | La capacidad del catálogo es la actual. |
| Matriz origen-destino del corredor Buenavista → Reforma | ⬜ | |
| Comparación 2024-11→2025-10 contra 2025-11→2026-10 | ⬜ | |
| Línea base con `station_status` | ⏸ | Depende de P-05. |
| Redactar limitaciones y no confundir correlación con causalidad | ⬜ | |

## 7. Share (5 pts), Act (10 pts) y documentos de apoyo

| Tarea | Estado | Notas |
|---|---|---|
| Mapa de estaciones por saldo matutino | ⬜ | `04_visualizaciones.ipynb`. |
| Perfil horario Buenavista contra 014 Reforma | ⬜ | |
| Ranking de saldo ÷ capacidad | ⬜ | |
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
| P-05 | Máquina para recolectar `station_status` | ⬜ |
| P-06 | Aprobar la arquitectura del pipeline | ⬜ |
| P-07 | Versión mínima de Python (3.11 o 3.10) | ⬜ |
| P-08 | Definición de "día laborable" (¿festivos?) | ⬜ |
| P-09 | Versionar la copia fechada del catálogo | ⬜ |
| P-10 | Franja de la mañana (¿incluye la hora 10?) | ⬜ |

## 9. Ruta crítica

1. **Iniciar `station_status` ya** (P-05): son ~7 días de espera que no se pueden acelerar.
2. Decidir P-06, P-08 y P-10 para poder construir el pipeline.
3. Pipeline hasta silver y gold → recalcular cifras → documento, video y pitch.
