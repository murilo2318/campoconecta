"""Componente reutilizável: o mesmo cartão aparece para o cidadão e para o gestor."""
import streamlit as st

from .badges import STATUS_ROTULO, TIPO_ROTULO, selo_urgencia


def cartao_relato(rel: dict, *, mostrar_fonte_ia: bool = False, chave: str = "") -> None:
    tri = rel["triagem"]
    with st.container(border=True):
        st.markdown(selo_urgencia(tri["urgencia"]), unsafe_allow_html=True)
        st.markdown(f"**{TIPO_ROTULO.get(tri['tipo'], tri['tipo'])}** · {rel.get('cidade') or 'local não identificado'}"
                    f" · {STATUS_ROTULO[rel['status']]}")
        st.write(tri["resumo"])
        st.caption(f"Sugestão de encaminhamento (ainda não enviado): {tri['encaminhar_para']}")
        st.caption(f"Protocolo: {rel['id']}")
        if rel.get("revisao_humana"):
            st.info("Este caso será conferido por uma pessoa antes de qualquer ação.", icon="👤")
        if mostrar_fonte_ia:
            st.caption("Classificação feita por " + ("inteligência artificial" if tri["fonte"] == "llm" else "regras automáticas (sem inteligência artificial)"))
        if rel.get("comentario_gestor"):
            st.caption(f"Comentário do gestor: {rel['comentario_gestor']}")
