#!/usr/bin/env python3
"""CLI: compara um sprite gerado com o sprite base e registra métricas em CSV.

Métricas:
  a) se o tamanho (W, H) bate exatamente
  b) IoU da silhueta do personagem contra o fundo
  c) posição do centro de massa da silhueta em cada imagem e a diferença (px)
  d) número de cores únicas em cada imagem

Segmentação da silhueta: usa o canal alfa se a imagem tiver transparência;
caso contrário, usa o pixel do canto superior esquerdo (0, 0) como cor de
fundo e marca como personagem qualquer pixel que difira dele além da
tolerância (--tolerancia).

Exemplo:
    python scripts/verificar_sprite.py --base sprites/base/heroi_idle.png \
        --gerado sprites/gerados/heroi/20260101_120000_seed123.png
"""
import argparse
import csv
import datetime as dt
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def parse_args():
    p = argparse.ArgumentParser(description="Compara sprite gerado com sprite base e registra métricas em CSV.")
    p.add_argument("--base", required=True, help="Caminho do sprite base.")
    p.add_argument("--gerado", required=True, help="Caminho do sprite gerado.")
    p.add_argument("--tolerancia", type=int, default=24, help="Tolerância (soma de diferença RGB) para segmentar por cor de fundo. Default: 24.")
    return p.parse_args()


def segmentar_silhueta(imagem: Image.Image, tolerancia: int) -> np.ndarray:
    if "A" in imagem.getbands():
        rgba = imagem.convert("RGBA")
        alpha = np.array(rgba)[:, :, 3]
        return alpha > 127
    rgb = imagem.convert("RGB")
    arr = np.array(rgb).astype(int)
    cor_fundo = arr[0, 0]
    diferenca = np.abs(arr - cor_fundo).sum(axis=2)
    return diferenca > tolerancia


def centro_de_massa(mascara: np.ndarray):
    ys, xs = np.nonzero(mascara)
    if len(xs) == 0:
        return None
    return float(xs.mean()), float(ys.mean())


def calcular_iou(mascara_a: np.ndarray, mascara_b: np.ndarray):
    if mascara_a.shape != mascara_b.shape:
        return None
    intersecao = np.logical_and(mascara_a, mascara_b).sum()
    uniao = np.logical_or(mascara_a, mascara_b).sum()
    if uniao == 0:
        return 0.0
    return float(intersecao) / float(uniao)


def contar_cores_unicas(imagem: Image.Image) -> int:
    rgb = imagem.convert("RGB")
    arr = np.array(rgb).reshape(-1, 3)
    return int(len(np.unique(arr, axis=0)))


def main():
    args = parse_args()
    caminho_base = Path(args.base)
    caminho_gerado = Path(args.gerado)

    if not caminho_base.exists():
        print(f"Erro: sprite base não encontrado: {caminho_base}", file=sys.stderr)
        sys.exit(1)
    if not caminho_gerado.exists():
        print(f"Aviso: sprite gerado ainda não existe: {caminho_gerado}. Nada a verificar.")
        return

    imagem_base = Image.open(caminho_base)
    imagem_base.load()
    imagem_gerada = Image.open(caminho_gerado)
    imagem_gerada.load()

    tamanho_base = imagem_base.size
    tamanho_gerado = imagem_gerada.size
    tamanho_bate = tamanho_base == tamanho_gerado

    mascara_base = segmentar_silhueta(imagem_base, args.tolerancia)
    mascara_gerada = segmentar_silhueta(imagem_gerada, args.tolerancia)

    iou = calcular_iou(mascara_base, mascara_gerada)

    centro_base = centro_de_massa(mascara_base)
    centro_gerado = centro_de_massa(mascara_gerada)
    if centro_base is not None and centro_gerado is not None:
        distancia_centro = math.hypot(centro_base[0] - centro_gerado[0], centro_base[1] - centro_gerado[1])
    else:
        distancia_centro = None

    cores_base = contar_cores_unicas(imagem_base)
    cores_gerado = contar_cores_unicas(imagem_gerada)

    print(f"Tamanho base:   {tamanho_base}")
    print(f"Tamanho gerado: {tamanho_gerado}")
    print(f"Tamanho bate exatamente: {tamanho_bate}")
    print(f"IoU da silhueta: {iou if iou is not None else 'N/A (tamanhos diferentes)'}")
    print(f"Centro de massa base:   {centro_base}")
    print(f"Centro de massa gerado: {centro_gerado}")
    print(f"Diferença do centro de massa (px): {distancia_centro}")
    print(f"Cores únicas base:   {cores_base}")
    print(f"Cores únicas gerado: {cores_gerado}")

    # CSV de métricas ao lado do sprite gerado (sprites/gerados/<personagem>/metricas.csv)
    pasta_saida = caminho_gerado.parent
    caminho_csv = pasta_saida / "metricas.csv"
    arquivo_novo = not caminho_csv.exists()

    with open(caminho_csv, "a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if arquivo_novo:
            escritor.writerow([
                "timestamp", "base", "gerado",
                "largura_base", "altura_base", "largura_gerado", "altura_gerado",
                "tamanho_bate", "iou",
                "centro_base_x", "centro_base_y", "centro_gerado_x", "centro_gerado_y",
                "distancia_centro_px",
                "cores_unicas_base", "cores_unicas_gerado",
            ])
        escritor.writerow([
            dt.datetime.now().isoformat(timespec="seconds"),
            str(caminho_base), str(caminho_gerado),
            tamanho_base[0], tamanho_base[1], tamanho_gerado[0], tamanho_gerado[1],
            tamanho_bate, iou,
            centro_base[0] if centro_base else "", centro_base[1] if centro_base else "",
            centro_gerado[0] if centro_gerado else "", centro_gerado[1] if centro_gerado else "",
            distancia_centro if distancia_centro is not None else "",
            cores_base, cores_gerado,
        ])

    print(f"Métricas registradas em: {caminho_csv}")


if __name__ == "__main__":
    main()
