"""Contratos dos módulos que outras matérias podem encaixar.

Quem for entregar um módulo só precisa respeitar estas entradas e saídas.
"""
from typing import Optional

from pydantic import BaseModel, Field


class Caixa(BaseModel):
    classe: str
    confianca: float = Field(ge=0, le=1)
    x: float
    y: float
    largura: float
    altura: float


class VisaoSaida(BaseModel):
    disponivel: bool = True
    tipo_dano: Optional[str] = None
    confianca: Optional[float] = Field(default=None, ge=0, le=1)
    caixas: list[Caixa] = []
    latencia_ms: Optional[float] = None
    mensagem: Optional[str] = None


class AssistenteEntrada(BaseModel):
    pergunta: str = Field(min_length=3, max_length=500)
    historico: list[dict] = []


class Fonte(BaseModel):
    doc_id: Optional[str] = None
    titulo: str
    trecho: str
    url: Optional[str] = None


class AssistenteSaida(BaseModel):
    disponivel: bool = True
    resposta: Optional[str] = None
    fontes: list[Fonte] = []
    abstencao: bool = False
    mensagem: Optional[str] = None
