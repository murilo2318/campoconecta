"""Regressão para datas de RPA e API no mesmo histórico."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ui.graficos import linha_do_tempo


def test_linha_do_tempo_aceita_datas_mistas_e_ignora_invalidas():
    datas = [
        "2026-11-09 10:00:00",
        "2026-11-09T13:00:00Z",
        "2026-11-10T02:00:00+00:00",
        "data-invalida",
    ]
    relatos = [{
        "criado_em": data, "cidade": None,
        "triagem": {"tipo": "praga_doenca", "urgencia": "media"},
    } for data in datas]

    figura = linha_do_tempo(relatos)

    assert list(figura.data[0].y) == [2, 1]
    assert [str(dia) for dia in figura.data[0].x] == ["2026-11-09", "2026-11-10"]
