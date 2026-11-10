"""Passo comum à API e ao robô: anonimiza, enriquece pelo CEP, triagem e monta o registro."""
from datetime import datetime, timezone

from ..providers import viacep
from .anonimizacao import anonimizar
from .triagem import triar


def processar_relato(rel_id: str, origem: str, descricao: str, cep: str | None,
                     criado_em: str | None = None) -> dict:
    descricao_anon = anonimizar(descricao)
    local = viacep.buscar_cep(cep) or {}
    tri = triar(descricao_anon)
    # Revisão humana: casos críticos; urgência alta triada só por regras; e "outro" triado só por regras,
    # porque as regras não entenderam o relato e a urgência baixa pode estar errada.
    revisao = tri.urgencia == "critica" or (
        tri.fonte == "regras" and (tri.urgencia == "alta" or tri.tipo == "outro"))
    return {
        "id": rel_id, "origem": origem,
        "criado_em": criado_em or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "descricao_anon": descricao_anon, "cep": cep,
        "cidade": local.get("cidade"), "uf": local.get("uf"),
        "tipo": tri.tipo, "urgencia": tri.urgencia, "resumo": tri.resumo,
        "encaminhar_para": tri.encaminhar_para, "fonte_triagem": tri.fonte,
        "revisao_humana": revisao,
    }
