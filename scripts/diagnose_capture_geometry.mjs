// DA internal diagnostic — untracked tooling, NOT part of any shipped patch.
// Purpose: measure exactly where the watchlist price column clips at the
// capture-01/03 environment (1920x1080, deviceScaleFactor 1), per
// CA-DATA1-3. Image-is-primary discipline requires the geometry to be
// measured, not assumed.
import { chromium } from "../frontend/node_modules/playwright/index.mjs";

async function login(page) {
  await page.goto("http://localhost:5173/login", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(900);
  await page
    .locator('input[data-testid="login-username-input"], input#username-input')
    .first()
    .fill("admin");
  await page
    .locator('input[data-testid="login-password-input"], input#password-input')
    .first()
    .fill("AxiomSecurePass2026!");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2500);
}

function rectOf(el) {
  const r = el.getBoundingClientRect();
  return { left: +r.left.toFixed(1), right: +r.right.toFixed(1), top: +r.top.toFixed(1), bottom: +r.bottom.toFixed(1), width: +r.width.toFixed(1) };
}

async function measure(page) {
  return page.evaluate(() => {
    const out = {};
    const grid = document.querySelector(".terminal-stage-grid");
    out.gridCols = grid ? getComputedStyle(grid).gridTemplateColumns : null;
    const slot = document.querySelector(".terminal-slot-left");
    const dock = document.querySelector('[data-testid="terminal-watchlist-dock"]');
    const rows = document.querySelector(".watchlist-rows-container");
    out.slotRect = slot ? (() => { const r = slot.getBoundingClientRect(); return { left: +r.left.toFixed(1), right: +r.right.toFixed(1), width: +r.width.toFixed(1) }; })() : null;
    out.dockRect = dock ? (() => { const r = dock.getBoundingClientRect(); return { left: +r.left.toFixed(1), right: +r.right.toFixed(1), width: +r.width.toFixed(1) }; })() : null;
    out.rowsRect = rows ? (() => { const r = rows.getBoundingClientRect(); return { left: +r.left.toFixed(1), right: +r.right.toFixed(1), width: +r.width.toFixed(1), clientWidth: rows.clientWidth, scrollWidth: rows.scrollWidth, overflowX: getComputedStyle(rows).overflowX }; })() : null;
    out.rows = {};
    for (const sym of ["USD/JPY", "BTC/USD", "ETH/USD", "SOL/USD", "EUR/USD"]) {
      const testid = `watchlist-row-${sym.toLowerCase().replace("/", "-")}`;
      const row = document.querySelector(`[data-testid="${testid}"]`);
      if (!row) { out.rows[sym] = null; continue; }
      const price = row.querySelector('[data-testid^="price-"]');
      const chip = row.querySelector('[data-testid^="watchlist-provenance-"]');
      const spark = row.querySelector('[data-testid^="watchlist-sparkline-"]');
      const tag = row.querySelector('[data-testid^="watchlist-sparkline-source-"]');
      const change = row.querySelector('[data-testid^="change-"]');
      const range = row.querySelector('[data-testid^="range-"]');
      const metrics = row.querySelector(".item-metrics-block");
      const symBlock = row.querySelector(".item-symbol-block");
      const clipRight = rows ? rows.getBoundingClientRect().right : null;
      const vis = (el) => {
        if (!el) return null;
        const r = el.getBoundingClientRect();
        const inside = clipRight !== null ? r.right <= clipRight + 0.5 : null;
        return { rect: { left: +r.left.toFixed(1), right: +r.right.toFixed(1), width: +r.width.toFixed(1) }, text: el.textContent?.trim()?.slice(0, 40), fullyInside: inside };
      };
      out.rows[sym] = {
        row: row.getBoundingClientRect() ? { right: +row.getBoundingClientRect().right.toFixed(1) } : null,
        symBlock: vis(symBlock),
        metrics: vis(metrics),
        price: vis(price),
        chip: vis(chip),
        spark: vis(spark),
        tag: vis(tag),
        change: vis(change),
        range: vis(range),
      };
    }
    return out;
  });
}

const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();
await login(page);
await page.goto("http://localhost:5173/", { waitUntil: "domcontentloaded" });
await page.waitForSelector('[data-testid="terminal-watchlist-dock"]', { state: "visible", timeout: 15000 });
await page.waitForTimeout(7000);
console.log(JSON.stringify(await measure(page), null, 2));
await browser.close();
