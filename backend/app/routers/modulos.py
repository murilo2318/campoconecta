"""Endpoints dos módulos abertos. Sem módulo real, devolvem o stub (disponivel=false)."""
import time

from fastapi import APIRouter, File, UploadFile

from ..modulos import registro
from ..schemas.modulos import AssistenteEntrada, AssistenteSaida, VisaoSaida

router = APIRouter(prefix="/modulos", tags=["modulos"])
_SLOTS = {s.chave: s for s in registro.SLOTS}


@router.get("")
def listar_modulos():
    return registro.status()


@router.post("/visao/analisar", response_model=VisaoSaida)
async def analisar_imagem(imagem: UploadFile = File(...)):
    func = registro.carregar(_SLOTS["visao"])
    if func is None:
        return VisaoSaida(disponivel=False, mensagem="Módulo de visão ainda não integrado.")
    conteudo = await imagem.read()
    inicio = time.perf_counter()
    try:
        saida = VisaoSaida.model_validate(func(conteudo))
    except Exception:
        return VisaoSaida(disponivel=False, mensagem="O módulo de visão falhou nesta imagem.")
    if saida.latencia_ms is None:
        saida.latencia_ms = round((time.perf_counter() - inicio) * 1000, 1)
    return saida


@router.post("/assistente/perguntar", response_model=AssistenteSaida)
def perguntar(entrada: AssistenteEntrada):
    func = registro.carregar(_SLOTS["assistente"])
    if func is None:
        return AssistenteSaida(disponivel=False, mensagem="Assistente ainda não integrado.")
    try:
        return AssistenteSaida.model_validate(func(entrada))
    except Exception:
        return AssistenteSaida(disponivel=False, mensagem="O assistente falhou nesta pergunta.")
