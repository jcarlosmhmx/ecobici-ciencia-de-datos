# Diccionario de datos: viajes ECOBICI CDMX (2024-01 a 2025-12)

- **Fuente:** <https://ecobici.cdmx.gob.mx/datos-abiertos/> (descarga con `descargar_ecobici.sh`).
- **Unidad de observación:** un renglón = un viaje (retiro y devolución de una bicicleta).
- **Archivos:** 24 CSV mensuales en `datos/raw/AAAA-MM.csv`, 42,377,769 viajes en total (de 1.45 M a 2.05 M por mes), 2.66 GB.
  Cada archivo agrupa los viajes por **fecha de arribo**, no de retiro.
- **Formato:** texto separado por comas, UTF-8, sin celdas vacías. 8 meses (2024-01 a 2024-09, salvo 2024-04) traen los
  encabezados entre comillas, y 6 meses escriben `Fecha Arribo` con espacio en vez de `Fecha_Arribo`.
- **Cifras:** salen de `notebooks/01_perfilado.ipynb` y `datos/perfil/calidad_por_mes.csv`. Si se re-ejecuta el notebook, hay que actualizarlas aquí.

| # | Columna original | Nombre en notebooks | Significado | Tipo (original → para análisis) | Ejemplo | Problemas detectados |
|---|---|---|---|---|---|---|
| 1 | `Genero_Usuario` | `genero` | Género declarado por el usuario al registrarse | texto → categoría | `M` | Valores M (68.65%), F (28.30%), O (1.93%). **"?" (sin dato): 475,613 viajes (1.12%)**, que pasan de 9 en 2024-01 a ~46–51 mil por mes a fines de 2025 (3.2% de 2025-12). 119 viajes con `NULL`. |
| 2 | `Edad_Usuario` | `edad` | Edad del usuario en años | texto → entero | `48` | Mínimo 16 (ninguna menor de 16). 1,788 valores `NULL` (0.004%). **9,169 viajes con > 80 años**, de ellos 493 con > 100 años (máx. 160), que casi seguro son errores de captura. Hay picos en 124 y 125 años. |
| 3 | `Bici` | `bici` | Número de identificación de la bicicleta | texto (identificador; no es una cantidad) | `3371879` | Todos numéricos y sin vacíos. No se le hacen cálculos aritméticos. |
| 4 | `Ciclo_Estacion_Retiro` | `est_retiro` | Código de la estación donde se tomó la bici | **texto** (por los ceros a la izquierda) | `015`, `271-272` | 681 códigos distintos en 24 meses (655 a 679 por mes). 12 **códigos dobles** de estaciones contiguas (p. ej. `271-272`), con ~3.7 M menciones entre retiro y arribo. Además, `tag 2` (2024-08) y `Temporal - 2da Sección Bosque Chapultepec` (2025-04) aparecen como códigos raros. No se encontraron códigos sin cero a la izquierda. |
| 5 | `Fecha_Retiro` | `fecha_retiro` | Fecha en que se tomó la bici | texto `dd/mm/aaaa` → fecha | `31/12/2023` | Formato consistente. Hay retiros de meses anteriores al del archivo (4,194 viajes). **113 retiros son anteriores a 2024** (el más antiguo, del 19/08/2022). |
| 6 | `Hora_Retiro` | `hora_retiro` | Hora en que se tomó la bici | texto `HH:MM:SS` → hora | `23:21:52` | Formato consistente. |
| 7 | `Ciclo_EstacionArribo` | `est_arribo` | Código de la estación donde se devolvió la bici | **texto** | `659` | Mismos problemas que `est_retiro`. 1,197,103 viajes (2.8%) regresan a la misma estación de donde salieron. |
| 8 | `Fecha_Arribo` (`Fecha Arribo` en 6 meses) | `fecha_arribo` | Fecha en que se devolvió la bici | texto `dd/mm/aaaa` → fecha | `01/01/2024` | Nombre de columna inconsistente. Todas las fechas de arribo caen dentro del mes de su archivo. |
| 9 | `Hora_Arribo` | `hora_arribo` | Hora en que se devolvió la bici | texto `HH:MM:SS` → hora | `00:00:02` | Formato consistente. |

## Variable derivada (se calcula; no viene en los datos)

| Nombre | Cálculo | Ejemplo | Problemas detectados |
|---|---|---|---|
| `duracion_min` | (fecha + hora de arribo) − (fecha + hora de retiro), en minutos | `12.3` | Mediana de 11.7 a 12.5 min según el mes. Ninguna negativa ni cero. **4,425 viajes < 1 min** (0.010%); 17,078 > 3 h; **1,164 > 24 h** (0.003%); el más largo, 1,188 días, corresponde a los retiros fechados en 2022–2023. |

## Hallazgos generales

- **0 celdas vacías y 0 duplicados exactos** dentro de cada mes.
- Las fechas y horas tienen formato uniforme y todas se pueden leer.
- Los problemas encontrados aún **no se han corregido**. Su tratamiento se decide en `02_limpieza.ipynb` y se registra en `bitacora_decisiones.md`.
