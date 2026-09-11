/**
 * BO-F-03 Level-I capture probe (DA evidence tooling, untracked).
 *
 * Flow: login -> terminal -> INTELLIGENCE dock
 *   1. Generation surface (window resolved over REAL BTCUSD H1) -> f03_generation_surface.png
 *   2. Generate SCENARIO via the UI -> persisted + re-read -> f03_scenario_card.png
 *   3. Generate PORTFOLIO-RISK via the UI -> persisted -> f03_portfolio_card.png
 *   4. Generate CORRELATION via the UI (BTCUSD x ETHUSD real pair) -> f03_correlation_card.png
 *   5. Generate SIGNAL-VALIDATION (no advisory signals) -> honest structured
 *      422 insufficient-data notice -> f03_insufficient.png
 * Also samples: five tabs, framing lines, no-actuation scan.
 *
 * Log: docs/evidence/f03/f03_capture_log.txt
 */

import { createRequire } from "module";
import * as fs from "fs";

const require = createRequire("/home/user/axiom/frontend/package.json");
const { chromium } = require("playwright");

const BASE = "http://127.0.0.1:5173";
const OUT = "/home/user/axiom/docs/evidence/f03";
fs.mkdirSync(OUT, { recursive: true });

const LINES = [];
const out = (line) => {
  console.log(line);
  LINES.push(line);
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
page.setDefaultTimeout(25000);

out(`=== BO-F-03 CAPTURE PROBE (${new Date().toISOString()}) ===`);
out(`target: ${BASE} (vite dev, backend proxy 127.0.0.1:8000)`);

await page.goto(`${BASE}/login`);
await page.getByTestId("login-username-input").fill("admin");
await page.getByTestId("login-password-input").fill("AxiomSecurePass2026!");
await page.getByTestId("login-submit-btn").click();
await page.waitForSelector('[data-testid="trading-terminal-workspace"]', { timeout: 20000 });
out("login: OK");

// Select BTC/USD first (the real-corpus series exists under BTCUSD H1).
await page.getByTestId("watchlist-row-btc-usd").click();
await page.waitForTimeout(800);
out("watchlist: BTC/USD selected");

// Right dock: switch to the INTELLIGENCE tab.
await page.getByTestId("right-dock-tab-intelligence").click();
await page.waitForSelector('[data-testid="terminal-intelligence-cards"]', { timeout: 20000 });
out("intelligence cards mounted");

// ---- 1. generation surface with the real-data window ------------------------
await page.waitForSelector('[data-testid="generation-window-note"]', { timeout: 25000 });
const genSurface = await page.evaluate(() => ({
  framing: document.querySelector('[data-testid="generation-framing"]')?.textContent,
  window: document.querySelector('[data-testid="generation-window-note"]')?.textContent,
  buttons: [...document.querySelectorAll('[data-testid^="gen-btn-"]')].map((el) => ({
    id: el.getAttribute("data-testid"),
    disabled: el.disabled,
  })),
}));
out(`generation surface: ${JSON.stringify(genSurface)}`);
fs.writeFileSync(`${OUT}/f03_generation_surface.png`, await page.screenshot());
out("capture 1 (generation surface) saved");

// ---- 2. SCENARIO generation (UI-driven, real data) --------------------------
await page.getByTestId("gen-btn-scenario").click();
await page.waitForSelector('[data-testid="gen-status-scenario"]', { timeout: 25000 });
out(`scenario status: ${await page.getByTestId("gen-status-scenario").textContent()}`);
await page.getByTestId("intel-tab-scenario").click();
await page.waitForSelector('[data-testid="intel-scenario-panel"]', { timeout: 20000 });
await page.waitForSelector('[data-testid="scenario-name"]', { timeout: 20000 });
const scenarioCard = await page.evaluate(() => ({
  name: document.querySelector('[data-testid="scenario-name"]')?.textContent,
  ret: document.querySelector('[data-testid="scenario-return"]')?.textContent,
  dataClass: document.querySelector('[data-testid="scenario-data-class"]')?.textContent,
  framing: document.querySelector('[data-testid="scenario-framing"]')?.textContent,
}));
out(`scenario card: ${JSON.stringify(scenarioCard)}`);
fs.writeFileSync(`${OUT}/f03_scenario_card.png`, await page.screenshot());
out("capture 2 (scenario card, real data) saved");

// ---- 3. PORTFOLIO-RISK generation -------------------------------------------
await page.getByTestId("gen-btn-portfolio-risk").click();
await page.waitForSelector('[data-testid="gen-status-portfolio-risk"]', { timeout: 25000 });
out(`portfolio-risk status: ${await page.getByTestId("gen-status-portfolio-risk").textContent()}`);
await page.getByTestId("intel-tab-portfolio-risk").click();
await page.waitForSelector('[data-testid="intel-portfolio-risk-panel"]', { timeout: 20000 });
await page.waitForSelector('[data-testid="portrisk-drawdown"]', { timeout: 20000 });
const portCard = await page.evaluate(() => ({
  drawdown: document.querySelector('[data-testid="portrisk-drawdown"]')?.textContent,
  vol: document.querySelector('[data-testid="portrisk-vol"]')?.textContent,
  stress: document.querySelector('[data-testid="portrisk-stress"]')?.textContent,
  dataClass: document.querySelector('[data-testid="portrisk-data-class"]')?.textContent,
}));
out(`portfolio-risk card: ${JSON.stringify(portCard)}`);
fs.writeFileSync(`${OUT}/f03_portfolio_card.png`, await page.screenshot());
out("capture 3 (portfolio-risk card, real data) saved");

// ---- 4. CORRELATION generation (BTCUSD x ETHUSD, real pair) ------------------
await page.getByTestId("gen-btn-correlation").click();
await page.waitForSelector('[data-testid="gen-status-correlation"]', { timeout: 25000 });
out(`correlation status: ${await page.getByTestId("gen-status-correlation").textContent()}`);
await page.getByTestId("intel-tab-correlation").click();
await page.waitForSelector('[data-testid^="corr-row-"]', { timeout: 20000 });
const corrCard = await page.evaluate(() => ({
  pair: document.querySelector(".corr-pair")?.textContent,
  r: document.querySelector(".corr-r")?.textContent,
  ci: document.querySelector(".corr-unc")?.textContent,
  dataClass: document.querySelector('[data-testid^="corr-data-class-"]')?.textContent,
}));
out(`correlation card: ${JSON.stringify(corrCard)}`);
fs.writeFileSync(`${OUT}/f03_correlation_card.png`, await page.screenshot());
out("capture 4 (correlation card, real pair) saved");

// ---- 5. SIGNAL-VALIDATION -> honest structured 422 --------------------------
await page.getByTestId("gen-btn-signal-validation").click();
await page.waitForSelector('[data-testid="gen-insufficient-signal-validation"]', { timeout: 25000 });
const insufficient = await page.evaluate(
  () => document.querySelector('[data-testid="gen-insufficient-signal-validation"]')?.textContent,
);
out(`insufficient-data notice: ${insufficient}`);
fs.writeFileSync(`${OUT}/f03_insufficient.png`, await page.screenshot());
out("capture 5 (insufficient-data notice) saved");

// ---- boundary scan -----------------------------------------------------------
const surfaceScan = await page.evaluate(() => {
  const surface = document.querySelector('[data-testid="terminal-intelligence-cards"]');
  const text = (surface?.textContent ?? "").toLowerCase();
  const forbidden = ["buy", "sell", "order", "broker", "execution", "account"];
  return { violations: forbidden.filter((f) => text.includes(f)) };
});
out(`no-actuation scan: ${JSON.stringify(surfaceScan)}`);

await browser.close();
fs.writeFileSync(`${OUT}/f03_capture_log.txt`, LINES.join("\n") + "\n");
out(`evidence written to ${OUT}`);
