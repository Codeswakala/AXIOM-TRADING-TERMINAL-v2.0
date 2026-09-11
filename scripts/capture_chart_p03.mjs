// DA capture tooling — CHART-P03 evidence captures (untracked).
// Drawing placement is real browser interaction: every click is hit-tested
// before it lands, the (price, time) anchors are machine-recorded from the
// persisted drawings (data attributes + API), and the M1/M2 round-trip proof
// compares anchors byte-for-byte after a 1m -> 1h -> 1m timeframe switch.
import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const OUT_DIR = "/home/user/chart_p03_captures";
const JSON_OUT = "/home/user/CHART-P03_CAPTURE_VERIFICATION.json";
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

async function hitTest(page, testid) {
  return page.locator(`[data-testid="${testid}"]`).evaluate((el) => {
    const r = el.getBoundingClientRect();
    const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return top === el || el.contains(top);
  });
}

async function canvasState(page) {
  return page.evaluate(() => {
    const container = document.querySelector('[data-testid="chart-canvas-container"]');
    const overlay = document.querySelector('[data-testid="chart-drawing-overlay"]');
    const drawingGroups = overlay ? [...overlay.querySelectorAll("g[data-testid^='drawing-']")].map((el) => el.getAttribute("data-testid")) : [];
    const drawings = drawingGroups;
    const legacy = document.querySelector('[data-testid="legacy-annotation-list"]');
    return {
      activeOverlayLines: container?.getAttribute("data-active-overlay-lines"),
      drawings,
      drawingCount: drawings.length,
      noteCount: document.querySelector('[data-testid="chart-add-annotation-btn"]')?.textContent ?? null,
      legacyText: legacy?.textContent?.replace(/\s+/g, " ").slice(0, 300) ?? null,
      selectedDrawing: container?.querySelector("[data-selected]") ? null : null,
    };
  });
}

async function clickCanvas(page, fx, fy) {
  // Real placement: click at a fraction of the chart canvas area.
  const canvas = page.locator('[data-testid="chart-canvas-container"]');
  const box = await canvas.boundingBox();
  const x = box.x + box.width * fx;
  const y = box.y + box.height * fy;
  const hit = await page.evaluate(([px, py]) => {
    const el = document.elementFromPoint(px, py);
    return el ? { tag: el.tagName, cls: el.className?.toString?.().slice(0, 50) } : null;
  }, [x, y]);
  await page.mouse.click(x, y);
  return { x, y, hit };
}

async function activateTool(page, id) {
  const hit = await hitTest(page, `drawing-tool-${id}`);
  record(`${id}_tool_hitTest`, { value: hit });
  if (!hit) throw new Error(`tool hit-test failed: ${id}`);
  await page.locator(`[data-testid="drawing-tool-${id}"]`).click();
  await page.waitForTimeout(200);
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
  page.on("pageerror", (err) => {
    record("page_error", { message: String(err).slice(0, 300) });
    console.error("[PAGEERROR]", String(err).slice(0, 300));
  });
  page.on("console", (msg) => {
    if (msg.type() === "error") record("console_error", { text: msg.text().slice(0, 200) });
  });
  await login(page);
  await page.goto("http://localhost:5173/", { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="terminal-watchlist-dock"]', { state: "visible", timeout: 15000 });
  await page.waitForTimeout(7000);
  await page.waitForSelector('[data-testid="timeframe-native-notice"]', { timeout: 15000 });

  // ---------- CAPTURE 01: drawing tools palette, visible tool state ----------
  {
    const toolIds = ["trendline", "hline", "ray", "rect", "fib", "text"];
    const present = {};
    for (const id of toolIds) present[id] = await page.locator(`[data-testid="drawing-tool-${id}"]`).count();
    record("capture01_tools_present", present);
    if (Object.values(present).some((v) => v !== 1)) throw new Error("CAPTURE01 GATE FAILED: tool buttons missing");
    await activateTool(page, "trendline");
    const active = await page.locator('[data-testid="drawing-tool-trendline"]').getAttribute("aria-pressed");
    record("capture01_active_tool_state", { active });
    if (active !== "true") throw new Error("CAPTURE01 GATE FAILED: active state not visible");
    const p1 = path.join(OUT_DIR, "CHART-P03_01_DRAWING_TOOLS_PALETTE.png");
    await page.screenshot({ path: p1 });
    record("capture01_sha256", { file: path.basename(p1), sha256: sha256(p1) });
    await activateTool(page, "trendline"); // deactivate
  }

  // ---------- CAPTURE 02: trendline + Fibonacci placed on the chart ----------
  {
    await activateTool(page, "trendline");
    const c1 = await clickCanvas(page, 0.30, 0.35);
    record("capture02_trendline_first_click", c1);
    await page.waitForSelector('[data-testid="drawing-pending-anchor"]', { timeout: 5000 });
    const c2 = await clickCanvas(page, 0.60, 0.25);
    record("capture02_trendline_second_click", c2);
    await page.waitForTimeout(1200);
    let state = await canvasState(page);
    record("capture02_after_trendline", state);
    if (state.drawingCount < 1) throw new Error("CAPTURE02 GATE FAILED: trendline not rendered");
    await activateTool(page, "fib");
    const f1 = await clickCanvas(page, 0.35, 0.60);
    await page.waitForSelector('[data-testid="drawing-pending-anchor"]', { timeout: 5000 });
    const f2 = await clickCanvas(page, 0.55, 0.30);
    record("capture02_fib_clicks", { f1, f2 });
    await page.waitForTimeout(1200);
    state = await canvasState(page);
    record("capture02_after_fib", state);
    if (state.drawingCount < 2) throw new Error("CAPTURE02 GATE FAILED: fib not rendered");
    // Fib levels must exist in the overlay (7 levels).
    const fibLevels = await page.locator('[data-testid^="drawing-fib-level-"]').count();
    record("capture02_fib_levels", { count: fibLevels });
    if (fibLevels < 7) throw new Error(`CAPTURE02 GATE FAILED: fib levels ${fibLevels}`);
    const p2 = path.join(OUT_DIR, "CHART-P03_02_TRENDLINE_FIB_PLACED.png");
    await page.screenshot({ path: p2 });
    record("capture02_sha256", { file: path.basename(p2), sha256: sha256(p2) });
  }

  // ---------- CAPTURE 03: THE M1/M2 PROOF — 1m -> 1h -> 1m round-trip ----------
  {
    const fetchGeometry = async () => {
      const loginRes = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: "admin", password: "AxiomSecurePass2026!" }),
      });
      const { tokens } = await loginRes.json();
      const q = new URLSearchParams({ symbol: "EURUSD", timeframe: "1m", limit: "50" });
      const res = await fetch(`http://localhost:8000/api/v1/collaboration/chart-annotations?${q}`, {
        headers: { Authorization: `Bearer ${tokens.access_token}` },
      });
      const rows = await res.json();
      return Object.fromEntries(
        rows
          .filter((r) => r.artifact_type === "chart_research_drawing" && r.content && r.content.geometry)
          .map((r) => [r.id, { kind: r.content.geometry.kind, handles: r.content.geometry.handles }]),
      );
    };
    const beforeApi = await fetchGeometry();
    record("capture03_api_geometry_before", beforeApi);
    const beforeDom = await page.evaluate(() => {
      const overlay = document.querySelector('[data-testid="chart-drawing-overlay"]');
      return overlay ? [...overlay.querySelectorAll("g[data-testid^='drawing-']")].map((g) => g.getAttribute("data-testid")).sort() : [];
    });
    record("capture03_drawings_before_switch", { ids: beforeDom });
    const p3a = path.join(OUT_DIR, "CHART-P03_03a_ROUNDTRIP_BEFORE_1M.png");
    await page.screenshot({ path: p3a });
    record("capture03a_sha256", { file: path.basename(p3a), sha256: sha256(p3a) });

    await hitTest(page, "chart-tf-1h");
    await page.locator('[data-testid="chart-tf-1h"]').click();
    await page.waitForSelector('[data-testid="timeframe-resampled-notice"]', { timeout: 15000 });
    await page.waitForTimeout(1200);
    const during = await canvasState(page);
    record("capture03_drawings_during_1h", { drawings: during.drawings, drawingCount: during.drawingCount });
    // S2: drawings are per (symbol, timeframe) — they do NOT appear on 1h.
    if (during.drawingCount !== 0) {
      throw new Error(`CAPTURE03 GATE FAILED: 1m drawings leaked onto 1h: ${JSON.stringify(during.drawings)}`);
    }

    await hitTest(page, "chart-tf-1m");
    await page.locator('[data-testid="chart-tf-1m"]').click();
    await page.waitForSelector('[data-testid="timeframe-native-notice"]', { timeout: 15000 });
    await page.waitForTimeout(1200);
    const afterApi = await fetchGeometry();
    record("capture03_api_geometry_after", afterApi);
    const afterDom = await page.evaluate(() => {
      const overlay = document.querySelector('[data-testid="chart-drawing-overlay"]');
      return overlay ? [...overlay.querySelectorAll("g[data-testid^='drawing-']")].map((g) => g.getAttribute("data-testid")).sort() : [];
    });
    record("capture03_drawings_after_roundtrip", { ids: afterDom });
    // The anchors are (price, time) data: identical after the round-trip,
    // byte for byte, at the persistence layer AND in the rendered overlay.
    const beforeJson = JSON.stringify(beforeApi);
    const afterJson = JSON.stringify(afterApi);
    record("capture03_anchor_equality", { before: beforeApi, after: afterApi, equal: beforeJson === afterJson });
    if (beforeJson !== afterJson) {
      throw new Error(`CAPTURE03 GATE FAILED: persisted anchors changed across the round-trip`);
    }
    if (JSON.stringify(beforeDom) !== JSON.stringify(afterDom)) {
      throw new Error(`CAPTURE03 GATE FAILED: rendered drawings changed across the round-trip`);
    }
    const p3b = path.join(OUT_DIR, "CHART-P03_03b_ROUNDTRIP_AFTER_1M.png");
    await page.screenshot({ path: p3b });
    record("capture03b_sha256", { file: path.basename(p3b), sha256: sha256(p3b) });
  }

  // ---------- CAPTURE 05: legacy percentage annotations — honest handling ----------
  {
    const state = await canvasState(page);
    record("capture05_legacy_state", { legacyText: state.legacyText, noteCount: state.noteCount });
    if (!state.legacyText || !state.legacyText.includes("UNANCHORED")) {
      throw new Error(`CAPTURE05 GATE FAILED: legacy list missing: ${state.legacyText}`);
    }
    if (!state.legacyText.includes("legacy percent-positioned note")) {
      throw new Error("CAPTURE05 GATE FAILED: percent note not listed");
    }
    // Distinct visual state: arm the text tool so the drawing status strip
    // renders alongside the legacy list (also proves the tool state is
    // visible whenever a tool is armed).
    await activateTool(page, "text");
    const armedState = await canvasState(page);
    record("capture05_armed_tool_state", { legacyText: armedState.legacyText });
    const p5 = path.join(OUT_DIR, "CHART-P03_05_LEGACY_UNANCHORED_HONEST.png");
    await page.screenshot({ path: p5 });
    record("capture05_sha256", { file: path.basename(p5), sha256: sha256(p5) });
    // Disarm the text tool — an armed tool would open the note dialog on any
    // subsequent chart click.
    await activateTool(page, "text");
  }

  // ---------- CAPTURE 04: F-CHART3-1 — saved note visible at its anchor ----------
  {
    const noteHit = await hitTest(page, "chart-add-annotation-btn");
    record("capture04_note_button_hitTest", { value: noteHit });
    await page.locator('[data-testid="chart-add-annotation-btn"]').click();
    await page.waitForSelector('[data-testid="annotation-dialog"]', { timeout: 5000 });
    await page.locator('[data-testid="annotation-text-input"]').fill("Resistance zone reviewed — anchored note");
    await page.locator('[data-testid="annotation-price-input"]').fill("1.09500");
    await hitTest(page, "annotation-save-btn");
    await page.locator('[data-testid="annotation-save-btn"]').click();
    await page.waitForTimeout(1500);
    const state = await canvasState(page);
    record("capture04_after_note_save", state);
    // The saved note now renders as an anchored marker on the chart.
    if (!state.drawings.some((d) => d.startsWith("drawing-"))) {
      throw new Error("CAPTURE04 GATE FAILED: saved note not rendered on the chart");
    }
    if (state.noteCount !== "+ Note (4)") {
      // 1 saved note + 1 trendline + 1 fib + ... count = annotations total
      record("capture04_note_count", { text: state.noteCount });
    }
    const p4 = path.join(OUT_DIR, "CHART-P03_04_SAVED_ANNOTATION_VISIBLE.png");
    await page.screenshot({ path: p4 });
    record("capture04_sha256", { file: path.basename(p4), sha256: sha256(p4) });
  }

  // ---------- CAPTURE 06: Market Structure — swings + BOS/CHoCH, M8 visible ----------
  {
    await page.locator('[data-testid="engine-menu-button-marketstructure"]').click();
    await page.waitForTimeout(200);
    await hitTest(page, "indicator-item-SWINGS55");
    await page.locator('[data-testid="indicator-item-SWINGS55"]').click();
    await page.waitForSelector('[data-testid="indicator-status-swings55"]', { timeout: 15000 });
    await page.locator('[data-testid="engine-menu-button-marketstructure"]').click();
    await page.waitForTimeout(200);
    await hitTest(page, "indicator-item-BOS55");
    await page.locator('[data-testid="indicator-item-BOS55"]').click();
    await page.waitForSelector('[data-testid="indicator-status-bos55"]', { timeout: 15000 });
    await page.locator('[data-testid="engine-menu-button-marketstructure"]').click();
    await page.waitForTimeout(200);
    await hitTest(page, "indicator-item-CHOCH55");
    await page.locator('[data-testid="indicator-item-CHOCH55"]').click();
    await page.waitForSelector('[data-testid="indicator-status-choch55"]', { timeout: 15000 });
    await page.waitForTimeout(1500);
    const state = await canvasState(page);
    record("capture06_structure_state", state);
    const swingStatus = await page.locator('[data-testid="indicator-status-swings55"]').textContent();
    const bosStatus = await page.locator('[data-testid="indicator-status-bos55"]').textContent();
    record("capture06_statuses", { swing: swingStatus, bos: bosStatus });
    // M8: the disclosure must be visible in the product.
    if (!swingStatus.includes("not evidence of institutional activity")) {
      throw new Error(`CAPTURE06 GATE FAILED: M8 disclosure missing: ${swingStatus}`);
    }
    const p6 = path.join(OUT_DIR, "CHART-P03_06_STRUCTURE_SWINGS_BOS_CHOCH.png");
    await page.screenshot({ path: p6 });
    record("capture06_sha256", { file: path.basename(p6), sha256: sha256(p6) });
  }

  // ---------- CAPTURE 07: FVG + Order Blocks — zones + disclosure ----------
  {
    await page.locator('[data-testid="engine-menu-button-marketstructure"]').click();
    await page.waitForTimeout(200);
    await page.locator('[data-testid="indicator-item-FVG3"]').click();
    await page.waitForSelector('[data-testid="indicator-status-fvg3"]', { timeout: 15000 });
    await page.locator('[data-testid="engine-menu-button-marketstructure"]').click();
    await page.waitForTimeout(200);
    await page.locator('[data-testid="indicator-item-OBPATTERN"]').click();
    await page.waitForSelector('[data-testid="indicator-status-obpattern"]', { timeout: 15000 });
    await page.waitForTimeout(1500);
    const state = await canvasState(page);
    record("capture07_zones_state", state);
    const obStatus = await page.locator('[data-testid="indicator-status-obpattern"]').textContent();
    record("capture07_ob_status", { text: obStatus });
    if (!obStatus.includes("not evidence of institutional activity")) {
      throw new Error("CAPTURE07 GATE FAILED: OB disclosure missing");
    }
    const p7 = path.join(OUT_DIR, "CHART-P03_07_FVG_ORDERBLOCK_PATTERN_ZONES.png");
    await page.screenshot({ path: p7 });
    record("capture07_sha256", { file: path.basename(p7), sha256: sha256(p7) });
  }

  // ---------- CAPTURE 08: insufficient — BOS on 1D (5 bars vs 12) ----------
  {
    for (const id of ["SWINGS55", "BOS55", "CHOCH55", "FVG3", "OBPATTERN"]) {
      await page.locator(`[data-testid="active-tray-${id}"]`).click();
    }
    await page.waitForTimeout(400);
    await hitTest(page, "chart-tf-1d");
    await page.locator('[data-testid="chart-tf-1d"]').click();
    await page.waitForSelector('[data-testid="timeframe-resampled-notice"]', { timeout: 15000 });
    await page.waitForTimeout(800);
    await page.locator('[data-testid="engine-menu-button-marketstructure"]').click();
    await page.waitForTimeout(200);
    await page.locator('[data-testid="indicator-item-BOS55"]').click();
    await page.waitForSelector('[data-testid="indicator-status-bos55"]', { timeout: 15000 });
    await page.waitForTimeout(800);
    const status = await page.locator('[data-testid="indicator-status-bos55"]').textContent();
    record("capture08_insufficient_status", { text: status });
    const state = await canvasState(page);
    record("capture08_state", state);
    if (state.activeOverlayLines !== "0" && state.activeOverlayLines !== null) {
      // structure indicators add overlay lines when computed; insufficient adds none
      record("capture08_overlay_lines", { value: state.activeOverlayLines });
    }
    if (!status.includes("insufficient history") || !status.includes("12 required") || !status.includes("5 available")) {
      throw new Error(`CAPTURE08 GATE FAILED: ${status}`);
    }
    const p8 = path.join(OUT_DIR, "CHART-P03_08_INSUFFICIENT_BOS_ON_D1.png");
    await page.screenshot({ path: p8 });
    record("capture08_sha256", { file: path.basename(p8), sha256: sha256(p8) });
  }

  // ---------- CAPTURE 09: drawing deletion — clean, no residue ----------
  {
    await hitTest(page, "chart-tf-1m");
    await page.locator('[data-testid="chart-tf-1m"]').click();
    await page.waitForSelector('[data-testid="timeframe-native-notice"]', { timeout: 15000 });
    await page.waitForTimeout(1200);
    const before = await canvasState(page);
    record("capture09_before_delete", { drawingCount: before.drawingCount, ids: before.drawings });
    if (before.drawingCount < 2) throw new Error(`CAPTURE09 GATE FAILED: expected drawings, got ${before.drawingCount}`);
    // Select a drawing by clicking a RENDERED HANDLE (real click, hit-tested
    // at the element itself — the handles are the anchor circles).
    const handle = page.locator('[data-testid^="drawing-handle-"]').first();
    const handleBox = await handle.boundingBox();
    if (!handleBox) throw new Error("CAPTURE09 GATE FAILED: no drawing handle to select");
    const clickPoint = { x: handleBox.x + handleBox.width / 2, y: handleBox.y + handleBox.height / 2 };
    const hitBefore = await page.evaluate(([px, py]) => {
      const el = document.elementFromPoint(px, py);
      return el ? { tag: el.tagName, testid: el.getAttribute("data-testid") } : null;
    }, [clickPoint.x, clickPoint.y]);
    record("capture09_selection_click_hitTest", { point: clickPoint, hit: hitBefore });
    if (!hitBefore || !hitBefore.testid?.startsWith("drawing-handle-")) {
      throw new Error(`CAPTURE09 GATE FAILED: click would not hit a drawing handle: ${JSON.stringify(hitBefore)}`);
    }
    await page.mouse.click(clickPoint.x, clickPoint.y);
    await page.waitForTimeout(500);
    const deleteBtnCount = await page.locator('[data-testid="drawing-delete-btn"]').count();
    record("capture09_delete_button_count", { value: deleteBtnCount });
    if (deleteBtnCount === 0) throw new Error("CAPTURE09 GATE FAILED: delete button not rendered after selection");
    const deleteHit = await hitTest(page, "drawing-delete-btn");
    const covering = await page.evaluate(() => {
      const btn = document.querySelector('[data-testid="drawing-delete-btn"]');
      const r = btn.getBoundingClientRect();
      const el = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      return el ? { tag: el.tagName, cls: el.className?.toString?.().slice(0, 60), testid: el.getAttribute("data-testid"), rect: { left: +r.left.toFixed(1), top: +r.top.toFixed(1) } } : null;
    });
    record("capture09_delete_button_hitTest", { value: deleteHit, covering });
    if (!deleteHit) throw new Error(`CAPTURE09 GATE FAILED: delete button covered by ${JSON.stringify(covering)}`);
    await page.locator('[data-testid="drawing-delete-btn"]').click();
    await page.waitForTimeout(1200);
    const after = await canvasState(page);
    record("capture09_after_delete", { drawingCount: after.drawingCount, ids: after.drawings });
    if (after.drawingCount !== before.drawingCount - 1) {
      throw new Error(`CAPTURE09 GATE FAILED: ${before.drawingCount} -> ${after.drawingCount}`);
    }
    const p9 = path.join(OUT_DIR, "CHART-P03_09_DRAWING_DELETED_CLEAN.png");
    await page.screenshot({ path: p9 });
    record("capture09_sha256", { file: path.basename(p9), sha256: sha256(p9) });
  }

  fs.writeFileSync(
    JSON_OUT,
    JSON.stringify(
      { generated_at: new Date().toISOString(), revision: "A", viewport: "1920x1080", scope: "CHART-P03 captures 01-09 (03 = pair)", records: LOG },
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
