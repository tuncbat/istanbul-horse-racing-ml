import pandas as pd
import numpy as np
from pathlib import Path

ROOT      = Path(__file__).resolve().parent.parent
RAW_DIR   = ROOT / "data" / "raw"
PROC_DIR  = ROOT / "data" / "processed"
PROC_DIR.mkdir(exist_ok=True)

latest = max(RAW_DIR.glob("*_program.csv"), key=lambda x: x.stat().st_mtime)
df = pd.read_csv(latest, sep=",", encoding="utf-8")
df = df[pd.to_numeric(df["At No"], errors="coerce").notnull()].copy()

def parse_last6(s):
    if pd.isna(s): return []
    return str(s).replace("Ç","1").replace("S","2").replace("K","3").replace("-","0").split()

df["last6_list"] = df["Son 6 Yarış"].apply(parse_last6)
df["win5"]       = df["last6_list"].apply(lambda x: x[:5].count("1") / 5 if len(x) >= 5 else np.nan)
df["avg_finish3"]= df["last6_list"].apply(lambda x: sum(int(i) if i in "123" else 4 for i in x[:3]) / 3 if len(x) >= 3 else np.nan)
df["kilo_num"]   = df["Kilo"].astype(str).str.replace(",",".").astype(float)
df["kilo_delta"] = df["kilo_num"] - df["kilo_num"].mean()

out = df[["At No","At İsmi","Yaş","AGF","win5","avg_finish3","kilo_delta"]]
out.to_csv(PROC_DIR / f"{latest.stem}_features.csv", index=False, encoding="utf-8")
print("✅ features oluşturuldu:", PROC_DIR / f"{latest.stem}_features.csv")
