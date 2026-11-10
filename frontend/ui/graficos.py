"""Gráficos Plotly alimentados pelo histórico real de relatos."""
import pandas as pd
import plotly.express as px

from .badges import ESTILO, TIPO_ROTULO

ORDEM = ["baixa", "media", "alta", "critica"]


def _df(relatos: list[dict]) -> pd.DataFrame:
    return pd.DataFrame([{
        "criado_em": pd.to_datetime(r["criado_em"], format="mixed", utc=True, errors="coerce"),
        "tipo": TIPO_ROTULO.get(r["triagem"]["tipo"], r["triagem"]["tipo"]),
        "urgencia": r["triagem"]["urgencia"], "cidade": r.get("cidade") or "Não identificada",
    } for r in relatos])


def urgencia_por_tipo(relatos: list[dict]):
    df = _df(relatos)
    contagem = df.groupby(["tipo", "urgencia"]).size().reset_index(name="relatos")
    fig = px.bar(contagem, x="tipo", y="relatos", color="urgencia", barmode="stack",
                 category_orders={"urgencia": ORDEM},
                 color_discrete_map={k: v[2] for k, v in ESTILO.items()},
                 labels={"tipo": "Tipo de ocorrência", "relatos": "Quantidade", "urgencia": "Urgência"},
                 title="Relatos por tipo e urgência")
    return fig


def linha_do_tempo(relatos: list[dict]):
    df = _df(relatos).dropna(subset=["criado_em"])
    por_dia = df.groupby(df["criado_em"].dt.date).size().reset_index(name="relatos")
    por_dia.columns = ["dia", "relatos"]
    return px.line(por_dia, x="dia", y="relatos", markers=True, title="Relatos por dia",
                   labels={"dia": "Dia", "relatos": "Quantidade"})
