# Reproduzir os cenários

É necessário um JDK (foi usado Temurin 21.0.13) e o JAR iSPD 2.0 oficial da UNESP. Não é necessário instalar o Java globalmente: podem-se usar os caminhos completos de `javac` e `java` de uma pasta extraída.

Na pasta deste documento, com o JAR em `/caminho/iSPD.jar`:

```bash
mkdir -p build resultados/2_workers resultados/4_workers
javac -cp /caminho/iSPD.jar -d build ExecutarCenarios.java
java -Djava.awt.headless=true -cp /caminho/iSPD.jar:build ExecutarCenarios modelos/cenario_2_workers.imsx resultados/2_workers
java -Djava.awt.headless=true -cp /caminho/iSPD.jar:build ExecutarCenarios modelos/cenario_4_workers.imsx resultados/4_workers
python calcular_ganho.py 34.003399999999914 17.005719999999958
```

No Windows, o separador do classpath é `;`, em vez de `:`. Para abrir a janela oficial Results com os valores da mesma execução, remover `-Djava.awt.headless=true` e acrescentar `--gui` ao fim. A janela deve ser encerrada depois de salvar as capturas.

Os arquivos `.imsx` são topologias válidas do iSPD. O adaptador lê a topologia, cria 500 tarefas com entrada de 0,016 Mbit, retorno de 0,008 Mbit, computação de 136 MFlops e chegada em 0 s, executa o motor oficial e exporta métricas. Ele é necessário porque o formulário/XML do iSPD 2.0 não expõe retorno separado. Simular somente o `.imsx` pela GUI utiliza a configuração de retorno padrão do gerador e pode produzir outro tempo.

O CSV `recursos.csv` usa ponto decimal. A contagem é observada nas tarefas concluídas por worker; o uso é derivado de segundos ocupados/tempo total. `resultado.json` guarda o Total Simulated Time sem arredondamento. `result.html` é produzido pelo exportador do próprio JAR, sem gráficos na execução headless.

## Custo real e carga sintética

Segundo a medição fornecida pelo usuário, **o custo de CPU da anonimização e das regras de triagem, sem rede, banco e e-mail, foi de cerca de 51 µs por relato (0,000051 s), medido em máquina de 2 vCPUs (não no equipamento do grupo)**. O resultado é a mediana de cinco rodadas sobre 60 textos, em x86_64 com Python 3.13. Não foi medido novamente nesta execução. Os comandos acima reproduzem o cenário sintético de **136 MFlops por tarefa** e seus tempos de **34,003400 s e 17,005720 s**. Não reproduzem uma calibração para 51 µs.

Com a capacidade hipotética de 1.000 MFlops por worker, a conversão desse custo seria `0,000051 × 1.000 = 0,051 MFlops por tarefa`. Para estudar essa carga, seria necessário alterar tanto o tamanho computacional nos dois modelos quanto o valor usado pelo adaptador e executar novas simulações, preservando todos os demais parâmetros. Não substituir os tempos atuais por estimativas nem reutilizar seu ganho como resultado da nova carga.
