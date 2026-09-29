# Caderno de Bordo — Coleção de Sprites (Naruto)

Projeto Autoral · Criatividade Computacional 2026.2 · Bloco 2

## 1. O prompt usado (na íntegra)

O prompt abaixo foi enviado exatamente igual, sem nenhuma alteração, em todas as tentativas de todas as referências. A única parte fixa que muda em relação a um template genérico é a descrição do personagem, que também foi mantida igual do início ao fim.

> Generate a new sprite sheet based on the provided reference sprite sheet and the character description below.
>
> CHARACTER DESCRIPTION:
>
> A young ninja boy with spiky yellow hair, a dark blue forehead protector, and three short whisker marks on each cheek. He wears an orange jacket and orange pants with dark blue accents, and dark blue sandals. Simple, small, cartoon-like proportions.
>
> STYLE AND TECHNICAL LIMITATIONS:
>
> Create the character as a native NES-era video game sprite. The image must look like a sprite that was originally created for an NES-era game, not like a modern high-resolution illustration converted into pixel art. Use the visual and technical limitations associated with NES-era sprites: extremely low-resolution sprite design, very small sprites, large clearly visible pixels, hard pixel edges, no anti-aliasing, no smooth edges, no gradients, no soft shadows, no subpixel details, very limited color palette, simple geometric pixel shapes, minimal shading, minimal texture, simplified facial features, simplified anatomy, simplified clothing details, no high-resolution details. The character must be designed directly at the same pixel scale and visual complexity as the reference. Do not create a detailed character and then convert it into pixel art. Do not simulate pixel art at a higher resolution. Do not use modern high-resolution pixel art. Do not add details that would require more pixels than the reference can represent. If a feature cannot be represented clearly at the reference's resolution, simplify that feature instead of adding more pixels.
>
> REFERENCE AS A TECHNICAL TEMPLATE:
>
> Treat the provided reference sprite sheet as a strict technical template, not merely as visual inspiration. Preserve its original pixel density, sprite scale, visual complexity, and level of abstraction. The generated sprites must have approximately the same amount of information and detail per sprite as the reference. Do not make the character more detailed than the original sprites, larger to show more details, or increase the pixel density.
>
> IMAGE DIMENSIONS:
>
> Use exactly the same canvas dimensions as the reference sprite sheet. Do not change the aspect ratio, crop the reference, extend the canvas, add margins or padding, or generate a larger canvas to accommodate additional detail. The output must preserve the same overall dimensions and proportions of the reference.
>
> SPRITE SHEET STRUCTURE:
>
> Generate exactly the same number of frames as the reference. Do not add, remove, duplicate, split, or merge frames. Each output frame corresponds directly to one frame of the reference. Preserve the same frame order, arrangement, spacing, and general composition of the sprite sheet.
>
> SPRITE SCALE:
>
> The character must remain approximately the same size relative to each frame as the character in the reference. Do not enlarge the character, make it occupy substantially more pixels, add extra space by increasing the canvas size, or compensate for the character description by increasing the sprite resolution. The character must be simplified to fit the reference sprite scale.
>
> POSITION:
>
> Preserve the approximate position of the character within each corresponding frame. Do not automatically center every sprite or independently reposition the character in each frame. Preserve the approximate amount of empty space surrounding the character, keeping it inside the same general area occupied by the corresponding reference sprite.
>
> POSES:
>
> Preserve the poses, body orientations, movements, and silhouettes of the corresponding reference frames. The generated character must follow the same animation sequence as the reference. Do not invent additional poses, remove poses, or combine multiple poses into one frame.
>
> COLOR LIMITATIONS:
>
> Preserve the limited-color visual language of the reference. Use a small, discrete palette. Do not introduce many additional shades, use gradients or smooth color transitions, add colors simply to create more realistic lighting or depth, use photographic color variation, or create hundreds or thousands of slightly different colors. The colors specified in the character description must be simplified into a small pixel-art palette while remaining visually recognizable. Keep the defining character colors consistent between frames.
>
> SHADING:
>
> Use extremely simple sprite-style shading, with only a small number of discrete color regions. Do not use realistic lighting, soft shadows, ambient occlusion, or texture shading. Do not add highlights or shadows that are not necessary to distinguish the character's forms.
>
> OUTLINES:
>
> Use hard, discrete pixel outlines consistent with the reference. Do not use anti-aliased outlines or create smooth curves. Represent curves and diagonals using stepped pixel shapes.
>
> CHARACTER CONSISTENCY:
>
> Every frame must depict the same character. Keep the character's defining characteristics consistent throughout the entire sprite sheet. Maintain the same clothing, hair, accessories, colors, and other identifying characteristics across all frames. Simplify these characteristics when necessary to fit the limited pixel resolution. Do not add additional visual details merely because they are mentioned in the character description.
>
> BACKGROUND:
>
> Preserve the background or transparency characteristics of the reference. Do not add unnecessary objects, effects, text, decorations, characters, or environmental elements.
>
> MOST IMPORTANT RULE:
>
> The reference's pixel limitations are more important than adding detail. When there is not enough resolution to represent a characteristic in detail, simplify it. Never increase the resolution, pixel density, sprite size, color complexity, or visual detail to accommodate the character description. The result should look like an authentic low-resolution NES-era game sprite sheet, not a modern detailed pixel-art illustration. Do not upscale, add detail, add unnecessary colors, add extra pixels, increase sprite size, or increase pixel density.

## 2. As referências usadas (o que varia na coleção)

1. Personagem de casaco azul (estilo cartoon, 20 poses)
2. Ninjas com espada (estilo realista escuro, 24 poses)
3. Ninja vermelho (estilo cartoon, 24 poses)
4. Personagem de terno correndo (estilo anime, 8 poses)
5. Guerreiro armado (estilo escuro/realista, sprite único)
6. Estilo Chrono Trigger (16 poses)
7. Luigi (sprite único)
8. Personagem estilo Kingdom Hearts (sprite único)

## 3. Quantas vezes cada referência foi gerada

Cada tentativa foi feita em um chat novo e separado, sempre reenviando o mesmo prompt sem nenhuma alteração e sem apontar o que tinha saído errado na tentativa anterior.

| Referência | Tentativas | Resultado final |
|---|---|---|
| 1. Casaco azul | 1 | Aprovada — permanece na coleção |
| 2. Ninjas com espada | 1 | Aprovada — permanece na coleção |
| 3. Ninja vermelho | 2 | Aprovada na 2ª tentativa |
| 4. Terno correndo | 1 | Aprovada — permanece na coleção |
| 5. Guerreiro armado | 3 (limite esgotado) | Não aprovada — falha estrutural persistente |
| 6. Chrono Trigger | 1 | Aprovada — permanece na coleção |
| 7. Luigi | 2 | Aprovada na 2ª tentativa |
| 8. Kingdom Hearts | 2 (3ª tentativa falhou por erro técnico) | Não aprovada — falha estrutural |

**Coleção final: 6 imagens (referências 1, 2, 3, 4, 6 e 7).**

## 4. Descarte comentado (motivo de cada tentativa não aproveitada)

- **Referência 3, tentativa 1:** descartada por ausência de bordas de pixel real (traço suavizado) e presença de sombreamento em degradê.
- **Referência 5, tentativa 1:** descartada por falha estrutural — pose mudou de combate para posição estática de frente.
- **Referência 5, tentativa 2:** descartada pela mesma falha estrutural, agravada por um item extra (mochila) não presente na descrição do personagem nem na referência, e por sombreamento em degradê no rosto e na mochila.
- **Referência 5, tentativa 3:** descartada por manter a mesma falha estrutural (pose estática, sem corresponder à pose de combate da referência), mesmo após remover a mochila e reduzir o sombreamento. Limite de 3 tentativas esgotado.
- **Referência 7, tentativa 1:** descartada por pose de três quartos com braço estendido, divergindo da postura reta e lateral da referência.
- **Referência 8, tentativa 1:** descartada por falha estrutural e falhas de estilo (cores em excesso, degradê, ausência de bordas de pixel real).
- **Referência 8, tentativa 2:** descartada por gerar quatro poses diferentes em vez de manter a referência como sprite único de uma pose, com inconsistência de detalhe entre elas.
- **Referência 8, tentativa 3:** não pôde ser gerada — falha técnica da ferramenta, não decisão do processo.

## 5. O que foi feito na mão

Nenhuma imagem foi editada, cortada ou retocada depois de gerada — isso violaria a restrição do eixo do grupo. O trabalho manual foi:

- Escrever a descrição do personagem uma única vez, mantida igual em todas as gerações.
- Criar o checklist de avaliação (perguntas obrigatórias e de pontuação) e aplicá-lo em cada imagem, comparando visualmente com a referência.
- Decidir, para cada referência com mais de uma tentativa, se valia a pena gerar de novo ou encerrar.

## 6. Limitações encontradas

- O Gemini não gera imagens no mesmo tamanho e resolução exatos da referência, mesmo quando isso é pedido explicitamente no prompt. Por isso o eixo do grupo foi ajustado de "mesmo tamanho, resolução e estrutura" para "mesma proporção e estrutura".
- O Gemini não permite fixar uma semente (seed), então não é possível reproduzir exatamente o mesmo resultado de novo.
- Na referência 5, a tentativa 2 gerou um item (mochila) não presente na descrição do personagem nem na referência. Isso contraria diretamente duas instruções explícitas do próprio prompt ("do not add additional visual details merely because they are mentioned in the character description" e "do not add unnecessary objects"), mostrando que o modelo nem sempre segue à risca as restrições declaradas, mesmo quando estão escritas com clareza.
- Na referência 8, uma tentativa de geração falhou por erro técnico da ferramenta, e não por decisão do grupo — diferente da referência 5, que esgotou as tentativas por resultado ruim repetido.

## 7. Skills usadas

**afiar-o-eixo**
- Quando: depois de já termos gerado as primeiras imagens (fora da ordem ideal, que seria antes de gerar).
- O que mudou: transformou o eixo de "sprites de jogos" (vago) para um parágrafo com restrição, constante e variável bem definidos.
- Onde atrapalhou: exigiu reescrever a restrição mais de uma vez, porque a primeira versão prometia coisas que o Gemini não conseguia cumprir na prática (como manter o tamanho exato).

**derrubar-a-ideia**
- Quando: logo depois de escrever o primeiro parágrafo do eixo.
- O que mudou: apontou que os critérios de descarte estavam vagos demais ("reconhecível", "diferença significativa de estilo") e não eram verificáveis por quem está de fora, o que levou à criação do checklist detalhado.
- Onde atrapalhou: insistiu em pedir exemplos concretos de descarte antes de termos qualquer imagem gerada, o que não fazia sentido nesse ponto do processo.

**abrir-o-leque:** não foi usada — o grupo já tinha escolhido a direção (sprites de personagens de jogos) antes de começar.

**escutar-a-reuniao:** não foi usada — o grupo não gravou nenhuma reunião.
