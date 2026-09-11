/**
 * BO-F-06 Level-I capture probe (DA evidence tooling, untracked).
 *
 * Flow: login -> terminal
 *   1. Rail legibility (midnight): semantic icons + visible labels
 *      -> f06_rail_midnight.png
 *   2. Rail in light + high-contrast themes (token-driven icon colors)
 *      -> f06_rail_light.png, f06_rail_highcontrast.png
 *   3. Dock legibility (expanded nav with icons + labels)
 *      -> f06_dock.png
 * Also samples: aria-labels retained, icon aria-hidden, label text values.
 *
 * Log: docs/evidence/f06/f06_capture_log.txt
 */

import { createRequire } from "module";
import * as fs from "fs";

const require = createRequire("/home/user/axiom/frontend/package.json");
const { chromium } = require("playwright");

const BASE = "http://127.0.0.1:5173";
const OUT = "/home/user/axiom/docs/evidence/f06";
fs.mkdirSync(OUT, { recursive: true });

const LINES = [];
const out = (line) => {
  console.log(line);
  LINES.push(line);
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
page.setDefaultTimeout(25000);

out(`=== BO-F-06 CAPTURE PROBE (${new Date().toISOString()}) ===`);
out(`target: ${BASE} (vite dev, backend proxy 127.0.0.1:8000)`);

await page.goto(`${BASE}/login`);
await page.getByTestId("login-username-input").fill("admin");
await page.getByTestId("login-password-input").fill("AxiomSecurePass2026!");
await page.getByTestId("login-submit-btn").click();
await page.waitForSelector('[data-testid="trading-terminal-workspace"]', { timeout: 20000 });
out("login: OK");

// ---- 1. rail legibility (midnight default) ----------------------------------
await page.waitForSelector('[data-testid="unified-module-rail"]', { timeout: 20000 });
const railState = await page.evaluate(() => {
  const buttons = [...document.querySelectorAll(".rail-button")];
  return {
    count: buttons.length,
    withSvg: buttons.filter((b) => b.querySelector("svg.workspace-icon")).length,
    withVisibleLabel: buttons.filter((b) => b.querySelector(".rail-label")).length,
    labels: [...document.querySelectorAll(".rail-label")].map((l) => l.textContent?.trim()),
    ariaLabeled: buttons.filter((b) => b.getAttribute("aria-label")).length,
    iconAriaHidden: [...document.querySelectorAll(".workspace-icon")].filter(
      (svg) => svg.getAttribute("aria-hidden") === "true",
    ).length,
  };
});
out(`rail (midnight): ${JSON.stringify(railState)}`);
fs.writeFileSync(`${OUT}/f06_rail_midnight.png`, await page.screenshot());
out("capture 1 (rail midnight) saved");

// ---- 2. rail across themes (token-driven icon colors) -----------------------
for (const theme of ["light", "high-contrast"]) {
  const toggle = page.getByTestId("shell-theme-toggle-btn");
  let current = await toggle.getAttribute("data-theme-id");
  for (let i = 0; i < 6 && current !== theme; i++) {
    await toggle.click();
    await page.waitForTimeout(150);
    current = await toggle.getAttribute("data-theme-id");
  }
  out(`theme now: ${await toggle.getAttribute("data-theme-id")}`);
  const themeState = await page.evaluate(() => ({
    railBg: getComputedStyle(document.querySelector(".unified-module-rail")).backgroundColor,
    iconStroke: (() => {
      const svg = document.querySelector("svg.workspace-icon");
      return svg ? getComputedStyle(svg).color : null;
    })(),
  }));
  out(`rail (${theme}): ${JSON.stringify(themeState)}`);
  fs.writeFileSync(`${OUT}/f06_rail_${theme.replace("-", "")}.png`, await page.screenshot());
  out(`capture (rail ${theme}) saved`);
}

// ---- 3. dock legibility -----------------------------------------------------
const dock = page.locator("[data-workspace-id]").first();
await dock.scrollIntoViewIfNeeded();
const dockState = await page.evaluate(() => {
  const links = [...document.querySelectorAll(".ix-nav-link")].slice(0, 4);
  return links.map((link) => ({
    icon: Boolean(link.querySelector("svg.workspace-icon")),
    label: link.querySelector(".ix-nav-copy span")?.textContent,
  }));
});
out(`dock: ${JSON.stringify(dockState)}`);
fs.writeFileSync(`${OUT}/f06_dock.png`, await page.screenshot());
out("capture 4 (dock) saved");

await browser.close();
fs.writeFileSync(`${OUT}/f06_capture_log.txt`, LINES.join("\n") + "\n");
out(`evidence written to ${OUT}`);
