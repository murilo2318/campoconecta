"""Selos de urgência. A cor nunca vem sozinha: sempre acompanha ícone e texto."""
ESTILO = {
    "critica": ("🔴", "CRÍTICA", "#B3261E"),
    "alta": ("🟠", "ALTA", "#9A3F00"),
    "media": ("🟡", "MÉDIA", "#7A5400"),
    "baixa": ("🟢", "BAIXA", "#1B6E3C"),
}
STATUS_ROTULO = {"pendente": "⏳ Aguardando análise", "aprovado": "✅ Aprovado", "rejeitado": "⛔ Rejeitado"}
TIPO_ROTULO = {"praga_doenca": "Praga ou doença", "clima_extremo": "Clima extremo", "agua_irrigacao": "Água e irrigação",
               "preco_mercado": "Preço e mercado", "credito_seguro": "Crédito e seguro", "outro": "Outro"}


def selo_urgencia(urgencia: str) -> str:
    icone, texto, cor = ESTILO.get(urgencia, ("⚪", urgencia.upper(), "#444444"))
    return (f"<span style='background:{cor};color:#fff;padding:2px 10px;border-radius:12px;"
            f"font-weight:600' role='status'>{icone} Urgência {texto}</span>")
