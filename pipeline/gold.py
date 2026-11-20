"""Capa gold: tablas agregadas pequeñas para el análisis (saldo por estación, persistencia, perfil horario, corredor)."""
from datetime import date

import duckdb
import pandas as pd

from . import config
from .catalogo import obtener_catalogo


def _primer_dia(mes):
    a, m = map(int, mes.split("-"))
    return date(a, m, 1)


def _primer_dia_siguiente(mes):
    a, m = map(int, mes.split("-"))
    return date(a + 1, 1, 1) if m == 12 else date(a, m + 1, 1)


def construir_gold(cfg):
    """Genera las tablas de datos/gold/ y devuelve un DataFrame con las validaciones de consistencia."""
    config.GOLD.mkdir(parents=True, exist_ok=True)
    a = cfg["analisis"]
    h0, h1, umbral = int(a["hora_inicio"]), int(a["hora_fin"]), int(a["umbral_persistencia_bicis"])
    silver = (config.SILVER / "viajes.parquet").as_posix()
    con = duckdb.connect()

    # Catálogo de estaciones (la capacidad es la ACTUAL, no la de 2024-2026)
    estaciones, _ = obtener_catalogo(cfg)
    con.execute("CREATE TABLE estaciones(codigo VARCHAR, nombre VARCHAR, lat DOUBLE, lon DOUBLE, capacidad INTEGER)")
    con.executemany("INSERT INTO estaciones VALUES (?,?,?,?,?)",
                    [(e["short_name"], e["name"], e["lat"], e["lon"], e["capacity"]) for e in estaciones])

    # Periodos de comparación (el fin es exclusivo)
    con.execute("CREATE TABLE periodos(nombre VARCHAR, ini DATE, fin DATE)")
    con.executemany("INSERT INTO periodos VALUES (?,?,?)",
                    [(p["nombre"], _primer_dia(p["desde"]), _primer_dia_siguiente(p["hasta"])) for p in cfg["periodos"]])

    # Días de descanso obligatorio (festivos oficiales): no cuentan como días laborables
    con.execute("CREATE TABLE festivos(dia DATE)")
    con.executemany("INSERT INTO festivos VALUES (?)", [(f,) for f in a["festivos"]])

    # Un registro por movimiento (salida = -1, llegada = +1), solo días laborables (lunes a viernes, sin festivos)
    con.execute(f"""
        CREATE VIEW ev AS
        SELECT p.nombre AS periodo, e.est, e.ts, e.d, CAST(e.ts AS DATE) AS dia, hour(e.ts) AS hora
        FROM (SELECT est_retiro AS est, ts_retiro AS ts, -1 AS d FROM read_parquet('{silver}')
              UNION ALL
              SELECT est_arribo, ts_arribo, 1 FROM read_parquet('{silver}')) e
        JOIN periodos p ON CAST(e.ts AS DATE) >= p.ini AND CAST(e.ts AS DATE) < p.fin
        WHERE dayofweek(e.ts) BETWEEN 1 AND 5 AND CAST(e.ts AS DATE) NOT IN (SELECT dia FROM festivos)""")
    con.execute("CREATE TABLE dias AS SELECT periodo, count(DISTINCT dia) AS n_dias FROM ev GROUP BY 1")
    # Días en que cada estación tuvo actividad (al menos un viaje, a cualquier hora). Si estuvo cerrada o sin servicio ese día,
    # no se cuenta como un día con saldo 0: no hay observación.
    con.execute("CREATE TABLE dias_est AS SELECT periodo, est, count(DISTINCT dia) AS n_dias FROM ev GROUP BY 1, 2")

    # Saldo de la franja de la mañana, por estación y día de actividad. Si la estación operó ese día pero no hubo movimiento
    # en la franja, el saldo es 0.
    con.execute(f"""
        CREATE TABLE mov AS
        SELECT *, SUM(d) OVER (PARTITION BY periodo, est, dia ORDER BY ts, d ROWS UNBOUNDED PRECEDING) AS acum
        FROM ev WHERE hora BETWEEN {h0} AND {h1}""")
    con.execute("""
        CREATE TABLE manana_estacion_dia AS
        WITH grilla AS (
          SELECT DISTINCT periodo, est, dia FROM ev
        ), agg AS (
          SELECT periodo, est, dia,
                 count(*) FILTER (WHERE d = -1) AS salidas, count(*) FILTER (WHERE d = 1) AS llegadas,
                 sum(d) AS saldo,
                 -least(0, min(acum)) AS bicis_necesarias,      -- bicis que debía haber a las 7:00 para no vaciarse
                 greatest(0, max(acum)) AS espacios_necesarios  -- espacios libres que debía haber para no llenarse
          FROM mov GROUP BY 1, 2, 3)
        SELECT g.periodo, g.est, g.dia,
               coalesce(a.salidas, 0) AS salidas, coalesce(a.llegadas, 0) AS llegadas, coalesce(a.saldo, 0) AS saldo,
               coalesce(a.bicis_necesarias, 0) AS bicis_necesarias, coalesce(a.espacios_necesarios, 0) AS espacios_necesarios
        FROM grilla g LEFT JOIN agg a USING (periodo, est, dia)""")

    con.execute(f"""
        CREATE TABLE persistencia_estacion AS
        SELECT m.periodo, m.est, e.nombre, e.capacidad,
               count(*) AS dias_laborables,
               any_value(n.n_dias) - count(*) AS dias_sin_actividad,
               round(avg(m.saldo), 1) AS saldo_medio,
               round(avg((m.saldo >= {umbral})::INT) * 100, 1) AS pct_dias_gana,
               round(avg((m.saldo <= -{umbral})::INT) * 100, 1) AS pct_dias_pierde,
               round(avg(m.bicis_necesarias), 1) AS bicis_necesarias_media,
               max(m.bicis_necesarias) AS bicis_necesarias_max,
               round(avg(m.espacios_necesarios), 1) AS espacios_necesarios_media,
               max(m.espacios_necesarios) AS espacios_necesarios_max,
               round(avg(m.saldo) / nullif(e.capacidad, 0), 2) AS presion
        FROM manana_estacion_dia m
        LEFT JOIN estaciones e ON e.codigo = m.est
        JOIN dias n ON n.periodo = m.periodo
        GROUP BY m.periodo, m.est, e.nombre, e.capacidad""")

    con.execute("""
        CREATE TABLE perfil_horario_estacion AS
        SELECT ev.periodo, ev.est, ev.hora,
               round(count(*) FILTER (WHERE ev.d = -1) / any_value(n.n_dias), 2) AS salidas_por_dia,
               round(count(*) FILTER (WHERE ev.d = 1) / any_value(n.n_dias), 2) AS llegadas_por_dia
        FROM ev JOIN dias_est n USING (periodo, est) GROUP BY ev.periodo, ev.est, ev.hora""")

    origenes = ", ".join(f"'{o}'" for o in a["origenes_buenavista"])
    con.execute(f"""
        CREATE TABLE od_corredor AS
        SELECT p.nombre AS periodo, s.est_retiro AS origen, s.est_arribo AS destino, count(*) AS viajes,
               round(count(*) / any_value(n.n_dias), 1) AS viajes_por_dia
        FROM read_parquet('{silver}') s
        JOIN periodos p ON CAST(s.ts_retiro AS DATE) >= p.ini AND CAST(s.ts_retiro AS DATE) < p.fin
        JOIN dias_est n ON n.periodo = p.nombre AND n.est = s.est_retiro
        WHERE dayofweek(s.ts_retiro) BETWEEN 1 AND 5 AND hour(s.ts_retiro) BETWEEN {h0} AND {h1}
          AND CAST(s.ts_retiro AS DATE) NOT IN (SELECT dia FROM festivos)
          AND s.est_retiro IN ({origenes})
        GROUP BY 1, 2, 3""")

    # Validación independiente: se recuentan los viajes directamente de silver y se comparan con las sumas de gold
    esperado = con.execute(f"""
        SELECT count(*) FILTER (WHERE hour(s.ts_retiro) BETWEEN {h0} AND {h1}
                                  AND dayofweek(s.ts_retiro) BETWEEN 1 AND 5
                                  AND CAST(s.ts_retiro AS DATE) NOT IN (SELECT dia FROM festivos)
                                  AND CAST(s.ts_retiro AS DATE) >= (SELECT min(ini) FROM periodos)
                                  AND CAST(s.ts_retiro AS DATE) < (SELECT max(fin) FROM periodos)),
               count(*) FILTER (WHERE hour(s.ts_arribo) BETWEEN {h0} AND {h1}
                                  AND dayofweek(s.ts_arribo) BETWEEN 1 AND 5
                                  AND CAST(s.ts_arribo AS DATE) NOT IN (SELECT dia FROM festivos)
                                  AND CAST(s.ts_arribo AS DATE) >= (SELECT min(ini) FROM periodos)
                                  AND CAST(s.ts_arribo AS DATE) < (SELECT max(fin) FROM periodos))
        FROM read_parquet('{silver}') s""").fetchone()
    obtenido = con.execute("SELECT sum(salidas), sum(llegadas) FROM manana_estacion_dia").fetchone()
    validaciones = pd.DataFrame([
        {"comprobación": "salidas de la mañana: gold = recuento directo de silver", "gold": int(obtenido[0]),
         "silver": int(esperado[0]), "coincide": int(obtenido[0]) == int(esperado[0])},
        {"comprobación": "llegadas de la mañana: gold = recuento directo de silver", "gold": int(obtenido[1]),
         "silver": int(esperado[1]), "coincide": int(obtenido[1]) == int(esperado[1])},
    ])
    if not validaciones["coincide"].all():
        raise AssertionError(f"Gold no cuadra con silver:\n{validaciones}")

    for tabla in ["estaciones", "manana_estacion_dia", "persistencia_estacion", "perfil_horario_estacion", "od_corredor"]:
        con.execute(f"COPY {tabla} TO '{(config.GOLD / (tabla + '.parquet')).as_posix()}' (FORMAT parquet)")
    return validaciones
