import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config  # noqa: E402
from app.providers import viacep  # noqa: E402


@pytest.fixture(autouse=True)
def ambiente(tmp_path, monkeypatch):
    """Isola banco, cache, outbox e log em pasta temporária e desliga a rede."""
    monkeypatch.setattr(config, "DB_PATH", str(tmp_path / "t.db"))
    monkeypatch.setattr(config, "CACHE_CEP_PATH", str(tmp_path / "cache.json"))
    monkeypatch.setattr(config, "OUTBOX_DIR", str(tmp_path / "outbox"))
    monkeypatch.setattr(config, "LOG_PATH", str(tmp_path / "robo.log"))
    monkeypatch.setattr(config, "GEMINI_API_KEY", "")
    monkeypatch.setattr(config, "GEMINI_MODEL", "")
    monkeypatch.setattr(config, "SMTP_HOST", "")

    def sem_rede(*a, **k):
        raise viacep.requests.ConnectionError("sem rede nos testes")
    monkeypatch.setattr(viacep.requests, "get", sem_rede)
    monkeypatch.setattr(viacep.time, "sleep", lambda s: None)
    viacep.reiniciar()
    return tmp_path
