// DA capture tooling — DATA-P02 capture 04: unavailable state, rendered
// honestly (untracked). Runs AFTER the fixture step: USDCHF M1 rows are
// deleted from the LOCAL dev database, so the REAL backend aggregation path
// returns kind=unavailable for a higher timeframe — no interception.
import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const OUT_DIR = "/home/user/data_p02_captures";
const JSON_OUT = "/home/user/DATA-P02_CAPTURE_VERIFICATION.json";
const LOG = [];

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

async function run() {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await login(page);
  await page.goto("http://localhost:5173/", { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="terminal-watchlist-dock"]', { state: "visible", timeout: 15000 });
  await page.waitForTimeout(7000);

  // API truth: USDCHF H1 must be unavailable after the fixture deletion.
  {
    const loginRes = await fetch("http://localhost:8000/api/v1/auth/login", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: "admin", password: "AxiomSecurePass2026!" }),
    });
    const { tokens } = await loginRes.json();
    const q = new URLSearchParams({ symbol: "USDCHF", timeframe: "H1", limit: "100", order: "asc" });
    const envelope = await (
      await fetch(`http://localhost:8000/api/v1/persistence/candle-series?${q}`, {
        headers: { Authorization: `Bearer ${tokens.access_token}` },
      })
    ).json();
    record("capture04_usdchf_h1_envelope", {
      kind: envelope.kind,
      detail: envelope.detail,
      bars: envelope.bars?.length ?? null,
    });
    if (envelope.kind !== "unavailable") {
      throw new Error("CAPTURE04 GATE FAILED: USDCHF H1 is not unavailable");
    }
  }

  // Interaction trace: hit-test the watchlist row before selecting USD/CHF.
  const hitOk = await page.locator('[data-testid="watchlist-row-usd-chf"]').evaluate((el) => {
    const r = el.getBoundingClientRect();
    const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return top === el || el.contains(top);
  });
  record("capture04_watchlist_row_hitTestBeforeClick", { value: hitOk });
  await page.locator('[data-testid="watchlist-row-usd-chf"]').click();
  await page.waitForTimeout(1200);
  const tfHit = await page.locator('[data-testid="chart-tf-1h"]').evaluate((el) => {
    const r = el.getBoundingClientRect();
    const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return top === el || el.contains(top);
  });
  record("capture04_tf1h_hitTestBeforeClick", { value: tfHit });
  await page.locator('[data-testid="chart-tf-1h"]').click();
  await page.waitForSelector('[data-testid="timeframe-unavailable-state"]', { timeout: 15000 });
  await page.waitForTimeout(800);

  const stateText = await page.locator('[data-testid="timeframe-unavailable-state"]').textContent();
  const resampledCount = await page.locator('[data-testid="timeframe-resampled-notice"]').count();
  const nativeCount = await page.locator('[data-testid="timeframe-native-notice"]').count();
  const unavailableTag = await page
    .locator('[data-testid="timeframe-unavailable-tag"]')
    .textContent()
    .catch(() => null);
  record("capture04_unavailable_state", {
    stateText: stateText?.replace(/\s+/g, " ").slice(0, 300) ?? null,
    unavailableTag,
    resampledNoticeCount: resampledCount,
    nativeNoticeCount: nativeCount,
    symbolBadge: await page.locator('[data-testid="chart-symbol-badge"]').textContent(),
  });
  if (resampledCount !== 0 || nativeCount !== 0) {
    throw new Error(`CAPTURE04 GATE FAILED: resampled=${resampledCount} native=${nativeCount} must be absent`);
  }
  if (!stateText || !stateText.includes("insufficient M1 coverage")) {
    throw new Error(`CAPTURE04 GATE FAILED: absence state missing detail: ${stateText}`);
  }

  // Legibility instrument: the absence text must be fully inside the canvas.
  const leg = await page.evaluate(() => {
    const clipEl = document.querySelector('[data-testid="chart-canvas-container"]');
    const clip = clipEl.getBoundingClientRect();
    const out = { clip: { left: +clip.left.toFixed(1), right: +clip.right.toFixed(1), top: +clip.top.toFixed(1), bottom: +clip.bottom.toFixed(1) }, elements: {} };
    for (const tid of ["timeframe-unavailable-state"]) {
      const el = document.querySelector(`[data-testid="${tid}"]`);
      const r = el.getBoundingClientRect();
      let ink = null;
      try {
        const range = document.createRange();
        range.selectNodeContents(el);
        ink = range.getBoundingClientRect();
      } catch { ink = null; }
      out.elements[tid] = {
        rect: { left: +r.left.toFixed(1), right: +r.right.toFixed(1), top: +r.top.toFixed(1), bottom: +r.bottom.toFixed(1) },
        inkRect: ink ? { left: +ink.left.toFixed(1), right: +ink.right.toFixed(1) } : null,
        verticallyInView: r.top >= clip.top - 0.5 && r.bottom <= clip.bottom + 0.5,
        inkFullyInside: ink !== null && ink.left >= clip.left - 0.5 && ink.right <= clip.right + 0.5 && r.top >= clip.top - 0.5 && r.bottom <= clip.bottom + 0.5,
      };
    }
    return out;
  });
  record("capture04_legibility", leg);
  const e = leg.elements["timeframe-unavailable-state"];
  if (!e || !e.verticallyInView || !e.inkFullyInside) {
    throw new Error("CAPTURE04 GATE FAILED: absence state not fully legible inside the canvas");
  }

  const p4 = path.join(OUT_DIR, "DATA-P02_04_UNAVAILABLE_STATE_HONEST_ABSENCE.png");
  await page.screenshot({ path: p4 });
  record("capture04_sha256", { file: path.basename(p4), sha256: sha256(p4) });

  // Merge this record into the part-A verification JSON (append-only).
  const prior = fs.existsSync(JSON_OUT) ? JSON.parse(fs.readFileSync(JSON_OUT, "utf8")) : { records: [] };
  prior.records = (prior.records || []).concat(LOG);
  prior.generated_at = new Date().toISOString();
  prior.scope = "DATA-P02 captures 01-05 complete";
  fs.writeFileSync(JSON_OUT, JSON.stringify(prior, null, 2));
  console.log("[DONE] merged verification JSON:", JSON_OUT);
  await browser.close();
}

run().catch((err) => {
  console.error("[FATAL]", err);
  process.exit(1);
});
