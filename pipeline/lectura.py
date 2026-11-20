"""Lectura de un CSV mensual de viajes. Todo se lee como texto para no perder ceros ni esconder valores raros."""

COLUMNAS = ["genero", "edad", "bici", "est_retiro", "fecha_retiro", "hora_retiro",
            "est_arribo", "fecha_arribo", "hora_arribo"]
ENCABEZADO = ("Genero_Usuario,Edad_Usuario,Bici,Ciclo_Estacion_Retiro,Fecha_Retiro,Hora_Retiro,"
              "Ciclo_EstacionArribo,Fecha_Arribo,Hora_Arribo")


def normalizar_encabezado(linea):
    """Quita comillas y espacios (algunos meses traen 'Fecha Arribo' o encabezados entre comillas)."""
    return linea.strip().replace('"', "").replace(" ", "_")


def validar_encabezado(ruta):
    with open(ruta, encoding="utf8", newline="") as f:
        encabezado = normalizar_encabezado(f.readline())
    if encabezado != ENCABEZADO:
        raise ValueError(f"{ruta.name}: encabezado inesperado.\n  Se encontró: {encabezado}\n  Se esperaba: {ENCABEZADO}")


def contar_filas_csv(ruta):
    """Filas de datos del CSV (sin el encabezado), contadas por separado de DuckDB para validar la carga."""
    filas, ultimo = 0, b"\n"
    with open(ruta, "rb") as f:
        while bloque := f.read(1 << 24):
            filas += bloque.count(b"\n")
            ultimo = bloque[-1:]
    if ultimo != b"\n":
        filas += 1
    return filas - 1


def sql_lectura(ruta):
    """Fragmento SQL que lee el CSV como texto, con los nombres de columna cortos."""
    return f"read_csv('{ruta.as_posix()}', all_varchar=true, header=true, names={COLUMNAS}, strict_mode=true)"
