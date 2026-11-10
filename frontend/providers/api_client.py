"""Único ponto de contato com o back-end. O front nunca chama o LLM diretamente."""
import os

import requests

API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")
TIMEOUT_S = float(os.getenv("API_TIMEOUT_S", "20"))


class ApiIndisponivel(Exception):
    """API fora do ar ou lenta demais."""


class ApiErro(Exception):
    """A API respondeu com erro. A mensagem já é amigável para o cidadão."""


def _pedir(metodo: str, caminho: str, **kw):
    try:
        r = requests.request(metodo, f"{API_URL}{caminho}", timeout=TIMEOUT_S, **kw)
    except requests.Timeout as e:
        raise ApiIndisponivel("O serviço demorou para responder. Tente novamente em instantes.") from e
    except requests.ConnectionError as e:
        raise ApiIndisponivel("Não foi possível conectar ao serviço. Tente novamente em instantes.") from e
    if r.status_code == 422:
        raise ApiErro("Verifique os campos: a descrição precisa de pelo menos 10 caracteres e o CEP, se informado, de 8 dígitos.")
    if r.status_code == 404:
        raise ApiErro("Esse relato não foi encontrado.")
    if r.status_code >= 500:
        raise ApiErro("O serviço teve um problema. Seu relato não foi perdido; tente de novo em alguns minutos.")
    try:
        return r.json()
    except ValueError as e:
        raise ApiErro("Recebemos uma resposta inesperada do serviço. Tente novamente.") from e


def criar_relato(descricao: str, cep: str | None) -> dict:
    return _pedir("POST", "/relatos", json={"descricao": descricao, "cep": cep or None})


def listar_relatos(urgencia=None, tipo=None, status=None) -> list[dict]:
    params = {k: v for k, v in (("urgencia", urgencia), ("tipo", tipo), ("status", status)) if v}
    return _pedir("GET", "/relatos", params=params)


def decidir(relato_id: str, status: str, comentario: str | None = None) -> dict:
    return _pedir("PATCH", f"/relatos/{relato_id}/decisao", json={"status": status, "comentario": comentario})


def avaliar(relato_id: str, avaliacao: str) -> dict:
    return _pedir("POST", f"/relatos/{relato_id}/feedback", json={"avaliacao": avaliacao})


def executar_robo() -> dict:
    return _pedir("POST", "/rpa/executar")


def status_modulos() -> list[dict]:
    return _pedir("GET", "/modulos")


def analisar_imagem(nome: str, conteudo: bytes, tipo_mime: str) -> dict:
    return _pedir("POST", "/modulos/visao/analisar", files={"imagem": (nome, conteudo, tipo_mime)})


def perguntar(pergunta: str, historico: list[dict]) -> dict:
    return _pedir("POST", "/modulos/assistente/perguntar", json={"pergunta": pergunta, "historico": historico})
