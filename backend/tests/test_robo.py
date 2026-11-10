import json
from pathlib import Path

import pandas as pd

from app import config
from app.pipelines.rpa import limpeza, robo
from app.providers import db

CSV = str(Path(__file__).resolve().parents[2] / "data" / "relatos_sinteticos.csv")


def test_limpeza_rejeita_cada_defeito_com_motivo():
    df, rej = limpeza.carregar_e_limpar(CSV)
    motivos = sorted(r["motivo"] for r in rej)
    assert motivos == ["data inválida", "descrição vazia ou curta", "id duplicado"]
    assert len(df) == 52
    assert pd.isna(df.loc[df["id_relato"] == "53", "cep"].iloc[0])   # CEP curto não rejeita a linha


def test_robo_executa_e_e_idempotente(tmp_path):
    rel_path = str(tmp_path / "rel.json")
    r1 = robo.executar(CSV, relatorio_path=rel_path)
    assert r1["status"] == "ok" and r1["processados"] == 52 and r1["rejeitados"] == 3
    assert r1["falhas_linha"] == 0
    with db.conexao() as c:
        n1 = c.execute("select count(*) from relatos").fetchone()[0]
    r2 = robo.executar(CSV, relatorio_path=rel_path)
    with db.conexao() as c:
        n2 = c.execute("select count(*) from relatos").fetchone()[0]
    assert n1 == n2 == 52 and r2["processados"] == 52
    assert json.loads(Path(rel_path).read_text(encoding="utf-8"))["status"] == "ok"
    assert list(Path(config.OUTBOX_DIR).glob("*.eml")), "e-mail deveria ter sido salvo em outbox"
    assert (Path(config.OUTBOX_DIR) / "quarentena.csv").exists()


def test_robo_nao_sobrescreve_decisao_humana(tmp_path):
    robo.executar(CSV, relatorio_path=str(tmp_path / "r.json"))
    with db.conexao() as c:
        db.atualizar_campos(c, "csv-1", status="aprovado", comentario_gestor="ok")
    robo.executar(CSV, relatorio_path=str(tmp_path / "r.json"))
    with db.conexao() as c:
        assert db.obter(c, "csv-1")["status"] == "aprovado"


def test_robo_arquivo_ausente_nao_levanta_excecao(tmp_path):
    r = robo.executar(str(tmp_path / "nao_existe.csv"), relatorio_path=str(tmp_path / "r.json"))
    assert r["status"] == "falha" and "FileNotFoundError" in r["erro_fatal"]


def test_robo_csv_sem_colunas_falha_com_mensagem(tmp_path):
    ruim = tmp_path / "ruim.csv"
    ruim.write_text("a,b\n1,2\n", encoding="utf-8")
    r = robo.executar(str(ruim), relatorio_path=str(tmp_path / "r.json"))
    assert r["status"] == "falha" and "Colunas ausentes" in r["erro_fatal"]


def test_banco_nao_guarda_texto_original_nem_dado_pessoal():
    robo.executar(CSV, relatorio_path="/dev/null")
    with db.conexao() as c:
        todos = " ".join(r["descricao_anon"] for r in db.listar(c))
    assert "123.456.789-09" not in todos and "cidadao.teste@exemplo.invalid" not in todos
