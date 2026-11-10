"""Robô em lote: CSV -> limpeza -> CEP -> triagem -> SQL -> e-mail -> relatório de execução.

Princípios: uma linha ruim nunca derruba o lote, tudo é registrado em log, o que o robô
não resolve vai para a quarentena e para a fila de revisão humana, e rodar duas vezes
não duplica nada.
"""
import json
import logging
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from ... import config
from ...providers import db
from ..processar import processar_relato
from .limpeza import carregar_e_limpar
from .relatorio_email import enviar_ou_salvar, montar_email

log = logging.getLogger("citizentech.robo")


def configurar_log() -> None:
    Path(config.LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
    raiz = logging.getLogger("citizentech")
    if not any(isinstance(h, logging.FileHandler) for h in raiz.handlers):
        h = logging.FileHandler(config.LOG_PATH, encoding="utf-8")
        h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        raiz.addHandler(h)
        raiz.addHandler(logging.StreamHandler())
        raiz.setLevel(logging.INFO)


def executar(csv_path: str | None = None, db_path: str | None = None,
             relatorio_path: str = "relatorio_execucao.json", enviar_email: bool = True) -> dict:
    configurar_log()
    csv_path = csv_path or config.CSV_EXEMPLO
    inicio = time.perf_counter()
    rel = {"inicio": datetime.now().isoformat(timespec="seconds"), "csv": csv_path,
           "lidos": 0, "processados": 0, "rejeitados": 0, "falhas_linha": 0,
           "via_llm": 0, "via_regras": 0, "cep_resolvido": 0, "revisao_humana": 0,
           "email": None, "status": "ok", "erro_fatal": None, "pendencias_para_humano": []}

    try:
        df, rejeitados = carregar_e_limpar(csv_path)
    except (FileNotFoundError, ValueError, pd.errors.ParserError, pd.errors.EmptyDataError) as e:
        log.error("Falha ao carregar o CSV: %s", e)
        rel.update(status="falha", erro_fatal=f"{type(e).__name__}: {e}")
        return _fechar(rel, inicio, relatorio_path)

    rel["lidos"] = len(df) + len(rejeitados)
    rel["rejeitados"] = len(rejeitados)
    if rejeitados:
        quarentena = Path(config.OUTBOX_DIR) / "quarentena.csv"
        quarentena.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rejeitados).to_csv(quarentena, index=False)
        rel["pendencias_para_humano"].append(f"{len(rejeitados)} linha(s) em {quarentena}")

    with db.conexao(db_path) as conn:
        for _, linha in df.iterrows():
            try:
                cep = linha["cep"] if isinstance(linha["cep"], str) else None  # Pandas converte None em NaN
                reg = processar_relato(f"csv-{linha['id_relato']}", "csv", linha["descricao"],
                                       cep, criado_em=linha["data"])
                db.upsert_relato(conn, reg)
                rel["processados"] += 1
                rel["via_llm" if reg["fonte_triagem"] == "llm" else "via_regras"] += 1
                rel["cep_resolvido"] += int(bool(reg["cidade"]))
                rel["revisao_humana"] += int(reg["revisao_humana"])
            except Exception as e:  # uma linha ruim não interrompe o lote
                rel["falhas_linha"] += 1
                log.error("Falha na linha %s: %s", linha["id_relato"], e)
        aprovados = db.listar(conn, status="aprovado")

    if enviar_email:
        try:
            rel["email"] = enviar_ou_salvar(montar_email(aprovados))
        except Exception as e:
            rel["email"] = f"falha: {type(e).__name__}"
            log.error("Falha ao montar ou enviar e-mail: %s", e)
    return _fechar(rel, inicio, relatorio_path)


def _fechar(rel: dict, inicio: float, relatorio_path: str) -> dict:
    rel["duracao_s"] = round(time.perf_counter() - inicio, 3)
    if rel["processados"]:
        rel["tempo_medio_por_relato_s"] = round(rel["duracao_s"] / rel["processados"], 4)
    Path(relatorio_path).write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Execução concluída: %s", {k: rel[k] for k in ("status", "processados", "rejeitados", "falhas_linha")})
    return rel
