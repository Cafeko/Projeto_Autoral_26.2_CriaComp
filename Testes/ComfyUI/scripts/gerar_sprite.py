#!/usr/bin/env python3
"""CLI: gera um sprite de personagem a partir de um sprite base + prompt de texto,
via ComfyUI local (FLUX.2 Klein), preservando pose/enquadramento/tamanho.

Exemplo:
    python scripts/gerar_sprite.py --base sprites/base/heroi_idle.png \
        --prompt prompts/heroi.txt --personagem heroi
"""
import argparse
import datetime as dt
import json
import random
import sys
import tempfile
from pathlib import Path

from PIL import Image

import comfy_client as cc

BASE_DIR = Path(__file__).resolve().parent.parent
SPRITES_GERADOS_DIR = BASE_DIR / "sprites" / "gerados"
WORKFLOWS_DIR = BASE_DIR / "workflows"


def parse_args():
    p = argparse.ArgumentParser(description="Gera um sprite a partir de um sprite base + prompt, via ComfyUI.")
    p.add_argument("--base", required=True, help="Caminho do sprite base (imagem de entrada).")
    p.add_argument("--prompt", required=True, help="Caminho do arquivo .txt com o prompt do personagem.")
    p.add_argument("--personagem", required=True, help="Nome do personagem (usado na pasta de saída).")
    p.add_argument("--seed", type=int, default=None, help="Seed do sampler. Default: aleatória.")
    p.add_argument("--escala", type=int, default=8, help="Fator de upscale nearest-neighbor antes de enviar. Default: 8.")
    p.add_argument("--workflow", default="flux2_klein_edit", help="Nome do arquivo em workflows/ (sem .json). Default: flux2_klein_edit.")
    p.add_argument("--server", default=cc.DEFAULT_SERVER, help=f"Endereço do servidor ComfyUI. Default: {cc.DEFAULT_SERVER}.")
    p.add_argument("--node-imagem", default=None, help="ID do node LoadImage (override manual, se houver ambiguidade).")
    p.add_argument("--node-prompt", default=None, help="ID do node de texto do prompt (override manual).")
    p.add_argument("--node-seed", default=None, help="ID do node com o campo seed/noise_seed (override manual).")
    p.add_argument("--timeout", type=float, default=300.0, help="Timeout (s) esperando a geração. Default: 300.")
    return p.parse_args()


def main():
    args = parse_args()

    caminho_base = Path(args.base)
    caminho_prompt = Path(args.prompt)

    if not caminho_base.exists():
        print(f"Erro: sprite base não encontrado: {caminho_base}", file=sys.stderr)
        sys.exit(1)
    if not caminho_prompt.exists():
        print(f"Erro: arquivo de prompt não encontrado: {caminho_prompt}", file=sys.stderr)
        sys.exit(1)

    texto_prompt = caminho_prompt.read_text(encoding="utf-8").strip()
    if not texto_prompt:
        print(f"Erro: arquivo de prompt está vazio: {caminho_prompt}", file=sys.stderr)
        sys.exit(1)

    seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)

    # Passo 1: dimensões originais
    imagem_base = Image.open(caminho_base)
    imagem_base.load()
    largura_original, altura_original = imagem_base.size
    print(f"Sprite base: {caminho_base.name} ({largura_original}x{altura_original}px)")

    # Passo 2: upscale nearest-neighbor por --escala
    nova_largura = largura_original * args.escala
    nova_altura = altura_original * args.escala
    imagem_ampliada = imagem_base.resize((nova_largura, nova_altura), Image.NEAREST)
    print(f"Ampliado {args.escala}x -> {nova_largura}x{nova_altura}px")

    try:
        workflow = cc.carregar_workflow(args.workflow, WORKFLOWS_DIR)

        with tempfile.TemporaryDirectory() as tmp_dir:
            caminho_temp = Path(tmp_dir) / f"upload_{caminho_base.stem}.png"
            imagem_ampliada.save(caminho_temp)

            # Passo 3: enviar ao ComfyUI e disparar o workflow
            print(f"Conectando ao ComfyUI em {args.server}...")
            info_upload = cc.enviar_imagem(caminho_temp, server=args.server)
            nome_enviado = info_upload["name"]
            print(f"Imagem enviada como '{nome_enviado}'.")

            node_imagem = cc.localizar_node_imagem(workflow, args.node_imagem)
            node_prompt = cc.localizar_node_prompt(workflow, args.node_prompt)
            node_seed = cc.localizar_node_seed(workflow, args.node_seed)
            print(f"Nodes identificados -> imagem: {node_imagem}, prompt: {node_prompt}, seed: {node_seed}")

            cc.injetar_imagem(workflow, node_imagem, nome_enviado)
            cc.injetar_prompt(workflow, node_prompt, texto_prompt)
            cc.injetar_seed(workflow, node_seed, seed)

            prompt_id, _ = cc.enfileirar_prompt(workflow, server=args.server)
            print(f"Prompt enfileirado (id={prompt_id}, seed={seed}). Aguardando geração...")

            entrada_historico = cc.aguardar_resultado(prompt_id, server=args.server, timeout=args.timeout)

            imagens_saida = cc.extrair_imagens_saida(entrada_historico)
            if not imagens_saida:
                print("Erro: ComfyUI não retornou nenhuma imagem de saída.", file=sys.stderr)
                sys.exit(1)

            # Passo 4: baixar a imagem resultante
            conteudo_imagem = cc.baixar_imagem(imagens_saida[0], server=args.server)
            print("Imagem gerada baixada.")
    except cc.ComfyUIConnectionError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
    except cc.ComfyUIError as e:
        print(f"Erro do ComfyUI: {e}", file=sys.stderr)
        sys.exit(1)

    # Passo 5: reduzir de volta para (W, H) com nearest-neighbor
    with tempfile.TemporaryDirectory() as tmp_dir:
        caminho_gerado_temp = Path(tmp_dir) / "gerado.png"
        caminho_gerado_temp.write_bytes(conteudo_imagem)
        imagem_gerada = Image.open(caminho_gerado_temp)
        imagem_gerada.load()
        imagem_final = imagem_gerada.resize((largura_original, altura_original), Image.NEAREST)

    # Passo 6: salvar
    pasta_saida = SPRITES_GERADOS_DIR / args.personagem
    pasta_saida.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_base_arquivo = f"{timestamp}_seed{seed}"
    caminho_final = pasta_saida / f"{nome_base_arquivo}.png"
    imagem_final.save(caminho_final)
    print(f"Sprite salvo em: {caminho_final}")

    # Passo 7: metadados
    metadados = {
        "personagem": args.personagem,
        "sprite_base": str(caminho_base),
        "prompt": texto_prompt,
        "seed": seed,
        "workflow": args.workflow,
        "modelo": cc.extrair_info_modelo(workflow),
        "escala_upscale": args.escala,
        "dimensoes_originais": [largura_original, altura_original],
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
    }
    caminho_json = pasta_saida / f"{nome_base_arquivo}.json"
    caminho_json.write_text(json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Metadados salvos em: {caminho_json}")


if __name__ == "__main__":
    main()
