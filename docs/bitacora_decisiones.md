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
