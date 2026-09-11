/**
 * BO-F-05 Level-I capture probe (DA evidence tooling, untracked).
 *
 * Flow: login -> terminal
 *   1. INTELLIGENCE dock -> CORRELATION tab -> Lineage toggle ->
 *      lineage evidence panel over the REAL persisted report
 *      -> f05_lineage_report.png
 *   2. SIGNALS dock -> expand the seeded signal -> Model Lineage & Audit
 *      section (report ids + audit correlation, no fabricated fallbacks)
 *      -> f05_signal_lineage.png
 *   3. Alerts detail record -> audit-correlation row (need an alert; the
 *      alert line is covered by f04 capture; here we capture the detail
 *      record row when an alert exists) -> f05_alert_lineage.png
 * Also samples: read-only (no controls inside the lineage panel),
 * honest "provenance not recorded" rendering where a field is absent.
 *
 * Log: docs/evidence/f05/f05_capture_log.txt
 */

import { createRequire } from "module";
import * as fs from "fs";

const require = createRequire("/home/user/axiom/frontend/package.json");
const { chromium } = require("playwright");

const BASE = "http://127.0.0.1:5173";
const OUT = "/home/user/axiom/docs/evidence/f05";
fs.mkdirSync(OUT, { recursive: true });

const LINES = [];
const out = (line) => {
  console.log(line);
  LINES.push(line);
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
page.setDefaultTimeout(25000);

out(`=== BO-F-05 CAPTURE PROBE (${new Date().toISOString()}) ===`);
out(`target: ${BASE} (vite dev, backend proxy 127.0.0.1:8000)`);

await page.goto(`${BASE}/login`);
await page.getByTestId("login-username-input").fill("admin");
await page.getByTestId("login-password-input").fill("AxiomSecurePass2026!");
await page.getByTestId("login-submit-btn").click();
await page.waitForSelector('[data-testid="trading-terminal-workspace"]', { timeout: 20000 });
out("login: OK");

// ---- 1. intelligence report lineage ----------------------------------------
await page.getByTestId("right-dock-tab-intelligence").click();
await page.waitForSelector('[data-testid="terminal-intelligence-cards"]', { timeout: 20000 });
await page.getByTestId("intel-tab-correlation").click();
await page.waitForSelector('[data-testid^="lineage-toggle-"]', { timeout: 25000 });
const toggle = page.locator('[data-testid^="lineage-toggle-"]').first();
out(`lineage toggle found: ${await toggle.getAttribute("data-testid")}`);
await toggle.click();
await page.waitForSelector('[data-testid="lineage-evidence-panel"]', { timeout: 25000 });
const reportLineage = await page.evaluate(() => ({
  hash: document.querySelector('[data-testid="lineage-report-hash"]')?.textContent,
  audit: document.querySelector('[data-testid="lineage-audit-correlation"]')?.textContent,
  rootNodes: [...document.querySelectorAll(".ix-node-label")].map((el) => el.textContent),
  fabricatedChainAbsent:
    !document.body.textContent.includes("Market Data Series") &&
    !document.body.textContent.includes("Grounded Model Registry"),
  panelControls: document.querySelectorAll('[data-testid="lineage-evidence-panel"] button').length,
}));
out(`report lineage: ${JSON.stringify(reportLineage)}`);
fs.writeFileSync(`${OUT}/f05_lineage_report.png`, await page.screenshot());
out("capture 1 (report lineage panel, real report) saved");

// ---- 2. signal lineage ------------------------------------------------------
await page.getByTestId("right-dock-tab-signals").click();
await page.waitForSelector('[data-testid^="signal-card-"]', { timeout: 25000 });
const signalCard = page.locator('[data-testid^="signal-card-"]').first();
await signalCard.click();
await page.waitForSelector('[data-testid^="signal-detail-lineage-"]', { timeout: 25000 });
const signalLineage = await page.evaluate(() => {
  const section = document.querySelector('[data-testid^="signal-detail-lineage-"]');
  const text = section?.textContent ?? "";
  return {
    hasExperimentId: text.includes("exp-f05-lineage"),
    // the UI renders the audit id truncated to 16 chars + ellipsis
    hasAuditCorrelation: text.includes("f05-signal-audit"),
    fabricatedFallbackAbsent: !text.includes("exp-001"),
    honestNotRecordedRendered: text.includes("not recorded"), // e.g. statistical report absent
  };
});
out(`signal lineage: ${JSON.stringify(signalLineage)}`);
fs.writeFileSync(`${OUT}/f05_signal_lineage.png`, await page.screenshot());
out("capture 2 (signal lineage section) saved");

// ---- 3. alerts detail audit-correlation (if an alert exists) ---------------
await page.getByTestId("right-dock-tab-alerts").click();
await page.waitForSelector('[data-testid="monitoring-alerts-panel"]', { timeout: 20000 });
const hasAlerts = (await page.locator('[data-testid^="alert-detail-open-"]').count()) > 0;
if (hasAlerts) {
  await page.locator('[data-testid^="alert-detail-open-"]').first().click();
  await page.waitForSelector('[data-testid="alerts-detail-record"]', { timeout: 25000 });
  const alertLineage = await page.evaluate(() => ({
    auditRow: document.querySelector('[data-testid="alerts-detail-audit"]')?.textContent,
  }));
  out(`alert detail audit row: ${JSON.stringify(alertLineage)}`);
  fs.writeFileSync(`${OUT}/f05_alert_lineage.png`, await page.screenshot());
  out("capture 3 (alert detail audit row) saved");
} else {
  const cardAudit = await page.evaluate(() => {
    const lines = [...document.querySelectorAll('[data-testid^="alert-audit-"]')];
    return lines.map((el) => el.textContent);
  });
  out(`no alerts seeded this session; card audit lines: ${JSON.stringify(cardAudit)}`);
}

await browser.close();
fs.writeFileSync(`${OUT}/f05_capture_log.txt`, LINES.join("\n") + "\n");
out(`evidence written to ${OUT}`);
