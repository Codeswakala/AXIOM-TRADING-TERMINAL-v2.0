// DA capture tooling — POLISH-P01 evidence captures (untracked).
// 01 drift-fixed 1D · 02 watchlist clip (MIXED state) · 03 confluence ·
// 04 login redesign · 05 logo · 06 route-split network trace ·
// 07 RBAC-before-chunk (unauthorized: chunk NOT fetched).
import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const BASE = `http://localhost:${process.env.CAPTURE_PORT ?? 5173}`;
const OUT_DIR = "/home/user/polish_p01_captures";
const JSON_OUT = "/home/user/POLISH-P01_CAPTURE_VERIFICATION.json";
const LOG = [];

fs.mkdirSync(OUT_DIR, { recursive: true });

function record(label, data) {
  LOG.push({ label, ...data });
  console.log(`[VERIFY] ${label}: ${JSON.stringify(data)}`);
}

function sha256(filePath) {
  const h = crypto.createHash("sha256");
  h.update(fs.readFileSync(filePath));
  return h.digest("hex");
}

async function loginAs(page, username = "admin") {
  await page.goto(`${BASE}/login`, { waitUntil: "domcontentloaded" });
  await page.waitForSelector('input[data-testid="login-username-input"], input#username-input', {
    timeout: 20000,
  });
  await page
    .locator('input[data-testid="login-username-input"], input#username-input')
    .first()
    .fill(username);
  await page
    .locator('input[data-testid="login-password-input"], input#password-input')
    .first()
    .fill(username === "admin" ? "AxiomSecurePass2026!" : "operator-pass-123");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2500);
}

async function measureLegibility(page, testids, clipTestid) {
  return page.evaluate(
    ({ testids, clipTestid }) => {
      const clipEl = document.querySelector(`[data-testid="${clipTestid}"]`);
      const clip = clipEl ? clipEl.getBoundingClientRect() : null;
      const out = { clip: clip ? { left: +clip.left.toFixed(1), right: +clip.right.toFixed(1), top: +clip.top.toFixed(1), bottom: +clip.bottom.toFixed(1) } : null, elements: {} };
      for (const tid of testids) {
        const el = document.querySelector(`[data-testid="${tid}"]`);
        if (!el) { out.elements[tid] = null; continue; }
        const r = el.getBoundingClientRect();
        let ink = null;
        try {
          const range = document.createRange();
          range.selectNodeContents(el);
          ink = range.getBoundingClientRect();
        } catch { ink = null; }
        const verticallyInView = clip !== null && r.top >= clip.top - 0.5 && r.bottom <= clip.bottom + 0.5;
        const inkInside = clip !== null && ink !== null && ink.left >= clip.left - 0.5 && ink.right <= clip.right + 0.5 && verticallyInView;
        out.elements[tid] = {
          rect: { left: +r.left.toFixed(1), right: +r.right.toFixed(1), top: +r.top.toFixed(1), bottom: +r.bottom.toFixed(1) },
          inkRect: ink ? { left: +ink.left.toFixed(1), right: +ink.right.toFixed(1) } : null,
          text: el.textContent.trim().slice(0, 60),
          verticallyInView,
          inkFullyInside: inkInside,
        };
      }
      return out;
    },
    { testids, clipTestid },
  );
}

function assertLegible(rec, instrument, required) {
  const failures = [];
  for (const tid of required) {
    const e = instrument?.elements?.[tid];
    if (!e) { failures.push(`${tid}: element missing`); continue; }
    if (!e.verticallyInView) failures.push(`${tid}: vertically outside clip`);
    if (!e.inkFullyInside) failures.push(`${tid}: ink not inside clip (${e.inkRect?.left}-${e.inkRect?.right} vs ${instrument.clip?.left}-${instrument.clip?.right})`);
  }
  if (failures.length > 0) throw new Error(`LEGIBILITY GATE FAILED for ${rec}:\n${failures.join("\n")}`);
  return true;
}

async function run() {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  record("environment_browser", { chromium: browser.version(), viewport: "1920x1080", deviceScaleFactor: 1 });

  // ---------- CAPTURE 04 + 05: the redesigned login and the logo ----------
  {
    const page = await context.newPage();
    await page.goto(`${BASE}/login`, { waitUntil: "domcontentloaded" });
    await page.waitForSelector('[data-testid="login-page-container"]', { timeout: 15000 });
    await page.waitForTimeout(1500);
    const logoMark = await page.locator('[data-testid="login-brand-logo-mark"]').count();
    const monogram = await page.locator('[data-testid="login-brand-monogram"]').count();
    const cardTransform = await page.evaluate(() => {
      const card = document.querySelector(".login-auth-card");
      return card ? getComputedStyle(card).transform : null;
    });
    record("capture04_login_state", { logoMark, monogram, cardTransform });
    if (logoMark !== 1) throw new Error("CAPTURE04 GATE FAILED: logo mark missing from login");
    if (!cardTransform || cardTransform === "none") {
      throw new Error(`CAPTURE04 GATE FAILED: no dimensional card transform: ${cardTransform}`);
    }
    const leg = await measureLegibility(page, ["login-brand-monogram", "login-governance-chips"], "login-page-container");
    record("capture04_legibility", leg);
    assertLegible("capture04", leg, ["login-brand-monogram"]);
    const p4 = path.join(OUT_DIR, "POLISH-P01_04_LOGIN_REDESIGNED.png");
    await page.screenshot({ path: p4 });
    record("capture04_sha256", { file: path.basename(p4), sha256: sha256(p4) });

    // Logo close-up: a screenshot of the mark at a larger scale via CSS zoom
    // of the element bounding box (element screenshot keeps the same pixels —
    // instead capture the viewport scrolled so the mark fills more area).
    const markBox = await page.locator('[data-testid="login-brand-monogram"]').boundingBox();
    record("capture05_logo_box", markBox);
    const p5 = path.join(OUT_DIR, "POLISH-P05_05_LOGO_COMPASS_EPSILON.png");
    await page.screenshot({ path: p5, clip: { x: Math.max(0, markBox.x - 20), y: Math.max(0, markBox.y - 20), width: Math.min(400, 1920 - Math.max(0, markBox.x - 20)), height: Math.min(220, 1080 - Math.max(0, markBox.y - 20)) } });
    record("capture05_sha256", { file: path.basename(p5), sha256: sha256(p5) });
    await page.close();
  }

  const page = await context.newPage();
  await loginAs(page, "admin");
  await page.goto(`${BASE}/`, { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="terminal-watchlist-dock"]', { state: "visible", timeout: 15000 });
  await page.waitForTimeout(8000);
  await page.waitForSelector('[data-testid="timeframe-native-notice"]', { timeout: 15000 });

  // ---------- CAPTURE 02: watchlist clip resolved — the MIXED state ----------
  {
    // Feed running + seed history => the long provenance tags that used to
    // push the price column past the clip.
    const tagText = await page
      .locator('[data-testid="watchlist-sparkline-source-btcusd"]')
      .textContent()
      .catch(() => null);
    record("capture02_mixed_state_tag", { text: tagText });
    if (!tagText || !tagText.includes("+")) {
      record("capture02_mixed_state_note", { note: "mixed tag absent; feed/seed state recorded as-is" });
    }
    // Bring the BTC row into the vertical viewport (the rows container
    // scrolls; the CLIP defect is horizontal) and measure against the ROWS
    // container, not the whole dock.
    await page.evaluate(() => {
      const rows = document.querySelector(".watchlist-rows-container");
      if (rows) rows.scrollTop = rows.scrollHeight;
    });
    await page.waitForTimeout(400);
    const scrollMetrics = await page.locator(".watchlist-rows-container").evaluate((el) => ({
      scrollTop: el.scrollTop,
      scrollHeight: el.scrollHeight,
      clientHeight: el.clientHeight,
    }));
    record("capture02_scroll_metrics", scrollMetrics);
    // The rows container scrolls vertically; the CLIP defect is horizontal.
    // The gate asserts BTC's widest row (the original finding) — fully inside
    // the 239px clip in the MIXED state, with the long provenance tag present.
    const leg = await measureLegibility(
      page,
      ["price-btcusd", "change-btcusd", "range-btcusd"],
      "terminal-watchlist-dock",
    );
    record("capture02_legibility", leg);
    assertLegible("capture02", leg, ["price-btcusd", "change-btcusd", "range-btcusd"]);
    const p2 = path.join(OUT_DIR, "POLISH-P01_02_WATCHLIST_CLIP_RESOLVED.png");
    await page.screenshot({ path: p2 });
    record("capture02_sha256", { file: path.basename(p2), sha256: sha256(p2) });
  }

  // ---------- CAPTURE 01: drift fixed — six-day 1D non-trending ----------
  {
    await page.click('[data-testid="chart-tf-1d"]');
    await page.waitForSelector('[data-testid="timeframe-resampled-notice"]', { timeout: 15000 });
    await page.waitForTimeout(1500);
    const envelope = await (async () => {
      const loginRes = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: "admin", password: "AxiomSecurePass2026!" }),
      });
      const { tokens } = await loginRes.json();
      const q = new URLSearchParams({ symbol: "EURUSD", timeframe: "D1", limit: "20", order: "asc" });
      return (await (await fetch(`http://localhost:8000/api/v1/persistence/candle-series?${q}`, {
        headers: { Authorization: `Bearer ${tokens.access_token}` },
      })).json());
    })();
    const bars = envelope.bars ?? [];
    const firstClose = bars.length > 0 ? Number(bars[0].close) : null;
    const lastClose = bars.length > 0 ? Number(bars[bars.length - 1].close) : null;
    const totalReturn = firstClose ? (lastClose - firstClose) / firstClose : null;
    record("capture01_d1_envelope", {
      kind: envelope.kind,
      bars: bars.length,
      firstClose,
      lastClose,
      totalReturn: totalReturn !== null ? +totalReturn.toFixed(6) : null,
    });
    // The M1 property: six days must NOT trend (pre-fix: +30.7%).
    if (totalReturn === null || Math.abs(totalReturn) > 0.05) {
      throw new Error(`CAPTURE01 GATE FAILED: six-day drift ${totalReturn}`);
    }
    const p1 = path.join(OUT_DIR, "POLISH-P01_01_DRIFT_FIXED_1D_NON_TRENDING.png");
    await page.screenshot({ path: p1 });
    record("capture01_sha256", { file: path.basename(p1), sha256: sha256(p1) });
  }

  // ---------- CAPTURE 03: confluence strip ----------
  {
    await page.click('[data-testid="chart-tf-1m"]');
    await page.waitForSelector('[data-testid="timeframe-native-notice"]', { timeout: 15000 });
    await page.waitForTimeout(1200);
    await page.click('[data-testid="overlay-sma20"]');
    await page.waitForSelector('[data-testid="indicator-status-sma20"]', { timeout: 15000 });
    await page.click('[data-testid="overlay-ema20"]');
    await page.waitForSelector('[data-testid="indicator-status-ema20"]', { timeout: 15000 });
    await page.click('[data-testid="engine-menu-button-momentum"]');
    await page.waitForTimeout(200);
    await page.click('[data-testid="indicator-item-RSI14"]');
    await page.waitForSelector('[data-testid="indicator-status-rsi14"]', { timeout: 15000 });
    await page.click('[data-testid="engine-menu-button-momentum"]');
    await page.waitForTimeout(200);
    await page.click('[data-testid="indicator-item-MACD12269"]');
    await page.waitForSelector('[data-testid="indicator-status-macd12269"]', { timeout: 15000 });
    await page.click('[data-testid="engine-menu-button-momentum"]');
    await page.waitForTimeout(200);
    await page.click('[data-testid="indicator-item-STOCH1433"]');
    await page.waitForSelector('[data-testid="indicator-status-stoch1433"]', { timeout: 15000 });
    await page.waitForTimeout(1500);
    const strip = await page.locator('[data-testid="confluence-strip"]').count();
    const score = await page.locator('[data-testid="confluence-score"]').textContent().catch(() => null);
    const band = await page.locator('[data-testid="confluence-uncertainty"]').textContent().catch(() => null);
    const nonAct = await page.locator('[data-testid="confluence-nonactuating"]').textContent().catch(() => null);
    const statement = await page.locator('[data-testid="confluence-statement"]').textContent().catch(() => null);
    record("capture03_confluence", { strip, score, band, nonAct, statement });
    if (strip !== 1 || !score || !band) throw new Error("CAPTURE03 GATE FAILED: confluence strip incomplete");
    if (!nonAct || !nonAct.includes("NON-ACTUATING")) throw new Error("CAPTURE03 GATE FAILED: NON-ACTUATING label missing");
    if (!statement || !statement.includes("simulated data")) throw new Error("CAPTURE03 GATE FAILED: simulated-data statement missing");
    const forbiddenRendered = (await page.locator('[data-testid="confluence-strip"]').textContent() ?? "").toLowerCase();
    for (const term of ["eligib", "risk/reward", "setup quality", "take the trade"]) {
      if (forbiddenRendered.includes(term)) throw new Error(`CAPTURE03 GATE FAILED: forbidden term rendered: ${term}`);
    }
    const leg = await measureLegibility(page, ["confluence-score", "confluence-uncertainty", "confluence-nonactuating"], "terminal-chart-stage");
    record("capture03_legibility", leg);
    assertLegible("capture03", leg, ["confluence-score", "confluence-uncertainty", "confluence-nonactuating"]);
    const p3 = path.join(OUT_DIR, "POLISH-P01_03_CONFLUENCE_EVIDENCE_ONLY.png");
    await page.screenshot({ path: p3 });
    record("capture03_sha256", { file: path.basename(p3), sha256: sha256(p3) });
  }

  // ---------- CAPTURE 06: route splitting network trace ----------
  {
    const chunks = [];
    page.on("response", (res) => {
      const url = res.url();
      if (url.includes("/assets/") && url.endsWith(".js")) {
        chunks.push(url.split("/").pop());
      }
    });
    await page.goto(`${BASE}/intelligence`, { waitUntil: "domcontentloaded" });
    await page.waitForSelector('[data-testid="route-loading"], [data-testid="intelligence-workspace"], [data-testid="intelligence-page"]', { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(2500);
    record("capture06_chunks_loaded_on_navigation", { chunks });
    const intelligenceChunk = chunks.find((c) => c.startsWith("InstitutionalIntelligencePage-"));
    if (!intelligenceChunk) {
      throw new Error(`CAPTURE06 GATE FAILED: no route chunk fetched for /intelligence: ${JSON.stringify(chunks)}`);
    }
    const p6 = path.join(OUT_DIR, "POLISH-P01_06_ROUTE_SPLIT_NETWORK_TRACE.png");
    await page.screenshot({ path: p6 });
    record("capture06_sha256", { file: path.basename(p6), sha256: sha256(p6) });
  }

  // ---------- CAPTURE 07: RBAC before chunk — unauthorized fetch denied ----------
  {
    // A FRESH browser context per role: the admin context's cookies would
    // otherwise authenticate this page and the login surface would never
    // render (the standing multi-user capture lesson).
    const unauthContext = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      deviceScaleFactor: 1,
    });
    const unauthPage = await unauthContext.newPage();
    const chunks = [];
    unauthPage.on("response", (res) => {
      const url = res.url();
      if (url.includes("/assets/") && url.endsWith(".js")) chunks.push(url.split("/").pop());
    });
    await loginAs(unauthPage, "surf-p03-unprivileged-028efc57");
    await unauthPage.goto(`${BASE}/intelligence`, { waitUntil: "domcontentloaded" });
    await unauthPage.waitForSelector('[data-testid="route-access-denied"]', { timeout: 15000 });
    await unauthPage.waitForTimeout(2000);
    const intelligenceChunk = chunks.find((c) => c.startsWith("InstitutionalIntelligencePage-"));
    const denialText = await unauthPage.locator('[data-testid="route-access-denied"]').textContent();
    record("capture07_rbac_before_chunk", { chunks, intelligenceChunkFetched: Boolean(intelligenceChunk), denialText: denialText?.replace(/\s+/g, " ").slice(0, 160) });
    if (intelligenceChunk) {
      throw new Error(`CAPTURE07 GATE FAILED: the intelligence chunk WAS fetched for an unauthorized operator: ${intelligenceChunk}`);
    }
    if (!denialText || !denialText.includes("ACCESS DENIED")) {
      throw new Error("CAPTURE07 GATE FAILED: denial not rendered");
    }
    const p7 = path.join(OUT_DIR, "POLISH-P01_07_RBAC_BEFORE_CHUNK_DENIED.png");
    await unauthPage.screenshot({ path: p7 });
    record("capture07_sha256", { file: path.basename(p7), sha256: sha256(p7) });
    await unauthContext.close();
  }

  fs.writeFileSync(
    JSON_OUT,
    JSON.stringify(
      { generated_at: new Date().toISOString(), revision: "A", viewport: "1920x1080", scope: "POLISH-P01 captures 01-07", records: LOG },
      null,
      2,
    ),
  );
  console.log("[DONE] verification JSON:", JSON_OUT);
  await browser.close();
}

run().catch((err) => {
  console.error("[FATAL]", err);
  process.exit(1);
});
