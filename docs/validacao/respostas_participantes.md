# Respostas dos participantes (Teste com pessoas reais)

Respostas dos três integrantes do grupo que testaram a tela em 10/11/2026, seguindo o formulário do roteiro. Os nomes foram retirados e os participantes aparecem como Participante 1, 2 e 3. Só foram feitos ajustes de forma (numeração e rótulos); o conteúdo é o enviado por eles. O Participante 1 é o autor do projeto. Os três são estudantes com muita familiaridade com computador; nenhum é produtor rural (ver limitações em docs/VALIDACAO_FRONT.md).

## Teste 1 (Participante 1)

Participante 1 — estudante; familiaridade com computador: muita
Data do teste: 10/11/2026

1. O que você tentou fazer, em ordem: Baixei o repositório por Git, usei o Docker Desktop já instalado, copiei a configuração de exemplo e executei docker compose up --build -d. Abri http://localhost:8501 e enviei “A bomba do poço quebrou e a horta está sem água desde ontem.” sem CEP. A tela confirmou o recebimento, classificou como “Água e irrigação”, com “Urgência ALTA”, e sugeriu “Secretaria de Agricultura (recursos hídricos)”. Considerei o tipo coerente com o problema e a prioridade alta plausível pela falta de água já em curso. Tentei enviar novamente com CEP 123. A tela recusou com “O CEP precisa ter 8 dígitos. Se não souber, deixe em branco.” e manteve o texto digitado. Abri “Meus relatos” e encontrei o envio original com a mesma classificação e status “Aguardando análise”.

2. Onde você travou ou ficou em dúvida: Não houve bloqueio no roteiro pela tela. Fiquei em dúvida sobre o prazo de análise e sobre como acompanhar o relato depois de encerrar a sessão, pois o histórico se apresenta como “Meus relatos nesta sessão”. Na preparação, o roteiro recebido não mencionava copiar .env.example para .env, necessário na configuração Docker presente no projeto.

3. O que você achou confuso (com suas palavras): O cabeçalho fala em análise por IA, mas o resultado informa “Classificação feita por regras automáticas”. A tela explica que haverá conferência humana, porém não informa quando isso ocorrerá nem como o produtor receberá retorno. “Encaminhamento sugerido” é compreensível, mas exige atenção para perceber que ainda não houve encaminhamento.

4. O que você mudaria na tela: Colocaria junto ao status uma explicação curta: “Seu relato foi registrado. Aguarda conferência; ainda não foi encaminhado.” Também mostraria um protocolo que pudesse ser guardado, instruções para acompanhar o caso após sair da sessão e, se houver um prazo definido pelo serviço, esse prazo. Ajustaria a apresentação para explicar que a classificação pode usar regras automáticas.

5. Você entendeu o que o sistema fez com o seu relato? (sim / mais ou menos / não) Por quê? Sim. A interface confirmou o registro, mostrou tipo e urgência, identificou o uso de regras automáticas e avisou que uma pessoa conferirá o caso antes de qualquer ação. O CEP inválido foi rejeitado com orientação de correção.


## Teste 2 (Participante 2)

Participante 2 — estudante; familiaridade com computador: muita
Data do teste: 10/11/2026

1. O que você tentou fazer, em ordem: Enviei o relato sobre a bomba quebrada e a horta sem água. Conferi a classificação “Água e irrigação” e a urgência alta. Depois tentei enviar com o CEP 123 e, por último, procurei o registro em “Meus relatos”.

2. Onde você travou ou ficou em dúvida: O envio funcionou. A dúvida foi sobre o que acontece depois de aparecer “Aguardando análise”: não encontrei um prazo nem uma indicação de como receber o retorno.

3. O que você achou confuso (com suas palavras): A sugestão de encaminhamento pode dar a impressão de que a Secretaria de Agricultura já recebeu o problema. O aviso sobre conferência humana ajuda, mas poderia ficar mais próximo do status.

4. O que você mudaria na tela: Acrescentaria uma mensagem dizendo que o relato foi salvo e ainda aguarda conferência antes do encaminhamento. Também mostraria um protocolo para acompanhamento.

5. Você entendeu o que o sistema fez com o seu relato? (sim / mais ou menos / não) Por quê? Sim. O sistema registrou o texto, classificou o problema e sugeriu um destino. A tela informou que uma pessoa precisa conferir antes de qualquer ação.

## Teste 3 (Participante 3)

Participante 3 — estudante; familiaridade com computador: muita
Data do teste: 10/11/2026

1. O que você tentou fazer, em ordem: Escrevi a frase solicitada e enviei sem CEP. O resultado foi “Água e irrigação”, com urgência alta. Repeti a tentativa usando 123 no CEP. O sistema pediu oito dígitos e manteve a descrição preenchida. Em “Meus relatos”, encontrei o envio original.
2. Onde você travou ou ficou em dúvida: Não houve bloqueio no formulário. Fiquei em dúvida se conseguiria encontrar o relato depois de fechar a página, porque o histórico diz “Meus relatos nesta sessão”.
3. O que você achou confuso (com suas palavras): A apresentação fala em inteligência artificial, mas o resultado diz que a classificação foi feita por regras automáticas. Falta uma explicação simples sobre essa diferença.
4. O que você mudaria na tela: Explicaria que a classificação pode usar regras automáticas e informaria como guardar ou consultar o relato após sair da sessão. Manteria a mensagem do CEP inválido, pois ela explica como corrigir o preenchimento.
5. Você entendeu o que o sistema fez com o seu relato? (sim / mais ou menos / não) Por quê? Sim. O registro e a classificação ficaram claros, e o tipo identificado combina com a falta de água descrita. Ainda faltam informações sobre o acompanhamento e o retorno após a análise humana.
