// DA capture tooling — CHART-P02 evidence captures 01-08 (untracked).
// Same discipline as CHART-P01: environment declared in the JSON, legibility
// instrument with hard gates, DOM-state corroboration, API envelopes.
import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const OUT_DIR = "/home/user/chart_p02_captures";
const JSON_OUT = "/home/user/CHART-P02_CAPTURE_VERIFICATION.json";
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
          text: el.textContent.trim().slice(0, 90),
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
    if (!e.inkFullyInside) failures.push(`${tid}: ink not inside clip`);
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

const ENGINE_OF = {
  HMA20: "trend", SUPERTREND103: "trend", ICHIMOKU952652: "trend",
  STOCH1433: "momentum", CCI20: "momentum", ROC12: "momentum", ADX14: "momentum",
  RSI14: "momentum", MACD12269: "momentum",
  KELTNER20: "volatility", DONCHIAN20: "volatility", ATR14: "volatility", BBANDS201: "volatility",
  PIVOTCL: "levels", CAMARILLA: "levels", PREVHL: "levels", SESSLVL: "levels",
  ZSCORE20: "statistics", PCTRANK20: "statistics", REGCHAN20: "statistics",
};

async function clickMenuItem(page, id) {
  const engine = ENGINE_OF[id];
  if (!engine) throw new Error(`no engine for ${id}`);
  const menuBtn = `engine-menu-button-${engine}`;
  const hit = await hitTestBeforeClick(page, menuBtn);
  record(`${id}_menu_hitTest`, { value: hit });
  await page.locator(`[data-testid="${menuBtn}"]`).click();
  await page.waitForTimeout(150);
  const itemHit = await hitTestBeforeClick(page, `indicator-item-${id}`);
  record(`${id}_item_hitTest`, { value: itemHit });
  await page.locator(`[data-testid="indicator-item-${id}"]`).click();
  await page.waitForTimeout(300);
}

async function clickDirectPill(page, id) {
  const tid = `overlay-${id.toLowerCase()}`;
  const hit = await hitTestBeforeClick(page, tid);
  record(`${id}_pill_hitTest`, { value: hit });
  await page.locator(`[data-testid="${tid}"]`).click();
  await page.waitForTimeout(300);
}

async function domState(page) {
  return page.evaluate(() => {
    const container = document.querySelector('[data-testid="chart-canvas-container"]');
    const panes = [...document.querySelectorAll('[data-testid^="indicator-pane-"]')].map((el) => {
      const r = el.getBoundingClientRect();
      return {
        testid: el.getAttribute("data-testid"),
        rect: { left: +r.left.toFixed(1), right: +r.right.toFixed(1), top: +r.top.toFixed(1), bottom: +r.bottom.toFixed(1) },
        syncedFrom: el.getAttribute("data-synced-range-from"),
        syncedTo: el.getAttribute("data-synced-range-to"),
      };
    });
    const price = (() => {
      const el = container;
      const r = el.getBoundingClientRect();
      return { left: +r.left.toFixed(1), right: +r.right.toFixed(1), top: +r.top.toFixed(1), bottom: +r.bottom.toFixed(1), height: +(r.bottom - r.top).toFixed(1) };
    })();
    return {
      activeOverlayLines: container?.getAttribute("data-active-overlay-lines"),
      activeIndicatorPanes: container?.getAttribute("data-active-indicator-panes"),
      activeIndicatorIds: container?.getAttribute("data-active-indicator-ids"),
      priceRangeFrom: container?.getAttribute("data-price-range-from"),
      priceRangeTo: container?.getAttribute("data-price-range-to"),
      pricePane: price,
      panes,
      refusal: document.querySelector('[data-testid="pane-budget-refusal"]')?.textContent?.trim() ?? null,
      budgetMeta: document.querySelector('[data-testid="pane-budget-meta"]')?.textContent?.trim() ?? null,
      trayPills: [...document.querySelectorAll('[data-testid^="active-tray-"]')].map((el) => el.getAttribute("data-testid")),
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

  // ---------- CAPTURE 01: toolbar at scale — all groups reachable ----------
  {
    const menuButtons = {};
    for (const engine of ["trend", "momentum", "volatility", "levels", "statistics"]) {
      const btn = await page.locator(`[data-testid="engine-menu-button-${engine}"]`).count();
      menuButtons[engine] = btn;
    }
    record("capture01_menu_buttons_present", menuButtons);
    if (Object.values(menuButtons).some((v) => v !== 1)) throw new Error("CAPTURE01 GATE FAILED: menu buttons missing");
    // Open the Levels menu for the screenshot; record item reachability.
    const levelsHit = await hitTestBeforeClick(page, "engine-menu-button-levels");
    record("capture01_levels_menu_hitTest", { value: levelsHit });
    await page.locator('[data-testid="engine-menu-button-levels"]').click();
    await page.waitForTimeout(300);
    const itemCounts = {};
    for (const engine of ["trend", "momentum", "volatility", "levels", "statistics"]) {
      // close whatever menu is open, then open the target one
      const openBtns = await page.locator(".engine-menu-button.open").count();
      if (openBtns > 0) {
        await page.locator(".engine-menu-button.open").click();
        await page.waitForTimeout(150);
      }
      await page.locator(`[data-testid="engine-menu-button-${engine}"]`).click();
      await page.waitForTimeout(200);
      itemCounts[engine] = await page.locator(`[data-testid^="indicator-item-"]`).count();
    }
    record("capture01_items_per_engine", itemCounts);
    const expected = { trend: 6, momentum: 6, volatility: 4, levels: 4, statistics: 3 };
    if (JSON.stringify(itemCounts) !== JSON.stringify(expected)) {
      throw new Error(`CAPTURE01 GATE FAILED: item counts ${JSON.stringify(itemCounts)}`);
    }
    // Re-open Levels for the screenshot and enable HMA20 for the tray.
    const openBtns2 = await page.locator(".engine-menu-button.open").count();
    if (openBtns2 > 0) {
      await page.locator(".engine-menu-button.open").click();
      await page.waitForTimeout(150);
    }
    await page.locator('[data-testid="engine-menu-button-levels"]').click();
    await page.waitForTimeout(300);
    const leg = await measureLegibility(page, ["engine-menu-button-trend", "engine-menu-button-momentum", "engine-menu-button-volatility", "engine-menu-button-levels", "engine-menu-button-statistics", "overlay-sma20"], "terminal-chart-stage");
    record("capture01_legibility", leg);
    assertLegible("capture01", leg, ["engine-menu-button-trend", "engine-menu-button-levels", "overlay-sma20"]);
    const p1 = path.join(OUT_DIR, "CHART-P02_01_TOOLBAR_23_INDICATORS_GROUPED.png");
    await page.screenshot({ path: p1 });
    record("capture01_sha256", { file: path.basename(p1), sha256: sha256(p1) });
    await page.locator('[data-testid="engine-menu-button-levels"]').click().catch(() => {});
  }

  // ---------- CAPTURE 02: trend overlays — Supertrend + Ichimoku ----------
  {
    const envelope = await apiIndicators("EURUSD", "M1", ["SUPERTREND103", "ICHIMOKU952652"]);
    record("capture02_api_envelope", {
      seriesKind: envelope.seriesKind,
      supertrend: envelope.indicators?.SUPERTREND103?.shape,
      supertrendLines: envelope.indicators?.SUPERTREND103?.lines ? Object.keys(envelope.indicators.SUPERTREND103.lines) : null,
      ichimokuLines: envelope.indicators?.ICHIMOKU952652?.lines ? Object.keys(envelope.indicators.ICHIMOKU952652.lines) : null,
    });
    await clickMenuItem(page, "SUPERTREND103");
    await page.waitForSelector('[data-testid="indicator-status-supertrend103"]', { timeout: 15000 });
    await clickMenuItem(page, "ICHIMOKU952652");
    await page.waitForSelector('[data-testid="indicator-status-ichimoku952652"]', { timeout: 15000 });
    await page.waitForTimeout(1200);
    const state = await domState(page);
    record("capture02_dom_state", state);
    // 2 supertrend + 5 ichimoku = 7 overlay lines
    if (state.activeOverlayLines !== "7" || !state.activeIndicatorIds.includes("ICHIMOKU952652")) {
      throw new Error(`CAPTURE02 GATE FAILED: ${JSON.stringify(state)}`);
    }
    const leg = await measureLegibility(page, ["indicator-status-supertrend103", "indicator-status-ichimoku952652", "active-tray-ICHIMOKU952652", "active-tray-SUPERTREND103"], "terminal-chart-stage");
    record("capture02_legibility", leg);
    assertLegible("capture02", leg, ["indicator-status-supertrend103", "indicator-status-ichimoku952652", "active-tray-ICHIMOKU952652"]);
    const p2 = path.join(OUT_DIR, "CHART-P02_02_TREND_SUPERTREND_ICHIMOKU.png");
    await page.screenshot({ path: p2 });
    record("capture02_sha256", { file: path.basename(p2), sha256: sha256(p2) });
  }

  // ---------- CAPTURE 03: momentum panes — price pane still usable ----------
  {
    // remove trend overlays via the tray
    await page.locator('[data-testid="active-tray-SUPERTREND103"]').click();
    await page.locator('[data-testid="active-tray-ICHIMOKU952652"]').click();
    await page.waitForTimeout(500);
    await clickMenuItem(page, "RSI14");
    await page.waitForSelector('[data-testid="indicator-status-rsi14"]', { timeout: 15000 });
    await clickMenuItem(page, "ADX14");
    await page.waitForSelector('[data-testid="indicator-status-adx14"]', { timeout: 15000 });
    await clickMenuItem(page, "STOCH1433");
    await page.waitForSelector('[data-testid="indicator-status-stoch1433"]', { timeout: 15000 });
    await page.waitForTimeout(1500);
    const state = await domState(page);
    record("capture03_dom_state", state);
    if (state.activeIndicatorPanes !== "3") throw new Error(`CAPTURE03 GATE FAILED: ${JSON.stringify(state)}`);
    // M6: price pane height must stay >= 280px.
    if (state.pricePane.height < 280) {
      throw new Error(`CAPTURE03 GATE FAILED: price pane ${state.pricePane.height}px < 280px`);
    }
    const stacked = state.panes.every((p) => p.rect.top >= state.pricePane.bottom - 1);
    record("capture03_price_pane", { height: state.pricePane.height, stacked });
    if (!stacked) throw new Error("CAPTURE03 GATE FAILED: pane overlaps price pane");
    const leg = await measureLegibility(page, ["indicator-status-rsi14", "indicator-status-adx14", "indicator-status-stoch1433", "pane-budget-meta"], "terminal-chart-stage");
    record("capture03_legibility", leg);
    assertLegible("capture03", leg, ["indicator-status-rsi14", "indicator-status-adx14", "indicator-status-stoch1433"]);
    const p3 = path.join(OUT_DIR, "CHART-P02_03_MOMENTUM_PANES_STACKED.png");
    await page.screenshot({ path: p3 });
    record("capture03_sha256", { file: path.basename(p3), sha256: sha256(p3) });
  }

  // ---------- CAPTURE 04: time-axis sync after zoom/pan (M7) ----------
  {
    const canvas = page.locator('[data-testid="chart-canvas-container"]');
    const box = await canvas.boundingBox();
    const cx = box.x + box.width / 2;
    const cy = box.y + box.height / 2;
    const before = await domState(page);
    record("capture04_range_before_zoom", { from: before.priceRangeFrom, to: before.priceRangeTo });
    // Zoom in with the wheel over the price canvas (lightweight-charts).
    await page.mouse.move(cx, cy);
    await page.waitForTimeout(200);
    await page.mouse.wheel(0, -600);
    await page.waitForTimeout(1200);
    const after = await domState(page);
    record("capture04_range_after_zoom", { from: after.priceRangeFrom, to: after.priceRangeTo, panes: after.panes.map((p) => ({ id: p.testid, from: p.syncedFrom, to: p.syncedTo })) });
    if (!after.priceRangeFrom || after.priceRangeFrom === before.priceRangeFrom) {
      throw new Error(`CAPTURE04 GATE FAILED: zoom did not change the visible range (${before.priceRangeFrom} -> ${after.priceRangeFrom})`);
    }
    const synced = after.panes.every(
      (p) => p.syncedFrom === after.priceRangeFrom && p.syncedTo === after.priceRangeTo,
    );
    record("capture04_panes_synced_to_price", { synced });
    if (!synced) throw new Error(`CAPTURE04 GATE FAILED: panes not synced: ${JSON.stringify(after.panes)}`);
    const p4 = path.join(OUT_DIR, "CHART-P02_04_TIME_AXIS_SYNC_AFTER_ZOOM.png");
    await page.screenshot({ path: p4 });
    record("capture04_sha256", { file: path.basename(p4), sha256: sha256(p4) });
  }

  // ---------- CAPTURE 05: levels — Pivots + Camarilla + Session levels ----------
  {
    for (const id of ["RSI14", "ADX14", "STOCH1433"]) {
      await page.locator(`[data-testid="active-tray-${id}"]`).click();
    }
    await page.waitForTimeout(500);
    const envelope = await apiIndicators("EURUSD", "M1", ["PIVOTCL", "CAMARILLA", "SESSLVL"]);
    record("capture05_api_envelope", {
      pivots: envelope.indicators?.PIVOTCL?.lines ? Object.keys(envelope.indicators.PIVOTCL.lines) : null,
      camarilla: envelope.indicators?.CAMARILLA?.lines ? Object.keys(envelope.indicators.CAMARILLA.lines) : null,
      sesslvl: envelope.indicators?.SESSLVL?.lines ? Object.keys(envelope.indicators.SESSLVL.lines) : null,
    });
    await clickMenuItem(page, "PIVOTCL");
    await page.waitForSelector('[data-testid="indicator-status-pivotcl"]', { timeout: 15000 });
    await clickMenuItem(page, "CAMARILLA");
    await page.waitForSelector('[data-testid="indicator-status-camarilla"]', { timeout: 15000 });
    await clickMenuItem(page, "SESSLVL");
    await page.waitForSelector('[data-testid="indicator-status-sesslvl"]', { timeout: 15000 });
    await page.waitForTimeout(1500);
    const state = await domState(page);
    record("capture05_dom_state", state);
    // 7 + 8 + 4 = 19 level lines
    if (state.activeOverlayLines !== "19") throw new Error(`CAPTURE05 GATE FAILED: ${JSON.stringify(state)}`);
    const leg = await measureLegibility(page, ["indicator-status-pivotcl", "indicator-status-camarilla", "indicator-status-sesslvl"], "terminal-chart-stage");
    record("capture05_legibility", leg);
    assertLegible("capture05", leg, ["indicator-status-pivotcl", "indicator-status-camarilla", "indicator-status-sesslvl"]);
    const p5 = path.join(OUT_DIR, "CHART-P02_05_LEVELS_PIVOTS_CAMARILLA_SESSION.png");
    await page.screenshot({ path: p5 });
    record("capture05_sha256", { file: path.basename(p5), sha256: sha256(p5) });
  }

  // ---------- CAPTURE 06: statistics — regression channel + Z-Score ----------
  {
    for (const id of ["PIVOTCL", "CAMARILLA", "SESSLVL"]) {
      await page.locator(`[data-testid="active-tray-${id}"]`).click();
    }
    await page.waitForTimeout(500);
    await clickMenuItem(page, "REGCHAN20");
    await page.waitForSelector('[data-testid="indicator-status-regchan20"]', { timeout: 15000 });
    await clickMenuItem(page, "ZSCORE20");
    await page.waitForSelector('[data-testid="indicator-status-zscore20"]', { timeout: 15000 });
    await page.waitForTimeout(1200);
    const state = await domState(page);
    record("capture06_dom_state", state);
    // regression 3 lines + z-score 1 = 4
    if (state.activeOverlayLines !== "4") throw new Error(`CAPTURE06 GATE FAILED: ${JSON.stringify(state)}`);
    const leg = await measureLegibility(page, ["indicator-status-regchan20", "indicator-status-zscore20", "active-tray-REGCHAN20"], "terminal-chart-stage");
    record("capture06_legibility", leg);
    assertLegible("capture06", leg, ["indicator-status-regchan20", "indicator-status-zscore20"]);
    const p6 = path.join(OUT_DIR, "CHART-P02_06_STATISTICS_REGCHAN_ZSCORE.png");
    await page.screenshot({ path: p6 });
    record("capture06_sha256", { file: path.basename(p6), sha256: sha256(p6) });
  }

  // ---------- CAPTURE 07: pane budget refusal (M6) ----------
  {
    for (const id of ["REGCHAN20", "ZSCORE20"]) {
      await page.locator(`[data-testid="active-tray-${id}"]`).click();
    }
    await page.waitForTimeout(500);
    await clickMenuItem(page, "RSI14");
    await page.waitForSelector('[data-testid="indicator-status-rsi14"]', { timeout: 15000 });
    await clickMenuItem(page, "MACD12269");
    await page.waitForSelector('[data-testid="indicator-status-macd12269"]', { timeout: 15000 });
    await clickMenuItem(page, "ATR14");
    await page.waitForSelector('[data-testid="indicator-status-atr14"]', { timeout: 15000 });
    await page.waitForTimeout(800);
    const before = await domState(page);
    record("capture07_before_fourth", { panes: before.activeIndicatorPanes, budget: before.budgetMeta });
    if (before.activeIndicatorPanes !== "3") throw new Error(`CAPTURE07 GATE FAILED: expected 3 panes, got ${before.activeIndicatorPanes}`);
    await clickMenuItem(page, "STOCH1433");
    await page.waitForSelector('[data-testid="pane-budget-refusal"]', { timeout: 15000 });
    await page.waitForTimeout(600);
    const after = await domState(page);
    record("capture07_after_refusal", { panes: after.activeIndicatorPanes, refusal: after.refusal, budget: after.budgetMeta });
    if (after.activeIndicatorPanes !== "3") throw new Error("CAPTURE07 GATE FAILED: a 4th pane was added");
    if (!after.refusal || !after.refusal.includes("STOCH1433")) {
      throw new Error(`CAPTURE07 GATE FAILED: refusal missing: ${after.refusal}`);
    }
    const leg = await measureLegibility(page, ["pane-budget-refusal", "pane-budget-meta"], "terminal-chart-stage");
    record("capture07_legibility", leg);
    assertLegible("capture07", leg, ["pane-budget-refusal"]);
    const p7 = path.join(OUT_DIR, "CHART-P02_07_PANE_BUDGET_REFUSAL.png");
    await page.screenshot({ path: p7 });
    record("capture07_sha256", { file: path.basename(p7), sha256: sha256(p7) });
  }

  // ---------- CAPTURE 08: insufficient — Ichimoku on 1D (5 bars vs 78) ----------
  {
    for (const id of ["RSI14", "MACD12269", "ATR14"]) {
      await page.locator(`[data-testid="active-tray-${id}"]`).click();
    }
    await page.waitForTimeout(500);
    const tfHit = await hitTestBeforeClick(page, "chart-tf-1d");
    record("capture08_tf1d_hitTest", { value: tfHit });
    await page.locator('[data-testid="chart-tf-1d"]').click();
    await page.waitForSelector('[data-testid="timeframe-resampled-notice"]', { timeout: 15000 });
    await page.waitForTimeout(800);
    const envelope = await apiIndicators("EURUSD", "D1", ["ICHIMOKU952652"]);
    record("capture08_api_envelope", { seriesKind: envelope.seriesKind, ichimoku: envelope.indicators?.ICHIMOKU952652 ?? null });
    await clickMenuItem(page, "ICHIMOKU952652");
    await page.waitForSelector('[data-testid="indicator-status-ichimoku952652"]', { timeout: 15000 });
    await page.waitForTimeout(800);
    const state = await domState(page);
    record("capture08_dom_state", state);
    const status = await page.locator('[data-testid="indicator-status-ichimoku952652"]').textContent();
    record("capture08_insufficient_status", { text: status });
    if (state.activeOverlayLines !== "0") {
      throw new Error(`CAPTURE08 GATE FAILED: a line was rendered for an insufficient indicator: ${JSON.stringify(state)}`);
    }
    if (!status.includes("insufficient history") || !status.includes("78") || !status.includes("5")) {
      throw new Error(`CAPTURE08 GATE FAILED: status missing counts: ${status}`);
    }
    const leg = await measureLegibility(page, ["indicator-status-ichimoku952652"], "terminal-chart-stage");
    record("capture08_legibility", leg);
    assertLegible("capture08", leg, ["indicator-status-ichimoku952652"]);
    const p8 = path.join(OUT_DIR, "CHART-P02_08_INSUFFICIENT_ICHIMOKU_ON_D1.png");
    await page.screenshot({ path: p8 });
    record("capture08_sha256", { file: path.basename(p8), sha256: sha256(p8) });
  }

  fs.writeFileSync(
    JSON_OUT,
    JSON.stringify(
      { generated_at: new Date().toISOString(), revision: "A", viewport: "1920x1080", scope: "CHART-P02 captures 01-08", records: LOG },
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
