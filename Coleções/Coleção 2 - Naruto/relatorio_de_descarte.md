# Relatório de Avaliação da Coleção — Sprites (Naruto)

**Projeto Autoral · Criatividade Computacional 2026.2 · Bloco 2**

## 1. Por que este relatório existe

Este documento mostra **como cada imagem da coleção foi avaliada**, com critérios fixos definidos antes da análise, para provar que o que ficou e o que foi descartado seguiu um critério, não uma escolha por gosto pessoal. Ele responde três perguntas: o que foi gerado, o que entrou na coleção final, e por que cada imagem descartada foi descartada.

## 2. Como cada imagem foi avaliada

Toda imagem passou pelas mesmas perguntas, na mesma ordem, divididas em dois grupos.

### 2.1 Perguntas obrigatórias (falhar em qualquer uma descarta a imagem na hora)

| # | Pergunta |
|---|---|
| A | O prompt foi enviado exatamente igual em todas as tentativas dessa referência, sem apontar falhas da tentativa anterior nem pedir correção? |
| B | A imagem não foi editada manualmente depois de gerada? |
| C | A proporção e a estrutura geral do resultado correspondem às da referência? |
| D | A pose corresponde à da referência? (único: a pose; spritesheet: cada pose, uma a uma, na posição correspondente) |

### 2.2 Perguntas de pontuação (a imagem precisa acertar a maioria)

| # | Pergunta |
|---|---|
| 1 | As características marcantes do personagem aparecem reconhecíveis? |
| 2 | O traço tem bordas de pixel real, sem suavização? |
| 3 | O nível de cores é similar ao da imagem original? |
| 4 | O nível de detalhe de shading e o contorno são similares aos da imagem original? |
| 5 | *(só spritesheet)* O número de poses bate com o da referência? (único: N/A) |
| 6 | O nível de detalhe é similar ao da imagem original? |

**Regra de aprovação:** as 4 obrigatórias precisam ser "sim". Das perguntas de pontuação, é preciso acertar pelo menos 5 de 6 em spritesheets, ou 4 de 5 em sprites únicos (que não têm a pergunta 5).

> Pose divergente reprova por si: é obrigatória D e exigência do eixo (manter proporção e estrutura) — falhar C/D já descarta, independente do placar.

**Limite de tentativas:** cada referência podia ser reenviada até 3 vezes, sempre com o mesmo prompt, sem nenhuma alteração no texto e sem apontar o que tinha saído errado na tentativa anterior.

## 3. Resultado resumido

| Imagem | Referência | Tentativas | Resultado |
|---|---|---|---|
| 1 | Personagem de casaco azul | 1 | ✅ Fica |
| 2 | Ninjas com espada | 1 | ✅ Fica |
| 3 | Ninja vermelho | 2 | ✅ Fica (2ª tentativa) |
| 4 | Personagem de terno correndo | 1 | ✅ Fica |
| 5 | Guerreiro armado | 3 | ❌ Descartada |
| 6 | Estilo Chrono Trigger | 1 | ✅ Fica |
| 7 | Luigi | 2 | ✅ Fica (2ª tentativa) |
| 8 | Estilo Kingdom Hearts | 2 (3ª não gerou) | ❌ Descartada |

**Coleção final: 6 imagens (1, 2, 3, 4, 6 e 7).**

## 4. Detalhamento de cada imagem

### Imagem 1 — Personagem de casaco azul
Uma tentativa, sem edição, estrutura compatível com a referência. Pontuação: 6/6.
**Resultado: fica na coleção.**

### Imagem 2 — Ninjas com espada
Uma tentativa, sem edição, estrutura compatível. Pontuação: 5/6 — falhou apenas na pergunta 2 (bordas de pixel real).
**Resultado: fica na coleção.**

### Imagem 3 — Ninja vermelho
- **Tentativa 1 (descartada):** faltaram bordas de pixel real e havia sombreamento em degradê.
- **Tentativa 2:** mesmo prompt, sem alterações. Corrigiu os dois problemas, manteve a estrutura de 24 poses compatível com a referência. Pontuação: 6/6.
**Resultado: fica na coleção, com a tentativa 2.**

### Imagem 4 — Personagem de terno correndo
Uma tentativa, sem edição, estrutura compatível. Pontuação: 6/6.
**Resultado: fica na coleção.**

### Imagem 5 — Guerreiro armado
- **Tentativa 1 (descartada):** pose mudou de combate para uma posição estática de frente — falhou as obrigatórias C e D.
- **Tentativa 2 (descartada):** mesma falha de estrutura/pose (C/D), e ainda apareceu uma mochila que não estava na descrição do personagem nem na referência, além de sombreamento em degradê no rosto e na mochila.
- **Tentativa 3 (descartada):** removeu a mochila e reduziu o sombreamento, mas manteve a mesma falha de estrutura/pose (C/D) — a pose continuou estática, sem corresponder à pose de combate da referência.

Limite de 3 tentativas esgotado sem sucesso.
**Resultado: não entra na coleção.**

### Imagem 6 — Estilo Chrono Trigger
Uma tentativa, sem edição, estrutura e poses compatíveis com a referência. Pontuação: 6/6.
**Resultado: fica na coleção.**

### Imagem 7 — Luigi
- **Tentativa 1 (descartada):** pose de três quartos, com o braço estendido à frente, diferente da postura reta e lateral da referência — falhou as obrigatórias C e D.
- **Tentativa 2:** mesmo prompt, sem alterações. Corrigiu a pose (D sim), manteve a orientação da referência. Pontuação: 5/5 (critério de sprite único: 1, 2, 3, 4 e 6-detalhe).
**Resultado: fica na coleção, com a tentativa 2.**

### Imagem 8 — Estilo Kingdom Hearts
- **Tentativa 1 (descartada):** falhou nas obrigatórias de estrutura/pose (C/D) e na maior parte da pontuação (cores em excesso, degradê, sem bordas de pixel real).
- **Tentativa 2 (descartada):** piorou o problema de estrutura/pose (C/D) — em vez de manter uma pose única como a referência, gerou quatro poses diferentes de corrida, com nível de detalhe inconsistente entre elas.
- **Tentativa 3:** não foi possível gerar — falha técnica da ferramenta, não decisão do grupo.

**Resultado: não entra na coleção.**

## 5. Por que 5 e 8 são descartes diferentes

| | Imagem 5 | Imagem 8 |
|---|---|---|
| Motivo do descarte | Resultado ruim repetido (3 tentativas, mesma falha) | Falha técnica interrompeu o processo |
| Tentativas esgotadas? | Sim, as 3 permitidas | Não — a 3ª não pôde ser gerada |
| Tipo de limitação | Do modelo (não segue a pose pedida) | Da ferramenta (falhou em gerar) |

Essa diferença está registrada porque são dois tipos de limitação diferentes: uma é o modelo produzindo resultado ruim de forma consistente, a outra é o modelo simplesmente não conseguindo produzir nada.
