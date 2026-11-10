"""Registro dos módulos das outras matérias.

Como encaixar um módulo de código: criar o arquivo indicado em `arquivo` com a função
`funcao`, respeitando o contrato em schemas/modulos.py. Sem o arquivo, o sistema usa o
stub e continua funcionando. Módulos de documento ou notebook ficam em entregas_externas/.
"""
import importlib
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class Slot:
    chave: str
    materia: str
    tipo: str                      # "endpoint" | "arquivos" | "documento"
    contrato: str                  # o que entra e o que sai
    arquivo: Optional[str] = None  # módulo Python esperado (só para endpoint)
    funcao: Optional[str] = None
    pasta: str = ""                # onde o responsável coloca a entrega


SLOTS: list[Slot] = [
    Slot("visao", "Visão Computacional", "endpoint",
         "imagem (bytes) -> VisaoSaida {tipo_dano, confianca, caixas[], latencia_ms}",
         "app.modulos.impl_visao", "analisar", "entregas_externas/visao/"),
    Slot("assistente", "Generative AI", "endpoint",
         "AssistenteEntrada {pergunta, historico} -> AssistenteSaida {resposta, fontes[], abstencao}",
         "app.modulos.impl_assistente", "perguntar", "entregas_externas/genai/"),
    Slot("corpus", "PLN (Fábrica de Corpus)", "arquivos",
         "gera corpus_texto/qa/chat/teste.jsonl; o texto puro pode alimentar o RAG do assistente",
         pasta="entregas_externas/pln/"),
    Slot("iot", "IoT (OuviAí)", "documento",
         "projeto Edge Impulse no celular; entrega são capturas, tabela de testes e vídeo",
         pasta="entregas_externas/iot/"),
    Slot("quantica", "Computação Quântica", "documento",
         "roadmap: gargalo real, capacidade quântica escolhida, ética, LGPD e ODS",
         pasta="entregas_externas/quantica/"),
    Slot("governanca", "Governança em IA e Business Analytics", "documento",
         "vídeo 5 a 7 min, relatório ABNT de 10 a 15 páginas, repositório; consolida todas as matérias",
         pasta="entregas_externas/governanca/"),
]


def carregar(slot: Slot) -> Optional[Callable]:
    """Devolve a função do módulo real, ou None se ainda não foi entregue."""
    if slot.tipo != "endpoint" or not slot.arquivo:
        return None
    try:
        return getattr(importlib.import_module(slot.arquivo), slot.funcao)
    except (ImportError, AttributeError):
        return None


def status() -> list[dict]:
    from pathlib import Path
    from .. import config
    saida = []
    for s in SLOTS:
        if s.tipo == "endpoint":
            integrado = carregar(s) is not None
            if integrado:                    # o módulo pode declarar que ainda não tem dados
                try:
                    verificar = getattr(importlib.import_module(s.arquivo), "disponivel", None)
                    integrado = bool(verificar()) if verificar else True
                except Exception:
                    integrado = False
        else:
            pasta = Path(config.RAIZ) / s.pasta
            integrado = pasta.is_dir() and any(p for p in pasta.iterdir() if p.name != "LEIAME.md")
        saida.append({"chave": s.chave, "materia": s.materia, "tipo": s.tipo,
                      "contrato": s.contrato, "pasta": s.pasta or s.arquivo,
                      "integrado": integrado})
    return saida
