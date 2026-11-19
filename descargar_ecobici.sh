#!/bin/bash
# Descarga los viajes de Ecobici 2024-2025 desde https://ecobici.cdmx.gob.mx/datos-abiertos/
# Los nombres originales son inconsistentes; se guardan como AAAA-MM.csv en datos/raw/
cd "$(dirname "$0")"
mkdir -p datos/raw
B=https://ecobici.cdmx.gob.mx/wp-content/uploads
while read mes url; do
  if [ -s "datos/raw/$mes.csv" ]; then echo "Ya existe $mes, se omite"; continue; fi
  echo "Descargando $mes..."
  curl -fL --retry 3 -o "datos/raw/$mes.csv" "$url" || echo "ERROR en $mes"
done <<LISTA
2024-01 $B/2024/02/ecobici_2024_enero.csv
2024-02 $B/2024/03/2024-02.csv
2024-03 $B/2024/04/datos_abiertos_2024_03-1-1.csv
2024-04 $B/2024/05/datos_abiertos_2024_04.csv
2024-05 $B/2024/06/2024-05-1.csv
2024-06 $B/2024/07/2024-06.csv
2024-07 $B/2024/08/datos_abiertos_2024_07.csv
2024-08 $B/2024/09/2024-08.csv
2024-09 $B/2024/10/2024-09.csv
2024-10 $B/2024/11/2024-10.csv
2024-11 $B/2024/12/2024-11.csv
2024-12 $B/2025/01/2024-12.csv
2025-01 $B/2025/02/2025-01.csv
2025-02 $B/2025/03/2025-02.csv
2025-03 $B/2025/04/2025-03.csv
2025-04 $B/2025/05/2025-04.csv
2025-05 $B/2025/06/2025-05.csv
2025-06 $B/2025/07/2025-06.csv
2025-07 $B/2025/08/2025-07.csv
2025-08 $B/2025/09/2025-08.csv
2025-09 $B/2025/10/2025-09.csv
2025-10 $B/2025/11/2025-10-1.csv
2025-11 $B/2025/12/2025-11.csv
2025-12 $B/2026/01/2025-12.csv
LISTA
echo "Listo:"; ls -lh datos/raw
