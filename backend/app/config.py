"""Configuração lida de variáveis de ambiente. Nenhuma chave fica no código."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

RAIZ = Path(__file__).resolve().parents[2]


def _lista(valor: str) -> list[str]:
    return [v.strip() for v in valor.split(",") if v.strip()]


DB_PATH = os.getenv("DB_PATH", str(RAIZ / "data" / "citizentech.db"))
LOG_PATH = os.getenv("LOG_PATH", str(RAIZ / "logs" / "robo.log"))
OUTBOX_DIR = os.getenv("OUTBOX_DIR", str(RAIZ / "outbox"))
CACHE_CEP_PATH = os.getenv("CACHE_CEP_PATH", str(RAIZ / "data" / "cache_cep.json"))
CSV_EXEMPLO = os.getenv("CSV_EXEMPLO", str(RAIZ / "data" / "relatos_sinteticos.csv"))


# CORS restrito: lista explícita de origens, nunca "*".
CORS_ORIGINS = _lista(os.getenv("CORS_ORIGINS", "http://localhost:8501"))

# LLM é opcional. Sem chave ou sem modelo, a triagem usa regras.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "")
LLM_TIMEOUT_S = float(os.getenv("LLM_TIMEOUT_S", "10"))

# E-mail: sem SMTP_HOST, a mensagem é salva em outbox/ como .eml.
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO", "extensao.rural@exemplo.invalid")
EMAIL_ORIGEM = os.getenv("EMAIL_ORIGEM", "campoconecta@exemplo.invalid")
