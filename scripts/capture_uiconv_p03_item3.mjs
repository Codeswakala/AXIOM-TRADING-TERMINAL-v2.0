import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import { execSync } from "child_process";

const EVIDENCE_DIR = "/home/user/axiom/docs/evidence/uiconv";
const LOG = [];

async function record(label, data) {
  LOG.push({ label, ...data });
  console.log(`[VERIFY] ${label}: ${JSON.stringify(data)}`);
}

async function login(page) {
  await page.goto("http://localhost:5173/login", { waitUntil: "networkidle" });
  await page.waitForTimeout(900);
  await page.locator('input[data-testid="login-username-input"], input#username-input').first().fill("admin");
  await page.locator('input[data-testid="login-password-input"], input#password-input').first().fill("AxiomSecurePass2026!");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2500);
}

async function run() {
  // ---------- CAPTURE 01: EMPTY STATE (artifact-free DB — no preferences seeded) ----------
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await login(page);

  await page.goto("http://localhost:5173/?open=settings", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(2500);
  const overlayVisible = await page.locator('[data-testid="workspace-settings-overlay"]').count();
  const emptyState = await page.locator('[data-testid="workspace-preferences-empty"]').count();
  const savedCards = await page.locator(".workspace-preference-card").count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM3_01_SETTINGS_EMPTY_STATE.png") });
  await record("01_SETTINGS_EMPTY_STATE", {
    url: page.url(),
    overlayVisible,
    emptyStateVerb: await page.locator('[data-testid="workspace-preferences-empty"]').textContent().catch(() => null),
    savedCards,
  });
  await browser.close();

  // ---------- SEED WORKSPACE PREFERENCES + PORTFOLIO ----------
  console.log("Seeding workspace preferences and portfolio data...");
  execSync("cd /home/user/axiom/backend && .venv/bin/python ../scripts/w7_u02_seed_workspace_preferences.py", { stdio: "inherit" });
  execSync("cd /home/user/axiom/backend && .venv/bin/python ../scripts/w7_u06_seed_portfolio_research.py", { stdio: "inherit" });

  // ---------- CAPTURE 02: POPULATED, SCROLLED TO PANEL BODY (OBS-CONV3-1 discipline) ----------
  const browser2 = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context2 = await browser2.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page2 = await context2.newPage();
  await login(page2);

  await page2.goto("http://localhost:5173/?open=settings", { waitUntil: "domcontentloaded" });
  await page2.waitForTimeout(3000);
  const cards = await page2.locator(".workspace-preference-card").count();
  const editor = await page2.locator('[data-testid="workspace-preference-editor"]').count();
  const createBtn = await page2.locator('[data-testid="workspace-pref-create-btn"]').count();
  const updateBtn = await page2.locator('[data-testid="workspace-pref-update-btn"]').count();
  const detail = await page2.locator('[data-testid="workspace-preference-detail"]').count();
  // Scroll the overlay body so the panel content below the fold is visually evidenced.
  await page2.locator(".ix-settings-body").evaluate((el) => { el.scrollTop = el.scrollHeight; });
  await page2.waitForTimeout(500);
  const bodyScroll = await page2.locator(".ix-settings-body").evaluate((el) => ({
    scrollTop: el.scrollTop,
    scrollHeight: el.scrollHeight,
    clientHeight: el.clientHeight,
  }));
  await page2.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM3_02_SETTINGS_POPULATED_SCROLLED.png") });
  await record("02_SETTINGS_POPULATED_SCROLLED", {
    url: page2.url(),
    savedCards: cards,
    editorVisible: editor,
    createButtonVisible: createBtn,
    updateButtonVisible: updateBtn,
    detailPanelVisible: detail,
    bodyScroll,
  });
  await browser2.close();

  // ---------- CAPTURE 03: /workspace LEGACY ROUTE REDIRECT ----------
  const browser3 = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context3 = await browser3.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page3 = await context3.newPage();
  await login(page3);

  await page3.goto("http://localhost:5173/workspace", { waitUntil: "domcontentloaded" });
  await page3.waitForTimeout(3000);
  const finalUrl = page3.url();
  const overlay3 = await page3.locator('[data-testid="workspace-settings-overlay"]').count();
  await page3.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM3_03_WORKSPACE_ROUTE_REDIRECT.png") });
  await record("03_WORKSPACE_ROUTE_REDIRECT", {
    url: finalUrl,
    settingsOverlayOpen: overlay3,
  });
  await browser3.close();

  fs.writeFileSync(path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM3_CAPTURE_VERIFICATION.json"), JSON.stringify(LOG, null, 2));
  console.log("ITEM3 CAPTURES COMPLETE");
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
