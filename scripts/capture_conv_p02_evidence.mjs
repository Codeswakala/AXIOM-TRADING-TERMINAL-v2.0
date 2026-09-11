import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";

const EVIDENCE_DIR = "/home/user/axiom/docs/evidence/uiconv";

if (!fs.existsSync(EVIDENCE_DIR)) {
  fs.mkdirSync(EVIDENCE_DIR, { recursive: true });
}

async function run() {
  const browser = await chromium.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  // Context 1: Standard viewport 1920x1080
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });

  const page = await context.newPage();

  // Step 1: Log in with operator credentials
  console.log("Step 1: Logging in with valid operator credentials...");
  await page.goto("http://localhost:5173/login", { waitUntil: "networkidle" });
  await page.waitForTimeout(1000);

  const userField = page.locator('input[data-testid="login-username-input"], input#username-input').first();
  const passField = page.locator('input[data-testid="login-password-input"], input#password-input').first();
  await userField.fill("admin");
  await passField.fill("AxiomSecurePass2026!");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2000);

  // Navigate to Terminal Root (/)
  console.log("Navigating to Terminal Root (/)...");
  await page.goto("http://localhost:5173/", { waitUntil: "networkidle" });
  await page.waitForTimeout(1500);

  // Ensure theme is dark
  const themeBtn = page.locator('[data-testid="shell-theme-toggle-btn"]').first();
  const themeText = await themeBtn.textContent();
  if (themeText && themeText.includes("Dark theme")) {
    await themeBtn.click();
    await page.waitForTimeout(500);
  }

  // Seed chart history for EUR/USD
  const seedBtn = page.locator('[data-testid="chart-seed-btn"]').first();
  if (await seedBtn.isVisible()) {
    await seedBtn.click();
    await page.waitForTimeout(1500);
  }

  // -------------------------------------------------------------
  // Capture 1: UI-CONV-P02_01_TERMINAL_SIGNALS_DRILLDOWN.png
  // Terminal with SIGNALS dock showing signal detail drill-down
  // -------------------------------------------------------------
  console.log("Capture 1: Terminal Signals Dock with Expanded Drill-Down...");
  const signalsTab = page.locator('[data-testid="right-dock-tab-signals"]').first();
  if (await signalsTab.isVisible()) {
    await signalsTab.click();
    await page.waitForTimeout(1000);
  }

  // Click first signal card to expand full lineage / explainability / guardrails
  const firstSignalCard = page.locator('.signal-card').first();
  if (await firstSignalCard.isVisible()) {
    await firstSignalCard.click();
    await page.waitForTimeout(1000);
  }

  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P02_01_TERMINAL_SIGNALS_DRILLDOWN.png"),
    fullPage: false,
  });

  // -------------------------------------------------------------
  // Capture 2: UI-CONV-P02_02_INTELLIGENCE_DOCK_CALIBRATION.png
  // INTELLIGENCE dock with calibration metrics, Wilson intervals, regime & correlation
  // -------------------------------------------------------------
  console.log("Capture 2: Intelligence Dock with Calibration & Uncertainty Intervals...");
  const intelTab = page.locator('[data-testid="right-dock-tab-intelligence"]').first();
  if (await intelTab.isVisible()) {
    await intelTab.click();
    await page.waitForTimeout(1200);
  }

  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P02_02_INTELLIGENCE_DOCK_CALIBRATION.png"),
    fullPage: false,
  });

  // -------------------------------------------------------------
  // Capture 3: UI-CONV-P02_03_SIGNALS_REDIRECT_TERMINAL.png
  // Route /signals redirecting to terminal with SIGNALS dock active
  // -------------------------------------------------------------
  console.log("Capture 3: /signals Redirect to Terminal with Active Signals Dock...");
  await page.goto("http://localhost:5173/signals", { waitUntil: "networkidle" });
  await page.waitForTimeout(1500);

  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P02_03_SIGNALS_REDIRECT_TERMINAL.png"),
    fullPage: false,
  });

  // -------------------------------------------------------------
  // Capture 4: UI-CONV-P02_04_CHART_STAGE_SEEDED_PROVENANCE.png
  // Chart stage with seeded data, overlays, and seed:synthetic provenance
  // -------------------------------------------------------------
  console.log("Capture 4: Chart Stage with Seeded Data & Provenance Labels...");
  await page.goto("http://localhost:5173/?view=chart", { waitUntil: "networkidle" });
  await page.waitForTimeout(1000);

  // Click overlays SMA20 and EMA20 if visible
  const sma20Btn = page.locator('[data-testid="overlay-sma20"]').first();
  if (await sma20Btn.isVisible()) {
    await sma20Btn.click();
    await page.waitForTimeout(300);
  }
  const ema20Btn = page.locator('[data-testid="overlay-ema20"]').first();
  if (await ema20Btn.isVisible()) {
    await ema20Btn.click();
    await page.waitForTimeout(300);
  }

  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P02_04_CHART_STAGE_SEEDED_PROVENANCE.png"),
    fullPage: false,
  });

  // -------------------------------------------------------------
  // Capture 5: UI-CONV-P02_05_COMMAND_PALETTE_EMPTY_QUERY.png
  // Command palette with EMPTY query showing all routes grouped (closes OBS-CONV-3)
  // -------------------------------------------------------------
  console.log("Capture 5: Command Palette with Empty Query (All Routes Grouped, Closes OBS-CONV-3)...");
  await page.keyboard.press("Control+KeyK");
  await page.waitForTimeout(1000);

  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P02_05_COMMAND_PALETTE_EMPTY_QUERY.png"),
    fullPage: false,
  });
  await page.keyboard.press("Escape");
  await page.waitForTimeout(500);

  await context.close();

  // -------------------------------------------------------------
  // Context 2: prefers-reduced-motion context
  // Capture 6: UI-CONV-P02_06_PREFERS_REDUCED_MOTION_LOGIN.png (closes OBS-CONV-2)
  // -------------------------------------------------------------
  console.log("Capture 6: Sign-In Surface with prefers-reduced-motion: reduce (Closes OBS-CONV-2)...");
  const reducedMotionContext = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });
  const loginPage = await reducedMotionContext.newPage();
  await loginPage.goto("http://localhost:5173/login", { waitUntil: "networkidle" });
  await loginPage.waitForTimeout(1500);

  await loginPage.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P02_06_PREFERS_REDUCED_MOTION_LOGIN.png"),
    fullPage: false,
  });

  await reducedMotionContext.close();
  await browser.close();

  console.log("All 6 CONV-P02 captures complete at exactly 1920x1080!");

  // Copy all captures to /home/user/uploads/ and /home/user/
  const destDirs = ["/home/user/uploads", "/home/user"];
  for (const dir of destDirs) {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    for (let i = 1; i <= 6; i++) {
      const numStr = String(i).padStart(2, "0");
      const files = fs.readdirSync(EVIDENCE_DIR).filter((f) => f.startsWith(`UI-CONV-P02_${numStr}_`));
      for (const f of files) {
        fs.copyFileSync(path.join(EVIDENCE_DIR, f), path.join(dir, f));
      }
    }
  }
  console.log("Copied all 6 screenshots to /home/user/uploads/ and /home/user/");
}

run().catch((err) => {
  console.error("Capture failed:", err);
  process.exit(1);
});
