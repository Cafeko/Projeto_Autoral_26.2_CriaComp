# Relatório de Avaliação da Coleção 3 — Sprites (Shaka de Virgem)

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

**Limite de tentativas:** cada referência pode ser reenviada até 5 vezes, sempre com o mesmo prompt, sem nenhuma alteração no texto e sem apontar o que saiu errado na tentativa anterior.

## 3. Resultado resumido

| Imagem | Referência | Tentativas avaliadas | Resultado |
|---|---|---|---|
| 01 | Naruto(atk1) | 1 | ❌ Nenhuma aprovada |
| 02 | Naruto(Idle) | 1 | ❌ Nenhuma aprovada |
| 03 | Naruto(walk) | 1 | ✅ Fica (tentativa 1) |

**Coleção final: 1 imagem (03).**

## 4. Detalhamento de cada imagem

### Imagem 01 — Naruto(atk1)
- **Tentativa 1 (descartada)**: Tipo spritesheet | A sim B sim C sim D não | 1 sim 2 sim 3 não 4 sim 5 sim 6 não | Placar 4/6 | Fica não. Motivo: Muda o braço no último frame e é bem mais simples visualmente.
**Resultado: não entra na coleção.**

### Imagem 02 — Naruto(Idle)
- **Tentativa 1 (descartada)**: Tipo spritesheet | A sim B sim C não D não | 1 sim 2 sim 3 não 4 sim 5 não 6 sim | Placar 4/6 | Fica não. Motivo: Um frame a menos que a referência.
**Resultado: não entra na coleção.**

### Imagem 03 — Naruto(walk)
- **Tentativa 1 (aprovada)**: Tipo spritesheet | A sim B sim C sim D sim | 1 sim 2 sim 3 não 4 sim 5 sim 6 sim | Placar 5/6 | Fica sim.
**Resultado: fica na coleção, com a tentativa 1.**

## 5. Observações sobre descartes (se houver tipos diferentes)

| | Imagem 01 | Imagem 02 |
|---|---|---|
| Motivo do descarte | Pose divergente (D não): muda o braço no último frame | Estrutura divergente (C não + Q5 não): um frame a menos |
| Tentativas esgotadas? | Não — 1 de 5 usada | Não — 1 de 5 usada |
| Tipo de limitação | Do modelo (não segue a pose pedida) | Do modelo (não mantém o nº de frames) |
