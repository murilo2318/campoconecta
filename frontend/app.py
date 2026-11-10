import streamlit as st

from features import gestor, historico, modulos, reportar
from state import store

st.set_page_config(page_title="CampoConecta", page_icon="🌾", layout="wide")
store.iniciar()

st.title("🌾 CampoConecta · CitizenTech")
st.caption("Relatos de pequenos produtores rurais (pragas, clima, água, preço e crédito), classificados por inteligência artificial ou por regras automáticas e sempre conferidos por pessoas.")

with st.sidebar:
    st.header("Como usar")
    st.markdown("1. Em **Relatar problema**, descreva o que viu.\n2. Veja a classificação e avalie.\n"
                "3. Um gestor confere os casos antes de qualquer encaminhamento.")
    st.divider()
    st.caption("Em emergência, ligue 193 (Bombeiros) ou 199 (Defesa Civil). Este sistema não substitui a assistência técnica nem o atendimento de emergência.")

abas = st.tabs(["Relatar problema", "Meus relatos", "Painel do gestor", "Módulos"])
for aba, tela in zip(abas, (reportar.tela, historico.tela, gestor.tela, modulos.tela)):
    with aba:
        tela()
