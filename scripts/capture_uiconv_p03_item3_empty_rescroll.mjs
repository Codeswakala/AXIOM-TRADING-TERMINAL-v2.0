import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";

const EVIDENCE_DIR = "/home/user/axiom/docs/evidence/uiconv";

async function run() {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await context.newPage();

  await page.goto("http://localhost:5173/login", { waitUntil: "networkidle" });
  await page.waitForTimeout(900);
  await page.locator('input[data-testid="login-username-input"], input#username-input').first().fill("admin");
  await page.locator('input[data-testid="login-password-input"], input#password-input').first().fill("AxiomSecurePass2026!");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2500);

  // OBS-CONV3-5 correction: empty state must be VISIBLE in frame — scroll the
  // overlay body so the SAVED PREFERENCES region with the line-171 sentence is shown.
  await page.goto("http://localhost:5173/?open=settings", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(2500);

  const emptySentence = await page.locator('[data-testid="workspace-preferences-empty"]').textContent().catch(() => null);
  const savedCards = await page.locator(".workspace-preference-card").count();

  // Scroll the settings body to the bottom so the Saved Preferences region is in frame.
  await page.locator(".ix-settings-body").evaluate((el) => { el.scrollTop = el.scrollHeight; });
  await page.waitForTimeout(600);
  const bodyScroll = await page.locator(".ix-settings-body").evaluate((el) => ({
    scrollTop: el.scrollTop,
    scrollHeight: el.scrollHeight,
    clientHeight: el.clientHeight,
  }));
  // Confirm the empty-state sentence is within the visible viewport after scrolling.
  const sentenceVisible = await page.locator('[data-testid="workspace-preferences-empty"]').evaluate((el) => {
    const r = el.getBoundingClientRect();
    return r.top >= 0 && r.bottom <= (window.innerHeight || 1080);
  }).catch(() => false);

  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM3_01_SETTINGS_EMPTY_STATE.png") });
  console.log(JSON.stringify({ emptySentence, savedCards, bodyScroll, sentenceVisibleInViewport: sentenceVisible }, null, 2));

  await browser.close();
  console.log("EMPTY RE-CAPTURE COMPLETE");
}

run().catch((err) => { console.error(err); process.exit(1); });
