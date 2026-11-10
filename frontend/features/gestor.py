import os

import streamlit as st

from providers import api_client
from state import store
from ui.badges import ESTILO, TIPO_ROTULO
from ui.cards import cartao_relato
from ui.graficos import linha_do_tempo, urgencia_por_tipo
from ui.mensagens import mostrar_erro, vazio


def _acesso() -> bool:
    pin = os.getenv("GESTOR_PIN", "")
    if st.session_state["gestor_autenticado"]:
        return True
    if not pin:
        st.warning("GESTOR_PIN não configurado: painel aberto apenas para demonstração.", icon="🔓")
        st.session_state["gestor_autenticado"] = True
        return True
    digitado = st.text_input("PIN do gestor", type="password")
    if digitado and digitado == pin:
        st.session_state["gestor_autenticado"] = True
        st.rerun()
    elif digitado:
        st.error("PIN incorreto.", icon="🔒")
    return False


def tela() -> None:
    st.subheader("Painel do gestor")
    if not _acesso():
        return

    c1, c2, c3 = st.columns(3)
    urgencia = c1.selectbox("Urgência", ["todas", *ESTILO.keys()], format_func=lambda v: "Todas" if v == "todas" else v.capitalize())
    tipo = c2.selectbox("Tipo", ["todos", *TIPO_ROTULO.keys()], format_func=lambda v: "Todos" if v == "todos" else TIPO_ROTULO[v])
    status = c3.selectbox("Situação", ["pendente", "aprovado", "rejeitado", "todas"], format_func=str.capitalize)

    try:
        todos = store.listar_cache()
        filtrados = store.listar_cache(None if urgencia == "todas" else urgencia,
                                       None if tipo == "todos" else tipo,
                                       None if status == "todas" else status)
    except Exception as e:  # noqa: BLE001
        mostrar_erro(e)
        return
    if not todos:
        vazio("Ainda não há relatos. Peça ao robô para processar o lote de exemplo abaixo.")
    else:
        g1, g2 = st.columns(2)
        g1.plotly_chart(urgencia_por_tipo(filtrados or todos), width="stretch")
        g2.plotly_chart(linha_do_tempo(filtrados or todos), width="stretch")

    st.markdown(f"**{len(filtrados)} relato(s)** com os filtros atuais")
    for rel in filtrados[:20]:
        cartao_relato(rel, mostrar_fonte_ia=True, chave=rel["id"])
        if rel["status"] == "pendente":
            comentario = st.text_input("Comentário (opcional)", key=f"com_{rel['id']}", max_chars=300)
            a, r, _ = st.columns([1, 1, 4])
            for coluna, rotulo, valor in ((a, "✅ Aprovar", "aprovado"), (r, "⛔ Rejeitar", "rejeitado")):
                if coluna.button(rotulo, key=f"{valor}_{rel['id']}"):
                    try:
                        api_client.decidir(rel["id"], valor, comentario or None)
                        store.invalidar()
                        st.rerun()
                    except Exception as e:  # noqa: BLE001
                        mostrar_erro(e)
    if len(filtrados) > 20:
        st.caption("Mostrando os 20 mais recentes. Use os filtros para refinar.")

    st.divider()
    st.markdown("**Robô em lote**")
    if st.button("▶️ Processar lote de exemplo e preparar e-mail"):
        try:
            with st.spinner("O robô está processando o lote..."):
                rel = api_client.executar_robo()
            store.invalidar()
            if rel.get("status") == "ok":
                st.success(f"Lote concluído: {rel['processados']} processados, {rel['rejeitados']} em quarentena.", icon="🤖")
            else:
                st.error("O robô não conseguiu ler o arquivo. A equipe técnica foi avisada no registro.", icon="⚠️")
            with st.expander("Relatório de execução"):
                st.json(rel)
        except Exception as e:  # noqa: BLE001
            mostrar_erro(e)
