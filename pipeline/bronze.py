"""Capa bronze: cada CSV mensual pasa a Parquet sin cambiar ningún valor (todo texto), con el mes de origen."""
import duckdb

from . import config, lectura


def construir_bronze(cfg):
    """Convierte los CSV de la ventana a Parquet y valida el conteo de cada mes contra el CSV.

    Devuelve una lista de diccionarios (uno por mes). Detiene el proceso si algún conteo no coincide.
    """
    config.BRONZE.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    resultado = []
    for mes in config.meses(cfg):
        csv = config.RAW / f"{mes}.csv"
        lectura.validar_encabezado(csv)
        filas_csv = lectura.contar_filas_csv(csv)
        destino = config.BRONZE / f"{mes}.parquet"
        con.execute(
            f"COPY (SELECT *, '{mes}' AS mes_archivo FROM {lectura.sql_lectura(csv)}) "
            f"TO '{destino.as_posix()}' (FORMAT parquet)"
        )
        filas_bronze = con.execute(f"SELECT count(*) FROM read_parquet('{destino.as_posix()}')").fetchone()[0]
        resultado.append({"mes": mes, "filas_csv": filas_csv, "filas_bronze": filas_bronze,
                          "coincide": filas_csv == filas_bronze})
    malos = [r["mes"] for r in resultado if not r["coincide"]]
    if malos:
        raise AssertionError(f"El conteo de bronze no coincide con el CSV en: {malos}")
    return resultado
