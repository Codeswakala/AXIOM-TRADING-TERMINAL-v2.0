// DA capture tooling — DATA-P01 correction cycle 3 (CA-DATA1-3), evidence-only.
// Untracked tooling; NOT part of any shipped patch. Re-captures 01 and 03 with
// the watchlist price column fully visible, using the identical interactions as
// scripts/capture_data_p01.mjs (same login, URL, waits, scroll), extended with
// the geometric legibility instrument: every element ITRGA requires legible is
// measured against the rows-container clip rect, hit-tested at its rightmost
// pixel, and recorded so the instrument and the shipped image must agree.
import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const OUT_DIR = "/home/user/data_p01_upload";
const JSON_OUT = "/home/user/DATA-P01_CAPTURE_VERIFICATION.json";
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

// Environment record: feed state + retained snapshot, from the machine's side.
async function recordEnvironment() {
  const loginRes = await fetch("http://localhost:8000/api/v1/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: "admin", password: "AxiomSecurePass2026!" }),
  });
  const { tokens } = await loginRes.json();
  const statsRes = await fetch("http://localhost:8000/api/v1/market/live/stats", {
    headers: { Authorization: `Bearer ${tokens.access_token}` },
  });
  const stats = await statsRes.json();
  const snapshot = stats.latest_by_symbol || {};
  record("environment_feed_state_at_capture", {
    running: stats.running,
    adapter: stats.adapter,
    snapshotSymbols: Object.keys(snapshot).length,
    snapshotSources: [...new Set(Object.values(snapshot).map((c) => c.source))],
    snapshotSample: Object.fromEntries(
      Object.entries(snapshot).slice(0, 3).map(([s, c]) => [s, { close: c.close, source: c.source }]),
    ),
    usdjpySnapshotClose: snapshot["USDJPY"]?.close ?? null,
  });
}

// Legibility instrument: rect containment inside the rows clip (both axes) +
// hit-test at the element's rightmost pixel. Elements below the container's
// visible bottom (e.g. rows hidden below the fold in the un-scrolled view)
// are recorded with vertical visibility false — measured, never claimed.
async function measureLegibility(page, testids) {
  return page.evaluate((testids) => {
    const rows = document.querySelector(".watchlist-rows-container");
    const clip = rows ? rows.getBoundingClientRect() : null;
    const out = {
      rowsContainer: clip
        ? { left: +clip.left.toFixed(1), right: +clip.right.toFixed(1), top: +clip.top.toFixed(1), bottom: +clip.bottom.toFixed(1), clientWidth: rows.clientWidth, scrollWidth: rows.scrollWidth, overflowX: getComputedStyle(rows).overflowX }
        : null,
      elements: {},
    };
    for (const tid of testids) {
      const el = document.querySelector(`[data-testid="${tid}"]`);
      if (!el) {
        out.elements[tid] = null;
        continue;
      }
      const r = el.getBoundingClientRect();
      // Ink rect: the precise painted extent of the glyphs (DOM Range), versus
      // the layout box which may carry empty glyph margin. Both are recorded —
      // the instrument must not overstate containment either way.
      let ink = null;
      try {
        const range = document.createRange();
        range.selectNodeContents(el);
        ink = range.getBoundingClientRect();
      } catch {
        ink = null;
      }
      const verticallyInView =
        clip !== null && r.top >= clip.top - 0.5 && r.bottom <= clip.bottom + 0.5;
      const boxInside = clip !== null && r.left >= clip.left - 0.5 && r.right <= clip.right + 0.5;
      const inkInside = clip !== null && ink !== null && ink.left >= clip.left - 0.5 && ink.right <= clip.right + 0.5;
      const hitX = Math.min(r.right - 1, r.left + r.width * 0.95);
      const hitY = r.top + r.height / 2;
      let hitRec = null;
      if (verticallyInView) {
        const hit = document.elementFromPoint(hitX, hitY);
        const hitRow = hit !== null ? hit.closest('[data-testid^="watchlist-row-"]') : null;
        const elRow = el.closest('[data-testid^="watchlist-row-"]');
        hitRec = {
          x: +hitX.toFixed(1),
          y: +hitY.toFixed(1),
          hitIsSelf: hit === el || (hit !== null && el.contains(hit)),
          hitTag: hit ? hit.tagName : null,
          hitWithinSameRow: hitRow === elRow && hitRow !== null,
        };
      }
      // Stroke-extent measurement: render the element's text at its computed
      // font into an offscreen canvas and find the rightmost painted pixel.
      // Distinguishes painted ink (what the image shows) from the advance box
      // (which can carry empty glyph margin past the clip boundary).
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
            if (imgData.data[row + x * 4 + 3] > 0) {
              if (x > rightmost) rightmost = x;
              break;
            }
          }
        }
        const advance = ctx.measureText(el.textContent.trim()).width;
        stroke = {
          strokeRightInViewport: +(r.left + (rightmost - 4)).toFixed(1),
          advanceRightInViewport: +(r.left + (advance + 4)).toFixed(1),
        };
      } catch {
        stroke = null;
      }
      out.elements[tid] = {
        rect: { left: +r.left.toFixed(1), right: +r.right.toFixed(1), top: +r.top.toFixed(1), bottom: +r.bottom.toFixed(1), width: +r.width.toFixed(1) },
        inkRect: ink ? { left: +ink.left.toFixed(1), right: +ink.right.toFixed(1) } : null,
        strokeExtent: stroke,
        text: el.textContent.trim(),
        verticallyInView,
        boxFullyInside: boxInside && verticallyInView,
        inkFullyInside: inkInside && verticallyInView,
        hitTestAtRightmostPixel: hitRec,
      };
    }
    return out;
  }, testids);
}

// Containment gate: required elements must be fully visible in both axes —
// if the instrument disagrees with the claim, the run fails instead of
// shipping a non-conforming artifact. Prices must be inside by ink rect;
// change percentages must have their PAINTED STROKES inside the boundary
// (the advance box may overshoot with empty glyph margin — that is recorded,
// never silently accepted).
function assertLegible(rec, instrument, requiredPrices, requiredChanges) {
  const failures = [];
  const clip = instrument.rowsContainer;
  for (const tid of requiredPrices) {
    const e = instrument?.elements?.[tid];
    if (!e) {
      failures.push(`${tid}: element missing`);
      continue;
    }
    if (!e.verticallyInView) failures.push(`${tid}: vertically outside the rows viewport`);
    if (!e.inkFullyInside) failures.push(`${tid}: ink (${e.inkRect?.left}-${e.inkRect?.right}) not inside clip (${clip.left}-${clip.right})`);
  }
  for (const tid of requiredChanges) {
    const e = instrument?.elements?.[tid];
    if (!e) {
      failures.push(`${tid}: element missing`);
      continue;
    }
    if (!e.verticallyInView) failures.push(`${tid}: vertically outside the rows viewport`);
    const sr = e.strokeExtent?.strokeRightInViewport;
    if (sr === undefined || sr === null) {
      failures.push(`${tid}: stroke extent unavailable`);
      continue;
    }
    if (sr > clip.right + 0.5) {
      failures.push(`${tid}: painted stroke reaches x=${sr}, beyond clip right ${clip.right}`);
    }
  }
  if (failures.length > 0) {
    throw new Error(`LEGIBILITY GATE FAILED for ${rec}:\n${failures.join("\n")}`);
  }
  return true;
}

async function run() {
  const browser = await chromium.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });
  record("environment_browser", { chromium: browser.version(), viewport: "1920x1080", deviceScaleFactor: 1 });
  await recordEnvironment();

  const page = await context.newPage();
  await login(page);

  // ---------- CAPTURE 01: WATCHLIST POPULATED ACROSS ALL ELEVEN ----------
  await page.goto("http://localhost:5173/", { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="terminal-watchlist-dock"]', {
    state: "visible",
    timeout: 15000,
  });
  await page.waitForTimeout(7000);

  const prices = {};
  for (const key of ["eurusd", "gbpusd", "usdjpy", "audusd", "usdcad", "usdchf", "nzdusd", "eurgbp", "btcusd", "ethusd", "solusd"]) {
    prices[key] = await page
      .locator(`[data-testid="price-${key}"]`)
      .textContent()
      .catch(() => null);
  }
  const populatedCount = Object.values(prices).filter((v) => v !== null && v !== "--").length;
  const dashCount = Object.values(prices).filter((v) => v === "--").length;
  const usdjpy3dp = /^\d{2,3}\.\d{3}$/.test(prices.usdjpy ?? "");
  record("capture01_all_eleven_prices", { prices, populatedCount, dashCount, usdjpy3dp });
  const chips = await page.locator('[data-testid^="watchlist-provenance-"]').count();
  const sparklines = await page.locator('[data-testid^="watchlist-sparkline-"]').count();
  const sparklineTags = await page.locator('[data-testid^="watchlist-sparkline-source-"]').count();
  record("capture01_provenance_and_sparklines", { chips, sparklines, sparklineTags });
  const tagText01 = await page.locator('[data-testid="watchlist-sparkline-source-usdjpy"]').textContent().catch(() => null);
  record("capture01_usdjpy_sparkline_source_tag", { text: tagText01 });

  // Legibility instrument — every price ITRGA requires legible in capture 01.
  const leg01 = await measureLegibility(page, [
    "price-eurusd",
    "price-gbpusd",
    "price-usdjpy",
    "price-audusd",
    "price-usdcad",
    "price-usdchf",
    "price-nzdusd",
    "price-eurgbp",
    "price-btcusd",
    "price-ethusd",
    "price-solusd",
    "change-usdjpy",
  ]);
  record("capture01_legibility", leg01);
  assertLegible("capture01", leg01, ["price-usdjpy", "price-btcusd"], []);
  const p1 = path.join(OUT_DIR, "DATA-P01_01_WATCHLIST_ALL_ELEVEN_POPULATED.png");
  await page.screenshot({ path: p1 });
  record("capture01_sha256", { file: path.basename(p1), sha256: sha256(p1) });

  // ---------- CAPTURE 03: SCROLLED TO CRYPTO ROWS, PROVENANCE IN FRAME ----------
  await page.evaluate(() => {
    const rows = document.querySelector(".watchlist-rows-container");
    if (rows) rows.scrollTop = rows.scrollHeight;
  });
  await page.waitForTimeout(500);
  const rowsMetrics = await page.locator(".watchlist-rows-container").evaluate((el) => ({
    scrollTop: el.scrollTop,
    scrollHeight: el.scrollHeight,
    clientHeight: el.clientHeight,
  }));
  const solRowVisible = await page.locator('[data-testid="watchlist-row-sol-usd"]').count();
  const solPrice = await page.locator('[data-testid="price-solusd"]').textContent().catch(() => null);
  const solProvenance = await page
    .locator('[data-testid="watchlist-provenance-solusd"]')
    .textContent()
    .catch(() => null);
  record("capture03_crypto_rows_scroll", { rowsMetrics, solRowVisible, solPrice, solProvenance });

  // Legibility instrument — crypto prices AND percentage changes, as required.
  const leg03 = await measureLegibility(page, [
    "price-btcusd",
    "price-ethusd",
    "price-solusd",
    "change-btcusd",
    "change-ethusd",
    "change-solusd",
  ]);
  record("capture03_legibility", leg03);
  assertLegible(
    "capture03",
    leg03,
    ["price-btcusd", "price-ethusd", "price-solusd"],
    ["change-btcusd", "change-ethusd", "change-solusd"],
  );
  const p3 = path.join(OUT_DIR, "DATA-P01_03_CRYPTO_ROWS_PROVENANCE_SCROLLED.png");
  await page.screenshot({ path: p3 });
  record("capture03_sha256", { file: path.basename(p3), sha256: sha256(p3) });

  // Re-declare the unchanged Rev C artifacts (02/04/05) so the per-phase JSON
  // remains a complete record; hashes are the Rev C values, verified on disk.
  for (const [name, expected] of [
    ["DATA-P01_02_ROW_SELECTION_INTERACTION.png", "766eb716486a63ddf46223665422646266cdc7ca0958fe9ae2c10612b41d0ca4"],
    ["DATA-P01_04_FEED_STOPPED_DASH_ABSENCE.png", "a83991693bb816fea4adb12c3ebba8ada6babdfba82e14a63c72914b1ef91ed4"],
    ["DATA-P01_05_SINGLE_SYMBOL_SPARKLINE_FAILURE.png", "8f160e77c1b700cb1705b278181a1e32bd944e10efe85372d26adcee62e57731"],
  ]) {
    const p = path.join(OUT_DIR, name);
    const actual = fs.existsSync(p) ? sha256(p) : null;
    record("unchanged_rev_c_artifact", { file: name, hashMatches: actual === expected, sha256: actual });
  }

  fs.writeFileSync(
    JSON_OUT,
    JSON.stringify(
      { generated_at: new Date().toISOString(), revision: "D", viewport: "1920x1080", scope: "CA-DATA1-3 evidence-only re-captures (01, 03)", records: LOG },
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
