import streamlit as st

from providers.api_client import ApiErro, ApiIndisponivel


def mostrar_erro(e: Exception) -> None:
    """Mensagem clara, sem detalhes técnicos."""
    if isinstance(e, (ApiIndisponivel, ApiErro)):
        st.error(str(e), icon="⚠️")
    else:
        st.error("Algo deu errado do nosso lado. Tente novamente em instantes.", icon="⚠️")


def vazio(texto: str) -> None:
    st.info(texto, icon="📭")
