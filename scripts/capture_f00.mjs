/**
 * BO-F-00 Level-I capture probe (DA evidence tooling, untracked).
 *
 * Evidence produced:
 *  - Wave login: two motion frames (t0, t0+700ms — must DIFFER: animation runs)
 *    and two reduced-motion frames (t0, t0+700ms — must be IDENTICAL: frozen).
 *  - Six theme screenshots of the operations surface with the applied
 *    `.ix-shell.theme-*` class and the computed --ix-bg-root token sampled.
 *  - Theme persistence probe: set Slate via the header toggle → debounced
 *    server persist → reload (restore path) → full sign-out/sign-in
 *    (re-login restore path) — the theme must survive both.
 *  - Favicon wired: link[rel=icon] present + /branding/axiom-logo.png → 200.
 *  - Landing <h1> present on "/".
 *
 * Log: docs/evidence/f00/f00_capture_log.txt
 * Images: docs/evidence/f00/f00_*.png
 */

import { createRequire } from "module";
import { createHash } from "crypto";
import * as fs from "fs";

// Resolve playwright from the frontend's node_modules regardless of where
// this script runs (the DA tooling scripts live outside the frontend tree).
const require = createRequire("/home/user/axiom/frontend/package.json");
const { chromium } = require("playwright");

const BASE = "http://127.0.0.1:5173";
const OUT = new URL("../docs/evidence/f00/", import.meta.url).pathname;
fs.mkdirSync(OUT, { recursive: true });

const LINES = [];
const out = (line) => {
  console.log(line);
  LINES.push(line);
};
const sha = (buf) => createHash("sha256").update(buf).digest("hex");

const THEME_ORDER = ["midnight", "light", "slate", "teal", "amber", "high-contrast"];

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
page.setDefaultTimeout(15000);

out(`=== BO-F-00 CAPTURE PROBE (${new Date().toISOString()}) ===`);
out(`target: ${BASE} (vite dev, backend proxy 127.0.0.1:8000)`);

// ---- 1. Wave login: motion frames -----------------------------------------
await page.goto(`${BASE}/login`);
await page.waitForSelector('[data-testid="login-decorative-scene"]');
await page.waitForTimeout(900);
const chips = await page.getByTestId("login-governance-chips").textContent();
out(`login governance chips: ${chips}`);
const wave = await page.evaluate(() => ({
  candles: document.querySelectorAll(".deco-candle.wave-candle").length,
  particles: document.querySelectorAll(".login-particle").length,
  glow: Boolean(document.querySelector('[data-testid="login-glow-pulse"]')),
  sceneText: document.querySelector('[data-testid="login-decorative-scene"]').textContent.trim(),
}));
out(`wave composition: ${JSON.stringify(wave)}`);
const motion1 = await page.screenshot();
await page.waitForTimeout(700);
const motion2 = await page.screenshot();
fs.writeFileSync(`${OUT}f00_login_wave_t1.png`, motion1);
fs.writeFileSync(`${OUT}f00_login_wave_t2.png`, motion2);
out(`motion frames: t1 sha256=${sha(motion1)} t2 sha256=${sha(motion2)} differ=${sha(motion1) !== sha(motion2)}`);

// ---- 2. Wave login: reduced-motion freeze ---------------------------------
await page.emulateMedia({ reducedMotion: "reduce" });
await page.waitForTimeout(500);
const frozen1 = await page.screenshot();
await page.waitForTimeout(700);
const frozen2 = await page.screenshot();
fs.writeFileSync(`${OUT}f00_login_frozen_t1.png`, frozen1);
fs.writeFileSync(`${OUT}f00_login_frozen_t2.png`, frozen2);
out(`frozen frames: t1 sha256=${sha(frozen1)} t2 sha256=${sha(frozen2)} identical=${sha(frozen1) === sha(frozen2)}`);
await page.emulateMedia({ reducedMotion: null });

// ---- 3. Login --------------------------------------------------------------
await page.getByTestId("login-username-input").fill("admin");
await page.getByTestId("login-password-input").fill("AxiomSecurePass2026!");
await page.getByTestId("login-submit-btn").click();
await page.waitForSelector('[data-testid="trading-terminal-workspace"]', { timeout: 20000 });
await page.waitForTimeout(2500);
out("login: OK — operations surface mounted");

// ---- 4. Landing h1 + favicon ----------------------------------------------
const h1 = await page.evaluate(() => {
  const el = document.querySelector("h1");
  return el ? { text: el.textContent.trim(), testid: el.getAttribute("data-testid") } : null;
});
out(`landing h1: ${JSON.stringify(h1)}`);
const favicon = await page.evaluate(async () => {
  const link = document.querySelector('link[rel="icon"]');
  if (!link) return { link: null };
  const status = await fetch(link.getAttribute("href")).then((r) => r.status);
  return { href: link.getAttribute("href"), status };
});
out(`favicon: ${JSON.stringify(favicon)}`);

// ---- 5. Six-theme walk -----------------------------------------------------
const toggle = page.getByTestId("shell-theme-toggle-btn");
for (let i = 0; i < THEME_ORDER.length; i++) {
  if (i > 0) await toggle.click();
  await page.waitForTimeout(350);
  const state = await page.evaluate(() => {
    const shell = document.querySelector(".ix-shell");
    const btn = document.querySelector('[data-testid="shell-theme-toggle-btn"]');
    return {
      themeId: btn?.getAttribute("data-theme-id"),
      shellClass: shell?.className,
      bgRoot: shell ? getComputedStyle(shell).getPropertyValue("--ix-bg-root").trim() : null,
    };
  });
  const shot = await page.screenshot();
  fs.writeFileSync(`${OUT}f00_theme_${THEME_ORDER[i].replace("-", "")}_home.png`, shot);
  out(`theme ${THEME_ORDER[i]}: data-theme-id=${state.themeId} bg-root-token="${state.bgRoot}" class-ok=${state.shellClass.includes(`theme-${THEME_ORDER[i]}`)}`);
  await page.waitForTimeout(200);
}

// ---- 6. Persistence probe: set Slate -> reload -> re-login -----------------
const target = "slate";
let current = await page.getByTestId("shell-theme-toggle-btn").getAttribute("data-theme-id");
for (let i = 0; i < 6 && current !== target; i++) {
  await toggle.click();
  await page.waitForTimeout(250);
  current = await page.getByTestId("shell-theme-toggle-btn").getAttribute("data-theme-id");
}
out(`persistence target theme: ${current}`);
await page.waitForTimeout(1600); // debounce (250ms) + server write
await page.reload();
await page.waitForSelector('[data-testid="trading-terminal-workspace"]', { timeout: 20000 });
await page.waitForTimeout(2500);
const afterReload = await page.getByTestId("shell-theme-toggle-btn").getAttribute("data-theme-id");
out(`after reload (same session, restore path): theme=${afterReload} restored=${afterReload === target}`);
await page.getByTestId("shell-signout-btn").click();
await page.waitForSelector('[data-testid="login-page-container"]');
await page.getByTestId("login-username-input").fill("admin");
await page.getByTestId("login-password-input").fill("AxiomSecurePass2026!");
await page.getByTestId("login-submit-btn").click();
await page.waitForSelector('[data-testid="trading-terminal-workspace"]', { timeout: 20000 });
await page.waitForTimeout(2500);
const afterRelogin = await page.getByTestId("shell-theme-toggle-btn").getAttribute("data-theme-id");
const shot = await page.screenshot();
fs.writeFileSync(`${OUT}f00_persistence_relogin.png`, shot);
out(`after full re-login: theme=${afterRelogin} restored=${afterRelogin === target}`);

await browser.close();
fs.writeFileSync(`${OUT}f00_capture_log.txt`, LINES.join("\n") + "\n");
out(`evidence written to ${OUT}`);
