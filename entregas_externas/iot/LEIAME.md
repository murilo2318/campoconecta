# Physical Computing, Embedded AI, Robotics & Cognitive IoT (OuviAí)

Esta pasta é do responsável pela matéria. O sistema roda sem ela; quando a entrega chegar, ela entra aqui.

## Obrigatório pelo enunciado

- Projeto OuviAí: reconhecer sons pelo microfone do celular e responder visualmente, com Edge Impulse (MFE + CNN)
- Pelo menos 3 situações: duas de interesse e ausência (ambiente). O enunciado cita campainha e batida na porta; permite trocar por eventos equivalentes, desde que justifique a relevância
- Pelo menos 20 gravações de 5 s por classe, 15 em Training e 5 em Test, 16 kHz, mono
- Model testing com Classify all nos arquivos de Test (5 por classe), com acertos e matriz de confusão; proibido reutilizar arquivos de Test no Training
- Deployment, Run this model no celular e validação ao vivo: pelo menos 5 tentativas por classe (15 no total), com percentual de acertos e falsos positivos na classe ambiente
- Não gravar conversas identificáveis sem consentimento; relacionar a pelo menos 1 ODS (10 ou 11)
- Entrega pelo Portal do Aluno: capa com RMs, descrição do problema e ODS, arquitetura, capturas do Edge Impulse, tabela de resultados, evidência da execução e limitações. Grupo de até 3

## Em aberto (decisão do responsável)

- Quais sons (o PDF da GS 2026.2 pede um dispositivo que reconheça sons e mostre respostas visuais no celular para pessoas com deficiência auditiva. Ideia para o campo: alarme da bomba ou do pivô de irrigação, buzina de máquina e sirene de alerta, mais a classe ambiente)
- Se haverá ligação com a API (opcional, fora do enunciado)

## Como encaixar

Colocar nesta pasta as capturas, a tabela de testes e o vídeo ou link. O módulo funciona de forma independente, sem código na API.

## Status

- [ ] Não iniciado
