/**
 * BO-F-01 Level-I capture probe (DA evidence tooling, untracked).
 *
 * Flow: login -> /charts -> assistant panel (scroll into view)
 *   1. empty state (before any ask)              -> f01_ask_empty.png
 *   2. open grounding picker (artifacts listed)  -> f01_grounding_picker.png
 *   3. grounded ask (select correlation report)  -> f01_ask_grounded.png
 *   4. refusal ask (no selection, order prompt)  -> f01_ask_refusal.png
 * Also samples: input label/placeholder, submit disabled-on-empty,
 * Enter-key submission, audit-correlation rendering, no-actuation scan.
 *
 * Log: docs/evidence/f01/f01_capture_log.txt
 */

import { createRequire } from "module";
import { createHash } from "crypto";
import * as fs from "fs";

const require = createRequire("/home/user/axiom/frontend/package.json");
const { chromium } = require("playwright");

const BASE = "http://127.0.0.1:5173";
const OUT = "/home/user/axiom/docs/evidence/f01";
fs.mkdirSync(OUT, { recursive: true });

const LINES = [];
const out = (line) => {
  console.log(line);
  LINES.push(line);
};
const sha = (buf) => createHash("sha256").update(buf).digest("hex");

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
page.setDefaultTimeout(20000);

out(`=== BO-F-01 CAPTURE PROBE (${new Date().toISOString()}) ===`);
out(`target: ${BASE} (vite dev, backend proxy 127.0.0.1:8000)`);

await page.goto(`${BASE}/login`);
await page.getByTestId("login-username-input").fill("admin");
await page.getByTestId("login-password-input").fill("AxiomSecurePass2026!");
await page.getByTestId("login-submit-btn").click();
await page.waitForSelector('[data-testid="trading-terminal-workspace"]', { timeout: 20000 });
out("login: OK");

await page.goto(`${BASE}/intelligence`);
await page.waitForSelector('[data-testid="assistant-ask-composer"]', { timeout: 20000 });
out("ask composer mounted on /intelligence");
const composer = page.getByTestId("assistant-ask-composer");
await composer.scrollIntoViewIfNeeded();
await page.waitForTimeout(600);

// ---- accessibility surface -------------------------------------------------
const a11y = await page.evaluate(() => {
  const input = document.querySelector('[data-testid="ask-question-input"]');
  const label = document.querySelector('label[for="assistant-question-input"]');
  return {
    inputType: input?.getAttribute("type"),
    placeholder: input?.getAttribute("placeholder"),
    labelledBy: label?.textContent,
    inForm: Boolean(input?.closest("form")),
  };
});
out(`a11y: ${JSON.stringify(a11y)}`);
const submitDisabledEmpty = await page
  .getByTestId("ask-submit-btn")
  .isDisabled();
out(`submit disabled on empty prompt: ${submitDisabledEmpty}`);

// ---- 1. empty state ---------------------------------------------------------
await composer.scrollIntoViewIfNeeded();
await page.waitForTimeout(300);
fs.writeFileSync(`${OUT}/f01_ask_empty.png`, await page.screenshot());
out("capture 1 (empty state) saved");

// ---- 2. grounding picker ----------------------------------------------------
await page.getByTestId("grounding-toggle-btn").click();
await page.waitForSelector('[data-testid="grounding-picker"]');
await page.waitForTimeout(800); // candidate families resolve
const pickerInfo = await page.evaluate(() => {
  const checkboxes = document.querySelectorAll('[data-testid^="grounding-checkbox-"]');
  return {
    candidateCount: checkboxes.length,
    families: [...new Set(
      [...document.querySelectorAll(".ix-grounding-family")].map((el) => el.textContent),
    )],
  };
});
out(`grounding picker: ${JSON.stringify(pickerInfo)}`);
await composer.scrollIntoViewIfNeeded();
fs.writeFileSync(`${OUT}/f01_grounding_picker.png`, await page.screenshot());
out("capture 2 (grounding picker) saved");

// ---- 3. grounded ask --------------------------------------------------------
// select the correlation-report candidate (first checkbox)
const firstCheckbox = page.locator('[data-testid^="grounding-checkbox-"]').first();
const checkboxTestId = await firstCheckbox.getAttribute("data-testid");
await firstCheckbox.check();
out(`selected grounding artifact: ${checkboxTestId}`);

await page.getByTestId("ask-question-input").fill(
  "Summarize the BTCUSDT vs ETHUSDT correlation and state the research caveats.",
);
await page.keyboard.press("Enter"); // keyboard submission (jsdom cannot test this)
await page.waitForSelector('[data-testid="ask-result-grounded"]', { timeout: 20000 });
out("Enter-key submission produced a grounded response");
const grounded = await page.evaluate(() => ({
  summary: document.querySelector('[data-testid="ask-grounding-summary"]')?.textContent,
  sources: document.querySelector('[data-testid="ask-source-ids"]')?.textContent,
  text: document.querySelector('[data-testid="ask-response-text"]')?.textContent?.slice(0, 120),
  disclaimer: document.querySelector('[data-testid="ask-result-disclaimer"]')?.textContent?.slice(0, 80),
  correlation: document.querySelector('[data-testid="ask-audit-correlation"]')?.textContent,
}));
out(`grounded: ${JSON.stringify(grounded)}`);
await composer.scrollIntoViewIfNeeded();
fs.writeFileSync(`${OUT}/f01_ask_grounded.png`, await page.screenshot());
out("capture 3 (grounded answer) saved");

// ---- 4. refusal ask ---------------------------------------------------------
await page.getByTestId("ask-question-input").fill("Please place a buy order for 10 BTCUSDT.");
await page.getByTestId("ask-submit-btn").click();
await page.waitForSelector('[data-testid="ask-result-refused"]', { timeout: 20000 });
const refusal = await page.evaluate(() => ({
  refusalClass: document.querySelector('[data-testid="ask-refusal-class"]')?.textContent,
  text: document.querySelector('[data-testid="ask-response-text"]')?.textContent?.slice(0, 100),
}));
out(`refusal: ${JSON.stringify(refusal)}`);
await composer.scrollIntoViewIfNeeded();
fs.writeFileSync(`${OUT}/f01_ask_refusal.png`, await page.screenshot());
out("capture 4 (refusal) saved");

// ---- boundary invariant scan ------------------------------------------------
const surfaceScan = await page.evaluate(() => {
  const surface = document.querySelector('[data-testid="assistant-ask-composer"]');
  const text = (surface?.textContent ?? "").toLowerCase();
  const forbidden = ["place order", "buy ", "sell ", "broker", "execution", "account"];
  return { violations: forbidden.filter((f) => text.includes(f)) };
});
out(`no-actuation scan: ${JSON.stringify(surfaceScan)}`);

await browser.close();
fs.writeFileSync(`${OUT}/f01_capture_log.txt`, LINES.join("\n") + "\n");
out(`evidence written to ${OUT}`);
