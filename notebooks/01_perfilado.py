"""Perfilado de calidad de los CSV crudos de Ecobici (fase Prepare).
Uso: python3 01_perfilado.py 2024-01 2024-02 ...   -> escribe datos/perfil/<mes>.json"""
import sys, json, re, pandas as pd
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent
RAW, OUT = BASE/"datos/raw", BASE/"datos/perfil"
COLS = ["genero","edad","bici","est_retiro","fecha_retiro","hora_retiro","est_arribo","fecha_arribo","hora_arribo"]
for mes in sys.argv[1:]:
    df = pd.read_csv(RAW/f"{mes}.csv", dtype=str, header=0, names=COLS, keep_default_na=False)
    p = {"mes": mes, "filas": len(df)}
    p["vacios"] = {c: int((df[c].str.strip()=="").sum()) for c in COLS}
    p["genero"] = df["genero"].value_counts().to_dict()
    edad = pd.to_numeric(df["edad"], errors="coerce")
    p["edad"] = {"no_numerica": int(edad.isna().sum()), "min": float(edad.min()), "max": float(edad.max()),
                 "mediana": float(edad.median()), "menor_16": int((edad<16).sum()), "mayor_80": int((edad>80).sum())}
    fmt = {}
    for c in ["fecha_retiro","fecha_arribo"]:
        s = df[c]
        fmt[c] = {"dd/mm/aaaa": int(s.str.fullmatch(r"\d{2}/\d{2}/\d{4}").sum()),
                  "aaaa-mm-dd": int(s.str.fullmatch(r"\d{4}-\d{2}-\d{2}").sum())}
        fmt[c]["otro"] = len(s) - sum(fmt[c].values())
        fmt[c]["ejemplo_otro"] = s[~s.str.fullmatch(r"\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2}")].head(3).tolist()
    p["formato_fecha"] = fmt
    def dt(f, h):
        x = f + " " + h
        out = pd.to_datetime(x, format="%d/%m/%Y %H:%M:%S", errors="coerce")
        m = out.isna()
        if m.any():  # respaldo para formatos distintos (p.ej. aaaa-mm-dd o sin segundos)
            out[m] = pd.to_datetime(x[m], format="mixed", dayfirst=True, errors="coerce")
        return out
    r, a = dt(df.fecha_retiro, df.hora_retiro), dt(df.fecha_arribo, df.hora_arribo)
    dur = (a - r).dt.total_seconds()/60
    p["fechas"] = {"retiro_min": str(r.min()), "retiro_max": str(r.max()), "arribo_min": str(a.min()), "arribo_max": str(a.max()),
                   "no_parseables": int((r.isna()|a.isna()).sum())}
    p["duracion_min"] = {"negativa": int((dur<0).sum()), "menor_1min": int(((dur>=0)&(dur<1)).sum()),
                         "mayor_3h": int((dur>180).sum()), "mayor_24h": int((dur>1440).sum()), "mediana": float(dur.median())}
    p["misma_estacion"] = int((df.est_retiro==df.est_arribo).sum())
    for c in ["est_retiro","est_arribo"]:
        p[c] = {"unicas": int(df[c].nunique()), "no_numericas": df[c][~df[c].str.fullmatch(r"\d+")].value_counts().head(5).to_dict()}
    p["duplicados"] = int(df.duplicated().sum())
    (OUT/f"{mes}.json").write_text(json.dumps(p, ensure_ascii=False, indent=1))
    print(mes, p["filas"], "ok", flush=True)
