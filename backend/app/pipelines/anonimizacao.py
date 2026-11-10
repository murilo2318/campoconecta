"""Anonimização local antes de qualquer gravação ou envio a LLM.

Cobre CPF, e-mail, telefone, placa e nomes introduzidos por frases como
"meu nome é Fulano". Não há NER: nomes soltos no texto podem passar. Essa é uma
limitação declarada. O texto original nunca é gravado.
"""
import re

_PADROES = [
    ("[CPF]", re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")),
    ("[EMAIL]", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("[TELEFONE]", re.compile(r"(?:\+?55\s?)?\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}\b")),
    ("[PLACA]", re.compile(r"\b[A-Za-z]{3}-?\d[A-Za-z0-9]\d{2}\b")),
]
_NOME_APOS_GATILHO = re.compile(
    r"\b((?i:meu nome é|me chamo|aqui é o|aqui é a|sou o|sou a))\s+"
    r"([A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wáéíóúâêôãõç]+(?:\s+(?:d[aeo]s?\s+)?[A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wáéíóúâêôãõç]+){0,3})"
)


def anonimizar(texto: str | None) -> str:
    if not texto:
        return ""
    saida = str(texto)
    for marcador, padrao in _PADROES:
        saida = padrao.sub(marcador, saida)
    saida = _NOME_APOS_GATILHO.sub(lambda m: f"{m.group(1)} [NOME]", saida)
    return saida
