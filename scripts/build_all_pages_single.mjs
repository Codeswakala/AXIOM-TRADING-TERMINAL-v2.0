// DA tooling — Operator request (2026-08-19): combine the 30 page captures
// into ONE self-contained HTML file. Each page is embedded base64-encoded and
// rendered into the viewer iframe via srcdoc on selection — full fidelity,
// no external files, no network needed.
import fs from "fs";

const CAPTURES_DIR = "/home/user/axiom_page_captures";
const MANIFEST_PATH = "/home/user/axiom_page_captures_manifest.json";
const OUT_PATH = "/home/user/AXIOM_ALL_PAGES.html";

const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf8"));
const captures = manifest.captures;

const pages = captures.map((c) => {
  const html = fs.readFileSync(`${CAPTURES_DIR}/${c.file}`, "utf8");
  return {
    file: c.file,
    url: c.requestedUrl,
    finalUrl: c.finalUrl,
    note: c.note,
    sha256: c.sha256,
    bytes: c.bytes,
    b64: Buffer.from(html, "utf8").toString("base64"),
  };
});

const navItems = pages
  .map(
    (p, i) => `<button class="nav-item" data-index="${i}" type="button">
  <span class="nav-idx">${String(i + 1).padStart(2, "0")}</span>
  <span class="nav-file">${p.file}</span>
  <span class="nav-url">${p.url}${p.finalUrl !== p.url ? " → " + p.finalUrl : ""}</span>
</button>`,
  )
  .join("\n");

// First page is the initial viewer content.
const firstB64 = pages[0].b64;

const master = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AXIOM — All Page Captures (single file)</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 0; height: 100vh; overflow: hidden;
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: #0d1117; color: #e6edf3;
  }
  .topbar {
    height: 48px; display: flex; align-items: center; gap: 12px;
    padding: 0 16px; background: #161b22; border-bottom: 1px solid #30363d;
  }
  .topbar h1 { font-size: 15px; margin: 0; font-weight: 600; letter-spacing: .02em; }
  .topbar .meta { color: #8b949e; font-size: 12px; }
  .topbar .meta b { color: #c9d1d9; }
  .layout { display: flex; height: calc(100vh - 48px); }
  nav.sidebar {
    width: 360px; min-width: 280px; overflow-y: auto;
    background: #0d1117; border-right: 1px solid #30363d;
    padding: 8px;
  }
  .sidebar-title {
    font-size: 11px; letter-spacing: .08em; text-transform: uppercase;
    color: #8b949e; padding: 6px 8px;
  }
  .nav-item {
    display: flex; align-items: center; gap: 8px; width: 100%;
    text-align: left; padding: 6px 8px; margin-bottom: 2px;
    background: transparent; border: 1px solid transparent; border-radius: 6px;
    color: #c9d1d9; font-size: 12px; cursor: pointer;
  }
  .nav-item:hover { background: #161b22; }
  .nav-item.active { background: rgb(37 99 235 / 14%); border-color: rgb(37 99 235 / 45%); color: #e6edf3; }
  .nav-idx { color: #58a6ff; font-family: ui-monospace, Consolas, monospace; font-size: 11px; min-width: 22px; }
  .nav-file { font-family: ui-monospace, Consolas, monospace; font-size: 11px; flex: 0 0 auto; max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .nav-url { color: #8b949e; font-size: 11px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  main.viewer { flex: 1; background: #010409; padding: 0; position: relative; }
  main.viewer iframe { width: 100%; height: 100%; border: none; background: #010409; }
  .viewer-label {
    position: absolute; top: 10px; right: 12px; z-index: 5;
    background: rgb(13 17 23 / 88%); border: 1px solid #30363d; border-radius: 6px;
    padding: 4px 10px; font-size: 11px; color: #8b949e; font-family: ui-monospace, Consolas, monospace;
  }
</style>
</head>
<body>
  <div class="topbar">
    <h1>AXIOM — All Page Captures</h1>
    <span class="meta"><b>${pages.length} pages</b> · single self-contained file · captured ${manifest.generatedAt} · click a page to view it</span>
  </div>
  <div class="layout">
    <nav class="sidebar" aria-label="Captured pages">
      <div class="sidebar-title">Pages (rendered DOM snapshots)</div>
${navItems}
    </nav>
    <main class="viewer">
      <div class="viewer-label" id="viewer-label">${pages[0].file}</div>
      <iframe id="viewer" title="Page capture viewer" srcdoc="${firstB64
        .replace(/"/g, "&quot;")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")}"></iframe>
    </main>
  </div>
<script>
(function () {
  var pages = ${JSON.stringify(pages.map((p) => ({ file: p.file, url: p.url, finalUrl: p.finalUrl, b64: p.b64 })))};
  var viewer = document.getElementById("viewer");
  var label = document.getElementById("viewer-label");
  var buttons = Array.prototype.slice.call(document.querySelectorAll(".nav-item"));
  function show(index) {
    viewer.srcdoc = atob(pages[index].b64);
    label.textContent = pages[index].file;
    buttons.forEach(function (b, i) {
      b.classList.toggle("active", i === index);
    });
  }
  show(0);
  buttons.forEach(function (btn, index) {
    btn.addEventListener("click", function () { show(index); });
  });
})();
</script>
</body>
</html>
`;

fs.writeFileSync(OUT_PATH, master);
console.log("written:", OUT_PATH, "|", (master.length / 1024 / 1024).toFixed(1), "MB |", pages.length, "pages embedded");
