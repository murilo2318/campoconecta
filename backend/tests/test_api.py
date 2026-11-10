import sys

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modulos import registro

cli = TestClient(app)


def test_health():
    assert cli.get("/health").json() == {"status": "ok"}


def test_criar_relato_valida_anonimiza_e_classifica():
    r = cli.post("/relatos", json={"descricao": "Meu nome é Ana Lima, gado morrendo no sítio depois de pastar.", "cep": "18150-000"})
    assert r.status_code == 201
    j = r.json()
    assert "Ana" not in j["descricao_anon"] and "[NOME]" in j["descricao_anon"]
    assert j["triagem"]["urgencia"] == "critica" and j["revisao_humana"] is True
    assert j["cep"] == "18150000" and j["status"] == "pendente"


@pytest.mark.parametrize("corpo", [
    {"descricao": "curto"}, {"descricao": "   "}, {"descricao": "x" * 1001},
    {"descricao": "Descrição válida com CEP errado", "cep": "123"}, {},
])
def test_entradas_invalidas_dao_422(corpo):
    assert cli.post("/relatos", json=corpo).status_code == 422


def test_decisao_feedback_e_filtros():
    a = cli.post("/relatos", json={"descricao": "Lagarta grande no milho do sítio"}).json()["id"]
    b = cli.post("/relatos", json={"descricao": "Geada forte queimou a horta inteira"}).json()["id"]
    assert cli.patch(f"/relatos/{a}/decisao", json={"status": "aprovado", "comentario": "ok"}).json()["status"] == "aprovado"
    assert cli.post(f"/relatos/{b}/feedback", json={"avaliacao": "incorreta"}).json()["feedback"] == "incorreta"
    assert [r["id"] for r in cli.get("/relatos", params={"status": "aprovado"}).json()] == [a]
    assert [r["id"] for r in cli.get("/relatos", params={"tipo": "clima_extremo"}).json()] == [b]


def test_404_e_decisao_invalida():
    assert cli.patch("/relatos/nao-existe/decisao", json={"status": "aprovado"}).status_code == 404
    assert cli.patch("/relatos/x/decisao", json={"status": "talvez"}).status_code == 422


def test_modulos_sem_implementacao_devolvem_stub():
    j = cli.post("/modulos/visao/analisar", files={"imagem": ("a.jpg", b"123", "image/jpeg")}).json()
    assert j["disponivel"] is False
    j = cli.post("/modulos/assistente/perguntar", json={"pergunta": "Como controlar lagarta no milho?"}).json()
    assert j["disponivel"] is False
    lista = cli.get("/modulos").json()
    assert {m["chave"] for m in lista} == {"visao", "assistente", "corpus", "iot", "quantica", "governanca"}


def test_modulo_visao_real_e_plugado_sem_mexer_no_resto(monkeypatch):
    import types
    fake = types.ModuleType("app.modulos.impl_visao")
    fake.analisar = lambda img: {"tipo_dano": "buraco", "confianca": 0.87, "caixas": []}
    monkeypatch.setitem(sys.modules, "app.modulos.impl_visao", fake)
    j = cli.post("/modulos/visao/analisar", files={"imagem": ("a.jpg", b"123", "image/jpeg")}).json()
    assert j["disponivel"] is True and j["tipo_dano"] == "buraco" and j["latencia_ms"] is not None


def test_modulo_que_quebra_nao_derruba_a_api(monkeypatch):
    import types
    fake = types.ModuleType("app.modulos.impl_visao")
    def quebra(img): raise RuntimeError("modelo corrompido")
    fake.analisar = quebra
    monkeypatch.setitem(sys.modules, "app.modulos.impl_visao", fake)
    j = cli.post("/modulos/visao/analisar", files={"imagem": ("a.jpg", b"1", "image/jpeg")}).json()
    assert j["disponivel"] is False


def test_cors_restritivo():
    ok = cli.options("/relatos", headers={"Origin": "http://localhost:8501", "Access-Control-Request-Method": "POST"})
    assert ok.headers.get("access-control-allow-origin") == "http://localhost:8501"
    nao = cli.options("/relatos", headers={"Origin": "http://site-malicioso.example", "Access-Control-Request-Method": "POST"})
    assert "access-control-allow-origin" not in nao.headers


def test_rpa_executar_via_api(tmp_path, monkeypatch):
    from app import config
    monkeypatch.chdir(tmp_path)
    j = cli.post("/rpa/executar").json()
    assert j["status"] == "ok" and j["processados"] == 52
