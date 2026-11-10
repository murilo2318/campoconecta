"""Acesso ao SQLite. O texto original do cidadão nunca é gravado, só a versão anonimizada."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from .. import config

COLUNAS = [
    "id", "origem", "criado_em", "descricao_anon", "cep", "cidade", "uf",
    "tipo", "urgencia", "resumo", "encaminhar_para", "fonte_triagem",
    "status", "comentario_gestor", "feedback", "revisao_humana",
]

DDL = """CREATE TABLE IF NOT EXISTS relatos (
    id TEXT PRIMARY KEY, origem TEXT, criado_em TEXT, descricao_anon TEXT,
    cep TEXT, cidade TEXT, uf TEXT, tipo TEXT, urgencia TEXT, resumo TEXT,
    encaminhar_para TEXT, fonte_triagem TEXT, status TEXT DEFAULT 'pendente',
    comentario_gestor TEXT, feedback TEXT, revisao_humana INTEGER DEFAULT 0)"""


@contextmanager
def conexao(path: str | None = None):
    path = path or config.DB_PATH
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute(DDL)
        yield conn
        conn.commit()
    finally:
        conn.close()


def upsert_relato(conn, reg: dict) -> None:
    """Idempotente: rodar duas vezes com o mesmo id atualiza a linha e não duplica.

    Campos de decisão humana (status, comentário, feedback) não são sobrescritos
    quando o registro já existe.
    """
    vals = {c: reg.get(c) for c in COLUNAS}
    vals["revisao_humana"] = int(bool(vals["revisao_humana"]))
    vals["status"] = vals["status"] or "pendente"
    cols = ", ".join(COLUNAS)
    marc = ", ".join(f":{c}" for c in COLUNAS)
    atualiza = ", ".join(
        f"{c}=excluded.{c}" for c in COLUNAS
        if c not in ("id", "status", "comentario_gestor", "feedback")
    )
    conn.execute(
        f"INSERT INTO relatos ({cols}) VALUES ({marc}) ON CONFLICT(id) DO UPDATE SET {atualiza}",
        vals,
    )


def listar(conn, urgencia=None, tipo=None, status=None) -> list[dict]:
    sql, params = "SELECT * FROM relatos WHERE 1=1", []
    for campo, valor in (("urgencia", urgencia), ("tipo", tipo), ("status", status)):
        if valor:
            sql += f" AND {campo} = ?"
            params.append(valor)
    sql += " ORDER BY criado_em DESC"
    return [dict(r) for r in conn.execute(sql, params).fetchall()]


def obter(conn, relato_id: str) -> dict | None:
    r = conn.execute("SELECT * FROM relatos WHERE id = ?", (relato_id,)).fetchone()
    return dict(r) if r else None


def atualizar_campos(conn, relato_id: str, **campos) -> bool:
    permitido = {"status", "comentario_gestor", "feedback"}
    campos = {k: v for k, v in campos.items() if k in permitido}
    if not campos:
        return False
    sets = ", ".join(f"{k} = ?" for k in campos)
    cur = conn.execute(f"UPDATE relatos SET {sets} WHERE id = ?", [*campos.values(), relato_id])
    return cur.rowcount > 0
