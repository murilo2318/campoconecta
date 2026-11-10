# Respostas dos participantes (teste com pessoas reais)

Respostas dos três integrantes do trio que faz o trabalho (Participante 1 é o autor do projeto; Participantes 2 e 3 são os outros dois membros da equipe), que testaram a tela em 10/11/2026, seguindo o formulário do roteiro. Os nomes foram retirados e os participantes aparecem como Participante 1, 2 e 3. Cada um reescreveu a própria resposta com suas palavras; o conteúdo é o dele. Os três são estudantes com muita familiaridade com computador; nenhum é produtor rural (ver limitações em docs/VALIDACAO_FRONT.md).

## Teste 1 (Participante 1)

Participante 1: estudante; familiaridade com computador: muita

Data do teste: 10/11/2026

**O que você tentou fazer, em ordem:** Clonei o repositório via Git, peguei o Docker Desktop que já estava no meu PC, copiei o arquivo de config de exemplo e rodei um docker compose up --build -d. Acessei o localhost:8501 e mandei o texto da bomba quebrada sem preencher o CEP. O sistema recebeu certinho, já marcou como "Água e irrigação" e deu urgência ALTA (o que faz todo sentido, já que a horta tava sem água). Depois fiz o teste de colocar só "123" no CEP. Ele barrou avisando que precisava de 8 dígitos ou era pra deixar em branco, mas pelo menos não apagou o texto que eu já tinha digitado. Fui na aba "Meus relatos" e tava lá o primeiro envio, classificado e "Aguardando análise".

**Onde você travou ou ficou em dúvida:** Na tela em si, fluiu bem, não travei em nada. Minha principal dúvida foi sobre o tempo que leva essa análise e como o usuário acompanha isso depois que fecha o site, já que ali diz "Meus relatos nesta sessão". Ah, um detalhe de infraestrutura: o roteiro de testes não avisava que precisava copiar o .env.example para o .env para subir o Docker.

**O que você achou confuso (com suas palavras):** Achei meio contraditório o cabeçalho falar de IA, mas no resultado aparecer que a classificação foi por "regras automáticas". Outra coisa: avisa que vai ter conferência humana, mas não diz quando nem como vão dar um retorno para o produtor. Aquele "Encaminhamento sugerido" dá pra entender, mas se a pessoa ler correndo, pode achar que já foi mandado pro órgão responsável.

**O que você mudaria na tela:** Eu deixaria o status mais claro, algo tipo: "Relato registrado. Aguardando conferência antes do envio". Seria legal também gerar um número de protocolo para a pessoa anotar, colocar uma estimativa de prazo (se existir) e explicar melhor como acompanhar o caso depois. E claro, daria uma ajustada nessa questão de IA vs Regras Automáticas para não confundir o usuário.

**Você entendeu o que o sistema fez com o seu relato?** Sim. Deu pra ver que ele registrou, classificou o tipo de problema e o nível de urgência, e deixou bem claro que alguém vai olhar antes de seguir com o processo. O teste de erro do CEP também funcionou bem e orientou o preenchimento.

## Teste 2 (Participante 2)

Participante 2: estudante; familiaridade com computador: muita

Data do teste: 10/11/2026

**O que você tentou fazer, em ordem:** Joguei lá o texto sobre a bomba que quebrou e a horta sem água. O sistema classificou logo como "Água e irrigação" com urgência alta. Depois fiz o teste forçando o CEP "123" para ver o que acontecia e, no fim, fui dar uma olhada na tela de "Meus relatos".

**Onde você travou ou ficou em dúvida:** Deu tudo certo com o envio, não agarrei em nada. O que pegou mesmo foi o status "Aguardando análise". Fiquei pensando: "tá, mas quanto tempo isso demora? Como é que me avisam depois?".

**O que você achou confuso (com suas palavras):** Aquele lance de "sugestão de encaminhamento" me passou um pouco a sensação de que a Secretaria de Agricultura já tava com o problema na mão. Tem o aviso de que um humano vai conferir o relato, mas acho que ele fica meio solto na tela. Poderia estar mais colado no status.

**O que você mudaria na tela:** Colocaria um aviso bem direto dizendo "Salvo! Aguardando conferência para ser encaminhado". E adicionaria um número de protocolo para facilitar o acompanhamento, com certeza.

**Você entendeu o que o sistema fez com o seu relato?** Sim, entendi de boa. Ele pegou o relato, classificou, sugeriu pra onde mandar e avisou que precisa do aval de um humano antes de rolar qualquer ação.

## Teste 3 (Participante 3)

Participante 3: estudante; familiaridade com computador: muita

Data do teste: 10/11/2026

**O que você tentou fazer, em ordem:** Digitei a frase do teste e mandei sem colocar o CEP. Bateu certinho: classificou como "Água e irrigação" e jogou a urgência lá pra cima. Quando tentei mandar só "123" no CEP, o sistema chiou pedindo 8 dígitos, mas foi bom que não apagou a descrição que eu já tinha escrito. Em seguida, fui no "Meus relatos" e meu primeiro envio estava lá salvo.

**Onde você travou ou ficou em dúvida:** O preenchimento do formulário foi super tranquilo. Minha pulga atrás da orelha foi com aquele título "Meus relatos nesta sessão". Logo pensei: "se eu fechar a aba agora, não vou mais conseguir consultar isso?".

**O que você achou confuso (com suas palavras):** Rolou uma pequena confusão: no começo da página fala de Inteligência Artificial, mas na resposta diz que usou "regras automáticas". Faltou só alinhar isso de um jeito simples para não confundir quem tá usando.

**O que você mudaria na tela:** Eu deixaria mais claro no texto que o sistema pode usar regras automáticas para classificar as coisas. Além disso, colocaria um jeito de a pessoa consultar o relato depois que fechar o navegador. A mensagem de erro do CEP eu não mexeria, achei que ficou excelente e diz exatamente o que tem que fazer.

**Você entendeu o que o sistema fez com o seu relato?** Sim, entendi sim. Ficou nítido como ele leu o texto e fez a classificação (que por sinal acertou bem no problema da água). Só senti falta de saber mesmo quais são os próximos passos de acompanhamento depois que a equipe fizer a análise manual.
