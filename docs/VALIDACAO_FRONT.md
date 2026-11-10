# Execução automatizada com perfis de teste

**Os perfis abaixo NÃO são pessoas reais e NÃO cumprem o requisito de três participantes.**

Data: 10/11/2026. Interface executada em Docker: http://localhost:8501 . Método: automação do navegador pelo agente, em três contextos isolados, identificados como **Perfil de teste 1**, **Perfil de teste 2** e **Perfil de teste 3**. As observações e sugestões são do agente; não são depoimentos de participantes. A coleta com pessoas reais está registrada mais abaixo, na seção “Teste com participantes reais”.

Este documento foi criado porque docs/VALIDACAO_FRONT.md não existia. O roteiro de referência era validacao/TESTE_COM_PESSOAS.md.

## Execução e triagem observada

| Perfil | Caso enviado | Registro de referência | Tipo / urgência | Avaliação técnica registrada |
|---|---|---|---|---|
| Perfil de teste 1 | Bomba do poço quebrada e horta sem água desde ontem | api-f15a4383 | Água e irrigação / alta | Tipo e encaminhamento coerentes; botão Útil acionado e confirmação exibida |
| Perfil de teste 2 | Lagartas no milho, metade da roça atingida | api-f48e53cf | Praga ou doença / média | Tipo coerente; urgência depende da interpretação da extensão do dano. Botão Útil acionado para verificar o fluxo |
| Perfil de teste 3 | Informações sobre Pronaf para a próxima safra, sem prazo urgente | api-6eb305de | Crédito e seguro / alta | Urgência possivelmente excessiva: a frase nega urgência, mas a regra reconhece palavras de urgência sem interpretar a negação. Botão Incorreta acionado |

Fonte dos três resultados: regras automáticas, sem Gemini. Os cliques acima verificam a gravação e a confirmação do mecanismo de avaliação; não são métricas de satisfação de participantes.

Cada perfil abriu Meus relatos. Perfil de teste 1 mostrou somente seu caso; Perfil de teste 2 mostrou seus dois envios de teste (um envio inicial e uma repetição); Perfil de teste 3 mostrou somente a consulta de crédito. Não houve mistura de relatos entre os históricos das sessões. A primeira execução foi assíncrona: o cartão de Perfil de teste 2 apareceu após a fotografia inicial da tela, resultando em uma repetição pelo agente. Isso foi registrado como ocorrência da execução automatizada, sem atribuir uma dificuldade a uma pessoa.

## O que dificultou o fluxo

| Perfil | Evidência observada | Consequência | Encaminhamento |
|---|---|---|---|
| Perfil de teste 1 | Texto “oi” foi bloqueado com a mensagem de mínimo de dez caracteres | Validação funciona, mas o formulário apagava o texto e mantinha o cartão anterior abaixo do erro | Preservar o rascunho e não apresentar o cartão anterior na tentativa inválida |
| Perfil de teste 2 | Descrição válida com CEP “123” foi bloqueada com mensagem de oito dígitos | A descrição inteira era apagada, exigindo reescrita; o cartão anterior permanecia e podia parecer resultado da nova tentativa | Correção aplicada no formulário |
| Perfil de teste 3 | Consulta com “sem prazo urgente” recebeu urgência alta | O tipo foi identificado, mas a urgência não respeitou a negação | Registrar caso para revisão das regras; não alterar o classificador nesta avaliação |

Não houve travamento fatal da interface durante os envios ou consulta aos históricos. Os problemas acima são distintos: perda de rascunho/exibição de resultado antigo são de interface; a interpretação de negação é uma limitação de triagem.

## Análise de usabilidade por perfil

As sugestões abaixo são hipóteses de melhoria elaboradas a partir do percurso observado, e não citações de falas de participantes.

- **Perfil de teste 1:** o tipo, a urgência e o encaminhamento estão visíveis; a confirmação humana também aparece. Sugestão: preservar o que foi digitado ao pedir correção de um campo.
- **Perfil de teste 2:** a mensagem do CEP explica o formato e permite deixar o campo em branco. A necessidade de reescrever o relato era o principal atrito. Sugestão: manter descrição e CEP disponíveis para edição.
- **Perfil de teste 3:** o botão Incorreta permite contestar a triagem, mas o sistema não explica quais termos produziram a urgência. Sugestão: revisar negações e, futuramente, permitir justificativa da contestação.

## Ajuste aplicado e verificação

Alterações em frontend/features/reportar.py:

1. O formulário preserva seus campos depois de Enviar, permitindo corrigir CEP ou descrição e tentar novamente sem reescrever tudo. Os campos também permanecem após sucesso; o cartão de confirmação identifica o resultado recebido.
2. Após validação inválida ou erro da API, a função retorna antes de renderizar o último cartão, evitando associar um resultado anterior à tentativa atual.

A regressão test_cep_invalido_preserva_rascunho_sem_mostrar_resultado_anterior reproduziu a falha antes da correção: havia um Success com o cartão anterior, mesmo com CEP inválido. Depois da correção, a suíte do frontend aprovou **9 testes em 2,12 s**, incluindo a preservação de descrição/CEP, ausência de resultado antigo e nenhuma segunda chamada à API.

A imagem Docker foi reconstruída e a correção foi conferida pela tela: após enviar um relato válido, preencher CEP “123” e enviar novamente, descrição e CEP permaneceram preenchidos, a mensagem de oito dígitos apareceu e nenhum cartão anterior foi mostrado. Evidência: validacao/perfis_automatizados/cep_invalido_depois.png. Este ajuste deriva de observação técnica no teste automatizado; não é apresentado como cumprimento da coleta com três participantes.

Reverificação após a revisão dos rótulos e da documentação: **9 testes aprovados em 2,14 s**.

## Teste com participantes reais

Em 10/11/2026 três pessoas usaram a tela seguindo o mesmo roteiro: enviar um relato sem CEP, conferir a classificação, tentar de novo com CEP “123” e achar o relato em Meus relatos. As respostas completas, com as palavras dos participantes, estão em [docs/validacao/respostas_participantes.md](validacao/respostas_participantes.md).

**Limitações:** os três participantes são estudantes com muita familiaridade com computador, e o Participante 1 é o autor do projeto; os outros dois são integrantes do grupo. Nenhum é produtor rural, então os resultados não mostram a dificuldade de quem tem pouca familiaridade com tecnologia. Os três seguiram o mesmo roteiro de tarefas, por isso os percursos são parecidos.

| Participante | Data | Perfil | Onde travou ou teve dúvida | O que achou confuso | Melhoria pedida |
|---|---|---|---|---|---|
| P1 | 10/11/2026 | Estudante; familiaridade muita | Dúvida sobre prazo de análise e sobre como acompanhar o relato após sair da sessão. O roteiro de instalação não citava a cópia do `.env` | Cabeçalho fala em IA, mas o resultado diz “regras automáticas”; “Encaminhamento sugerido” exige atenção para ver que ainda não houve encaminhamento | Mensagem junto ao status (“registrado, aguarda conferência, ainda não foi encaminhado”), protocolo para guardar, explicar regras automáticas |
| P2 | 10/11/2026 | Estudante; familiaridade muita | Sem prazo nem forma de receber retorno depois de “Aguardando análise” | A sugestão de encaminhamento pode dar a impressão de que a Secretaria já recebeu o problema | Mensagem de que o relato foi salvo e aguarda conferência antes do encaminhamento; protocolo |
| P3 | 10/11/2026 | Estudante; familiaridade muita | Dúvida se acharia o relato depois de fechar a página (“Meus relatos nesta sessão”) | Apresentação fala em IA, mas a classificação foi por regras automáticas | Explicar regras automáticas; informar como guardar ou consultar o relato depois |

Pontos que apareceram em mais de um participante: (1) o texto fala em IA, mas a triagem pode ser por regras (P1, P3); (2) não fica claro que o relato ainda não foi encaminhado (P1, P2); (3) falta protocolo e forma de acompanhar depois da sessão (P1, P2, P3). O CEP inválido foi bem compreendido pelos três e a descrição foi mantida.

## Melhoria implementada a partir do feedback

Ligada aos pontos acima:

1. **Protocolo e status (P1, P2, P3):** após o envio, a tela mostra “Relato registrado. Protocolo: …. Guarde este código.” e o aviso “Ainda não foi encaminhado: uma pessoa vai conferir o caso antes de qualquer ação”. O protocolo também aparece em cada cartão.
2. **Encaminhamento (P1, P2):** o rótulo mudou de “Encaminhamento sugerido” para “Sugestão de encaminhamento (ainda não enviado)”.
3. **IA ou regras (P1, P3):** o cabeçalho passou a dizer “classificados por inteligência artificial ou por regras automáticas e sempre conferidos por pessoas”, e o cartão diz “regras automáticas (sem inteligência artificial)” quando for o caso.
4. **Histórico (P1, P3):** Meus relatos avisa que a lista vale só enquanto a página estiver aberta e pede para guardar o protocolo.
5. **README (P1):** o passo de copiar `.env.example` para `.env` foi incluído na instrução do Docker.

**Não foi implementado:** prazo de análise e consulta do relato por protocolo depois de sair da sessão. A tela não promete isso, porque o sistema ainda não guarda sessões nem tem esse serviço; fica como trabalho futuro.

Verificação: teste novo `test_envio_mostra_protocolo_e_avisa_que_ainda_nao_foi_encaminhado` e suíte do frontend com **10 testes aprovados**.

Estado: coleta com participantes feita (com as limitações acima); resta atualizar a evidência/vídeo do Front com a tela alterada.
