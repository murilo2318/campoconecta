# Requisitos da Global Solution 2026.2: obrigatório x em aberto

Prazo final informado: **19/11/2026, 23h55**, pelo Portal do Aluno; meta interna: **18/11/2026**. Os campos e eventuais instruções específicas de cada professor no Portal ainda não foram conferidos em sessão autenticada.

Integrantes: **Pedro Leal Murad — RM565460; Murilo Benhossi — RM562358; Nicolas Lemos Ribeiro — RM553273**.

Legenda: ✅ evidência local disponível para o item, 🟡 parcial, ⬜ pendente. O status não certifica nota, conformidade jurídica ou submissão ao Portal. Evidência consolidada: [`validacao/RELATORIO_EXECUCAO.md`](validacao/RELATORIO_EXECUCAO.md).

## Parte 1. Matérias deste trio (RPA, Front-end e Cluster)

### AI for RPA (peso na nota da disciplina)

| Critério | Peso | Mínimo exigido pelo enunciado | Status | Onde está |
|---|---|---|---|---|
| Uso dos temas | 30% | Pelo menos 3 temas da disciplina, cada um com função real no fluxo, e quadro de temas no README | ✅ 4 temas em uso (Pandas, API ViaCEP, SQL, e-mail); quadro no README, seção 4 | `backend/app/pipelines/rpa/`, `providers/` |
| Funcionamento ponta a ponta | 25% | Entrada, processamento com IA e saída em execução contínua; README permite rodar sem ajuda | ✅ | `backend/rpa_run.py` |
| Resiliência e segurança | 20% | Exceções tratadas, dados inválidos, caminho seguro, log, chaves fora do código | ✅ | `robo.py`, `viacep.py`, `.env.example` |
| Evidências de validação | 15% | Execução com dados de teste, resultado medido em amostra, pelo menos 1 caso de falha tratado e demonstrado | 🟡 60 rótulos revisados e regras medidas: tipo/urgência 100%/90%, 100%/95% e 55%/30% nos três conjuntos. RPA: 52 processadas, 3 rejeitadas, 0 falhas; gravação local RPA pronta, arquivo público no repositório; formato de link a confirmar no Portal. Medição Gemini não realizada | `backend/avaliar.py`, `data/casos_teste.csv` |
| Dados, ética, ODS e organização | 10% | Parágrafo sobre proteção de dados, ética e ODS; entrega organizada e no prazo | 🟡 Parágrafo escrito, medidas e limites declarados; envio no prazo ainda não comprovado | README, seção 7 |

Regras do enunciado: LLM é opcional; só dados sintéticos ou públicos; nenhuma chave no repositório; ponto de entrada claro.
Diferenciais já atendidos: timeout, retry com espera, idempotência, disjuntor, relatório de execução, revisão humana, quarentena.
Em aberto para o grupo: tema de scraping (opcional), uso de LLM real (precisa de chave e modelo no `.env`).

### Front-end em Sistemas de IA (nota máxima 10,0)

| Critério | Nota | Exigência | Status | Onde está |
|---|---|---|---|---|
| Fluxo e integração com IA | 2,0 | Entrada validada, LLM só no back-end com saída Pydantic, resposta útil ao produtor, problema real delimitado | ✅ código e fonte do problema no README (WRI Brasil/Censo 2017 e CPI sobre o Pronaf, com limites declarados) | `routers/relatos.py`, `schemas/relato.py` |
| Arquitetura | 2,0 | Front e back separados, camadas `features/ ui/ state/ providers/` e `routers/ schemas/ pipelines/ providers/` | ✅ | `frontend/`, `backend/app/` |
| Estado, performance, robustez | 1,5 | `session_state`, `st.cache_data`, falhas tratadas, segredos fora do repo, CORS restrito | ✅ | `state/store.py`, `main.py` |
| UX/UI, acessibilidade, visualização | 2,0 | Layout, latência, cores com texto ou ícone, human-in-the-loop, gráfico Plotly, 2 filtros, componente reutilizável | ✅ | `ui/`, `features/gestor.py` |
| Deploy e repositório | 1,0 | Deploy público ou Docker, README completo, requirements por serviço, `.env.example` | 🟡 Docker build e saúde da API/interface verificados em 10/11/2026; README atualizado. Repositório público criado e código publicado no GitHub | `docker-compose.yml` |
| Justificativa, validação, impacto | 1,5 | Problema e público com fonte, 1 ou 2 ODS, decisões técnicas, ética e limites da IA, teste com pelo menos 3 pessoas com um ajuste, tabela com pelo menos 3 casos de teste da IA | 🟡 Problema, decisões, ética e métricas documentados; teste com três participantes e melhoria motivada pelo feedback feitos (docs/VALIDACAO_FRONT.md) | |

Entregáveis: repositório público único, vídeo de até 5 min (demonstração, código, validação, um erro tratado), link no Portal.
Feito em 10/11/2026: validação com três participantes (o trio do trabalho, com limitações declaradas em docs/VALIDACAO_FRONT.md) e melhoria a partir do feedback. Em aberto: regravar o vídeo do Front com a tela nova; confirmação no Portal do formato dos links dos vídeos próprios já gravados e publicados no repositório. Perfis com autenticação e deploy em plataforma permanecem diferenciais não comprovados. A correção técnica do gráfico de datas não conta como ajuste a partir de feedback humano.

### Cluster Computing (10,0 pontos)

| Critério | Pontos | Exigência | Status |
|---|---|---|---|
| Integração com CitizenTech | 2,0 | Demanda de processamento ligada à função de IA, carga coerente e justificada | ✅ Modelos e vínculo com classificação de relatos em `docs/cluster/`; parâmetros declarados como hipóteses |
| Modelagem no iSPD | 2,0 | Dois cenários, 2 e 4 workers; só o número de workers muda | ✅ Dois cenários executados no iSPD; modelos em `docs/cluster/modelos/` |
| Resultados quantitativos | 2,0 | Capturas e tabela com tempo total e indicadores por recurso, com unidades | ✅ Tabela e quatro capturas nativas conferidas em `docs/cluster/` |
| Análise de desempenho | 3,0 | Comparação crítica, redução percentual, T2/T4, gargalos e limites, sem presumir ganho | ✅ Resultados calculados, análise e limites no relatório de `docs/cluster/` |
| Clareza e reprodução | 1,0 | Relatório de 2 a 4 páginas, arquivos do iSPD ou capturas suficientes | ✅ Modelos, adaptador, capturas e relatório final de quatro páginas; PDF no pacote separado |

O roteiro recebido diz que tamanho computacional e comunicação são hipóteses do modelo, que a carga deve ser a mesma nos dois cenários e que resultado sem ganho pode valer nota integral se bem interpretado. O custo local informado é cerca de 51 µs para anonimização e regras juntas, sem rede, banco e e-mail; mediana de cinco rodadas sobre 60 textos em 2 vCPUs x86_64/Python 3.13, fora do equipamento do grupo. Os resultados do iSPD preservam a carga sintética intensificada de 136 MFlops e não simulam uma calibração de 0,051 MFlops.

## Parte 2. Matérias em aberto (dos outros integrantes)

Cada pasta em `entregas_externas/` (Visão, IoT, Quântica, Governança) tem um `LEIAME.md` com o obrigatório do enunciado e o que o responsável decide.

| Matéria | O que é obrigatório (resumo) | Fica em aberto | Como encaixa | Status |
|---|---|---|---|---|
| Visão Computacional | Detectar manutenção de estruturas (GS 2026.2); ideia para o tema: danos em estradas vicinais. Métricas, integração com imagem e vídeo, latência e FPS | Base, arquitetura, limiar | Endpoint `/modulos/visao/analisar` (arquivo `impl_visao.py`) | ⬜ |
| Generative AI | Assistente com RAG, avaliação por componente e ponta a ponta, 10 perguntas, 2 testes adversariais, vídeo de 5 min | Base, chunking, LLM | Endpoint `/modulos/assistente/perguntar` (arquivo `impl_assistente.py`) | ⬜ Não incluído nesta versão |
| PLN | Fábrica de corpus: ingestão, limpeza, anonimização, 3 corpus JSONL e teste, relatório e vídeo | Tema dos documentos, modelo gerador | Arquivos; o texto puro pode alimentar o RAG | ⬜ |
| IoT | OuviAí no Edge Impulse, 15 gravações de treino e 5 de teste por classe, validação ao vivo no celular | Quais sons | Independente da API | ⬜ |
| Quântica | Gargalo real, capacidade quântica, roadmap, ética, LGPD e ODS, sem programar | Gargalo e capacidade | Documento | ⬜ |
| Governança | Vídeo de 5 a 7 min com todos os módulos, repositório, relatório ABNT de 10 a 15 páginas, conclusão do grupo | Quem consolida | Consolida todas as matérias | ⬜ |

## Avisos e pontos a confirmar com os professores

- Fonte: slides oficiais da GS 2026.2 (PDF de 04/11/2026). O tema CitizenTech é fixo; o problema é escolha do grupo. A entrega vai ao professor de cada disciplina até 19/11, 23h55. O vídeo pitch de até 7 min com solução integradora concorre ao prêmio e vai na disciplina indicada (provável Governança: confirmar).
- Limite de integrantes: RPA diz até 5, o deck geral diz trio, dupla ou individual, Front e GenAI até 3.
- Vídeos: Front e GenAI até 5 min, PLN até 5 min, Governança de 5 a 7 min. Cada matéria tem um vídeo próprio, e vídeos iguais podem ser tratados como plágio.
- PLN: o PDF se chama "GS 2027" e o prazo está como "a definir pelo professor".
- Quântica: o texto recebido não traz formato de entrega nem data.
- Governança: commit depois da entrega pode reduzir a nota. Congelar o repositório no prazo.
- Conclusões e textos de análise devem ser escritos pelo grupo. Evitar jargão de IA, hipérboles e travessões em excesso.

## Pendências de pessoas, acesso e entrega

- **Validação humana:** três participantes ainda precisam usar a tela e fornecer feedback real; não foram inventadas falas ou aprovações. Registrar o feedback e um ajuste decorrente dele continua obrigatório no roteiro recebido.
- **Gemini:** chave/modelo e execução real ainda não confirmados; as métricas documentadas são de regras. LLM opcional no roteiro de RPA não transforma resultado de regras em medição de LLM.
- **GitHub e vídeos:** integrantes/RMs já constam no README; repositório e arquivos de vídeos publicados em https://github.com/murilo2318/campoconecta . Confirmar formato aceito no Portal. As gravações distintas de Front e RPA estão em docs/videos/.
- **Portal do Aluno:** não houve conferência autenticada nem envio comprovado a RPA, Front ou Cluster. Não marcar entrega concluída sem recibo do Portal.
- **Fontes do roteiro:** a tabela resume os materiais recebidos no pacote. As exigências específicas de cada professor no Portal prevalecem quando forem conferidas.


Atualização Cluster: capturas nativas das abas Global/Results e Resources dos dois cenários incluídas em docs/cluster/resultados/. Tempos conferidos: 34,0034 s e 17,0057 s. O relatório distingue o custo local informado de 51 µs (anonimização e regras) da carga sintética de 136 MFlops usada nos cenários.
