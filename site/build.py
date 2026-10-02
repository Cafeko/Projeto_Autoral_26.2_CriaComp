"""Gera site/data.json + copia assets para site/assets/.

Uso:  python site/build.py
Rode de novo sempre que adicionar GIFs em animacoes/ ou editar animacoes.json,
planilhas de avaliação ou relatórios. Não apaga flags já marcadas em animacoes.json.
"""
from pathlib import Path
import json, re, shutil, datetime
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
COLS = ROOT / "Coleções"
SITE = ROOT / "site"
ASSETS = SITE / "assets"
IMG_EXTS = {".png", ".jpg", ".jpeg", ".jfif", ".webp", ".gif"}

COLECOES = [
    {"id": "c1", "pasta": "Coleção 1 - Goku", "nome": "Coleção 1 — Goku",
     "personagem": "Goku", "limite": 5, "status": "encerrada",
     "xlsx": "avaliacao_colecao1.xlsx"},
    {"id": "c2", "pasta": "Coleção 2 - Naruto", "nome": "Coleção 2 — Naruto",
     "personagem": "Naruto", "limite": 3, "status": "encerrada",
     "xlsx": "avaliacao_colecao2.xlsx"},
    {"id": "c3", "pasta": "Coleção 3 - Shaka de Virgem", "nome": "Coleção 3 — Shaka",
     "personagem": "Shaka de Virgem", "limite": 5, "status": "em andamento",
     "xlsx": "avaliacao_colecao3.xlsx"},
]

def v(x):
    return "" if x is None else str(x).strip()

def norm_tipo(raw):
    return v(raw).lower()

def norm_placar(raw, tipo):
    """Sempre 'pontuação/total': 5/6, 5/5, 4/6...; vazio se não avaliado."""
    s = v(raw)
    if not s or s in ("—", "N/A", "-"):
        return ""
    m = re.match(r"(\d+)\s*/\s*(\d+)", s)
    if m:
        return f"{m.group(1)}/{m.group(2)}"
    m = re.match(r"(\d+)", s)
    if m:
        total = 6 if tipo == "spritesheet" else 5 if tipo == "único" else ""
        return f"{m.group(1)}/{total}" if total else m.group(1)
    return s

def load_avaliacao(path):
    """(nome_pasta, tentativa) -> dict com tipo, A-D, placar, fica, obs."""
    out = {}
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    for row in ws.iter_rows(min_row=3, values_only=True):
        if not row or not row[0] or str(row[0]).startswith("Legenda"):
            continue
        vals = list(row) + [""] * 17
        nome, t = str(vals[0]), vals[1]
        try:
            t = int(t)
        except (TypeError, ValueError):
            continue
        out[(nome, t)] = {
            "tipo": norm_tipo(vals[3]), "placar": v(vals[14]),
            "fica": v(vals[15]).lower() == "sim", "obs": v(vals[16]),
        }
    return out

REFS_C2 = {
    "imagem 1": "Personagem de casaco azul",
    "imagem 2": "Ninjas com espada",
    "imagem 3": "Ninja vermelho",
    "imagem 4": "Personagem de terno correndo",
    "imagem 5": "Guerreiro armado",
    "imagem 6": "Estilo Chrono Trigger",
    "imagem 7": "Luigi",
    "imagem 8": "Estilo Kingdom Hearts",
}

def gif_entries(folder, ginfo):
    """Normaliza animacoes.json (formato novo 'gifs' em lista ou antigo 'gif' único).
    Devolve [(asset_ou_None, modificada, nota)]."""
    items = []
    if isinstance(ginfo.get("gifs"), list):
        items = ginfo["gifs"]
    elif ginfo.get("gif"):
        items = [{"arquivo": ginfo["gif"],
                  "spritesheet_modificada": ginfo.get("spritesheet_modificada", False),
                  "nota": ginfo.get("nota", "")}]
    out = []
    for g in items:
        rel = None
        if g.get("arquivo") and (folder / g["arquivo"]).exists():
            rel = str(g["arquivo"]).replace("\\", "/")
        out.append((rel, bool(g.get("spritesheet_modificada", False)), g.get("nota", "")))
    return out

def tentativa_nums(folder):
    nums = set()
    for base in [folder, folder / "Descartadas"]:
        if base.is_dir():
            for p in base.iterdir():
                if p.is_file():
                    m = re.match(r"tentativa (\d+) - ", p.name)
                    if m:
                        nums.add(int(m.group(1)))
    meta = json.loads((folder / "animacoes.json").read_text(encoding="utf-8")) \
        if (folder / "animacoes.json").exists() else {"tentativas": {}}
    for n in meta.get("tentativas", {}):
        nums.add(int(n))
    return sorted(nums), meta.get("tentativas", {})

def copy_asset(src, dest_rel):
    dest = ASSETS / dest_rel
    if dest.suffix.lower() == ".jfif":
        # Chrome não exibe .jfif no <img>: copia com extensão .jpg (mesmos bytes)
        dest = dest.with_suffix(".jpg")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return "assets/" + str(dest.relative_to(ASSETS)).replace("\\", "/")

def short_t(base_dir, n, k, ext, kind):
    """Nome curto e único para o asset copiado (evita MAX_PATH no file://).
    O nome original vai em 'nome' no data.json só para exibição."""
    if kind == "anim":
        name = f"t{n}.gif" if k == 0 else f"t{n}-{k}.gif"
    elif kind == "ref":
        name = f"ref{n}{ext}"
    else:
        name = f"t{n}-{k}{ext}"
    return base_dir / name

def main():
    if ASSETS.exists():
        shutil.rmtree(ASSETS)
    data = {"gerado_em": datetime.date.today().isoformat(),
            "eixo": "", "colecoes": [], "testes": []}
    eixo_txt = (ROOT / "Eixo.txt").read_text(encoding="utf-8")
    data["eixo"] = re.sub(r"^EIXO\s*", "", eixo_txt).strip()
    for col in COLECOES:
        cdir = COLS / col["pasta"]
        aval = load_avaliacao(cdir / col["xlsx"])
        cdata = {k: col[k] for k in ("id", "nome", "personagem", "limite", "status")}
        cdata["imagens"] = []
        all_folders = []
        for grupo in ["Finais", "Descartados"]:
            gdir = cdir / grupo
            if not gdir.is_dir():
                continue
            for d in gdir.iterdir():
                if d.is_dir():
                    all_folders.append((grupo, d))
        all_folders.sort(key=lambda t: int(re.match(r"imagem (\d+)", t[1].name).group(1))
                         if re.match(r"imagem (\d+)", t[1].name) else 999)
        for grupo, folder in all_folders:
                if not folder.is_dir():
                    continue
                m = re.match(r"imagem (\d+) - (.*)", folder.name)
                if m:
                    numero, ref = m.group(1), m.group(2)
                else:
                    numero, ref = folder.name.replace("imagem ", ""), REFS_C2.get(folder.name, folder.name)
                nums, meta = tentativa_nums(folder)
                # referência
                ref_imgs, ref_gifs = [], []
                basedir = Path(col["id"]) / grupo / numero
                kref = 0
                for p in sorted((folder / "Original").iterdir()) if (folder / "Original").is_dir() else []:
                    if p.is_file() and p.suffix.lower() in IMG_EXTS:
                        rel = copy_asset(p, short_t(basedir / "Original", kref, 0, p.suffix.lower(), "ref"))
                        kref += 1
                        entry = {"src": rel, "nome": p.name}
                        if p.suffix.lower() == ".gif":
                            ref_gifs.append(entry)
                        else:
                            ref_imgs.append(entry)
                tents = []
                aprovada = None
                for n in nums:
                    files = []
                    k = 0
                    for base in [folder, folder / "Descartadas"]:
                        for p in sorted(base.iterdir()) if base.is_dir() else []:
                            if p.is_file() and re.match(rf"tentativa {n} - ", p.name) and p.suffix.lower() in IMG_EXTS:
                                sub = Path("Descartadas") if base.name == "Descartadas" else Path()
                                rel = copy_asset(p, short_t(basedir / sub, n, k, p.suffix.lower(), "tent"))
                                files.append({"src": rel, "nome": p.name})
                                k += 1
                    ev = aval.get((folder.name, n), {})
                    fica = ev.get("fica", False)
                    if fica and aprovada is None:
                        aprovada = n
                    mkey, ginfo = str(n), meta.get(str(n), {})
                    gif_list = []
                    for gi, (rel, mod, nota) in enumerate(gif_entries(folder, ginfo)):
                        asset = copy_asset(folder / rel, short_t(basedir / "animacoes", n, gi, Path(rel).suffix.lower(), "anim")) if rel else None
                        gif_list.append({"gif": asset, "nome": Path(rel).name if rel else "",
                                         "gif_modificada": mod, "gif_nota": nota})
                    tipo = ev.get("tipo", "")
                    tents.append({
                        "n": n, "arquivos": files, "tipo": tipo,
                        "aprovada": fica, "placar": norm_placar(ev.get("placar", ""), tipo),
                        "motivo": ev.get("obs", ""),
                        "gif": gif_list[0]["gif"] if gif_list else None,
                        "gif_modificada": gif_list[0]["gif_modificada"] if gif_list else False,
                        "gif_nota": gif_list[0]["gif_nota"] if gif_list else "",
                        "gifs": gif_list,
                    })
                tipos = {t["tipo"] for t in tents if t["tipo"]}
                unico = bool(tipos) and all(t == "único" for t in tipos)
                cdata["imagens"].append({
                    "numero": numero, "referencia": ref, "grupo": grupo,
                    "status": "fica" if aprovada else "descartada",
                    "unico": unico,
                    "tipo": "único" if unico else ("spritesheet" if "spritesheet" in tipos else ""),
                    "tentativa_aprovada": aprovada,
                    "tentativas": tents,
                    "referencia_imagens": ref_imgs,
                    "referencia_animacao": ref_gifs[0]["src"] if ref_gifs else None,
                    "referencia_animacoes": ref_gifs,
                })
        data["colecoes"].append(cdata)
    # testes
    tbase = ROOT / "Testes" / "Imagens de teste"
    if tbase.is_dir():
        grupos, ti = {}, 0
        for p in sorted(tbase.rglob("*")):
            if p.is_file() and p.suffix.lower() in IMG_EXTS:
                g = str(p.parent.relative_to(tbase)) or "raiz"
                rel = copy_asset(p, Path("testes") / f"teste{ti:03d}{p.suffix.lower()}")
                ti += 1
                grupos.setdefault(g, []).append({"src": rel, "nome": p.name})
        data["testes"] = [{"grupo": g, "arquivos": a} for g, a in sorted(grupos.items())]
    (SITE / "data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    # data.js embute os dados para a página abrir até com duplo clique (file://)
    (SITE / "data.js").write_text("window.SITE_DATA = " + json.dumps(data, ensure_ascii=False) + ";", encoding="utf-8")
    n_img = sum(len(i["tentativas"]) for c in data["colecoes"] for i in c["imagens"])
    n_gif = sum(1 for c in data["colecoes"] for i in c["imagens"] for t in i["tentativas"] if t["gif"])
    print(f"OK: {len(data['colecoes'])} coleções, {n_img} tentativas, {n_gif} GIFs, "
          f"{sum(len(t['arquivos']) for t in data['testes'])} arquivos de teste")

if __name__ == "__main__":
    main()
