# Relatório da execução - CampoConecta v2

Data: 10/11/2026. Base: CampoConecta_planoA_v2.zip fornecido pelo usuário. A v1 foi apenas diagnóstico e não é a entrega atualizada.

## Execução confirmada

- Python 3.12.6 em ambiente isolado; dependências dos dois serviços instaladas.
- Backend: 33 testes aprovados; aviso de depreciação Starlette/httpx.
- Frontend inicial: 7 aprovados. O fluxo real encontrou falha do gráfico temporal com datas de formatos mistos do lote e da API. Regressão reproduziu AttributeError: Can only use .dt accessor with datetimelike values. Correção normaliza datas com format="mixed", utc=True e errors="coerce". Datas inválidas ficam fora do gráfico.
- Frontend após a correção: 8 testes aprovados (7 originais e 1 regressão). A regressão passou também na imagem Docker reconstruída.
- Docker Compose: build e inicialização reais concluídos. API /health e interface /_stcore/health responderam HTTP 200. Não houve erro de build do projeto; o serviço Docker estava inicialmente desligado e foi iniciado.
- RPA local sem rede/LLM: 55 linhas lidas, 52 processadas, 3 rejeitadas, 0 falhas de linha; 4,886 s, 0,094 s/relato e 36 casos para revisão humana.
- RPA na gravação Docker com rede: 52 processadas, 3 rejeitadas, 0 falhas; 29 CEPs resolvidos, 12,149 s e 0,2336 s/relato. ViaCEP recusou outros CEPs e o fluxo continuou. Sem Gemini e sem SMTP; e-mail foi salvo em arquivo, não enviado. Essa medição difere da carga sintética intensificada usada no Cluster e da execução local sem rede.
- Rejeições demonstradas: id duplicado, descrição vazia e data inválida (quarentena).
- Fluxo visual real: entrada curta rejeitada com mensagem; relato sintético de bomba de irrigação recebido e classificado; acesso ao gestor, comentário e aprovação; filtro Aprovado confirmou o mesmo relato e comentário. Conferência API também retornou201 na criação e200 na aprovação.

## Revisão dos 60 rótulos e medição

Foram revisados 20 casos em cada um dos três CSVs. Somente as urgências dos casos 14 e 16 de casos_teste.csv foram corrigidas de média para baixa: informações Pronaf e contratação de seguro, sem dano/prazo declarado. Tipos e textos foram preservados. Os outros dois conjuntos não foram alterados. A revisão detalhada registra ambiguidades e não adapta os rótulos para favorecer as regras.

|Conjunto|Acerto tipo|Acerto urgência|
|---|---:|---:|
|casos_teste (revisado)|100%|90%|
|casos_novos|100%|95%|
|casos_novos_2|55%|30%|

Resultados somente com regras, Gemini explicitamente desativado. Não são resultados de LLM. O conjunto mais difícil evidencia limites de generalização; os exemplos não equivalem a validação com produtores reais.

## Cluster

Motor oficial iSPD2.0 com adaptador da API pública para o retorno exato0,001 MB.500 tarefas,136 MFlops/tarefa,1000 MFlops/worker,RoundRobin,100 Mbps e 1 ms, todas hipóteses declaradas. Dois workers: 34,003400s,250 tarefas por worker. Quatro: 17,005720s,125 por worker. Redução 49,988178%,speedup 1,999527. Relatório de 4 páginas, fontes, modelos, adaptador, logs, resultados por recurso e capturas das exportações HTML oficiais em ../cluster/. Capturas nativas de Global/Results e Resources dos dois cenários foram concluídas e conferidas em 10/11/2026; os tempos coincidem com as métricas já registradas.

## Vídeos locais

- ../videos/front.mp4: gravação real,2min51,739s, abaixo de5min. Mostra erro de validação, envio, classificação, aprovação, métricas e código. Sem narração. O teste com pessoas ainda não integra a gravação.
- ../videos/rpa.mp4: gravação distinta, execução real 41,975 s, via painel temporário que transmite a saída do comando no container e mostra linhas da quarentena. Sem narração. O painel de gravação é uma ferramenta temporária e não uma tela de produto.

Os arquivos estão publicados no repositório GitHub. O Portal ainda precisa ser consultado para confirmar se esse formato de hospedagem/link é aceito.

## Situação das pendências

1. Gemini: chave e modelo ausentes. A medição com LLM ainda não ocorreu.
2. Teste com 3 participantes: realizado em 10/11/2026 e registrado em ../VALIDACAO_FRONT.md, com melhoria implementada a partir do feedback (protocolo, aviso de status e explicação de regras vs. IA). O ajuste de datas dos gráficos é um bug técnico à parte.
3. GitHub: publicação autorizada e executada em 10/11/2026 em https://github.com/murilo2318/campoconecta . O acesso ao gh foi validado com rede disponível. Conferência prévia excluiu .env, bancos, PDFs e logs de configuração resolvida.
4. Portal: a conferência dos campos e a submissão são feitas pelo grupo na área do aluno.
5. Capturas nativas Results/Resources concluídas, com 34,0034 s e 17,0057 s confirmados.

## Alterações do projeto

frontend/ui/graficos.py; frontend/tests/test_graficos.py; data/casos_teste.csv (duas urgências); README.md (integrantes,ética,métricas/status); .gitignore ampliado para excluir segredos,bancos ePDFs; novos arquivos em docs/cluster,docs/validacao e docs/videos. Regras de classificação preservadas.


Atualização do custo local informada pelo usuário: o custo de CPU da anonimização e das regras de triagem, sem rede, banco e e-mail, foi de cerca de 51 µs por relato, medido em máquina de 2 vCPUs x86_64 com Python 3.13 (não no equipamento do grupo). Trata-se da mediana de cinco rodadas sobre 60 textos; não foi medido no Mac desta execução. Os cenários de 136 MFlops continuam identificados como carga sintética intensificada, sem atribuí-los ao custo local atual.


Atualização Front: avaliação automatizada em três contextos isolados registrada em ../VALIDACAO_FRONT.md, com os rótulos Perfil de teste 1, Perfil de teste 2 e Perfil de teste 3. Envios, triagem, histórico e avaliação foram verificados. A tentativa com CEP inválido apagava o rascunho e apresentava um cartão anterior; o formulário agora preserva os campos e retorna antes desse cartão na tentativa inválida. Regressão reproduziu a falha antes e passou depois; suíte final: 9 passed in 2.12s. Docker reconstruído e nova conferência visual concluída. A classificação de consulta negando urgência ainda deve ser revisada. Os perfis não são pessoas reais e não cumprem o requisito de três participantes. As observações são do agente; a tabela para a coleta com participantes está em ../VALIDACAO_FRONT.md e permanece A PREENCHER.


Nota: os logs detalhados do Docker (compose, HTTP, build do web e instalação do pytest) não fazem parte deste repositório; ficam com o grupo e podem ser enviados a pedido.
