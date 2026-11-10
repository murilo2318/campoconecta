"""Testes de tela com o AppTest do Streamlit. A API é substituída por funções falsas."""
import sys
from pathlib import Path

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from providers import api_client  # noqa: E402

APP = str(Path(__file__).resolve().parents[1] / "app.py")

REL = {"id": "api-1", "origem": "api", "criado_em": "2026-11-09T10:00:00", "descricao_anon": "x", "cep": None,
       "cidade": "Ibiúna", "uf": "SP", "status": "pendente", "comentario_gestor": None, "feedback": None,
       "revisao_humana": True,
       "triagem": {"tipo": "praga_doenca", "urgencia": "critica", "resumo": "Gado morrendo",
                   "encaminhar_para": "Defesa Agropecuária e Assistência Técnica", "fonte": "regras"}}


def _app(monkeypatch, **fakes):
    st.cache_data.clear()          # o cache de listagem não pode vazar entre testes
    padrao = {"listar_relatos": lambda *a, **k: [REL], "status_modulos": lambda: [
        {"chave": "visao", "materia": "Visão", "tipo": "endpoint", "contrato": "", "pasta": "x", "integrado": False}]}
    padrao.update(fakes)
    for nome, f in padrao.items():
        monkeypatch.setattr(api_client, nome, f)
    return AppTest.from_file(APP, default_timeout=15).run()


def test_abre_sem_erro(monkeypatch):
    at = _app(monkeypatch)
    assert not at.exception
    assert len(at.tabs) == 4


def _enviar(at, texto):
    """Preenche e envia o formulário em uma única execução, como o usuário faria."""
    at.text_area[0].input(texto)
    at.button[0].click()
    return at.run()


def test_validacao_antes_do_envio(monkeypatch):
    chamadas = []
    at = _app(monkeypatch, criar_relato=lambda *a: chamadas.append(a))
    _enviar(at, "curto")
    assert chamadas == [] and any("10 caracteres" in w.value for w in at.warning)


def test_envio_valido_mostra_cartao_com_texto_e_icone(monkeypatch):
    chamadas = []
    at = _app(monkeypatch, listar_relatos=lambda *a, **k: [],        # o cartão só pode vir do envio
              criar_relato=lambda d, c: chamadas.append((d, c)) or REL)
    _enviar(at, "Gado morrendo no sítio depois de pastar")
    assert not at.exception and len(chamadas) == 1
    html = " ".join(m.value for m in at.markdown)
    assert "Urgência CRÍTICA" in html and "🔴" in html          # cor sempre com texto e ícone
    assert any("conferido por uma pessoa" in i.value for i in at.info)


def test_api_fora_do_ar_mostra_mensagem_amigavel(monkeypatch):
    def cai(*a):
        raise api_client.ApiIndisponivel("Não foi possível conectar ao serviço. Tente novamente em instantes.")
    at = _app(monkeypatch, listar_relatos=lambda *a, **k: [], criar_relato=cai)
    _enviar(at, "Gado morrendo no sítio depois de pastar")
    assert not at.exception
    assert any("Não foi possível conectar" in e.value for e in at.error)
    assert not any("Traceback" in e.value or "ConnectionError" in e.value for e in at.error)


def test_erro_inesperado_nao_vaza_detalhe_tecnico(monkeypatch):
    def quebra(*a):
        raise RuntimeError("KeyError: segredo interno")
    at = _app(monkeypatch, listar_relatos=lambda *a, **k: [], criar_relato=quebra)
    _enviar(at, "Gado morrendo no sítio depois de pastar")
    assert not at.exception
    assert any("Algo deu errado" in e.value for e in at.error)
    assert not any("segredo interno" in e.value for e in at.error)


def test_listagem_vazia_e_modulos_vazios_nao_quebram(monkeypatch):
    at = _app(monkeypatch, listar_relatos=lambda *a, **k: [], status_modulos=lambda: [])
    assert not at.exception


def test_painel_do_gestor_lista_e_decide(monkeypatch):
    decisoes = []
    at = _app(monkeypatch, decidir=lambda i, s, c=None: decisoes.append((i, s)) or REL)
    aprovar = [b for b in at.button if "Aprovar" in b.label][0]
    aprovar.click().run()
    assert decisoes == [("api-1", "aprovado")]


def test_cep_invalido_preserva_rascunho_sem_mostrar_resultado_anterior(monkeypatch):
    chamadas = []
    at = _app(monkeypatch, listar_relatos=lambda *a, **k: [],
              criar_relato=lambda d, c: chamadas.append((d, c)) or REL)
    _enviar(at, "A bomba quebrou e preciso de assistência para irrigar")
    assert at.success
    novo = "O poço secou e preciso de orientação para irrigar a horta."
    at.text_area[0].input(novo)
    at.text_input[0].input("123")
    at.button[0].click().run()
    assert len(chamadas) == 1
    assert any("8 dígitos" in w.value for w in at.warning)
    assert not at.success
    assert at.text_area[0].value == novo
    assert at.text_input[0].value == "123"


def test_envio_mostra_protocolo_e_avisa_que_ainda_nao_foi_encaminhado(monkeypatch):
    """Melhoria ligada ao feedback dos Participantes 1, 2 e 3 (docs/VALIDACAO_FRONT.md)."""
    at = _app(monkeypatch, listar_relatos=lambda *a, **k: [], criar_relato=lambda d, c: REL)
    _enviar(at, "Gado morrendo no sítio depois de pastar")
    assert any("api-1" in s.value for s in at.success)
    assert any("não foi encaminhado" in i.value for i in at.info)
    legendas = " ".join(c.value for c in at.caption)
    assert "Protocolo: api-1" in legendas and "sem inteligência artificial" in legendas
