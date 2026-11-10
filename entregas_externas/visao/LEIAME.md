# Visão Computacional

Esta pasta é do responsável pela matéria. O sistema roda sem ela; quando a entrega chegar, ela entra aqui.

## Obrigatório pelo enunciado

- Escolher classificação de fissuras (Concrete Crack Images ou SDNET2018) ou detecção de danos em vias (RDD2022)
- Preparar os dados (redimensionar, normalizar) e separar treino, validação e teste sem repartir recortes da mesma imagem entre conjuntos
- Usar CNN, transferência de aprendizado ou detector de objetos, com amostra dos dados e arquitetura pré-treinada
- Classificação: precisão, recall, F1 e matriz de confusão. Detecção: precisão, recall e mAP. Analisar acertos e erros (sombra, textura, iluminação, obstáculos)
- Funcionalidade integrada ao CitizenTech que recebe uma imagem e mostra a classe ou as caixas, com a confiança do modelo
- Processar um vídeo curto ou sequência de imagens para simular monitoramento
- Medir latência média por imagem e FPS, informando equipamento e resolução; justificar arquitetura, pré-processamento e limiar de confiança
- Entregas: notebook ou código, vídeo de demonstração, relatório breve
- A solução apoia a triagem de locais para inspeção. A presença de fissura na imagem não define gravidade nem segurança estrutural

## Em aberto (decisão do responsável)

- Qual base e qual tarefa (classificar ou detectar)
- Arquitetura e limiar
- Como o resultado aparece no front
- O PDF da GS 2026.2 pede detecção de manutenção predial ou de estruturas para apoiar a administração municipal. Ideia para este tema: danos em estradas vicinais (RDD2022), que travam o escoamento da produção do pequeno produtor

## Como encaixar

Criar `app/modulos/impl_visao.py` com `analisar(imagem_bytes: bytes) -> dict` (formato `VisaoSaida` em `app/schemas/modulos.py`). Notebook e relatório ficam nesta pasta.

## Status

- [ ] Não iniciado
