"""Monta o e-mail de alerta. Com SMTP configurado envia; sem SMTP salva um .eml em outbox/."""
import logging
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

from ... import config

log = logging.getLogger("citizentech.email")
_ROTULO = {"critica": "CRÍTICA", "alta": "ALTA", "media": "MÉDIA", "baixa": "BAIXA"}


def montar_email(relatos: list[dict], destino: str | None = None) -> EmailMessage:
    destino = destino or config.EMAIL_DESTINO
    msg = EmailMessage()
    msg["Subject"] = f"[CampoConecta] {len(relatos)} relato(s) para ação"
    msg["From"], msg["To"] = config.EMAIL_ORIGEM, destino

    linhas = [f"- ({_ROTULO[r['urgencia']]}) {r['tipo']} | {r.get('cidade') or 'cidade não identificada'} "
              f"| {r['resumo']}" for r in relatos] or ["Nenhum relato aprovado no período."]
    msg.set_content("Relatos aprovados pelo gestor, sem dados pessoais:\n\n" + "\n".join(linhas))

    itens = "".join(
        f"<tr><td><b>{_ROTULO[r['urgencia']]}</b></td><td>{r['tipo']}</td>"
        f"<td>{r.get('cidade') or '-'}</td><td>{r['resumo']}</td></tr>" for r in relatos
    )
    msg.add_alternative(
        "<p>Relatos aprovados pelo gestor, sem dados pessoais.</p>"
        "<table border='1' cellpadding='4'><tr><th>Urgência</th><th>Tipo</th><th>Cidade</th><th>Resumo</th></tr>"
        f"{itens}</table>", subtype="html")
    return msg


def enviar_ou_salvar(msg: EmailMessage) -> str:
    """Devolve 'enviado' ou o caminho do .eml salvo. Falha de SMTP cai no .eml."""
    if config.SMTP_HOST:
        try:
            with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=10) as s:
                s.starttls()
                if config.SMTP_USER:
                    s.login(config.SMTP_USER, config.SMTP_PASSWORD)
                s.send_message(msg)
            return "enviado"
        except (smtplib.SMTPException, OSError) as e:
            log.error("SMTP falhou (%s). Salvando em outbox.", type(e).__name__)
    pasta = Path(config.OUTBOX_DIR)
    pasta.mkdir(parents=True, exist_ok=True)
    arq = pasta / f"alerta_{datetime.now():%Y%m%d_%H%M%S}.eml"
    arq.write_bytes(bytes(msg))
    return str(arq)
