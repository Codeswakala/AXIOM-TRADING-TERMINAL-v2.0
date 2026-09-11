/**
 * BO-F-02 Level-I capture probe (DA evidence tooling, untracked).
 *
 * Flow: login -> terminal -> SIGNALS dock (default)
 *   1. predictive family (default) with deferred-empty state -> f02_predictive_deferred.png
 *   2. switch family tab to STRUCTURAL (EUR/USD, 1h aggregated seed) -> f02_structural.png
 *   3. select BTC/USD (real corpus H1) -> structural events over REAL data -> f02_structural_real.png
 *   4. honest empty: EUR/USD + 1d (insufficient series) -> f02_structural_empty.png
 * Also samples: family tab separation, descriptive framing text, no-actuation scan.
 *
 * Log: docs/evidence/f02/f02_capture_log.txt
 */

import { createRequire } from "module";
import { createHash } from "crypto";
import * as fs from "fs";

const require = createRequire("/home/user/axiom/frontend/package.json");
const { chromium } = require("playwright");

const BASE = "http://127.0.0.1:5173";
const OUT = "/home/user/axiom/docs/evidence/f02";
fs.mkdirSync(OUT, { recursive: true });

const LINES = [];
const out = (line) => {
  console.log(line);
  LINES.push(line);
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
page.setDefaultTimeout(20000);

out(`=== BO-F-02 CAPTURE PROBE (${new Date().toISOString()}) ===`);
out(`target: ${BASE} (vite dev, backend proxy 127.0.0.1:8000)`);

await page.goto(`${BASE}/login`);
await page.getByTestId("login-username-input").fill("admin");
await page.getByTestId("login-password-input").fill("AxiomSecurePass2026!");
await page.getByTestId("login-submit-btn").click();
await page.waitForSelector('[data-testid="trading-terminal-workspace"]', { timeout: 20000 });
out("login: OK");

// The right dock's SIGNALS tab is default-mounted.
await page.waitForSelector('[data-testid="terminal-signal-stream"]', { timeout: 20000 });
out("signal stream mounted (SIGNALS dock)");

// ---- 1. predictive family (default) + deferred empty state -----------------
await page.waitForSelector('[data-testid="signal-deferred-empty-state"]', { timeout: 20000 });
const familyTabs = await page.evaluate(() => ({
  structural: document.querySelector('[data-testid="signal-family-structural"]')?.getAttribute("aria-selected"),
  predictive: document.querySelector('[data-testid="signal-family-predictive"]')?.getAttribute("aria-selected"),
  predictiveLabel: document.querySelector('[data-testid="predictive-family-label"]')?.textContent,
  deferredText: document.querySelector('[data-testid="signal-deferred-empty-state"]')?.textContent?.slice(0, 140),
}));
out(`family tabs (default predictive): ${JSON.stringify(familyTabs)}`);
fs.writeFileSync(`${OUT}/f02_predictive_deferred.png`, await page.screenshot());
out("capture 1 (predictive deferred-empty) saved");

// ---- 2. structural family over EUR/USD 1h (honest empty: 80-bar M1 seed is
// insufficient for the 55-lookback structure indicators — the honest
// unavailable/insufficient empty state, not a fabricated list) ---------------
await page.getByTestId("signal-family-structural").click();
await page.waitForSelector('[data-testid="structural-signal-stream"]', { timeout: 20000 });
await page.waitForFunction(
  () => document.querySelector('[data-testid="structural-count-badge"]')?.textContent?.includes("EVENTS"),
  undefined,
  { timeout: 20000 },
);
const structuralState = await page.evaluate(() => ({
  framing: document.querySelector('[data-testid="structural-descriptive-framing"]')?.textContent,
  count: document.querySelector('[data-testid="structural-count-badge"]')?.textContent,
  provenance: document.querySelector('[data-testid="structural-provenance-line"]')?.textContent,
  firstEventLabel: document.querySelector('[data-testid^="structural-label-"]')?.textContent ?? null,
  firstEventDirection: document.querySelector('[data-testid^="structural-direction-"]')?.textContent ?? null,
  firstEventTime: document.querySelector('[data-testid="structural-signal-stream"] .signal-as-of')?.textContent ?? null,
}));
out(`structural (EUR/USD 1h): ${JSON.stringify(structuralState)}`);
fs.writeFileSync(`${OUT}/f02_structural.png`, await page.screenshot());
out("capture 2 (structural honest empty over seed-only series) saved");

// ---- 3. structural events over the REAL corpus (BTC/USD H1) ----------------
await page.getByTestId("watchlist-row-btc-usd").click();
await page.waitForTimeout(1200);
await page.waitForFunction(
  () => document.querySelector('[data-testid="structural-provenance-line"]')?.textContent?.includes("BTCUSD"),
  undefined,
  { timeout: 20000 },
);
const realState = await page.evaluate(() => ({
  count: document.querySelector('[data-testid="structural-count-badge"]')?.textContent,
  provenance: document.querySelector('[data-testid="structural-provenance-line"]')?.textContent,
  firstEventLabel: document.querySelector('[data-testid^="structural-label-"]')?.textContent ?? null,
  firstEventTime: document.querySelector('[data-testid="structural-signal-stream"] .signal-as-of')?.textContent ?? null,
}));
out(`structural (BTC/USD 1h, REAL corpus): ${JSON.stringify(realState)}`);
fs.writeFileSync(`${OUT}/f02_structural_real.png`, await page.screenshot());
out("capture 3 (structural events, real corpus) saved");

// ---- 4. honest empty state: EUR/USD + 1d (insufficient series) -------------
await page.getByTestId("watchlist-row-eur-usd").click();
await page.getByTestId("structural-tf-1d").click();
await page.waitForSelector('[data-testid="structural-empty-state"]', { timeout: 20000 });
const emptyText = await page.evaluate(
  () => document.querySelector('[data-testid="structural-empty-state"]')?.textContent,
);
out(`structural empty state: ${emptyText}`);
fs.writeFileSync(`${OUT}/f02_structural_empty.png`, await page.screenshot());
out("capture 4 (honest empty state) saved");

// ---- boundary scan ----------------------------------------------------------
const surfaceScan = await page.evaluate(() => {
  const surface = document.querySelector('[data-testid="structural-signal-stream"]');
  const text = (surface?.textContent ?? "").toLowerCase();
  const forbidden = ["buy", "sell", "order", "broker", "execution", "account"];
  return { violations: forbidden.filter((f) => text.includes(f)) };
});
out(`no-actuation scan (structural): ${JSON.stringify(surfaceScan)}`);

await browser.close();
fs.writeFileSync(`${OUT}/f02_capture_log.txt`, LINES.join("\n") + "\n");
out(`evidence written to ${OUT}`);
