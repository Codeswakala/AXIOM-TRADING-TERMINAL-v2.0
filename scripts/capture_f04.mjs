/**
 * BO-F-04 Level-I capture probe (DA evidence tooling, untracked).
 *
 * Flow: login -> terminal -> ALERTS dock
 *   1. ALL domain (4 seeded alerts across the four concrete domains)
 *      -> f04_all_domains.png
 *   2. MARKET filter (LIVE_DATA_STALE)  -> f04_market_filter.png
 *   3. RISK filter (DRIFT_DETECTED)     -> f04_risk_filter.png
 *   4. RESEARCH filter (honest empty)   -> f04_research_empty.png
 *   5. Ack state (read-state-only)      -> f04_ack_state.png
 * Also samples: domain chips, absolute-UTC timestamps, lineage lines,
 * no-actuation scan.
 *
 * Log: docs/evidence/f04/f04_capture_log.txt
 */

import { createRequire } from "module";
import * as fs from "fs";

const require = createRequire("/home/user/axiom/frontend/package.json");
const { chromium } = require("playwright");

const BASE = "http://127.0.0.1:5173";
const OUT = "/home/user/axiom/docs/evidence/f04";
fs.mkdirSync(OUT, { recursive: true });

const LINES = [];
const out = (line) => {
  console.log(line);
  LINES.push(line);
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
page.setDefaultTimeout(25000);

out(`=== BO-F-04 CAPTURE PROBE (${new Date().toISOString()}) ===`);
out(`target: ${BASE} (vite dev, backend proxy 127.0.0.1:8000)`);

await page.goto(`${BASE}/login`);
await page.getByTestId("login-username-input").fill("admin");
await page.getByTestId("login-password-input").fill("AxiomSecurePass2026!");
await page.getByTestId("login-submit-btn").click();
await page.waitForSelector('[data-testid="trading-terminal-workspace"]', { timeout: 20000 });
out("login: OK");

await page.getByTestId("right-dock-tab-alerts").click();
await page.waitForSelector('[data-testid="monitoring-alerts-panel"]', { timeout: 20000 });
await page.waitForSelector('[data-testid="alerts-domain-count"]', { timeout: 25000 });
out("alerts dock mounted");

// ---- 1. ALL domains ---------------------------------------------------------
await page.waitForFunction(
  () => document.querySelectorAll('[data-testid^="alert-item-"]').length >= 4,
  undefined,
  { timeout: 25000 },
);
const allState = await page.evaluate(() => ({
  count: document.querySelector('[data-testid="alerts-domain-count"]')?.textContent,
  items: [...document.querySelectorAll('[data-testid^="alert-item-"]')].map((el) => {
    const id = el.getAttribute("data-testid");
    return {
      id,
      domain: el.querySelector('[data-testid^="alert-domain-"]')?.getAttribute("data-domain"),
      created: el.querySelector('[data-testid^="alert-created-"]')?.textContent,
      lineage: el.querySelector('[data-testid^="alert-lineage-"]')?.textContent,
    };
  }),
}));
out(`ALL: ${JSON.stringify(allState)}`);
fs.writeFileSync(`${OUT}/f04_all_domains.png`, await page.screenshot());
out("capture 1 (all domains) saved");

// ---- 2. MARKET filter -------------------------------------------------------
await page.getByTestId("alerts-domain-market").click();
await page.waitForFunction(
  () => document.querySelectorAll('[data-testid^="alert-item-"]').length === 1,
  undefined,
  { timeout: 25000 },
);
const marketState = await page.evaluate(() => ({
  count: document.querySelector('[data-testid="alerts-domain-count"]')?.textContent,
  type: document.querySelector('.check-name')?.textContent,
  domain: document.querySelector('[data-testid^="alert-domain-"]')?.getAttribute("data-domain"),
}));
out(`MARKET filter: ${JSON.stringify(marketState)}`);
fs.writeFileSync(`${OUT}/f04_market_filter.png`, await page.screenshot());
out("capture 2 (market filter) saved");

// ---- 3. RISK filter ---------------------------------------------------------
await page.getByTestId("alerts-domain-risk").click();
await page.waitForFunction(
  () => document.querySelector(".check-name")?.textContent === "DRIFT_DETECTED",
  undefined,
  { timeout: 25000 },
);
const riskState = await page.evaluate(() => ({
  count: document.querySelector('[data-testid="alerts-domain-count"]')?.textContent,
  type: document.querySelector(".check-name")?.textContent,
  domain: document.querySelector('[data-testid^="alert-domain-"]')?.getAttribute("data-domain"),
}));
out(`RISK filter: ${JSON.stringify(riskState)}`);
fs.writeFileSync(`${OUT}/f04_risk_filter.png`, await page.screenshot());
out("capture 3 (risk filter) saved");

// ---- 4. RESEARCH filter (honest empty) --------------------------------------
await page.getByTestId("alerts-domain-research").click();
await page.waitForSelector('[data-testid="alerts-domain-empty"]', { timeout: 25000 });
const researchEmpty = await page.evaluate(
  () => document.querySelector('[data-testid="alerts-domain-empty"]')?.textContent,
);
out(`RESEARCH filter empty: ${researchEmpty}`);
fs.writeFileSync(`${OUT}/f04_research_empty.png`, await page.screenshot());
out("capture 4 (research honest empty) saved");

// ---- 5. Ack read-state-only -------------------------------------------------
await page.getByTestId("alerts-domain-all").click();
await page.waitForFunction(
  () => document.querySelectorAll('[data-testid^="alert-item-"]').length >= 4,
  undefined,
  { timeout: 25000 },
);
const beforeAck = await page.evaluate(() => ({
  ackButtons: document.querySelectorAll('[data-testid^="alert-ack-"]').length,
  ackedText: [...document.querySelectorAll(".alert-evidence")].filter((el) =>
    el.textContent?.includes("Ack: yes"),
  ).length,
}));
out(`before ack: ${JSON.stringify(beforeAck)}`);
const firstAck = page.locator('[data-testid^="alert-ack-"]').first();
await firstAck.click();
await page.waitForFunction(
  () => document.querySelectorAll('[data-testid^="alert-ack-"]').length === 3,
  undefined,
  { timeout: 25000 },
);
const afterAck = await page.evaluate(() => ({
  ackButtons: document.querySelectorAll('[data-testid^="alert-ack-"]').length,
  ackedText: [...document.querySelectorAll(".alert-evidence")].filter((el) =>
    el.textContent?.includes("Ack: yes"),
  ).length,
  detailOpen: document.querySelectorAll('[data-testid^="alert-detail-open-"]').length,
}));
out(`after ack: ${JSON.stringify(afterAck)}`);
fs.writeFileSync(`${OUT}/f04_ack_state.png`, await page.screenshot());
out("capture 5 (ack state) saved");

// ---- boundary scan -----------------------------------------------------------
// Button-label scan only (the disclaimer itself contains the NEGATED word
// "remediate" — "they do not retrain, remediate, or act" — which is the
// constitutional boundary text, not a control). Mirrors the unit-test scan.
const surfaceScan = await page.evaluate(() => {
  const labels = [...document.querySelectorAll('[data-testid="monitoring-alerts-panel"] button')]
    .map((el) => (el.textContent ?? "").toLowerCase())
    .join(" ");
  const forbidden = ["buy", "sell", "order", "broker", "execution", "account", "remediate"];
  return { violations: forbidden.filter((f) => labels.includes(f)) };
});
out(`no-actuation scan: ${JSON.stringify(surfaceScan)}`);

await browser.close();
fs.writeFileSync(`${OUT}/f04_capture_log.txt`, LINES.join("\n") + "\n");
out(`evidence written to ${OUT}`);
