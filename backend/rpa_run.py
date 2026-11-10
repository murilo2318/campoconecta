"""Ponto de entrada do robô. Uso: python rpa_run.py [caminho.csv]"""
import json
import sys

from app.pipelines.rpa.robo import executar

if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else None
    print(json.dumps(executar(caminho), ensure_ascii=False, indent=2))
