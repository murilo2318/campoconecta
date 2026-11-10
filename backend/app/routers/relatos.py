import logging
import uuid

from fastapi import APIRouter, HTTPException, Query

from ..pipelines.processar import processar_relato
from ..providers import db
from ..schemas.relato import Decisao, Feedback, RelatoEntrada, RelatoSaida, Triagem

router = APIRouter(prefix="/relatos", tags=["relatos"])
log = logging.getLogger("citizentech.api")


def _para_saida(r: dict) -> RelatoSaida:
    return RelatoSaida(
        id=r["id"], origem=r["origem"], criado_em=r["criado_em"], descricao_anon=r["descricao_anon"],
        cep=r["cep"], cidade=r["cidade"], uf=r["uf"], status=r["status"],
        comentario_gestor=r["comentario_gestor"], feedback=r["feedback"],
        revisao_humana=bool(r["revisao_humana"]),
        triagem=Triagem(tipo=r["tipo"], urgencia=r["urgencia"], resumo=r["resumo"] or "",
                        encaminhar_para=r["encaminhar_para"] or "Ouvidoria",
                        fonte=r["fonte_triagem"] or "regras"),
    )


@router.post("", response_model=RelatoSaida, status_code=201)
def criar_relato(entrada: RelatoEntrada):
    reg = processar_relato(f"api-{uuid.uuid4().hex[:8]}", "api", entrada.descricao, entrada.cep)
    with db.conexao() as conn:
        db.upsert_relato(conn, reg)
        return _para_saida(db.obter(conn, reg["id"]))


@router.get("", response_model=list[RelatoSaida])
def listar_relatos(urgencia: str | None = Query(None), tipo: str | None = Query(None),
                   status: str | None = Query(None)):
    with db.conexao() as conn:
        return [_para_saida(r) for r in db.listar(conn, urgencia, tipo, status)]


@router.patch("/{relato_id}/decisao", response_model=RelatoSaida)
def decidir(relato_id: str, decisao: Decisao):
    with db.conexao() as conn:
        if not db.atualizar_campos(conn, relato_id, status=decisao.status,
                                   comentario_gestor=decisao.comentario):
            raise HTTPException(404, "Relato não encontrado.")
        return _para_saida(db.obter(conn, relato_id))


@router.post("/{relato_id}/feedback", response_model=RelatoSaida)
def avaliar(relato_id: str, fb: Feedback):
    with db.conexao() as conn:
        if not db.atualizar_campos(conn, relato_id, feedback=fb.avaliacao):
            raise HTTPException(404, "Relato não encontrado.")
        return _para_saida(db.obter(conn, relato_id))
