"""Triagem de relatos: LLM com saída validada por Pydantic e regras como caminho seguro."""
import logging
import re
import unicodedata

from pydantic import ValidationError

from .. import dominio
from ..providers import llm
from ..schemas.relato import Triagem

log = logging.getLogger("citizentech.triagem")


def _norm(t: str) -> str:
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


# Palavras-chave (expressões regulares sobre texto sem acento) e sinais de urgência.
# O início de cada padrão respeita limite de palavra, então "seca" não casa com "secretaria".
_TIPOS = {
    "credito_seguro": [r"credito", r"financiamento", r"pronaf", r"seguro", r"emprestimo", r"divida", r"proagro",
                       r"\bbanco\b", r"parcela", r"custeio"],
    "clima_extremo": [r"geada", r"granizo", r"estiagem", r"\bseca\b", r"vendaval", r"ventania", r"\bvento\b",
                      r"tempestade", r"queimada", r"incendio", r"\bfogo\b", r"chamas", r"onda de calor",
                      r"falta de chuva", r"nao cai (uma )?gota", r"sem chuva", r"enchente", r"chuva forte", r"\bfrio\b"],
    "praga_doenca": [r"praga", r"lagarta", r"ferrugem", r"pulga", r"gafanhoto", r"doenca", r"doente", r"fungo",
                     r"mofo", r"broca", r"cochonilha", r"carrapato", r"aftosa", r"mastite", r"pulgao",
                     r"bicharada", r"\binseto", r"\bubere", r"furando"],
    "agua_irrigacao": [r"irriga", r"\bpoco\b", r"bomba", r"acude", r"nascente", r"represa", r"cisterna",
                       r"falta de agua", r"sem agua", r"\bmina\b", r"\bcano\b", r"\bcorrego\b"],
    "preco_mercado": [r"preco", r"atravessador", r"\bvend", r"mercado", r"comprador", r"pra comprar", r"frete",
                      r"escoar", r"escoamento", r"feira", r"cooperativa"],
}
_ORDEM = ("credito_seguro", "clima_extremo", "praga_doenca", "agua_irrigacao", "preco_mercado")
# Perda grave ou risco imediato à saúde: vai para revisão humana.
_CRITICOS = [r"morrendo", r"morreu", r"mortandade", r"intoxic", r"envenen", r"passou mal", r"vomit", r"desmai",
             r"queimada", r"incendio", r"\bfogo\b", r"chamas", r"perda total", r"perdi toda", r"perdi quase tudo",
             r"alastrando", r"se espalhando", r"destruiu", r"toda a lavoura", r"derrubou o galpao"]
_ALTOS = [r"perdendo", r"vence", r"prazo", r"secando", r"sem agua", r"nao consigo vender", r"sem comprador",
          r"ninguem pra comprar", r"quebrou", r"estourou", r"doente", r"geada", r"inchad", r"\bpus\b",
          r"perdi a safra", r"nao tenho como pagar", r"atolou", r"nao entra", r"secou", r"fechou", r"folhas pretas"]
# Pedido de informação, sem problema em andamento.
_BAIXOS = [r"queria saber", r"como pedir", r"vai ter", r"onde vende", r"informacao", r"duvida"]


def _casa(padroes, t: str) -> bool:
    return any(re.search(p, t) for p in padroes)


def triar_por_regras(texto: str) -> Triagem:
    t = _norm(texto)
    tipo = "outro"
    for nome in _ORDEM:
        if _casa(_TIPOS[nome], t):
            tipo = nome
            break
    if _casa(_CRITICOS, t):
        urg = "critica"
    elif _casa(_ALTOS, t):
        urg = "alta"
    elif _casa(_BAIXOS, t):
        urg = "baixa"
    elif tipo != "outro":
        urg = "media"
    else:
        urg = "baixa"
    resumo = " ".join(texto.split())[:197] + ("..." if len(texto) > 197 else "")
    return Triagem(tipo=tipo, urgencia=urg, resumo=resumo,
                   encaminhar_para=dominio.ENCAMINHAMENTO[tipo], fonte="regras")


def triar(texto_anonimizado: str) -> Triagem:
    """Tenta o LLM; resposta vazia, inválida ou erro de rede caem nas regras."""
    try:
        bruto = llm.classificar(texto_anonimizado)
        tipo = bruto.get("tipo")
        t = Triagem(
            tipo=tipo, urgencia=bruto.get("urgencia"),
            resumo=str(bruto.get("resumo", ""))[:200] or texto_anonimizado[:200],
            encaminhar_para=dominio.ENCAMINHAMENTO.get(tipo, "Ouvidoria"), fonte="llm",
        )
        return t
    except llm.LLMIndisponivel as e:
        log.info("LLM indisponível, usando regras: %s", e)
    except (ValidationError, AttributeError, TypeError) as e:
        log.warning("Resposta do LLM inválida, usando regras: %s", type(e).__name__)
    return triar_por_regras(texto_anonimizado)
