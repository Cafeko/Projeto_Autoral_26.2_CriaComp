let DATA = null;
const state = { col: "todas", status: "todas", gif: "todas", q: "" };
const U = (p) => encodeURI(p);
const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;");
const cap = (nome) => `<div class="cap">${esc(nome)}</div>`;
function shots(arr) {
  return (arr || []).map((a) => `<div class="pic"><a href="${U(a.src)}" target="_blank" title="abrir em tamanho real"><img loading="lazy" src="${U(a.src)}"></a>${cap(a.nome || a.src)}</div>`).join("");
}

// quando servido por site/serve.py, recarrega sozinho após cada rebuild;
// em file:// ou hospedagem estática o fetch falha e nada acontece.
async function liveReload() {
  try {
    const r = await fetch("/__built", { cache: "no-store" });
    if (!r.ok) return;
    const t0 = await r.text();
    setInterval(async () => {
      try {
        const r2 = await fetch("/__built", { cache: "no-store" });
        if (r2.ok && (await r2.text()) !== t0) location.reload();
      } catch (e) { /* sem servidor: ignora */ }
    }, 3000);
  } catch (e) { /* file:// ou estático: ignora */ }
}

async function init() {
  // upscale nítido: sprites minúsculos exibem ampliados (pixelated = sem borrar)
  document.addEventListener("load", (e) => {
    const t = e.target;
    if (t && t.tagName === "IMG" && t.closest(".pic")) {
      const w = t.naturalWidth;
      if (w && w < 240) t.style.width = Math.min(w * 4, 560) + "px";
    }
  }, true);
  // marca imagens que não carregarem, para sabermos quais são
  document.addEventListener("error", (e) => {
    const t = e.target;
    if (t && t.tagName === "IMG" && t.closest(".pic") && !t.dataset.err) {
      t.dataset.err = "1";
      const s = document.createElement("span");
      s.className = "pend";
      s.textContent = "não carregou: " + (t.getAttribute("src") || "").split("/").pop();
      t.replaceWith(s);
    }
  }, true);
  liveReload();
  DATA = window.SITE_DATA;
  document.getElementById("eixo").textContent = DATA.eixo;
  const pills = document.getElementById("colPills");
  const mk = (id, label) => {
    const b = document.createElement("button");
    b.textContent = label; b.dataset.id = id;
    if (id === "todas") b.classList.add("on");
    b.onclick = () => {
      state.col = id;
      pills.querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
      render();
    };
    pills.appendChild(b);
  };
  mk("todas", "Todas");
  DATA.colecoes.forEach((c) => mk(c.id, c.nome));
  mk("testes", "Testes");
  let nF = 0, nT = 0, nG = 0;
  DATA.colecoes.forEach((c) => c.imagens.forEach((i) => {
    if (i.status === "fica") nF++;
    i.tentativas.forEach((t) => { nT++; nG += (t.gifs || []).filter((g) => g.gif).length; });
  }));
  document.getElementById("stats").textContent =
    `${DATA.colecoes.length} coleções · ${nF} imagens aprovadas · ${nT} tentativas · ${nG} animações`;
  for (const id of ["fStatus", "fGif"]) document.getElementById(id).onchange = (e) => {
    state[id === "fStatus" ? "status" : "gif"] = e.target.value; render();
  };
  document.getElementById("q").oninput = (e) => { state.q = e.target.value.toLowerCase(); render(); };
  document.getElementById("galeria").addEventListener("click", (e) => {
    const card = e.target.closest(".card");
    if (!card) return;
    const v = e.target.closest("[data-view]");
    if (v) {
      card.querySelectorAll("[data-view]").forEach((x) => x.classList.toggle("on", x === v));
      card.querySelector(".view-sheets").hidden = v.dataset.view !== "sheets";
      card.querySelector(".view-gifs").hidden = v.dataset.view !== "gifs";
      return;
    }
    const p = e.target.closest("[data-t]");
    if (p) {
      card.querySelectorAll("[data-t]").forEach((x) => x.classList.toggle("on", x === p));
      card.querySelectorAll("[data-tpanel]").forEach((x) => { x.hidden = x.dataset.tpanel !== p.dataset.t; });
    }
  });
  render();
}

function gifItems(list, n) {
  list = list || [];
  const real = list.filter((g) => g.gif);
  if (!real.length) return `<span class="pend">GIF pendente — solte o gif na mesma pasta da tentativa</span>`;
  return real.map((g) => {
    const name = `<span class="cap">${esc(g.nome || String(g.gif).split("/").pop())}</span>`;
    return `<div class="pic"><a href="${U(g.gif)}" target="_blank" title="abrir em tamanho real"><img loading="lazy" src="${U(g.gif)}"></a>${name}</div>`;
  }).join("");
}

function card(col, i, idx) {
  const badge = i.status === "fica"
    ? `<span class="badge ok">FICA${i.tentativa_aprovada ? " · t" + i.tentativa_aprovada : ""}</span>`
    : `<span class="badge no">DESCARTADA</span>`;
  const refShots = shots(i.referencia_imagens);
  const refGifList = (i.referencia_animacoes && i.referencia_animacoes.length
    ? i.referencia_animacoes
    : (i.referencia_animacao ? [{ src: i.referencia_animacao }] : []));
  const refGifHtml = refGifList.length
    ? refGifList.map((a) => `<div class="pic"><a href="${U(a.src)}" target="_blank" title="abrir em tamanho real"><img loading="lazy" src="${U(a.src)}"></a>${cap(a.nome || a.src)}</div>`).join("")
    : `<span class="pend">Sem animação da referência</span>`;
  const def = i.tentativa_aprovada ?? (i.tentativas[0] && i.tentativas[0].n);
  const pick = `<span class="tpick">Tentativa: ` + i.tentativas.map((t) =>
    `<button data-t="${t.n}" class="${t.n === def ? "on" : ""}">T${t.n}${t.aprovada ? " ✓" : ""}</button>`).join("") + `</span>`;
  const badgeT = (t) => `${t.aprovada ? `<span class="badge ok">aprovada</span>` : `<span class="badge no">descartada</span>`}
    ${t.placar ? `<span class="meta">${esc(t.placar)}</span>` : ""}`;
  const motivoT = (t) => (!t.aprovada && t.motivo) ? `<div class="motivo">${esc(t.motivo)}</div>` : "";
  const sheetPanels = i.tentativas.map((t) => `
    <div class="side" data-tpanel="${t.n}" ${t.n === def ? "" : "hidden"}>
      <h4>T${t.n} ${badgeT(t)}</h4>
      ${shots(t.arquivos)}
      ${motivoT(t)}
    </div>`).join("");
  const gifPanels = i.tentativas.map((t) => `
    <div class="side" data-tpanel="${t.n}" ${t.n === def ? "" : "hidden"}>
      <h4>T${t.n} ${badgeT(t)}</h4>
      ${gifItems(t.gifs)}
      ${motivoT(t)}
    </div>`).join("");
  const sheets = `<div class="cmp"><div class="side"><h4>Referência</h4>${refShots}</div>${sheetPanels}</div>`;
  const gifs = `<div class="cmp"><div class="side"><h4>Referência</h4>${refGifHtml}</div>${gifPanels}</div>`;
  const tabs = i.unico ? "" :
    `<span class="tabs"><button class="on" data-view="sheets">Sheets lado a lado</button><button data-view="gifs">Animações lado a lado</button></span>`;
  const gifsView = i.unico ? "" : `<div class="view-gifs" hidden>${gifs}</div>`;
  return `<article class="card">
    <header>${badge}<h2>${esc(i.numero)} · ${esc(i.referencia)}</h2>
      <span class="meta">${i.unico ? "sprite único" : "spritesheet"} · ${esc(col.nome)} · ${i.tentativas.length} tentativa(s)</span>
      ${tabs}</header>
    <div class="pickbar">${pick}</div>
    <div class="view-sheets">${sheets}</div>
    ${gifsView}
  </article>`;
}

function render() {
  const gal = document.getElementById("galeria");
  const showTests = state.col === "testes";
  document.getElementById("testes").hidden = !showTests;
  gal.innerHTML = "";
  if (showTests) { renderTests(); return; }
  let html = "";
  DATA.colecoes.filter((c) => state.col === "todas" || c.id === state.col).forEach((col) => {
    const imgs = col.imagens.filter((i) => {
      if (state.status !== "todas" && i.status !== state.status) return false;
      const hasGif = i.tentativas.some((t) => (t.gifs || []).some((g) => g.gif));
      if (state.gif === "com" && !hasGif) return false;
      if (state.gif === "sem" && hasGif && !i.tentativas.some((t) => !(t.gifs || []).some((g) => g.gif))) return false;
      if (state.q && !(i.referencia + " " + i.numero).toLowerCase().includes(state.q)) return false;
      return true;
    });
    if (imgs.length) html += `<h2>${esc(col.nome)} <span class="meta">· ${col.limite} tentativas/ref · ${esc(col.status)}</span></h2>` +
      imgs.map((i) => card(col, i)).join("");
  });
  gal.innerHTML = html || `<p class="meta">Nada encontrado com esses filtros.</p>`;
}

function renderTests() {
  const g = document.getElementById("testesGrid");
  const q = state.q;
  g.innerHTML = DATA.testes.map((t) => {
    const files = t.arquivos.filter((a) => !q || (a.src + " " + (a.nome || "")).toLowerCase().includes(q));
    if (!files.length) return "";
    return `<h3 style="grid-column:1/-1">${esc(t.grupo)} <span class="meta">· ${files.length}</span></h3>` +
      files.map((a) => `<figure><a href="${U(a.src)}" target="_blank"><img loading="lazy" src="${U(a.src)}"></a><figcaption>${esc(a.nome || a.src)}</figcaption></figure>`).join("");
  }).join("");
}

init();
