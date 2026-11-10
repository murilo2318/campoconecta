import streamlit as st

from state import store
from ui.cards import cartao_relato
from ui.graficos import urgencia_por_tipo
from ui.mensagens import mostrar_erro, vazio


def tela() -> None:
    st.subheader("Meus relatos nesta sessão")
    ids = set(store.meus_ids())
    if not ids:
        vazio("Você ainda não enviou nenhum relato. Use a aba “Relatar problema”.")
        return
    try:
        meus = [r for r in store.listar_cache() if r["id"] in ids]
    except Exception as e:  # noqa: BLE001
        mostrar_erro(e)
        return
    st.caption("Esta lista vale só enquanto a página estiver aberta. Guarde o protocolo de cada relato.")
    for i, rel in enumerate(meus):
        cartao_relato(rel, chave=f"h{i}")
    if len(meus) >= 2:
        st.plotly_chart(urgencia_por_tipo(meus), width="stretch")
