"""Mede a triagem em conjuntos rotulados de data/.
Uso: python avaliar.py [casos_teste|casos_novos|casos_novos_2]   (usa o LLM se estiver configurado, senão só as regras)"""
import sys
from pathlib import Path

import pandas as pd

from app.pipelines.triagem import triar, triar_por_regras

ARQ = sys.argv[1] if len(sys.argv) > 1 else "casos_teste"
df = pd.read_csv(Path(__file__).resolve().parents[1] / "data" / f"{ARQ}.csv")
for nome, f in (("regras", triar_por_regras), ("triar (LLM se houver, senão regras)", triar)):
    pred = [f(t) for t in df["texto"]]
    df["tipo_obtido"] = [p.tipo for p in pred]
    df["urg_obtida"] = [p.urgencia for p in pred]
    acerto_tipo = (df["tipo_obtido"] == df["tipo_esperado"]).mean()
    acerto_urg = (df["urg_obtida"] == df["urgencia_esperada"]).mean()
    print(f"\n== {nome} | n={len(df)} | acerto tipo={acerto_tipo:.0%} | acerto urgência={acerto_urg:.0%}")
    erros = df[(df["tipo_obtido"] != df["tipo_esperado"]) | (df["urg_obtida"] != df["urgencia_esperada"])]
    print(erros[["texto", "tipo_esperado", "tipo_obtido", "urgencia_esperada", "urg_obtida"]].to_string(index=False))
    print("\nMatriz de confusão (urgência):")
    print(pd.crosstab(df["urgencia_esperada"], df["urg_obtida"]))
