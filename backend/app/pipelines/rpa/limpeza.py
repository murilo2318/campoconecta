"""Etapa de limpeza com Pandas. Cada linha rejeitada vai para a quarentena com o motivo."""
import re

import pandas as pd

COLUNAS_OBRIGATORIAS = ["id_relato", "data", "cep", "descricao"]


def carregar_e_limpar(caminho_csv: str) -> tuple[pd.DataFrame, list[dict]]:
    """Devolve (linhas válidas, rejeitados). Arquivo ausente ou sem colunas levanta
    FileNotFoundError ou ValueError, que o robô trata como falha da execução inteira."""
    df = pd.read_csv(caminho_csv, dtype=str, keep_default_na=False)
    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas ausentes no CSV: {faltando}")

    rejeitados: list[dict] = []
    validos = []
    vistos: set[str] = set()
    for _, linha in df.iterrows():
        rid = linha["id_relato"].strip()
        motivo = None
        if not rid:
            motivo = "id vazio"
        elif rid in vistos:
            motivo = "id duplicado"
        else:
            descricao = " ".join(linha["descricao"].split())
            data = pd.to_datetime(linha["data"], errors="coerce", dayfirst=False)
            if len(descricao) < 10:
                motivo = "descrição vazia ou curta"
            elif pd.isna(data):
                motivo = "data inválida"
        if motivo:
            rejeitados.append({**linha.to_dict(), "motivo": motivo})
            continue
        vistos.add(rid)
        cep = re.sub(r"\D", "", linha["cep"])
        validos.append({
            "id_relato": rid, "data": data.isoformat(timespec="seconds"),
            "cep": cep if len(cep) == 8 else None, "descricao": descricao,
        })
    return pd.DataFrame(validos, columns=["id_relato", "data", "cep", "descricao"]), rejeitados
