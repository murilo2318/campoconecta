"""Estado centralizado da sessão. Nenhuma tela mexe em st.session_state diretamente."""
import streamlit as st

from providers import api_client


def iniciar() -> None:
    st.session_state.setdefault("meus_ids", [])          # histórico do cidadão nesta sessão
    st.session_state.setdefault("ultimo_resultado", None)
    st.session_state.setdefault("gestor_autenticado", False)
    st.session_state.setdefault("chat", [])


def registrar_relato(rel: dict) -> None:
    st.session_state["meus_ids"].append(rel["id"])
    st.session_state["ultimo_resultado"] = rel
    listar_cache.clear()


def meus_ids() -> list[str]:
    return st.session_state["meus_ids"]


@st.cache_data(ttl=15, show_spinner=False)
def listar_cache(urgencia=None, tipo=None, status=None) -> list[dict]:
    """Cache curto para não repetir a chamada à API a cada rerun do Streamlit."""
    return api_client.listar_relatos(urgencia, tipo, status)


def invalidar() -> None:
    listar_cache.clear()
