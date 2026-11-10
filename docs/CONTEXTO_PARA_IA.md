# Contexto do projeto para quem (pessoa ou IA) for continuar o trabalho

Atualizado em 10/11/2026. Leia este arquivo, depois `README.md` e `docs/REQUISITOS.md`.

## O que é
CampoConecta (CitizenTech, Plano A): relatos do pequeno produtor rural (praga ou doença, clima extremo, água e irrigação, preço e mercado, crédito e seguro). O produtor relata, a IA classifica tipo e urgência, o técnico da assistência técnica aprova e um robô envia um e-mail ao órgão ou à cooperativa. Global Solution 2026.2 da FIAP. **Prazo: 19/11/2026, 23h55, Portal do Aluno** (cada disciplina é entregue ao seu professor). Meta interna: fechar até 18/11.

Esta versão cobre só as três matérias do Murilo (RPA, Front-end e Cluster) e deixa slots abertos para as outras. Existe um projeto irmão, o Plano B (tema de enchente, nove disciplinas), em outra pasta. O tema muda trocando `backend/app/dominio.py`, as regras em `pipelines/triagem.py` e os dados em `data/gerar_dados.py`.

O PDF oficial da GS (slides de 04/11/2026) fixa só o desafio CitizenTech; o problema é escolha do grupo. Cada disciplina pede uma peça aplicada ao protótipo, e a Governança integra todas (vídeo de até 7 min, documentação ABNT e GitHub).

## Quem faz o quê (a confirmar)
- Murilo: AI for RPA, Front-end e Mobile, Cluster Computing.
- Colega 1: Computação Quântica, Visão Computacional, PLN.
- Colega 2 (por eliminação): Governança em IA, IoT, Generative AI.

## Arquitetura
- `backend/app` (FastAPI): `routers/` endpoints, `schemas/` Pydantic, `pipelines/` lógica (anonimização, triagem, RPA), `providers/` (SQLite, ViaCEP, LLM), `modulos/` (encaixe das outras matérias).
- `frontend` (Streamlit): `features/` telas, `ui/` componentes, `state/`, `providers/api_client.py`.
- A triagem usa LLM só se `GEMINI_API_KEY` e `GEMINI_MODEL` estiverem no `.env`; sem isso usa regras. Chaves nunca vão para o repositório.

## Pontos de encaixe (contratos)
- `POST /modulos/visao/analisar` (multipart `imagem`) → `VisaoSaida {disponivel, tipo_dano, confianca, caixas[], latencia_ms, mensagem}`. Implementar `analisar(imagem_bytes) -> dict` em `backend/app/modulos/impl_visao.py`.
- `POST /modulos/assistente/perguntar` → `AssistenteSaida {resposta, fontes[], abstencao}`. Implementar `perguntar(entrada)` em `backend/app/modulos/impl_assistente.py` (neste projeto o arquivo não existe, então o sistema devolve o stub).
- `POST /relatos`, `GET /relatos`, `PATCH /relatos/{id}/decisao`, `POST /relatos/{id}/feedback`, `POST /rpa/executar`, `GET /health`.
- Contratos completos: `backend/app/schemas/modulos.py` e `backend/app/modulos/registro.py`. A tela "Módulos" do front mostra o que está integrado.

## Como rodar e testar
```bash
cp .env.example .env
pip install -r backend/requirements.txt -r frontend/requirements.txt
cd backend && uvicorn app.main:app --port 8000      # API
cd frontend && streamlit run app.py                 # interface
cd backend && python rpa_run.py                     # robô em lote
cd backend && pytest -q                             # 33 testes
cd frontend && pytest -q                            # 7 testes
cd backend && python avaliar.py casos_novos_2       # triagem (casos_teste, casos_novos, casos_novos_2)
```

## Estado por disciplina
| Disciplina | Estado | O que falta |
|---|---|---|
| AI for RPA | Pronta no código (Pandas, ViaCEP, SQLite idempotente, e-mail, quarentena, log, disjuntor). Tema rural adaptado | Revisar rótulos dos 60 casos, medir com LLM ligado, demonstrar uma falha tratada no vídeo, texto de ética e ODS. Opcional: scraping de preços |
| Front-end | Pronta no código (camadas, cache, acessibilidade, Plotly, testes) | Testar Docker (nunca rodou), teste com 3 pessoas e um ajuste, tabela de casos da IA, vídeo (≤5 min), campos `[PREENCHER]` do README |
| Cluster | Só o kit (`docs/cluster/PARAMETROS.md`, `calcular_ganho.py`) | Modelar no iSPD (2 e 4 workers), capturas, tabela, análise, relatório de 2 a 4 páginas. **Só a pessoa com o iSPD consegue** |
| Visão, IoT, Quântica, Governança | Não iniciadas. Cada pasta de `entregas_externas/` tem um LEIAME com o obrigatório e ideias para o tema rural | Tudo |
| Generative AI, PLN | Não incluídas nesta versão | Tudo (o Plano B tem uma versão pronta, com tema de enchente, que pode servir de modelo) |

## Regras que valem para quem continuar
1. Não invente métrica, resultado ou fonte. Número só entra se foi medido; o que for rascunho ou otimista deve estar marcado assim.
2. Dados sintéticos ou públicos apenas. Nada de dado pessoal real, chave, `.env`, PDFs grandes ou banco no git.
3. Cada integrante entrega, entende e defende as próprias matérias. Não sobrescreva a entrega de outra pessoa sem combinar.
4. Vídeos: um por matéria, sem repetir o mesmo vídeo (risco de plágio). Limites: Front, GenAI e PLN até 5 min, Governança de 5 a 7.
5. Textos de justificativa, ética e conclusão devem ser escritos ou reescritos pelo grupo.
6. O sistema classifica e encaminha; não dá recomendação agronômica.
7. Rode os testes antes de cada commit. Não ajuste as regras olhando `casos_novos_2.csv`: ele é o conjunto de medição honesta.

## Limites conhecidos
- Triagem só por regras: 55% de tipo e 30% de urgência em 20 casos nunca usados para ajustar (`data/casos_novos_2.csv`). Os 100% do conjunto 1 e os 100%/95% do conjunto 2 são de regras ajustadas nos mesmos casos. Falta medir com o LLM ligado.
- Falha de segurança observada nas regras: relato de intoxicação ("boca queimando") saiu como urgência baixa. Mitigação: relato triado só por regras e classificado como "outro" vai para revisão humana.
- Fila de revisão: 36 de 52 relatos do lote sintético ficam para revisão humana sem LLM, o que é muito.
- Anonimização: regex e frase-gatilho ("meu nome é"). Nomes soltos podem passar.
- ViaCEP: sem rede o robô segue sem cidade; os CEPs sintéticos de municípios do interior de SP não foram conferidos online.
- Docker: arquivos escritos, nunca executados.
- Fontes do problema: WRI Brasil/Censo 2017 e CPI. Não medem o volume de relatos nem o tempo perdido na triagem; isso é hipótese do grupo.
