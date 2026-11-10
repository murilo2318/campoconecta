"""Consulta de CEP no ViaCEP com timeout, retry com espera crescente e cache em disco.

A função nunca lança exceção: se a rede falhar, usa o cache; sem cache, devolve None
e o fluxo segue sem cidade e UF.
"""
import json
import logging
import time
from pathlib import Path

import requests

from .. import config

log = logging.getLogger("citizentech.viacep")
URL = "https://viacep.com.br/ws/{cep}/json/"

# Disjuntor: depois de FALHAS_PARA_ABRIR consultas seguidas sem sucesso, o provedor é
# tratado como fora do ar por PAUSA_S segundos e as consultas vão direto ao cache.
FALHAS_PARA_ABRIR = 3
PAUSA_S = 60.0
_falhas_seguidas = 0
_aberto_ate = 0.0


def reiniciar() -> None:
    global _falhas_seguidas, _aberto_ate
    _falhas_seguidas, _aberto_ate = 0, 0.0


def _ler_cache() -> dict:
    try:
        return json.loads(Path(config.CACHE_CEP_PATH).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _gravar_cache(cache: dict) -> None:
    try:
        p = Path(config.CACHE_CEP_PATH)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    except OSError as e:
        log.warning("Não foi possível gravar o cache de CEP: %s", e)


def buscar_cep(cep: str | None, tentativas: int = 3, timeout: float = 5.0, espera: float = 0.5):
    """Devolve {'cidade': ..., 'uf': ...} ou None. CEP inexistente também devolve None."""
    global _falhas_seguidas, _aberto_ate
    if not isinstance(cep, str) or len(cep) != 8 or not cep.isdigit():
        return None
    try:
        cache = _ler_cache()
        if cep in cache:                      # CEP já conhecido: não gasta chamada de rede
            return cache[cep]
        if time.monotonic() < _aberto_ate:
            log.info("Disjuntor aberto, ViaCEP ignorado para %s", cep)
            return None
        for i in range(tentativas):
            try:
                resp = requests.get(URL.format(cep=cep), timeout=timeout)
                resp.raise_for_status()
                dados = resp.json()
                if dados.get("erro"):
                    log.info("CEP %s não existe no ViaCEP", cep)
                    return None
                res = {"cidade": dados.get("localidade"), "uf": dados.get("uf")}
                _falhas_seguidas = 0
                cache[cep] = res
                _gravar_cache(cache)
                return res
            except (requests.RequestException, ValueError) as e:
                log.warning("ViaCEP falhou (%s/%s) para %s: %s", i + 1, tentativas, cep, e)
                if i < tentativas - 1:
                    time.sleep(espera * (2 ** i))
        _falhas_seguidas += 1
        if _falhas_seguidas >= FALHAS_PARA_ABRIR:
            _aberto_ate = time.monotonic() + PAUSA_S
            log.error("ViaCEP fora do ar: disjuntor aberto por %.0f s", PAUSA_S)
        return None
    except Exception as e:  # nunca propaga
        log.error("Erro inesperado na consulta de CEP: %s", e)
        return None
