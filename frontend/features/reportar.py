import streamlit as st

from providers import api_client
from state import store
from ui.cards import cartao_relato
from ui.mensagens import mostrar_erro


def tela() -> None:
    st.subheader("Relatar um problema")
    st.write("Conte o que está acontecendo, de forma simples. **Não escreva CPF, telefone ou outros dados pessoais**: "
             "nós também mascaramos esses dados, mas é mais seguro não enviar.")
    with st.form("form_relato", clear_on_submit=False):
        descricao = st.text_area("O que está acontecendo? (obrigatório)", max_chars=1000, height=140,
                                 help="Mínimo de 10 caracteres.")
        cep = st.text_input("CEP do local (opcional)", max_chars=9, placeholder="00000-000")
        enviar = st.form_submit_button("Enviar relato", type="primary")

    if enviar:
        digitos = "".join(c for c in cep if c.isdigit())
        if len(" ".join(descricao.split())) < 10:
            st.warning("Descreva o problema com pelo menos 10 caracteres.", icon="✏️")
            return
        elif cep and len(digitos) != 8:
            st.warning("O CEP precisa ter 8 dígitos. Se não souber, deixe em branco.", icon="✏️")
            return
        else:
            try:
                with st.spinner("Analisando seu relato..."):
                    rel = api_client.criar_relato(descricao, digitos or None)
                store.registrar_relato(rel)
            except Exception as e:  # noqa: BLE001 - qualquer falha vira mensagem amigável
                mostrar_erro(e)
                return

    rel = st.session_state.get("ultimo_resultado")
    if rel:
        st.success("Relato recebido. Veja como ele foi classificado:", icon="✅")
        cartao_relato(rel, mostrar_fonte_ia=True, chave="ultimo")
        st.write("**A classificação ajudou?** Sua avaliação nos ajuda a corrigir erros.")
        c1, c2, _ = st.columns([1, 1, 3])
        for coluna, rotulo, valor in ((c1, "👍 Útil", "util"), (c2, "👎 Incorreta", "incorreta")):
            if coluna.button(rotulo, key=f"fb_{valor}_{rel['id']}"):
                try:
                    api_client.avaliar(rel["id"], valor)
                    st.toast("Obrigado pela avaliação!")
                except Exception as e:  # noqa: BLE001
                    mostrar_erro(e)
