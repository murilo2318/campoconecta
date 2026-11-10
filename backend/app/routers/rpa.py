from fastapi import APIRouter

from ..pipelines.rpa.robo import executar

router = APIRouter(prefix="/rpa", tags=["rpa"])


@router.post("/executar")
def executar_robo():
    """Roda o robô em lote sobre o CSV de exemplo e devolve o relatório de execução."""
    return executar(relatorio_path="relatorio_execucao.json")
