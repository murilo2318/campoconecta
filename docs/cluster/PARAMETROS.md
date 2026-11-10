# Cluster Computing: parâmetros e interpretação dos resultados

Os dois cenários foram executados no motor oficial iSPD 2.0. Os modelos, o adaptador, os comandos e os resultados estão nesta pasta. A evidência gráfica nativa e sua situação atual são descritas no relatório.

## 1. Tarefa e custo real informado

Tarefa repetida: anonimizar e classificar um relato do CampoConecta em lote. Segundo a medição fornecida pelo usuário, **o custo de CPU da anonimização e das regras de triagem, sem rede, banco e e-mail, foi de cerca de 51 µs por relato (0,000051 s), medido em máquina de 2 vCPUs (não no equipamento do grupo)**. Inclui expressões regulares/frases-gatilho da anonimização e regras de tipo e urgência; exclui ViaCEP, SQLite, geração de .eml e demais etapas do robô. O valor é a mediana de cinco rodadas sobre 60 textos, em x86_64 com Python 3.13. Ele substitui a referência anterior de custo por relato; não foi realizado um novo benchmark nesta execução.

Com a capacidade hipotética de 1.000 MFlops por worker, a conversão seria `0,000051 × 1.000 = 0,051 MFlops por tarefa`. Essa conta é uma calibração aproximada, não uma medição direta de MFlops. O tempo médio do robô completo inclui outras etapas e não deve ser usado como custo isolado da classificação sem delimitar o que foi medido.

## 2. Cenários sintéticos executados

| Parâmetro | Cenário A | Cenário B | Origem |
|---|---|---|---|
| Workers, além de um mestre | 2 | 4 | Variável experimental |
| Capacidade por worker e mestre | 1.000 MFlops | igual | Hipótese |
| Carga disponível no instante zero | 500 tarefas | igual | Hipótese de semana de safra em lote |
| Computação por tarefa | 136 MFlops | igual | Carga sintética intensificada; não representa 51 µs |
| Entrada por tarefa | 0,002 MB = 0,016 Mbit | igual | Hipótese |
| Saída por tarefa | 0,001 MB = 0,008 Mbit | igual | Hipótese, configurada pelo adaptador |
| Banda e latência | 100 Mbps; 1 ms | igual | Hipótese |
| Escalonador | RoundRobin | igual | Controle experimental |

A única diferença entre os modelos executados é o número de workers. Os **136 MFlops por tarefa** foram preservados para comparar com os resultados já medidos; não devem ser apresentados como custo real atual. Recalibrar para **0,051 MFlops** requer alterar ambos os modelos e o adaptador e executar novamente os dois cenários. Com computação muito menor, a comunicação pode dominar e o ganho pode mudar.

## 3. Resultados do cenário sintético de 136 MFlops

| Indicador | 2 workers | 4 workers |
|---|---|---|
| Total Simulated Time | 34,003400 s | 17,005720 s |
| Tarefas por worker | 250; 250 | 125; 125; 125; 125 |
| Uso de cada worker | 99,990001% | 99,966364% |

O uso é derivado de segundos ocupados divididos pelo tempo simulado. A coluna “Processing performed” da versão usada apresenta segundos, não quantidade de tarefas.

O cálculo foi executado com `python calcular_ganho.py 34.003399999999914 17.005719999999958`: redução de 49,988178%, razão T2/T4 de 1,999527 e eficiência relativa de 99,976361%, antes do arredondamento do script.

## 4. Limite de interpretação

Os resultados acima comprovam o comportamento do cenário sintético de 136 MFlops. Eles não são resultados de uma carga calibrada ao custo real informado de 51 µs, nem incluem a espera por Gemini, ViaCEP, banco, aprovação humana ou e-mail. O relatório de duas a quatro páginas deve manter essa distinção, explicar gargalos e apresentar fontes, comandos e evidências suficientes para reprodução.
