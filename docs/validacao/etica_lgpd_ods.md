# Parágrafo proposto — ética, LGPD e ODS (v2)

O CampoConecta pretende ajudar pequenos produtores a organizar pedidos de apoio e dar visibilidade a problemas que podem afetar sua renda, sua produção de alimentos e sua capacidade de enfrentar eventos climáticos, em diálogo com os ODS 1, 2 e 13. Essa contribuição é uma intenção do projeto, ainda não um impacto demonstrado. A classificação automática serve como apoio: a decisão de encaminhamento deve permanecer com uma pessoa, e o sistema não oferece diagnóstico nem prescrição agronômica ou veterinária. Para reduzir a exposição de dados, o processamento aplica regras locais de anonimização antes de armazenar o relato ou enviá-lo ao provedor de IA. Essas regras têm limites: nomes sem os padrões previstos podem passar, e CEP, comentários do gestor e outras informações de contexto ainda podem identificar alguém. Por isso, usamos relatos sintéticos na demonstração e, antes de aceitar dados reais, precisamos definir finalidade, base legal, acesso, retenção e atendimento aos direitos dos titulares, além de revisar o compartilhamento com serviços externos. Não afirmamos conformidade integral com a LGPD nem substituição de atendimento de emergência.

## Base no funcionamento observado

- `backend/app/pipelines/processar.py`: aplica anonimização ao texto e marca urgências críticas, altas por regras e a categoria outro por regras para revisão humana.
- `backend/app/pipelines/anonimizacao.py`: regras para CPF, e-mail, telefone, placa e nomes introduzidos por alguns gatilhos; não há reconhecimento geral de nomes.
- `backend/app/providers/llm.py`: envia o texto ao Gemini quando chave e modelo estão configurados; a IA é orientada a classificar, sem conselho agronômico.
- `backend/app/providers/viacep.py`: consulta serviço externo de CEP e mantém cache local.
- `backend/app/providers/db.py`: armazena CEP e campos de comentário/feedback além da descrição tratada; comentário livre não passa pelo mesmo anonimizador.

O parágrafo descreve medidas existentes e decisões pendentes; não é parecer jurídico nem comprovação de conformidade.
