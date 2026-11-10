"""Vocabulário do problema em um lugar só.

Tema: apoio ao pequeno produtor rural (CampoConecta). Para trocar o tema,
basta alterar esta lista e as regras em pipelines/triagem.py.
"""
from typing import Literal

Tipo = Literal["praga_doenca", "clima_extremo", "agua_irrigacao", "preco_mercado", "credito_seguro", "outro"]
Urgencia = Literal["baixa", "media", "alta", "critica"]
Status = Literal["pendente", "aprovado", "rejeitado"]

TIPOS: tuple[str, ...] = ("praga_doenca", "clima_extremo", "agua_irrigacao", "preco_mercado", "credito_seguro", "outro")
URGENCIAS: tuple[str, ...] = ("baixa", "media", "alta", "critica")

# Órgão sugerido para cada tipo. É uma tabela simples, editável.
ENCAMINHAMENTO = {
    "praga_doenca": "Defesa Agropecuária e Assistência Técnica",
    "clima_extremo": "Defesa Civil e Assistência Técnica",
    "agua_irrigacao": "Secretaria de Agricultura (recursos hídricos)",
    "preco_mercado": "Cooperativa e Secretaria de Abastecimento",
    "credito_seguro": "Banco ou cooperativa de crédito e Extensão Rural",
    "outro": "Ouvidoria",
}
