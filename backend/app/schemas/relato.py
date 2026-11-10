"""Modelos Pydantic de entrada e saída. A validação acontece aqui, no back-end."""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from ..dominio import Status, Tipo, Urgencia


class RelatoEntrada(BaseModel):
    descricao: str = Field(min_length=10, max_length=1000)
    cep: Optional[str] = Field(default=None, description="8 dígitos, com ou sem hífen")

    @field_validator("descricao")
    @classmethod
    def _descricao_nao_vazia(cls, v: str) -> str:
        v = " ".join(v.split())
        if len(v) < 10:
            raise ValueError("Descreva o problema com pelo menos 10 caracteres.")
        return v

    @field_validator("cep")
    @classmethod
    def _cep_valido(cls, v: Optional[str]) -> Optional[str]:
        if v is None or not v.strip():
            return None
        digitos = "".join(c for c in v if c.isdigit())
        if len(digitos) != 8:
            raise ValueError("CEP deve ter 8 dígitos.")
        return digitos


class Triagem(BaseModel):
    """Saída estruturada da IA. É o que o LLM precisa devolver, e não texto livre."""
    tipo: Tipo
    urgencia: Urgencia
    resumo: str = Field(max_length=200)
    encaminhar_para: str
    fonte: Literal["llm", "regras"] = "regras"


class RelatoSaida(BaseModel):
    id: str
    origem: str
    criado_em: datetime
    descricao_anon: str
    cep: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    triagem: Triagem
    status: Status = "pendente"
    comentario_gestor: Optional[str] = None
    feedback: Optional[Literal["util", "incorreta"]] = None
    revisao_humana: bool = False


class Decisao(BaseModel):
    status: Literal["aprovado", "rejeitado"]
    comentario: Optional[str] = Field(default=None, max_length=300)


class Feedback(BaseModel):
    avaliacao: Literal["util", "incorreta"]
