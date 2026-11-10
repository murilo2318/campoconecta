# Cluster Computing: parâmetros e modelo de relatório

O iSPD é o simulador exigido e é uma aplicação gráfica. Esta pasta só prepara os números e o texto. Os dois cenários (2 e 4 workers) precisam ser montados e executados no iSPD pelo grupo.

## 1. Tarefa simulada (preencher)

Tarefa repetida escolhida: classificar relatos do CampoConecta em lote (o mesmo passo que o robô faz em cada relato).

| Parâmetro | Valor | Unidade | Origem |
|---|---|---|---|
| Quantidade de tarefas | (definir, ex.: número de relatos de um dia de temporal) | tarefas | Hipótese declarada |
| Tamanho computacional por tarefa | (calcular abaixo) | MFlops | Hipótese a partir de medição |
| Comunicação por tarefa (entrada) | (tamanho médio de um relato em JSON) | MB | Hipótese declarada |
| Comunicação por tarefa (saída) | (tamanho médio da triagem em JSON) | MB | Hipótese declarada |

Como justificar o tamanho computacional: o robô registra `tempo_medio_por_relato_s` no `relatorio_execucao.json`. Com a capacidade de referência da máquina em MFlops (informar como hipótese), `MFlops_por_tarefa = tempo_medio_por_relato_s × capacidade_MFlops`. Na execução de demonstração sem rede e sem LLM, o robô mediu cerca de 0,13 s por relato; com LLM real o tempo é dominado pela espera de rede e deve ser medido de novo.

## 2. Cenários (iguais em tudo, exceto o número de workers)

| Parâmetro | Cenário A | Cenário B |
|---|---|---|
| Workers | 2 | 4 |
| Capacidade de cada worker (MFlops) | igual | igual |
| Escalonador | igual | igual |
| Banda (Mbps) | igual | igual |
| Latência (ms) | igual | igual |
| Carga total | igual | igual |

## 3. Resultados (preencher depois da simulação)

| Indicador | 2 workers | 4 workers |
|---|---|---|
| Total Simulated Time (s) | | |
| Tarefas por worker (aba Resources) | | |
| Uso de cada worker | | |

Depois de preencher T2 e T4, rode `python calcular_ganho.py T2 T4`.

## 4. Estrutura sugerida do relatório (2 a 4 páginas)

1. Vínculo com o desafio: função de IA do protótipo e por que essa tarefa foi simulada.
2. Parâmetros: tabelas acima, com unidades.
3. Comparação: capturas legíveis dos dois cenários e tabela de resultados.
4. Discussão: redução percentual, razão T2/T4, distribuição da carga, gargalos (mestre, comunicação) e limites de extrapolar a simulação para o protótipo real.
5. Reprodução: arquivos do iSPD ou capturas e parâmetros suficientes para refazer.
