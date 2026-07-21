// wabisabi-docs client layer. No framework — the pages are pre-rendered; this
// just adds the interactive shell: theme toggle, mobile nav, project switcher,
// ⌘K search over the per-project index, outline scrollspy, and copy buttons.
(function () {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  // ---- theme ----
  const root = document.documentElement;
  function currentTheme() {
    return root.dataset.theme || "dark";
  }
  $$("[data-theme-toggle]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const next = currentTheme() === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try {
        localStorage.setItem("wd-theme", next);
      } catch (e) {}
    }),
  );

  // ---- mobile nav ----
  const body = document.body;
  const menuBtn = $("[data-menu]");
  const scrim = $("[data-scrim]");
  if (menuBtn) menuBtn.addEventListener("click", () => body.classList.toggle("nav-open"));
  if (scrim) scrim.addEventListener("click", () => body.classList.remove("nav-open"));
  $$(".sidebar .nav-item").forEach((a) => a.addEventListener("click", () => body.classList.remove("nav-open")));

  // ---- project switcher ----
  const switcherBtn = $("[data-switcher]");
  const switcherMenu = $("[data-switcher-menu]");
  if (switcherBtn && switcherMenu) {
    switcherBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = switcherMenu.hasAttribute("hidden");
      if (open) switcherMenu.removeAttribute("hidden");
      else switcherMenu.setAttribute("hidden", "");
      switcherBtn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", () => {
      switcherMenu.setAttribute("hidden", "");
      switcherBtn.setAttribute("aria-expanded", "false");
    });
  }

  // ---- copy buttons (into the code header when present, else on the <pre>) ----
  $$(".prose pre").forEach((pre) => {
    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.type = "button";
    btn.textContent = "Copy";
    btn.addEventListener("click", () => {
      const code = pre.querySelector("code");
      navigator.clipboard.writeText(code ? code.innerText : pre.innerText).then(() => {
        btn.textContent = "Copied";
        btn.classList.add("copied");
        setTimeout(() => {
          btn.textContent = "Copy";
          btn.classList.remove("copied");
        }, 1400);
      });
    });
    const block = pre.closest(".code-block");
    const head = block && block.querySelector(".code-head");
    if (head) head.appendChild(btn);
    else pre.appendChild(btn);
  });

  // ---- tabbed content: build the tab bar from the panels' data-tab labels ----
  $$("[data-tabs]").forEach((wrap) => {
    const panels = $$(".tab-panel", wrap);
    if (!panels.length) return;
    const bar = document.createElement("div");
    bar.className = "tab-bar";
    panels.forEach((panel, i) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "tab-btn" + (i === 0 ? " active" : "");
      b.textContent = panel.getAttribute("data-tab") || "Tab " + (i + 1);
      b.addEventListener("click", () => {
        panels.forEach((p, j) => (p.hidden = j !== i));
        $$(".tab-btn", bar).forEach((x, j) => x.classList.toggle("active", j === i));
      });
      bar.appendChild(b);
      panel.hidden = i !== 0;
    });
    wrap.insertBefore(bar, panels[0]);
  });

  // ---- connect-to-AI modal ----
  const connectOv = $("[data-connect-overlay]");
  if (connectOv) {
    const openConnect = () => connectOv.removeAttribute("hidden");
    const closeConnect = () => connectOv.setAttribute("hidden", "");
    $$("[data-connect-open]").forEach((b) => b.addEventListener("click", openConnect));
    $$("[data-connect-close]").forEach((b) => b.addEventListener("click", closeConnect));
    connectOv.addEventListener("click", (e) => {
      if (e.target === connectOv) closeConnect();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !connectOv.hasAttribute("hidden")) closeConnect();
    });
    $$(".copy-btn", connectOv).forEach((btn) => {
      btn.addEventListener("click", () => {
        const row = btn.closest(".connect-url, .connect-snippet");
        const codeEl = row && row.querySelector("code");
        navigator.clipboard.writeText(codeEl ? codeEl.innerText : "").then(() => {
          btn.textContent = "Copied";
          btn.classList.add("copied");
          setTimeout(() => {
            btn.textContent = "Copy";
            btn.classList.remove("copied");
          }, 1400);
        });
      });
    });
  }

  // ---- dismissible mobile ad anchor (per browsing session) ----
  const adAnchor = $("[data-ad-anchor]");
  if (adAnchor) {
    let closed = false;
    try {
      closed = sessionStorage.getItem("wd-ad-anchor") === "1";
    } catch (e) {}
    if (closed) {
      adAnchor.remove();
    } else {
      const x = $("[data-ad-anchor-close]", adAnchor);
      if (x)
        x.addEventListener("click", () => {
          adAnchor.remove();
          try {
            sessionStorage.setItem("wd-ad-anchor", "1");
          } catch (e) {}
        });
    }
  }

  // ---- image lightbox ----
  let lb = null;
  function openLightbox(src) {
    if (!lb) {
      lb = document.createElement("div");
      lb.className = "lightbox";
      lb.hidden = true;
      lb.innerHTML = '<img alt="">';
      lb.addEventListener("click", () => (lb.hidden = true));
      document.body.appendChild(lb);
    }
    lb.querySelector("img").src = src;
    lb.hidden = false;
  }
  $$(".prose img").forEach((img) => img.addEventListener("click", () => openLightbox(img.currentSrc || img.src)));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && lb && !lb.hidden) lb.hidden = true;
  });

  // ---- outline scrollspy ----
  const tocLinks = $$(".toc-list a");
  if (tocLinks.length) {
    const byId = {};
    tocLinks.forEach((a) => (byId[a.getAttribute("href").slice(1)] = a));
    const heads = $$(".prose h2[id], .prose h3[id]");
    let active = null;
    const spy = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            const a = byId[en.target.id];
            if (a && a !== active) {
              if (active) active.classList.remove("active");
              a.classList.add("active");
              active = a;
            }
          }
        });
      },
      { rootMargin: "-80px 0px -70% 0px", threshold: 0 },
    );
    heads.forEach((h) => spy.observe(h));
  }

  // ---- search ----
  const overlay = $("[data-search-overlay]");
  const input = $("[data-search-input]");
  const results = $("[data-search-results]");
  const project = body.dataset.project;
  const relativePrefix = (body.dataset.searchPath || "").replace("search-index.json", "");
  let index = null;
  let hits = [];
  let sel = 0;

  function openSearch() {
    if (!overlay) return;
    overlay.removeAttribute("hidden");
    if (input) {
      input.value = "";
      input.focus();
    }
    if (results) results.innerHTML = "";
    if (index === null && project) {
      const searchPath = body.dataset.searchPath || `/${project}/search-index.json`;
      fetch(searchPath)
        .then((r) => r.json())
        .then((data) => (index = data))
        .catch(() => (index = []));
    }
  }
  function closeSearch() {
    if (overlay) overlay.setAttribute("hidden", "");
  }

  function score(entry, tokens) {
    const title = entry.title.toLowerCase();
    const headings = (entry.headings || []).join(" ").toLowerCase();
    const bodyText = (entry.body || "").toLowerCase();
    let s = 0;
    for (const t of tokens) {
      if (!t) continue;
      if (title.includes(t)) s += title.startsWith(t) ? 14 : 10;
      if (headings.includes(t)) s += 5;
      if (bodyText.includes(t)) s += 1;
      if (!title.includes(t) && !headings.includes(t) && !bodyText.includes(t)) return 0;
    }
    return s;
  }

  function highlight(text, tokens) {
    let out = esc(text);
    for (const t of tokens) {
      if (!t) continue;
      out = out.replace(new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig"), "<mark>$1</mark>");
    }
    return out;
  }

  function runSearch() {
    if (!results) return;
    const q = (input.value || "").trim().toLowerCase();
    if (!q || !index) {
      results.innerHTML = "";
      hits = [];
      return;
    }
    const tokens = q.split(/\s+/);
    hits = index
      .map((e) => ({ e, s: score(e, tokens) }))
      .filter((x) => x.s > 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, 8)
      .map((x) => x.e);
    sel = 0;
    if (!hits.length) {
      results.innerHTML = '<div class="search-empty">No results</div>';
      return;
    }
    results.innerHTML = hits
      .map(
        (e, i) =>
          `<a class="search-hit${i === 0 ? " active" : ""}" href="${relativePrefix}${e.url}"><span class="h-title">${highlight(e.title, tokens)}</span><span class="h-crumb">${esc(e.group || "")}</span></a>`,
      )
      .join("");
  }

  function moveSel(d) {
    const els = $$(".search-hit", results);
    if (!els.length) return;
    els[sel] && els[sel].classList.remove("active");
    sel = (sel + d + els.length) % els.length;
    els[sel].classList.add("active");
    els[sel].scrollIntoView({ block: "nearest" });
  }

  if (input) input.addEventListener("input", runSearch);
  $$("[data-search-open]").forEach((b) => b.addEventListener("click", openSearch));
  if (overlay)
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) closeSearch();
    });

  document.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      openSearch();
      return;
    }
    if (overlay && overlay.hasAttribute("hidden")) return;
    if (e.key === "Escape") closeSearch();
    else if (e.key === "ArrowDown") {
      e.preventDefault();
      moveSel(1);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      moveSel(-1);
    } else if (e.key === "Enter") {
      const els = $$(".search-hit", results);
      if (els[sel]) window.location.href = els[sel].getAttribute("href");
    }
  });

  // ---- syntax highlighting initialization ----
  if (window.hljs) {
    window.hljs.configure({ ignoreUnescapedHTML: true });
    window.hljs.highlightAll();
  }
})();
