# Validação do frontend por perfis

Data: 10/11/2026. Interface executada em Docker: http://localhost:8501 .
Método: execução automatizada no navegador pelo agente, em três contextos isolados. P1–Murilo, P2–Pedro e P3–Nicolas são os rótulos de perfil solicitados para organizar a avaliação; os comentários técnicos abaixo são do agente, não depoimentos atribuídos aos integrantes. A coleta com participantes continua em aberto.

Este documento foi criado porque docs/VALIDACAO_FRONT.md não existia. O roteiro de referência era validacao/TESTE_COM_PESSOAS.md.

## Execução e triagem observada

| Perfil | Caso enviado | Registro de referência | Tipo / urgência | Avaliação técnica registrada |
|---|---|---|---|---|
| P1 – Murilo | Bomba do poço quebrada e horta sem água desde ontem | api-f15a4383 | Água e irrigação / alta | Tipo e encaminhamento coerentes; botão Útil acionado e confirmação exibida |
| P2 – Pedro | Lagartas no milho, metade da roça atingida | api-f48e53cf | Praga ou doença / média | Tipo coerente; urgência depende da interpretação da extensão do dano. Botão Útil acionado para verificar o fluxo |
| P3 – Nicolas | Informações sobre Pronaf para a próxima safra, sem prazo urgente | api-6eb305de | Crédito e seguro / alta | Urgência possivelmente excessiva: a frase nega urgência, mas a regra reconhece palavras de urgência sem interpretar a negação. Botão Incorreta acionado |

Fonte dos três resultados: regras automáticas, sem Gemini. Os cliques acima verificam a gravação e a confirmação do mecanismo de avaliação; não são métricas de satisfação de participantes.

Cada perfil abriu Meus relatos. P1 mostrou somente seu caso; P2 mostrou seus dois envios de teste (um envio inicial e uma repetição); P3 mostrou somente a consulta de crédito. Não houve mistura de relatos entre os históricos das sessões. A primeira execução foi assíncrona: o cartão de P2 apareceu após a fotografia inicial da tela, resultando em uma repetição pelo agente. Isso foi registrado como ocorrência da execução automatizada, sem atribuir uma dificuldade ao participante.

## O que dificultou o fluxo

| Perfil | Evidência observada | Consequência | Encaminhamento |
|---|---|---|---|
| P1 – Murilo | Texto “oi” foi bloqueado com a mensagem de mínimo de dez caracteres | Validação funciona, mas o formulário apagava o texto e mantinha o cartão anterior abaixo do erro | Preservar o rascunho e não apresentar o cartão anterior na tentativa inválida |
| P2 – Pedro | Descrição válida com CEP “123” foi bloqueada com mensagem de oito dígitos | A descrição inteira era apagada, exigindo reescrita; o cartão anterior permanecia e podia parecer resultado da nova tentativa | Correção aplicada no formulário |
| P3 – Nicolas | Consulta com “sem prazo urgente” recebeu urgência alta | O tipo foi identificado, mas a urgência não respeitou a negação | Registrar caso para revisão das regras; não alterar o classificador nesta avaliação |

Não houve travamento fatal da interface durante os envios ou consulta aos históricos. Os problemas acima são distintos: perda de rascunho/exibição de resultado antigo são de interface; a interpretação de negação é uma limitação de triagem.

## Análise de usabilidade por perfil

As sugestões abaixo são hipóteses de melhoria elaboradas a partir do percurso observado, e não citações de falas dos integrantes.

- **P1 – Murilo:** o tipo, a urgência e o encaminhamento estão visíveis; a confirmação humana também aparece. Sugestão: preservar o que foi digitado ao pedir correção de um campo.
- **P2 – Pedro:** a mensagem do CEP explica o formato e permite deixar o campo em branco. A necessidade de reescrever o relato era o principal atrito. Sugestão: manter descrição e CEP disponíveis para edição.
- **P3 – Nicolas:** o botão Incorreta permite contestar a triagem, mas o sistema não explica quais termos produziram a urgência. Sugestão: revisar negações e, futuramente, permitir justificativa da contestação.

## Ajuste aplicado e verificação

Alterações em frontend/features/reportar.py:

1. O formulário preserva seus campos depois de Enviar, permitindo corrigir CEP ou descrição e tentar novamente sem reescrever tudo. Os campos também permanecem após sucesso; o cartão de confirmação identifica o resultado recebido.
2. Após validação inválida ou erro da API, a função retorna antes de renderizar o último cartão, evitando associar um resultado anterior à tentativa atual.

A regressão test_cep_invalido_preserva_rascunho_sem_mostrar_resultado_anterior reproduziu a falha antes da correção: havia um Success com o cartão anterior, mesmo com CEP inválido. Depois da correção, a suíte do frontend aprovou **9 testes em 2,12 s**, incluindo a preservação de descrição/CEP, ausência de resultado antigo e nenhuma segunda chamada à API.

A imagem Docker foi reconstruída e a correção foi conferida pela tela: após enviar um relato válido, preencher CEP “123” e enviar novamente, descrição e CEP permaneceram preenchidos, a mensagem de oito dígitos apareceu e nenhum cartão anterior foi mostrado. Evidência: validacao/perfis_automatizados/cep_invalido_depois.png. Este ajuste deriva de observação técnica no teste automatizado; não é apresentado como cumprimento da coleta com três participantes.

## Próxima validação com participantes

Para cada integrante que efetivamente utilizar a tela, registrar a data, as tarefas, suas próprias palavras e a melhoria solicitada. Só então atualizar o estado da coleta de feedback dos participantes em docs/PENDENCIAS.md. Não substituir esse registro por comentários produzidos pelo agente.
