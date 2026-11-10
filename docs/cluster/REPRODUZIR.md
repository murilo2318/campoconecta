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

Os arquivos `.imsx` são topologias válidas do iSPD. O adaptador lê a topologia, cria 500 tarefas com entrada0,016 Mbit, retorno0,008 Mbit, computação136 MFlops e chegada0 s, executa o motor oficial e exporta métricas. Ele é necessário porque o formulário/XML do iSPD 2.0 não expõe retorno separado. Simular somente o `.imsx` pela GUI utiliza a configuração de retorno padrão do gerador e pode produzir outro tempo.

O CSV `recursos.csv` usa ponto decimal. A contagem é observada nas tarefas concluídas por worker; o uso é derivado de segundos ocupados/tempo total. `resultado.json` guarda o Total Simulated Time sem arredondamento. `result.html` é produzido pelo exportador do próprio JAR, sem gráficos na execução headless.
