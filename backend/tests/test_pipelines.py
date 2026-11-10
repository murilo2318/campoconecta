from app.pipelines import anonimizacao, triagem
from app.providers import llm, viacep


def test_anonimiza_dados_estruturados_e_preserva_o_resto():
    t = ("Meu nome é Carlos Almeida, CPF 123.456.789-09, e-mail a@b.com, tel (11) 91234-5678, "
         "placa ABC1D23. Lagarta no milho, três talhões atacados.")
    s = anonimizacao.anonimizar(t)
    for sensivel in ("Carlos", "123.456", "a@b.com", "91234", "ABC1D23"):
        assert sensivel not in s
    for marcador in ("[NOME]", "[CPF]", "[EMAIL]", "[TELEFONE]", "[PLACA]"):
        assert marcador in s
    assert "Lagarta no milho, três talhões atacados" in s


def test_anonimiza_vazio_e_none():
    assert anonimizacao.anonimizar(None) == ""
    assert anonimizacao.anonimizar("") == ""


def test_regras_casos_basicos():
    assert triagem.triar_por_regras("Gado morrendo depois de pastar").urgencia == "critica"
    assert triagem.triar_por_regras("Lagarta no milho").tipo == "praga_doenca"
    assert triagem.triar_por_regras("horário do curso").tipo == "outro"


def test_llm_valido_e_usado(monkeypatch):
    monkeypatch.setattr(llm, "classificar",
                        lambda t: {"tipo": "clima_extremo", "urgencia": "alta", "resumo": "Geada na horta"})
    r = triagem.triar("qualquer texto")
    assert r.fonte == "llm" and r.urgencia == "alta"


def test_llm_resposta_invalida_cai_nas_regras(monkeypatch):
    monkeypatch.setattr(llm, "classificar", lambda t: {"tipo": "inventado", "urgencia": "enorme"})
    r = triagem.triar("Lagarta grande no milho")
    assert r.fonte == "regras" and r.tipo == "praga_doenca"


def test_llm_vazio_cai_nas_regras(monkeypatch):
    monkeypatch.setattr(llm, "classificar", lambda t: {})
    assert triagem.triar("Granizo na lavoura").fonte == "regras"


def test_llm_fora_do_ar_cai_nas_regras(monkeypatch):
    def falha(t):
        raise llm.LLMIndisponivel("timeout")
    monkeypatch.setattr(llm, "classificar", falha)
    assert triagem.triar("Árvore caiu").fonte == "regras"


def test_viacep_sem_rede_e_sem_cache_devolve_none():
    assert viacep.buscar_cep("18150000") is None


def test_viacep_cep_invalido_nem_chama_a_rede():
    assert viacep.buscar_cep("123") is None
    assert viacep.buscar_cep(None) is None


def test_viacep_usa_cache_quando_a_rede_cai():
    viacep._gravar_cache({"18150000": {"cidade": "Ibiúna", "uf": "SP"}})
    assert viacep.buscar_cep("18150000")["cidade"] == "Ibiúna"


def test_disjuntor_para_de_chamar_a_rede_depois_de_falhas_seguidas(monkeypatch):
    chamadas = []

    def falha(*a, **k):
        chamadas.append(1)
        raise viacep.requests.ConnectionError("fora do ar")
    monkeypatch.setattr(viacep.requests, "get", falha)
    for cep in ("18150000", "18170000", "08940000"):      # 3 CEPs diferentes, 3 tentativas cada
        assert viacep.buscar_cep(cep) is None
    antes = len(chamadas)
    assert viacep.buscar_cep("09320000") is None           # disjuntor aberto: não chama a rede
    assert len(chamadas) == antes


def test_cep_conhecido_vem_do_cache_sem_rede(monkeypatch):
    viacep._gravar_cache({"18150000": {"cidade": "Ibiúna", "uf": "SP"}})
    monkeypatch.setattr(viacep.requests, "get", lambda *a, **k: (_ for _ in ()).throw(AssertionError("não deveria chamar")))
    assert viacep.buscar_cep("18150000")["uf"] == "SP"


def test_outro_triado_so_por_regras_vai_para_revisao_humana():
    from app.pipelines.processar import processar_relato
    r = processar_relato("t-1", "api", "Texto que as regras não entendem de jeito nenhum", None)
    assert r["tipo"] == "outro" and r["fonte_triagem"] == "regras" and r["revisao_humana"] is True
