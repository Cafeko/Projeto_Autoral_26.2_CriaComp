"""Cliente HTTP para o ComfyUI local (FLUX.2 Klein), usado pelo pipeline de sprites.

Não assume índices fixos de node: procura os nodes relevantes (LoadImage,
node de texto do prompt, node com campo de seed) por class_type e, em caso
de ambiguidade, permite escolha manual por ID (ver --node-imagem,
--node-prompt, --node-seed em gerar_sprite.py).
"""
import json
import time
import urllib.parse
import uuid
from pathlib import Path

import requests

DEFAULT_SERVER = "127.0.0.1:8188"

# Classes de node candidatas para cada papel no workflow. A lista é
# propositalmente ampla porque o grafo do FLUX.2 Klein pode variar.
LOAD_IMAGE_CLASSES = ["LoadImage"]
TEXT_PROMPT_CLASSES = [
    "CLIPTextEncode",
    "CLIPTextEncodeFlux",
    "T5TextEncode",
    "CLIPTextEncodeSDXL",
    "String Literal",
    "PrimitiveStringMultiline",
]
SAMPLER_CLASSES_HINT = [
    "KSampler",
    "KSamplerAdvanced",
    "SamplerCustom",
    "SamplerCustomAdvanced",
    "RandomNoise",
]
# Campos considerados ao procurar informação de modelo para os metadados.
MODEL_FIELDS = (
    "unet_name",
    "ckpt_name",
    "clip_name",
    "clip_name1",
    "clip_name2",
    "vae_name",
)


class ComfyUIError(Exception):
    """Erro genérico do pipeline ComfyUI (workflow, nodes, resposta da API)."""


class ComfyUIConnectionError(ComfyUIError):
    """Falha ao conectar no servidor ComfyUI."""


def _base_url(server: str) -> str:
    return f"http://{server}"


def _erro_conexao(server: str, origem: Exception) -> ComfyUIConnectionError:
    erro = ComfyUIConnectionError(
        f"ComfyUI não está rodando em {server}. Abra o ComfyUI e tente novamente."
    )
    erro.__cause__ = origem
    return erro


# --------------------------------------------------------------------------
# Carregar workflow
# --------------------------------------------------------------------------

def carregar_workflow(nome: str, workflows_dir: Path) -> dict:
    """Carrega um workflow exportado em formato API (workflows/<nome>.json)."""
    caminho = Path(nome)
    if caminho.suffix.lower() != ".json":
        caminho = workflows_dir / f"{nome}.json"
    elif not caminho.is_absolute() and not caminho.exists():
        caminho = workflows_dir / caminho.name

    if not caminho.exists():
        raise ComfyUIError(
            f"Workflow '{nome}' não encontrado em {workflows_dir}. "
            "Exporte o workflow em formato API no ComfyUI (Save (API Format)) "
            f"e salve o arquivo como {workflows_dir / (nome if nome.endswith('.json') else nome + '.json')}."
        )
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------
# Upload de imagem
# --------------------------------------------------------------------------

def enviar_imagem(caminho_imagem: Path, server: str = DEFAULT_SERVER) -> dict:
    """POST /upload/image. Retorna {'name', 'subfolder', 'type'}."""
    url = f"{_base_url(server)}/upload/image"
    try:
        with open(caminho_imagem, "rb") as f:
            arquivos = {"image": (caminho_imagem.name, f, "image/png")}
            resp = requests.post(url, files=arquivos, data={"overwrite": "true"}, timeout=30)
    except requests.exceptions.ConnectionError as e:
        raise _erro_conexao(server, e)
    if resp.status_code != 200:
        raise ComfyUIError(f"Falha ao enviar imagem ({resp.status_code}): {resp.text}")
    return resp.json()


# --------------------------------------------------------------------------
# Localização de nodes no workflow
# --------------------------------------------------------------------------

def _iter_nodes(workflow: dict):
    for node_id, node in workflow.items():
        yield node_id, node


def _titulo(node: dict) -> str:
    return node.get("_meta", {}).get("title", "")


def encontrar_por_classe(workflow: dict, classes: list) -> list:
    return [nid for nid, node in _iter_nodes(workflow) if node.get("class_type") in classes]


def _nodes_referenciados(workflow: dict) -> set:
    """IDs de node cuja saída é usada como input de algum outro node (ou seja, 'conectado' no grafo)."""
    referenciados = set()
    for _, node in _iter_nodes(workflow):
        for valor in node.get("inputs", {}).values():
            if isinstance(valor, list) and len(valor) == 2 and isinstance(valor[0], str):
                referenciados.add(valor[0])
    return referenciados


def localizar_node_imagem(workflow: dict, node_id: str = None) -> str:
    if node_id:
        if node_id not in workflow:
            raise ComfyUIError(f"Node de imagem '{node_id}' não existe no workflow.")
        return node_id
    candidatos = encontrar_por_classe(workflow, LOAD_IMAGE_CLASSES)
    if not candidatos:
        raise ComfyUIError(
            "Nenhum node LoadImage encontrado no workflow. Use --node-imagem <id> para indicar manualmente."
        )
    if len(candidatos) > 1:
        # Se houver nodes LoadImage "órfãos" (não conectados a nada), ignora-os.
        referenciados = _nodes_referenciados(workflow)
        conectados = [nid for nid in candidatos if nid in referenciados]
        if len(conectados) == 1:
            return conectados[0]
        raise ComfyUIError(
            f"Múltiplos nodes LoadImage encontrados ({candidatos}). Use --node-imagem <id> para escolher."
        )
    return candidatos[0]


def localizar_node_prompt(workflow: dict, node_id: str = None) -> str:
    if node_id:
        if node_id not in workflow:
            raise ComfyUIError(f"Node de prompt '{node_id}' não existe no workflow.")
        return node_id
    candidatos = encontrar_por_classe(workflow, TEXT_PROMPT_CLASSES)
    if not candidatos:
        raise ComfyUIError(
            "Nenhum node de texto (CLIPTextEncode ou similar) encontrado no workflow. "
            "Use --node-prompt <id> para indicar manualmente."
        )
    if len(candidatos) > 1:
        # Se houver exatamente um com "positive" no título e sem "negative", usa ele
        # (cobre o caso comum de par positive/negative prompt).
        positivos = [
            nid for nid in candidatos
            if "positive" in _titulo(workflow[nid]).lower()
            and "negative" not in _titulo(workflow[nid]).lower()
        ]
        if len(positivos) == 1:
            return positivos[0]
        raise ComfyUIError(
            f"Múltiplos nodes de texto encontrados ({candidatos}). "
            "Renomeie o título do node de prompt positivo no ComfyUI para conter 'positive', "
            "ou use --node-prompt <id> para escolher."
        )
    return candidatos[0]


def localizar_node_seed(workflow: dict, node_id: str = None) -> str:
    if node_id:
        if node_id not in workflow:
            raise ComfyUIError(f"Node de seed '{node_id}' não existe no workflow.")
        return node_id
    candidatos = []
    for nid, node in _iter_nodes(workflow):
        inputs = node.get("inputs", {})
        for chave in ("seed", "noise_seed"):
            if isinstance(inputs.get(chave), (int, float)):
                candidatos.append(nid)
                break
    if not candidatos:
        raise ComfyUIError(
            "Nenhum node com campo 'seed'/'noise_seed' encontrado no workflow. "
            "Use --node-seed <id> para indicar manualmente."
        )
    if len(candidatos) > 1:
        preferidos = [nid for nid in candidatos if workflow[nid].get("class_type") in SAMPLER_CLASSES_HINT]
        if len(preferidos) == 1:
            return preferidos[0]
        raise ComfyUIError(
            f"Múltiplos nodes com campo de seed encontrados ({candidatos}). "
            "Use --node-seed <id> para escolher."
        )
    return candidatos[0]


# --------------------------------------------------------------------------
# Injeção de valores no workflow
# --------------------------------------------------------------------------

def injetar_imagem(workflow: dict, node_id: str, nome_arquivo: str) -> None:
    workflow[node_id]["inputs"]["image"] = nome_arquivo


def injetar_prompt(workflow: dict, node_id: str, texto: str) -> None:
    inputs = workflow[node_id]["inputs"]
    if "text" in inputs:
        inputs["text"] = texto
        return
    # Variantes com campos separados (ex.: CLIPTextEncodeFlux com clip_l/t5xxl).
    encontrado = False
    for chave in ("clip_l", "t5xxl", "text_g", "text_l"):
        if chave in inputs:
            inputs[chave] = texto
            encontrado = True
    if not encontrado:
        raise ComfyUIError(
            f"Node de prompt '{node_id}' não tem campo 'text' (ou variante conhecida) em 'inputs'."
        )


def injetar_seed(workflow: dict, node_id: str, seed: int) -> None:
    inputs = workflow[node_id]["inputs"]
    if "seed" in inputs:
        inputs["seed"] = seed
    elif "noise_seed" in inputs:
        inputs["noise_seed"] = seed
    else:
        raise ComfyUIError(f"Node de seed '{node_id}' não tem campo 'seed'/'noise_seed' em 'inputs'.")


def extrair_info_modelo(workflow: dict) -> dict:
    """Varre o workflow por campos de nome de modelo (unet/clip/vae/ckpt)."""
    info = {}
    for _, node in _iter_nodes(workflow):
        inputs = node.get("inputs", {})
        for chave in MODEL_FIELDS:
            valor = inputs.get(chave)
            if isinstance(valor, str):
                info[chave] = valor
    return info


# --------------------------------------------------------------------------
# Disparo e espera do workflow
# --------------------------------------------------------------------------

def enfileirar_prompt(workflow: dict, server: str = DEFAULT_SERVER, client_id: str = None):
    client_id = client_id or str(uuid.uuid4())
    payload = {"prompt": workflow, "client_id": client_id}
    url = f"{_base_url(server)}/prompt"
    try:
        resp = requests.post(url, json=payload, timeout=30)
    except requests.exceptions.ConnectionError as e:
        raise _erro_conexao(server, e)
    if resp.status_code != 200:
        raise ComfyUIError(f"Erro ao enfileirar prompt ({resp.status_code}): {resp.text}")
    dado = resp.json()
    if "prompt_id" not in dado:
        raise ComfyUIError(f"Resposta inesperada do ComfyUI ao enfileirar prompt: {dado}")
    return dado["prompt_id"], client_id


def aguardar_resultado(prompt_id: str, server: str = DEFAULT_SERVER, timeout: float = 300.0, intervalo: float = 2.0) -> dict:
    """Faz polling em /history/<prompt_id> até o job terminar (sucesso ou erro)."""
    url = f"{_base_url(server)}/history/{prompt_id}"
    inicio = time.time()
    while time.time() - inicio < timeout:
        try:
            resp = requests.get(url, timeout=15)
        except requests.exceptions.ConnectionError as e:
            raise _erro_conexao(server, e)
        if resp.status_code == 200:
            historico = resp.json()
            entrada = historico.get(prompt_id)
            if entrada:
                status = entrada.get("status", {})
                status_str = status.get("status_str")
                if status_str == "error":
                    raise ComfyUIError(f"ComfyUI reportou erro na geração do prompt {prompt_id}: {status}")
                if status.get("completed") or entrada.get("outputs"):
                    return entrada
        time.sleep(intervalo)
    raise ComfyUIError(f"Timeout ({timeout}s) esperando resultado do prompt {prompt_id}.")


def extrair_imagens_saida(entrada_historico: dict) -> list:
    """Retorna lista de dicts {filename, subfolder, type} das imagens de saída."""
    imagens = []
    for _, saida in entrada_historico.get("outputs", {}).items():
        for img in saida.get("images", []):
            imagens.append(img)
    return imagens


def baixar_imagem(info_imagem: dict, server: str = DEFAULT_SERVER) -> bytes:
    """GET /view. Retorna os bytes da imagem gerada."""
    params = {
        "filename": info_imagem["filename"],
        "subfolder": info_imagem.get("subfolder", ""),
        "type": info_imagem.get("type", "output"),
    }
    url = f"{_base_url(server)}/view?" + urllib.parse.urlencode(params)
    try:
        resp = requests.get(url, timeout=30)
    except requests.exceptions.ConnectionError as e:
        raise _erro_conexao(server, e)
    if resp.status_code != 200:
        raise ComfyUIError(f"Falha ao baixar imagem gerada ({resp.status_code}): {resp.text}")
    return resp.content
