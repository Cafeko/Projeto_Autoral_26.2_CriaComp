# Projeto Autoral 2026.2 — Coleções de Sprites

Criatividade Computacional (UFPE), Bloco 2. Três coleções de sprites e spritesheets
(Goku, Naruto e Shaka de Virgem) geradas com IA a partir de um eixo declarado.

## Ver a galeria (para visitantes)

Acesse pelo link, sem instalar nada:

**https://cafeko.github.io/Projeto_Autoral_26.2_CriaComp/site/**

Dá para filtrar por coleção, ver aprovadas × descartadas lado a lado com a
referência, comparar as animações (quando houver GIF) e pesquisar por nome.
Cada tentativa mostra placar e motivo da avaliação.

## Atualizar a galeria (para o grupo)

1. Edite as pastas em `Coleções/`, as planilhas `avaliacao_colecao*.xlsx`,
   os `animacoes.json` ou o `Eixo.txt` e salve.
2. Faça commit e `git push origin main`.
3. O GitHub reconstrói o site sozinho (Actions → "Rebuild gallery") e o link
   acima se atualiza em ~2 minutos. Não precisa rodar nada manualmente.

Para ver as mudanças na hora, na sua máquina: `python site/serve.py` e abra
`http://localhost:8000/site/` — a página recarrega sozinha a cada save.

## Estrutura

- `Eixo.txt` — o eixo declarado (1 parágrafo).
- `Coleções/` — Coleção 1 (Goku), Coleção 2 (Naruto), Coleção 3 (Shaka):
  `Finais/` e `Descartados/`, cada imagem com `Original/`, tentativas,
  `animacoes/` (GIFs) e `animacoes.json` (flags de animação).
- `caderno_de_bordo.md` — prompts, tentativas, descarte, limitações e skills.
- `site/` — galeria estática (`build.py` gera, `serve.py` serve com rebuild auto).
- `Testes/` — experimentos de ferramenta e prompt (apoio, não artefatos).
