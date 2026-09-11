// DA capture tooling — DATA-P02 evidence captures 01/02/03/05 (untracked).
// Same discipline as DATA-P01 cycle 3: environment declared in the JSON,
// legibility instrument (layout box, ink rect, painted-stroke extent,
// hit-test at the rightmost pixel) with a HARD GATE that fails the run if a
// required element is not fully legible inside its containing panel.
// Capture 04 (unavailable state) runs in capture_data_p02_unavailable.mjs
// after its fixture step.
import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const OUT_DIR = "/home/user/data_p02_captures";
const JSON_OUT = "/home/user/DATA-P02_CAPTURE_VERIFICATION.json";
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

async function apiSeries(symbol, timeframe) {
  const loginRes = await fetch("http://localhost:8000/api/v1/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: "admin", password: "AxiomSecurePass2026!" }),
  });
  const { tokens } = await loginRes.json();
  const q = new URLSearchParams({ symbol, timeframe, limit: "100", order: "asc" });
  const res = await fetch(`http://localhost:8000/api/v1/persistence/candle-series?${q}`, {
    headers: { Authorization: `Bearer ${tokens.access_token}` },
  });
  return res.json();
}

// Session boundary math mirroring frontend/src/terminal/sessions.ts (fixed
// UTC windows) — the instrument recomputes labels and compares against the DOM.
const SESSIONS = [
  { id: "tokyo", label: "TOKYO", start: 0, end: 9 },
  { id: "london", label: "LONDON", start: 7, end: 16 },
  { id: "newyork", label: "NEW YORK", start: 12, end: 21 },
];
const hhmm = (h) => `${String(h).padStart(2, "0")}:00`;
function sessionsAtTime(d) {
  const day = d.getUTCDay();
  if (day === 0 || day === 6) return [];
  const hour = d.getUTCHours();
  return SESSIONS.filter((s) => hour >= s.start && hour < s.end);
}
function overlapPeriod(a, b) {
  const sa = SESSIONS.find((s) => s.id === a);
  const sb = SESSIONS.find((s) => s.id === b);
  const start = Math.max(sa.start, sb.start);
  const end = Math.min(sa.end, sb.end);
  return `${hhmm(start)}–${hhmm(end)} UTC`;
}
function sessionLabelOfDate(d) {
  const active = sessionsAtTime(d);
  if (active.length === 0) {
    const day = d.getUTCDay();
    return day === 0 || day === 6 ? "MARKET CLOSED (WEEKEND)" : "NO ACTIVE SESSION";
  }
  if (active.length === 1) return active[0].label;
  return `${active[0].label} + ${active[1].label} (overlap ${overlapPeriod(active[0].id, active[1].id)})`;
}

// Legibility instrument (DATA-P01 cycle-3 standard): containment inside the
// chart stage, ink rect via DOM Range, painted-stroke extent via canvas,
// hit-test at the element's rightmost pixel.
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

function assertLegible(rec, instrument, required, clipTestid) {
  const failures = [];
  for (const tid of required) {
    const e = instrument?.elements?.[tid];
    if (!e) { failures.push(`${tid}: element missing`); continue; }
    if (!e.verticallyInView) failures.push(`${tid}: vertically outside ${clipTestid}`);
    if (!e.inkFullyInside) failures.push(`${tid}: ink (${e.inkRect?.left}-${e.inkRect?.right}) not inside clip (${instrument.clip.left}-${instrument.clip.right})`);
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

async function run() {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  record("environment_browser", { chromium: browser.version(), viewport: "1920x1080", deviceScaleFactor: 1 });

  // Environment: feed state + retained snapshot (machine-recorded).
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
      snapshotSources: [...new Set(Object.values(stats.latest_by_symbol || {}).map((c) => c.source))],
    });
  }

  const page = await context.newPage();
  await login(page);
  await page.goto("http://localhost:5173/", { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="terminal-watchlist-dock"]', { state: "visible", timeout: 15000 });
  await page.waitForTimeout(7000);

  // ---------- CAPTURE 01: 1m NATIVE — no resampled notice ----------
  {
    await page.waitForSelector('[data-testid="timeframe-native-notice"]', { timeout: 15000 });
    const resampledCount = await page.locator('[data-testid="timeframe-resampled-notice"]').count();
    const nativeCount = await page.locator('[data-testid="timeframe-native-notice"]').count();
    const envelope = await apiSeries("EURUSD", "M1");
    record("capture01_1m_native", {
      envelopeKind: envelope.kind,
      envelopeBars: envelope.bars?.length ?? null,
      firstOpenTime: envelope.bars?.[0]?.open_time ?? null,
      lastOpenTime: envelope.bars?.[envelope.bars.length - 1]?.open_time ?? null,
      nativeNoticeCount: nativeCount,
      resampledNoticeCount: resampledCount,
    });
    if (resampledCount !== 0 || nativeCount !== 1) {
      throw new Error(`CAPTURE01 GATE FAILED: resampled=${resampledCount} native=${nativeCount}`);
    }
    const leg = await measureLegibility(page, ["timeframe-native-notice"], "terminal-chart-stage");
    record("capture01_legibility", leg);
    assertLegible("capture01", leg, ["timeframe-native-notice"], "terminal-chart-stage");
    const p1 = path.join(OUT_DIR, "DATA-P02_01_1M_NATIVE_NO_RESAMPLED_NOTICE.png");
    await page.screenshot({ path: p1 });
    record("capture01_sha256", { file: path.basename(p1), sha256: sha256(p1) });
  }

  // ---------- CAPTURE 02: 1h AGGREGATED — notice true, bars differ ----------
  {
    const hitOk = await hitTestBeforeClick(page, "chart-tf-1h");
    record("capture02_tf1h_hitTestBeforeClick", { value: hitOk });
    await page.locator('[data-testid="chart-tf-1h"]').click();
    await page.waitForSelector('[data-testid="timeframe-resampled-notice"]', { timeout: 15000 });
    await page.waitForTimeout(1200);
    const envelope = await apiSeries("EURUSD", "H1");
    const allHourAligned = (envelope.bars ?? []).every((b) => b.open_time.endsWith(":00:00Z"));
    const allCompleteH1 = (envelope.bars ?? []).every((b) => b.complete === true && b.constituents === 60);
    record("capture02_1h_aggregated_envelope", {
      kind: envelope.kind,
      sourceTimeframe: envelope.sourceTimeframe,
      excludedPartialBuckets: envelope.excludedPartialBuckets,
      bars: envelope.bars?.length ?? null,
      firstOpenTime: envelope.bars?.[0]?.open_time ?? null,
      lastOpenTime: envelope.bars?.[envelope.bars.length - 1]?.open_time ?? null,
      allHourAligned,
      allComplete: allCompleteH1,
    });
    if (envelope.kind !== "aggregated" || envelope.sourceTimeframe !== "M1" || !allHourAligned || !allCompleteH1) {
      throw new Error("CAPTURE02 GATE FAILED: envelope is not fully hour-aligned aggregated");
    }
    const notice = await page.locator('[data-testid="timeframe-resampled-notice"]').textContent();
    record("capture02_notice_text", { text: notice });
    if (!notice.includes("wall-clock aligned") || !notice.includes("60-minute buckets")) {
      throw new Error(`CAPTURE02 GATE FAILED: notice inaccurate: ${notice}`);
    }
    const leg = await measureLegibility(page, ["timeframe-resampled-notice"], "terminal-chart-stage");
    record("capture02_legibility", leg);
    assertLegible("capture02", leg, ["timeframe-resampled-notice"], "terminal-chart-stage");
    const p2 = path.join(OUT_DIR, "DATA-P02_02_1H_AGGREGATED_NOTICE_TRUE.png");
    await page.screenshot({ path: p2 });
    record("capture02_sha256", { file: path.basename(p2), sha256: sha256(p2) });
  }

  // ---------- CAPTURE 03: 1d AGGREGATED — wall-clock day boundaries ----------
  {
    const hitOk = await hitTestBeforeClick(page, "chart-tf-1d");
    record("capture03_tf1d_hitTestBeforeClick", { value: hitOk });
    await page.locator('[data-testid="chart-tf-1d"]').click();
    await page.waitForSelector('[data-testid="timeframe-resampled-notice"]', { timeout: 15000 });
    await page.waitForTimeout(1200);
    const envelope = await apiSeries("EURUSD", "D1");
    const allDayAligned = (envelope.bars ?? []).every((b) => b.open_time.endsWith("T00:00:00Z"));
    const allCompleteD1 = (envelope.bars ?? []).every((b) => b.complete === true && b.constituents === 1440);
    record("capture03_1d_aggregated_envelope", {
      kind: envelope.kind,
      bars: envelope.bars?.length ?? null,
      firstOpenTime: envelope.bars?.[0]?.open_time ?? null,
      lastOpenTime: envelope.bars?.[envelope.bars.length - 1]?.open_time ?? null,
      allDayAligned,
      allComplete: allCompleteD1,
    });
    if (envelope.kind !== "aggregated" || !allDayAligned || !allCompleteD1) {
      throw new Error("CAPTURE03 GATE FAILED: D1 bars not wall-clock day aligned");
    }
    const notice = await page.locator('[data-testid="timeframe-resampled-notice"]').textContent();
    record("capture03_notice_text", { text: notice });
    if (!notice.includes("1440-minute buckets")) {
      throw new Error(`CAPTURE03 GATE FAILED: notice inaccurate: ${notice}`);
    }
    const leg = await measureLegibility(page, ["timeframe-resampled-notice"], "terminal-chart-stage");
    record("capture03_legibility", leg);
    assertLegible("capture03", leg, ["timeframe-resampled-notice"], "terminal-chart-stage");
    const p3 = path.join(OUT_DIR, "DATA-P02_03_1D_AGGREGATED_DAY_BOUNDARIES.png");
    await page.screenshot({ path: p3 });
    record("capture03_sha256", { file: path.basename(p3), sha256: sha256(p3) });
  }

  // ---------- CAPTURE 05: SESSION CONTEXT — current session + bar hover ----------
  {
    await page.locator('[data-testid="chart-tf-1m"]').click();
    await page.waitForSelector('[data-testid="timeframe-native-notice"]', { timeout: 15000 });
    await page.waitForTimeout(1500);

    const strip = await page.evaluate(() => {
      const grab = (id) => document.querySelector(`[data-testid="${id}"]`)?.textContent?.trim() ?? null;
      return {
        clock: grab("session-clock"),
        current: grab("session-current"),
        overlap: grab("session-overlap"),
        span: grab("session-series-span"),
      };
    });
    // Instrument↔image agreement: recompute the session label from the
    // DISPLAYED clock text and compare with the displayed current label.
    const clockMatch = /^(\d{2}):(\d{2}) UTC$/.exec(strip.clock ?? "");
    if (!clockMatch) throw new Error(`CAPTURE05 GATE FAILED: unparsable clock ${strip.clock}`);
    const expectedFromClock = (() => {
      const h = Number(clockMatch[1]);
      const m = Number(clockMatch[2]);
      const now = new Date();
      // use today's UTC date with the displayed hour/minute
      const d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), h, m));
      return sessionLabelOfDate(d);
    })();
    record("capture05_session_strip", { strip, expectedFromClock, matches: strip.current === expectedFromClock });
    if (strip.current !== expectedFromClock) {
      throw new Error(`CAPTURE05 GATE FAILED: displayed ${strip.current} vs recomputed ${expectedFromClock}`);
    }

    // Hover over the chart canvas to surface the bar-level session readout.
    const canvas = page.locator('[data-testid="chart-canvas-container"]');
    const box = await canvas.boundingBox();
    const hoverPoint = { x: box.x + box.width * 0.55, y: box.y + box.height * 0.5 };
    const hitAtHover = await page.evaluate(([x, y]) => {
      const el = document.elementFromPoint(x, y);
      return el ? { tag: el.tagName, cls: el.className?.toString?.().slice(0, 60), testid: el.getAttribute("data-testid") } : null;
    }, [hoverPoint.x, hoverPoint.y]);
    record("capture05_hover_target_hitTest", { point: hoverPoint, hit: hitAtHover });
    await page.mouse.move(hoverPoint.x, hoverPoint.y);
    await page.waitForTimeout(800);
    const hoveredText = await page
      .locator('[data-testid="session-hovered-bar"]')
      .textContent()
      .catch(() => null);
    record("capture05_hovered_bar_readout", { text: hoveredText });
    if (!hoveredText) throw new Error("CAPTURE05 GATE FAILED: hover readout did not appear");
    // Self-consistency: recompute the session from the readout's own bar time.
    const barMatch = /^BAR (\d{2}):(\d{2}) UTC — (.+)$/.exec(hoveredText);
    if (!barMatch) throw new Error(`CAPTURE05 GATE FAILED: unparsable readout ${hoveredText}`);
    const expectedBar = (() => {
      const now = new Date();
      const d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), Number(barMatch[1]), Number(barMatch[2])));
      return sessionLabelOfDate(d);
    })();
    record("capture05_hovered_bar_self_consistency", { displayed: barMatch[3], recomputed: expectedBar, matches: barMatch[3] === expectedBar });
    if (barMatch[3] !== expectedBar) {
      throw new Error(`CAPTURE05 GATE FAILED: readout ${barMatch[3]} vs recomputed ${expectedBar}`);
    }
    const leg = await measureLegibility(
      page,
      ["session-clock", "session-current", "session-hovered-bar", "session-series-span"],
      "terminal-chart-stage",
    );
    record("capture05_legibility", leg);
    assertLegible("capture05", leg, ["session-clock", "session-current", "session-hovered-bar"], "terminal-chart-stage");
    const p5 = path.join(OUT_DIR, "DATA-P02_05_SESSION_CONTEXT_HOVER_READOUT.png");
    await page.screenshot({ path: p5 });
    record("capture05_sha256", { file: path.basename(p5), sha256: sha256(p5) });
  }

  fs.writeFileSync(
    JSON_OUT,
    JSON.stringify(
      { generated_at: new Date().toISOString(), revision: "A", viewport: "1920x1080", scope: "DATA-P02 captures 01/02/03/05 (capture 04 appended separately)", records: LOG },
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
