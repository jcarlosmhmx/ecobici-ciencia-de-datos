"""Capa silver: viajes con tipos correctos y reglas de limpieza aplicadas, con conteo de lo que se excluye y por qué."""
import duckdb

from . import config
from .catalogo import obtener_catalogo

# Orden de las reglas: un viaje se cuenta en la primera que incumple.
MOTIVOS = [
    ("fecha_invalida", "fecha u hora que no se pueden interpretar"),
    ("duracion_negativa", "el arribo es anterior al retiro"),
    ("menos_de_1_min", "dura menos de la duración mínima"),
    ("mas_de_24_h", "dura más de la duración máxima"),
    ("retiro_muy_antiguo", "retiro anterior al mes previo al del archivo"),
]


def construir_silver(cfg):
    """Genera datos/silver/viajes.parquet y devuelve (resumen por motivo, resumen por mes)."""
    import pandas as pd

    config.SILVER.mkdir(parents=True, exist_ok=True)
    config.PERFIL.mkdir(parents=True, exist_ok=True)
    estaciones, _ = obtener_catalogo(cfg)
    con = duckdb.connect()
    con.execute("CREATE TABLE cat(codigo VARCHAR)")
    con.executemany("INSERT INTO cat VALUES (?)", [(e["short_name"],) for e in estaciones])
    archivos_bronze = [(config.BRONZE / f"{mes}.parquet").as_posix() for mes in config.meses(cfg)]
    minimo = int(cfg["limpieza"]["duracion_minima_segundos"])
    maximo = int(cfg["limpieza"]["duracion_maxima_horas"]) * 3600

    con.execute(f"""
        CREATE VIEW clasificado AS
        WITH t AS (
          SELECT genero, TRY_CAST(TRY_CAST(edad AS DOUBLE) AS INTEGER) AS edad,
                 est_retiro, est_arribo, mes_archivo,
                 TRY_STRPTIME(fecha_retiro || ' ' || hora_retiro, '%d/%m/%Y %H:%M:%S') AS ts_retiro,
                 TRY_STRPTIME(fecha_arribo || ' ' || hora_arribo, '%d/%m/%Y %H:%M:%S') AS ts_arribo
          FROM read_parquet({archivos_bronze})
        ), d AS (SELECT *, date_diff('second', ts_retiro, ts_arribo) AS duracion_s FROM t)
        SELECT *, CASE
            WHEN ts_retiro IS NULL OR ts_arribo IS NULL THEN 'fecha_invalida'
            WHEN duracion_s < 0 THEN 'duracion_negativa'
            WHEN duracion_s < {minimo} THEN 'menos_de_1_min'
            WHEN duracion_s > {maximo} THEN 'mas_de_24_h'
            WHEN ts_retiro < date_trunc('month', strptime(mes_archivo, '%Y-%m')) - INTERVAL 1 MONTH
                 THEN 'retiro_muy_antiguo'
        END AS motivo_exclusion
        FROM d""")

    con.execute(f"""
        COPY (SELECT c.genero, c.edad, c.est_retiro, c.est_arribo, c.ts_retiro, c.ts_arribo, c.duracion_s, c.mes_archivo,
                     c.est_retiro IN (SELECT codigo FROM cat) AS retiro_en_catalogo,
                     c.est_arribo IN (SELECT codigo FROM cat) AS arribo_en_catalogo
              FROM clasificado c WHERE c.motivo_exclusion IS NULL)
        TO '{(config.SILVER / "viajes.parquet").as_posix()}' (FORMAT parquet)""")

    por_mes = con.execute("""
        SELECT mes_archivo AS mes, count(*) AS viajes_bronze,
               count(*) FILTER (WHERE motivo_exclusion IS NULL) AS viajes_silver,
               count(*) FILTER (WHERE motivo_exclusion IS NOT NULL) AS excluidos
        FROM clasificado GROUP BY 1 ORDER BY 1""").df()
    por_motivo = con.execute("""
        SELECT coalesce(motivo_exclusion, 'conservado') AS motivo, count(*) AS viajes
        FROM clasificado GROUP BY 1 ORDER BY 2 DESC""").df()
    total = por_motivo["viajes"].sum()
    por_motivo["porcentaje"] = (por_motivo["viajes"] / total * 100).round(3)

    en_silver = con.execute(
        f"SELECT count(*) FROM read_parquet('{(config.SILVER / 'viajes.parquet').as_posix()}')").fetchone()[0]
    assert en_silver == int(por_mes["viajes_silver"].sum()), "silver no coincide con el conteo de viajes conservados"
    assert int(por_mes["viajes_bronze"].sum()) == int(por_mes["viajes_silver"].sum() + por_mes["excluidos"].sum())
    por_motivo.to_csv(config.PERFIL / "limpieza_resumen.csv", index=False)
    return por_motivo, por_mes
