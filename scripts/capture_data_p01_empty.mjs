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

  // ---------- CAPTURE 04: FEED STOPPED — M5 `--` ABSENCE PATH ----------
  // This script runs against a FRESH backend process where the live feed has
  // never been started: no live:simulated quotes exist (latest_by_symbol is
  // empty), while the seeded candles persist in the database. The watchlist
  // must render `--` for every price and still render sparklines from the
  // seeded series — absence is preserved, and candle-derived context does
  // not fabricate a price.
  await page.goto("http://localhost:5173/", { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="terminal-watchlist-dock"]', {
    state: "visible",
    timeout: 15000,
  });
  await page.waitForTimeout(6000);

  const prices = {};
  for (const key of ["eurusd", "gbpusd", "usdjpy", "audusd", "usdcad", "usdchf", "nzdusd", "eurgbp", "btcusd", "ethusd", "solusd"]) {
    prices[key] = await page
      .locator(`[data-testid="price-${key}"]`)
      .textContent()
      .catch(() => null);
  }
  const allDash = Object.values(prices).every((v) => v === "--");
  const sparklines = await page.locator('[data-testid^="watchlist-sparkline-"]').count();
  const chips = await page.locator('[data-testid^="watchlist-provenance-"]').count();
  record("capture04_feed_stopped_absence", { prices, allDash, sparklines, priceChips: chips });

  const p4 = path.join(OUT_DIR, "DATA-P01_04_FEED_STOPPED_DASH_ABSENCE.png");
  await page.screenshot({ path: p4 });
  record("capture04_sha256", { file: path.basename(p4), sha256: sha256(p4) });

  // Merge this record into the part-A verification JSON (append-only).
  const prior = fs.existsSync(JSON_OUT) ? JSON.parse(fs.readFileSync(JSON_OUT, "utf8")) : { records: [] };
  prior.records = (prior.records || []).concat(LOG);
  prior.generated_at = new Date().toISOString();
  fs.writeFileSync(JSON_OUT, JSON.stringify(prior, null, 2));
  console.log("[DONE] merged verification JSON:", JSON_OUT);
  await browser.close();
}

run().catch((err) => {
  console.error("[FATAL]", err);
  process.exit(1);
});
