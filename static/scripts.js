
(() => {
  try {
    if (localStorage.getItem("theme") === "dark") {

      document.documentElement.classList.add("dark-mode");
    }
  } catch { /* localStorage pode falhar em navegação privada */ }
})();


const clamp = (n, min, max) => Math.min(Math.max(n, min), max);

function getMaxChapter() {
  const fromBody = parseInt(document.body?.dataset?.maxChapter, 10);
  if (!Number.isNaN(fromBody) && fromBody > 0) return fromBody;
  return 2334; 
}

function getCurrentChapter() {
  const parts = window.location.pathname.replace(/\/+$/,'').split('/').filter(Boolean);
  const last = parts[parts.length - 1];
  const n = parseInt(last, 10);
  return Number.isFinite(n) ? n : 1;
}

function buildUrlWithChapter(n) {
  const { origin, pathname, search, hash } = window.location;
  const parts = pathname.replace(/\/+$/,'').split('/').filter(Boolean);
  if (!parts.length) parts.push(String(n));
  else parts[parts.length - 1] = String(n);
  return origin + '/' + parts.join('/') + (search || '') + (hash || '');
}

function navigateToChapter(n, { max }) {
  const safe = clamp(n, 1, max);
  if (safe !== getCurrentChapter()) {
    window.location.href = buildUrlWithChapter(safe);
  }
}


function applySavedPreferences() {
  try {
    const font = localStorage.getItem("fontFamily");
    if (font) document.body.style.fontFamily = font;

    const fontSize = localStorage.getItem("fontSize");
    if (fontSize) {
      document.querySelectorAll(".content").forEach(el => { el.style.fontSize = fontSize; });
    }

    const fontSelector = document.getElementById("fontSelector");
    if (fontSelector && font) fontSelector.value = font;

    const fontSizeSelector = document.getElementById("fontSizeSelector");
    if (fontSizeSelector && fontSize) fontSizeSelector.value = fontSize;
  } catch { /* ignora erros de storage */ }
}


window.LightDark = function LightDark() {
  const el = document.documentElement;
  el.classList.toggle("dark-mode");
  try {
    localStorage.setItem("theme", el.classList.contains("dark-mode") ? "dark" : "light");
  } catch {}
};

window.changeFont = function changeFont(font) {
  document.body.style.fontFamily = font;
  try { localStorage.setItem("fontFamily", font); } catch {}
};

window.changeFontSize = function changeFontSize(size) {
  document.querySelectorAll(".content").forEach(el => { el.style.fontSize = size; });
  try { localStorage.setItem("fontSize", size); } catch {}
};

window.redirectToPage = function redirectToPage() {
  const select = document.getElementById("lang");
  const value = select?.value;
  if (value) {

    window.location.href = `${window.location.origin}/${value}/1`;
  }
};


function initChapterSelect(selectId, current, max) {
  const sel = document.getElementById(selectId);
  if (!sel) return;

  // Evita repopular se o HTML já trouxe opções
  if (!sel.options || sel.options.length <= 1) {
    const frag = document.createDocumentFragment();
    for (let i = 1; i <= max; i++) {
      const opt = document.createElement("option");
      opt.value = String(i);
      opt.textContent = `Chapter ${i}`;
      if (i === current) opt.selected = true;
      frag.appendChild(opt);
    }
    sel.appendChild(frag);
  } else {
    const target = sel.querySelector(`option[value="${current}"]`);
    if (target) target.selected = true;
  }

  sel.addEventListener("change", () => {
    const chosen = parseInt(sel.value, 10);
    if (Number.isFinite(chosen) && chosen !== current) {
      navigateToChapter(chosen, { max });
    }
  });


  const def = document.getElementById(
    selectId === "list" ? "defaultoptiontop" : "defaultoptionbottom"
  );
  if (def) {
    def.textContent = `Chapter ${current}`;
    def.value = String(current);
  }
}


function bindNavButton(btnId, delta, current, max) {
  const btn = document.getElementById(btnId);
  if (!btn) return;

  const target = current + delta;
  const outOfBounds = target < 1 || target > max;


  btn.style.display = outOfBounds ? "none" : "";

  btn.addEventListener("click", () => {
    navigateToChapter(current + delta, { max });
  }, { passive: true });
}


function enableKeyboardNav(current, max) {
  document.addEventListener("keydown", (e) => {
    const tag = (document.activeElement?.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select" || e.metaKey || e.ctrlKey || e.altKey) return;

    if (e.key === "ArrowLeft") {
      e.preventDefault();
      navigateToChapter(current - 1, { max });
    } else if (e.key === "ArrowRight") {
      e.preventDefault();
      navigateToChapter(current + 1, { max });
    }
  });
}


function initLangSelectize() {
  try {
    if (window.jQuery && typeof jQuery.fn.selectize === "function" && jQuery("#lang").length) {
      jQuery("#lang").selectize({ sortField: "text" });
    }
  } catch { /* ignora se não houver jQuery/selectize */ }
}

document.addEventListener("DOMContentLoaded", () => {
  const max = getMaxChapter();
  const current = clamp(getCurrentChapter(), 1, max);

  applySavedPreferences();
  initLangSelectize();


  initChapterSelect("list", current, max);
  initChapterSelect("listbottom", current, max);


  bindNavButton("prevChapter", -1, current, max);
  bindNavButton("nextChapter", +1, current, max);


  bindNavButton("prevChapterBottom", -1, current, max);
  bindNavButton("nextChapterBottom", +1, current, max);


  enableKeyboardNav(current, max);
});
