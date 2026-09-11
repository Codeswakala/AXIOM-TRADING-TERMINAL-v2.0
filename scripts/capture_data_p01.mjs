import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const OUT_DIR = "/home/user/data_p01_captures";
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

async function run() {
  const browser = await chromium.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });
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
  const chips = await page.locator('[data-testid^="watchlist-provenance-"]').count();
  const sparklines = await page.locator('[data-testid^="watchlist-sparkline-"]').count();
  const sparklineTags = await page.locator('[data-testid^="watchlist-sparkline-source-"]').count();
  record("capture01_all_eleven_prices", { prices, populatedCount, dashCount });
  record("capture01_provenance_and_sparklines", { chips, sparklines, sparklineTags });

  const p1 = path.join(OUT_DIR, "DATA-P01_01_WATCHLIST_ALL_ELEVEN_POPULATED.png");
  await page.screenshot({ path: p1 });
  record("capture01_sha256", { file: path.basename(p1), sha256: sha256(p1) });

  // ---------- CAPTURE 02: INTERACTION TRACE — ROW SELECTION ----------
  const gbpRow = page.locator('[data-testid="watchlist-row-gbp-usd"]');
  await gbpRow.scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  const hitTestOwnsPointer = await gbpRow.evaluate((el) => {
    const r = el.getBoundingClientRect();
    const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return top === el || el.contains(top);
  });
  record("capture02_row_hitTestBeforeClick", { value: hitTestOwnsPointer });
  const tickerBefore = await page.locator('[data-testid="ticker-symbol-badge"]').textContent().catch(() => null);
  await gbpRow.click();
  await page.waitForTimeout(800);
  const tickerAfter = await page.locator('[data-testid="ticker-symbol-badge"]').textContent().catch(() => null);
  const gbpSelected = await page
    .locator('[data-testid="watchlist-row-gbp-usd"]')
    .evaluate((el) => el.classList.contains("selected"));
  record("capture02_selection_landed", { tickerBefore, tickerAfter, gbpSelected });
  const p2 = path.join(OUT_DIR, "DATA-P01_02_ROW_SELECTION_INTERACTION.png");
  await page.screenshot({ path: p2 });
  record("capture02_sha256", { file: path.basename(p2), sha256: sha256(p2) });

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
  const p3 = path.join(OUT_DIR, "DATA-P01_03_CRYPTO_ROWS_PROVENANCE_SCROLLED.png");
  await page.screenshot({ path: p3 });
  record("capture03_sha256", { file: path.basename(p3), sha256: sha256(p3) });

  // ---------- CAPTURE 05: SINGLE-SYMBOL SPARKLINE FAILURE (R1) ----------
  const pageError = await context.newPage();
  await pageError.route(
    /\/api\/v1\/persistence\/candles\?.*symbol=GBPUSD/,
    (route) => route.abort(),
  );
  await pageError.goto("http://localhost:5173/", { waitUntil: "domcontentloaded" });
  await pageError.waitForSelector('[data-testid="terminal-watchlist-dock"]', {
    state: "visible",
    timeout: 15000,
  });
  await pageError.waitForTimeout(7000);
  const gbpSparkline = await pageError.locator('[data-testid="watchlist-sparkline-gbpusd"]').count();
  const gbpPrice = await pageError.locator('[data-testid="price-gbpusd"]').textContent().catch(() => null);
  const eurSparkline = await pageError.locator('[data-testid="watchlist-sparkline-eurusd"]').count();
  const rowCount = await pageError.locator('[data-testid^="watchlist-row-"]').count();
  record("capture05_single_symbol_sparkline_failure", {
    gbpSparklinePresent: gbpSparkline > 0,
    gbpPrice,
    eurSparklinePresent: eurSparkline > 0,
    totalRows: rowCount,
  });
  const p5 = path.join(OUT_DIR, "DATA-P01_05_SINGLE_SYMBOL_SPARKLINE_FAILURE.png");
  await pageError.screenshot({ path: p5 });
  record("capture05_sha256", { file: path.basename(p5), sha256: sha256(p5) });

  fs.writeFileSync(
    JSON_OUT,
    JSON.stringify(
      { generated_at: new Date().toISOString(), viewport: "1920x1080", records: LOG },
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
