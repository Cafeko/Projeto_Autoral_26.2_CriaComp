# Testes — ComfyUI (FLUX.2 Klein)

Pipeline para gerar variações de um personagem a partir de um sprite base +
um prompt único de texto, mantendo a mesma pose, enquadramento e tamanho do
sprite original, sem retoque manual. Usa o ComfyUI local (FLUX.2 Klein 4B)
via API em `http://127.0.0.1:8188`.

**O ComfyUI precisa estar aberto e rodando localmente antes de executar
qualquer script deste diretório.**

## Estrutura

```
Testes/ComfyUI/
├── requirements.txt
├── scripts/
│   ├── comfy_client.py      # cliente HTTP da API do ComfyUI
│   ├── gerar_sprite.py      # CLI: gera um sprite
│   └── verificar_sprite.py  # CLI: compara base x gerado e registra métricas
├── sprites/
│   ├── base/                # sprites originais de entrada
│   └── gerados/<personagem>/  # saídas, uma subpasta por personagem
├── workflows/                # workflow_api.json exportado do ComfyUI (formato API)
└── prompts/                  # arquivos .txt com o prompt de cada personagem
```

## Setup

```bash
cd "Testes/ComfyUI"
pip install -r requirements.txt
```

Exporte o workflow do ComfyUI em **formato API** ("Save (API Format)" no
menu do ComfyUI) e salve em `workflows/flux2_klein_edit.json` (ou outro nome,
passado via `--workflow`).

## Nodes esperados no workflow

`comfy_client.py` **não** assume índice fixo de node — ele procura por
`class_type` (com override manual por ID se houver ambiguidade). Confirme
que o seu grafo tem nodes compatíveis com isto antes de rodar de verdade:

| Papel | Como é localizado | Classes aceitas |
|---|---|---|
| Imagem de entrada | único node `LoadImage` no grafo | `LoadImage` |
| Prompt de texto | único node de texto, ou o que tiver "prompt"/"positive" no título se houver mais de um | `CLIPTextEncode`, `CLIPTextEncodeFlux`, `T5TextEncode`, `CLIPTextEncodeSDXL`, `String Literal`, `PrimitiveStringMultiline` |
| Seed | único node com campo `seed` ou `noise_seed` (int); em caso de empate, prioriza classes de sampler | `KSampler`, `KSamplerAdvanced`, `SamplerCustom`, `SamplerCustomAdvanced`, `RandomNoise`, ou qualquer outro com esses campos |

Se o seu grafo tiver mais de um node de cada tipo (ex.: prompt positivo e
negativo, ou `RandomNoise` + `KSamplerAdvanced` com seeds separados), use os
overrides `--node-imagem`, `--node-prompt`, `--node-seed` com o ID do node
(visível no ComfyUI ao exportar o JSON, ou renomeando o título do node para
conter "prompt"/"positive" no caso do prompt).

Se algum node não existir/for ambíguo, os scripts avisam com o ID dos
candidatos encontrados — rode uma vez para conferir antes de gerar em lote.

## Uso

### 1. Gerar um sprite

```bash
python scripts/gerar_sprite.py \
  --base sprites/base/heroi_idle.png \
  --prompt prompts/heroi.txt \
  --personagem heroi \
  --escala 8 \
  --workflow flux2_klein_edit
```

Passos executados:
1. Lê o sprite base e guarda as dimensões originais (W, H).
2. Amplia com nearest-neighbor (`Image.NEAREST`) por `--escala` vezes (default 8).
   Nenhum outro filtro de resize é usado em nenhuma etapa do pipeline.
3. Envia a imagem ampliada ao ComfyUI e dispara o workflow com o prompt e a seed.
4. Baixa a imagem gerada.
5. Reduz a imagem gerada de volta para (W, H) com nearest-neighbor.
6. Salva em `sprites/gerados/<personagem>/<timestamp>_seed<seed>.png`.
7. Salva um `.json` ao lado com personagem, sprite base, prompt completo, seed,
   workflow, modelo (unet/clip/vae lidos do próprio workflow) e timestamp.

Argumentos:

| Flag | Obrigatório | Default | Descrição |
|---|---|---|---|
| `--base` | sim | — | Caminho do sprite base |
| `--prompt` | sim | — | Caminho do `.txt` do prompt |
| `--personagem` | sim | — | Nome usado na pasta de saída |
| `--seed` | não | aleatória | Seed do sampler |
| `--escala` | não | `8` | Fator de upscale nearest-neighbor antes de enviar |
| `--workflow` | não | `flux2_klein_edit` | Nome do arquivo em `workflows/` (sem `.json`) |
| `--server` | não | `127.0.0.1:8188` | Endereço do ComfyUI |
| `--node-imagem` / `--node-prompt` / `--node-seed` | não | auto-detectado | Override manual de ID de node |
| `--timeout` | não | `300` | Timeout (s) esperando a geração |

Se o ComfyUI não estiver rodando, o script para com uma mensagem clara
("ComfyUI não está rodando em 127.0.0.1:8188...") em vez de travar.

### 2. Verificar um sprite gerado

```bash
python scripts/verificar_sprite.py \
  --base sprites/base/heroi_idle.png \
  --gerado sprites/gerados/heroi/20260101_120000_seed123.png
```

Compara base x gerado e imprime/registra:
- se o tamanho bate exatamente;
- IoU da silhueta do personagem contra o fundo (segmentado por alpha, se
  houver transparência, ou por diferença de cor em relação ao pixel do
  canto superior esquerdo);
- centro de massa da silhueta em cada imagem e a diferença em pixels;
- número de cores únicas em cada imagem.

O resultado é anexado (sem sobrescrever execuções anteriores) em
`sprites/gerados/<personagem>/metricas.csv`. Se a imagem gerada ainda não
existir, o script avisa e não quebra.

## Notas

- Este pipeline não faz retoque manual em nenhuma etapa: apenas
  nearest-neighbor para escalar e a chamada ao ComfyUI para gerar.
- `workflow_api.json` não é versionado automaticamente por este setup — ele
  é lido de `workflows/`, mas cabe a quem estiver rodando o pipeline
  exportá-lo do ComfyUI.
