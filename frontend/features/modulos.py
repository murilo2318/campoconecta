import pandas as pd
import streamlit as st

from providers import api_client
from ui.mensagens import mostrar_erro


def tela() -> None:
    st.subheader("Módulos do projeto")
    st.write("Estado de cada parte da Global Solution. Módulos ainda não entregues aparecem como pendentes e o sistema continua funcionando.")
    try:
        mods = api_client.status_modulos()
    except Exception as e:  # noqa: BLE001
        mostrar_erro(e)
        return
    if not mods:
        st.info("Nenhum módulo cadastrado.", icon="📭")
        return
    df = pd.DataFrame(mods)
    df["Situação"] = df["integrado"].map({True: "✅ Integrado", False: "⏳ Pendente"})
    st.dataframe(df[["materia", "Situação", "tipo", "pasta"]].rename(
        columns={"materia": "Matéria", "tipo": "Tipo", "pasta": "Onde entregar"}),
        hide_index=True, width="stretch")
