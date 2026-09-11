// DA capture tooling — CHART-P01 evidence captures 01-06 (untracked).
// Same discipline as DATA-P02: environment declared in the JSON, legibility
// instrument (layout box, ink rect, painted-stroke extent, hit-test at the
// rightmost pixel) with HARD GATES; canvas line presence is corroborated by
// machine-recorded DOM state (data-active-overlay-lines / pane testids) and
// the API envelopes — the IMAGE is primary for the lines themselves.
import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const OUT_DIR = "/home/user/chart_p01_captures";
const JSON_OUT = "/home/user/CHART-P01_CAPTURE_VERIFICATION.json";
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

async function apiIndicators(symbol, timeframe, indicators) {
  const loginRes = await fetch("http://localhost:8000/api/v1/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: "admin", password: "AxiomSecurePass2026!" }),
  });
  const { tokens } = await loginRes.json();
  const q = new URLSearchParams({ symbol, timeframe, indicators: indicators.join(",") });
  const res = await fetch(`http://localhost:8000/api/v1/persistence/indicator-series?${q}`, {
    headers: { Authorization: `Bearer ${tokens.access_token}` },
  });
  return res.json();
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
        let stroke = null;
        try {
          const cs = getComputedStyle(el);
          const canvas = document.createElement("canvas");
          canvas.width = Math.ceil(r.width) + 8;
          canvas.height = Math.ceil(r.height) + 8;
          const ctx = canvas.getContext("2d");
          ctx.font = `${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
          ctx.textBaseline = "alphabetic";
          ctx.fillStyle = "#ffffff";
          ctx.fillText(el.textContent.trim(), 4, canvas.height - 4);
          const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
          let rightmost = -1;
          for (let y = 0; y < canvas.height; y++) {
            const row = y * canvas.width * 4;
            for (let x = canvas.width - 1; x >= 0; x--) {
              if (imgData.data[row + x * 4 + 3] > 0) { if (x > rightmost) rightmost = x; break; }
            }
          }
          stroke = { strokeRightInViewport: +(r.left + (rightmost - 4)).toFixed(1) };
        } catch { stroke = null; }
        const hitX = Math.min(r.right - 1, r.left + r.width * 0.95);
        const hitY = r.top + r.height / 2;
        let hitRec = null;
        if (verticallyInView) {
          const hit = document.elementFromPoint(hitX, hitY);
          hitRec = { x: +hitX.toFixed(1), y: +hitY.toFixed(1), hitIsSelf: hit === el || (hit !== null && el.contains(hit)), hitTag: hit ? hit.tagName : null };
        }
        out.elements[tid] = {
          rect: { left: +r.left.toFixed(1), right: +r.right.toFixed(1), top: +r.top.toFixed(1), bottom: +r.bottom.toFixed(1), width: +r.width.toFixed(1) },
          inkRect: ink ? { left: +ink.left.toFixed(1), right: +ink.right.toFixed(1) } : null,
          strokeExtent: stroke,
          text: el.textContent.trim(),
          verticallyInView,
          inkFullyInside: inkInside,
          hitTestAtRightmostPixel: hitRec,
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

async function hitTestBeforeClick(page, testid) {
  return page.locator(`[data-testid="${testid}"]`).evaluate((el) => {
    const r = el.getBoundingClientRect();
    const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return top === el || el.contains(top);
  });
}

async function clickPill(page, testid) {
  const hit = await hitTestBeforeClick(page, testid);
  record(`${testid}_hitTestBeforeClick`, { value: hit });
  if (!hit) throw new Error(`hit-test failed for ${testid}`);
  await page.locator(`[data-testid="${testid}"]`).click();
}

async function domState(page) {
  return page.evaluate(() => {
    const container = document.querySelector('[data-testid="chart-canvas-container"]');
    const statuses = [...document.querySelectorAll('[data-testid^="indicator-status-"]')].map(
      (el) => ({ testid: el.getAttribute("data-testid"), text: el.textContent.trim() }),
    );
    const panes = [...document.querySelectorAll('[data-testid^="indicator-pane-"]')].map((el) => {
      const r = el.getBoundingClientRect();
      return { testid: el.getAttribute("data-testid"), rect: { left: +r.left.toFixed(1), right: +r.right.toFixed(1), top: +r.top.toFixed(1), bottom: +r.bottom.toFixed(1) } };
    });
    const pricePane = (() => {
      const el = document.querySelector('[data-testid="chart-canvas-container"]');
      const r = el.getBoundingClientRect();
      return { left: +r.left.toFixed(1), right: +r.right.toFixed(1), top: +r.top.toFixed(1), bottom: +r.bottom.toFixed(1) };
    })();
    return {
      activeOverlayLines: container?.getAttribute("data-active-overlay-lines"),
      activeIndicatorPanes: container?.getAttribute("data-active-indicator-panes"),
      activeIndicatorIds: container?.getAttribute("data-active-indicator-ids"),
      pricePaneRect: pricePane,
      panes,
      statuses,
    };
  });
}

async function run() {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  record("environment_browser", { chromium: browser.version(), viewport: "1920x1080", deviceScaleFactor: 1 });

  {
    const loginRes = await fetch("http://localhost:8000/api/v1/auth/login", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: "admin", password: "AxiomSecurePass2026!" }),
    });
    const { tokens } = await loginRes.json();
    const stats = await (await fetch("http://localhost:8000/api/v1/market/live/stats", {
      headers: { Authorization: `Bearer ${tokens.access_token}` },
    })).json();
    record("environment_feed_state_at_capture", {
      running: stats.running,
      snapshotSymbols: Object.keys(stats.latest_by_symbol || {}).length,
    });
  }

  const page = await context.newPage();
  await login(page);
  await page.goto("http://localhost:5173/", { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="terminal-watchlist-dock"]', { state: "visible", timeout: 15000 });
  await page.waitForTimeout(7000);
  await page.waitForSelector('[data-testid="timeframe-native-notice"]', { timeout: 15000 });

  // ---------- CAPTURE 01: SMA20 + SMA50 on 1m — F-CHART-1 proof ----------
  {
    const envelope = await apiIndicators("EURUSD", "M1", ["SMA20", "SMA50"]);
    record("capture01_api_envelope", {
      seriesKind: envelope.seriesKind,
      sma20: { shape: envelope.indicators?.SMA20?.shape, points: envelope.indicators?.SMA20?.points?.length ?? null },
      sma50: { shape: envelope.indicators?.SMA50?.shape, points: envelope.indicators?.SMA50?.points?.length ?? null },
    });
    await clickPill(page, "overlay-sma20");
    await page.waitForSelector('[data-testid="indicator-status-sma20"]', { timeout: 15000 });
    await clickPill(page, "overlay-sma50");
    await page.waitForSelector('[data-testid="indicator-status-sma50"]', { timeout: 15000 });
    await page.waitForTimeout(1200);
    const state = await domState(page);
    record("capture01_dom_state", state);
    if (state.activeOverlayLines !== "2" || state.activeIndicatorIds !== "SMA20,SMA50") {
      throw new Error(`CAPTURE01 GATE FAILED: ${JSON.stringify(state)}`);
    }
    const leg = await measureLegibility(page, ["overlay-sma20", "overlay-sma50", "indicator-status-sma20", "indicator-status-sma50"], "terminal-chart-stage");
    record("capture01_legibility", leg);
    assertLegible("capture01", leg, ["overlay-sma20", "overlay-sma50", "indicator-status-sma20", "indicator-status-sma50"]);
    const p1 = path.join(OUT_DIR, "CHART-P01_01_SMA20_SMA50_REAL_LINES.png");
    await page.screenshot({ path: p1 });
    record("capture01_sha256", { file: path.basename(p1), sha256: sha256(p1) });
  }

  // ---------- CAPTURE 02: EMA20 vs SMA20 together ----------
  {
    await clickPill(page, "overlay-sma50"); // off
    await page.waitForTimeout(400);
    await clickPill(page, "overlay-ema20");
    await page.waitForSelector('[data-testid="indicator-status-ema20"]', { timeout: 15000 });
    await page.waitForTimeout(1200);
    const state = await domState(page);
    record("capture02_dom_state", state);
    if (state.activeOverlayLines !== "2" || state.activeIndicatorIds !== "SMA20,EMA20") {
      throw new Error(`CAPTURE02 GATE FAILED: ${JSON.stringify(state)}`);
    }
    const leg = await measureLegibility(page, ["overlay-sma20", "overlay-ema20", "indicator-status-ema20"], "terminal-chart-stage");
    record("capture02_legibility", leg);
    assertLegible("capture02", leg, ["overlay-sma20", "overlay-ema20", "indicator-status-ema20"]);
    const p2 = path.join(OUT_DIR, "CHART-P02_02_EMA20_VS_SMA20_DIVERGENCE.png");
    await page.screenshot({ path: p2 });
    record("capture02_sha256", { file: path.basename(p2), sha256: sha256(p2) });
  }

  // ---------- CAPTURE 03: RSI + MACD in separate panes ----------
  {
    await clickPill(page, "overlay-sma20"); // off
    await clickPill(page, "overlay-ema20"); // off
    await page.waitForTimeout(400);
    await clickPill(page, "indicator-rsi14");
    await page.waitForSelector('[data-testid="indicator-status-rsi14"]', { timeout: 15000 });
    await clickPill(page, "indicator-macd12269");
    await page.waitForSelector('[data-testid="indicator-status-macd12269"]', { timeout: 15000 });
    await page.waitForTimeout(1500);
    const state = await domState(page);
    record("capture03_dom_state", state);
    if (state.activeIndicatorPanes !== "2" || state.activeOverlayLines !== "0") {
      throw new Error(`CAPTURE03 GATE FAILED: ${JSON.stringify(state)}`);
    }
    // S2: the panes sit BELOW the price pane (stacked), never inside it.
    const price = state.pricePaneRect;
    const stacked = state.panes.every((p) => p.rect.top >= price.bottom - 1);
    record("capture03_price_pane_undistorted", { stacked, pricePaneRect: price, panes: state.panes });
    if (!stacked) throw new Error("CAPTURE03 GATE FAILED: pane overlaps price pane");
    const leg = await measureLegibility(page, ["indicator-rsi14", "indicator-macd12269", "indicator-status-rsi14", "indicator-status-macd12269"], "terminal-chart-stage");
    record("capture03_legibility", leg);
    assertLegible("capture03", leg, ["indicator-status-rsi14", "indicator-status-macd12269"]);
    const p3 = path.join(OUT_DIR, "CHART-P01_03_RSI_MACD_SEPARATE_PANES.png");
    await page.screenshot({ path: p3 });
    record("capture03_sha256", { file: path.basename(p3), sha256: sha256(p3) });
  }

  // ---------- CAPTURE 04: Bollinger Bands ----------
  {
    await clickPill(page, "indicator-rsi14"); // off
    await clickPill(page, "indicator-macd12269"); // off
    await page.waitForTimeout(400);
    await clickPill(page, "indicator-bbands201");
    await page.waitForSelector('[data-testid="indicator-status-bbands201"]', { timeout: 15000 });
    await page.waitForTimeout(1200);
    const state = await domState(page);
    record("capture04_dom_state", state);
    // Bollinger renders THREE overlay lines (upper/middle/lower).
    if (state.activeOverlayLines !== "3" || state.activeIndicatorIds !== "BBANDS201") {
      throw new Error(`CAPTURE04 GATE FAILED: ${JSON.stringify(state)}`);
    }
    const leg = await measureLegibility(page, ["indicator-bbands201", "indicator-status-bbands201"], "terminal-chart-stage");
    record("capture04_legibility", leg);
    assertLegible("capture04", leg, ["indicator-status-bbands201"]);
    const p4 = path.join(OUT_DIR, "CHART-P01_04_BOLLINGER_BANDS.png");
    await page.screenshot({ path: p4 });
    record("capture04_sha256", { file: path.basename(p4), sha256: sha256(p4) });
  }

  // ---------- CAPTURE 05: insufficient — SMA50 on 1d (5 bars) ----------
  {
    await clickPill(page, "indicator-bbands201"); // off
    await page.waitForTimeout(400);
    const tfHit = await hitTestBeforeClick(page, "chart-tf-1d");
    record("capture05_tf1d_hitTestBeforeClick", { value: tfHit });
    await page.locator('[data-testid="chart-tf-1d"]').click();
    await page.waitForSelector('[data-testid="timeframe-resampled-notice"]', { timeout: 15000 });
    await page.waitForTimeout(1000);
    const envelope = await apiIndicators("EURUSD", "D1", ["SMA50"]);
    record("capture05_api_envelope", {
      seriesKind: envelope.seriesKind,
      bars: envelope.indicators?.SMA50?.shape === "insufficient" ? null : "computed",
      sma50: envelope.indicators?.SMA50 ?? null,
    });
    await clickPill(page, "overlay-sma50");
    await page.waitForSelector('[data-testid="indicator-status-sma50"]', { timeout: 15000 });
    await page.waitForTimeout(1000);
    const state = await domState(page);
    record("capture05_dom_state", state);
    const statusText = (state.statuses.find((s) => s.testid === "indicator-status-sma50") || {}).text || "";
    record("capture05_insufficient_status", { text: statusText });
    if (state.activeOverlayLines !== "0") {
      throw new Error(`CAPTURE05 GATE FAILED: a line was rendered for an insufficient indicator: ${JSON.stringify(state)}`);
    }
    if (!statusText.includes("insufficient history") || !statusText.includes("50") || !statusText.includes("no series rendered")) {
      throw new Error(`CAPTURE05 GATE FAILED: insufficient status missing: ${statusText}`);
    }
    const leg = await measureLegibility(page, ["overlay-sma50", "indicator-status-sma50"], "terminal-chart-stage");
    record("capture05_legibility", leg);
    assertLegible("capture05", leg, ["indicator-status-sma50"]);
    const p5 = path.join(OUT_DIR, "CHART-P01_05_INSUFFICIENT_HISTORY_NO_LINE.png");
    await page.screenshot({ path: p5 });
    record("capture05_sha256", { file: path.basename(p5), sha256: sha256(p5) });
  }

  // ---------- CAPTURE 06: all indicators off — clean chart ----------
  {
    await clickPill(page, "overlay-sma50"); // off
    await page.waitForTimeout(600);
    const state = await domState(page);
    record("capture06_dom_state", state);
    const statusStripCount = await page.locator('[data-testid="chart-indicator-status"]').count();
    record("capture06_clean", { statusStripCount });
    if (state.activeOverlayLines !== "0" || state.activeIndicatorPanes !== "0" || statusStripCount !== 0) {
      throw new Error(`CAPTURE06 GATE FAILED: residue present: ${JSON.stringify(state)}`);
    }
    const leg = await measureLegibility(page, ["chart-tf-1d", "chart-provenance-badge"], "terminal-chart-stage");
    record("capture06_legibility", leg);
    const p6 = path.join(OUT_DIR, "CHART-P01_06_ALL_INDICATORS_OFF_CLEAN.png");
    await page.screenshot({ path: p6 });
    record("capture06_sha256", { file: path.basename(p6), sha256: sha256(p6) });
  }

  fs.writeFileSync(
    JSON_OUT,
    JSON.stringify(
      { generated_at: new Date().toISOString(), revision: "A", viewport: "1920x1080", scope: "CHART-P01 captures 01-06", records: LOG },
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
