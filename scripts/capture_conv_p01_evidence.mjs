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

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });

  const page = await context.newPage();

  // 1. Capture 1: UI-CONV-P01_01_LOGIN_SURFACE.png
  console.log("Capture 1: Login Surface (3D Split View, Governance Chips, AX Monogram)...");
  await page.goto("http://localhost:5173/login", { waitUntil: "networkidle" });
  await page.waitForTimeout(1500);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P01_01_LOGIN_SURFACE.png"),
    fullPage: false,
  });

  // 2. Capture 2: UI-CONV-P01_02_LOGIN_FAILED_AUTH_ERROR.png
  console.log("Capture 2: Login Failed-Auth Error State...");
  const userField = page.locator('input[data-testid="login-username-input"], input#username-input').first();
  const passField = page.locator('input[data-testid="login-password-input"], input#password-input').first();
  await userField.fill("invalid_operator");
  await passField.fill("WrongPassword123!");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(1500);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P01_02_LOGIN_FAILED_AUTH_ERROR.png"),
    fullPage: false,
  });

  // 3. Log in with valid credentials
  console.log("Logging in with valid operator credentials...");
  await userField.fill("admin");
  await passField.fill("AxiomSecurePass2026!");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2000);

  // Navigate explicitly to Terminal Root (/)
  console.log("Navigating explicitly to Terminal Root (/)...");
  await page.goto("http://localhost:5173/", { waitUntil: "networkidle" });
  await page.waitForTimeout(1000);

  // Ensure theme is dark
  const themeBtn = page.locator('[data-testid="shell-theme-toggle-btn"]').first();
  const themeText = await themeBtn.textContent();
  if (themeText && themeText.includes("Dark theme")) {
    await themeBtn.click();
    await page.waitForTimeout(500);
  }

  // Click Operations rail button
  const opsRailBtn = page.locator('[data-testid="rail-btn-monitor-operations"]').first();
  if (await opsRailBtn.isVisible()) {
    await opsRailBtn.click();
    await page.waitForTimeout(1000);
  }

  // Seed chart history for EUR/USD
  const seedBtn = page.locator('[data-testid="chart-seed-btn"]').first();
  if (await seedBtn.isVisible()) {
    await seedBtn.click();
    await page.waitForTimeout(1500);
  }

  // Ensure bottom dock is on Trade Plans tab
  const plansTab = page.locator('[data-testid="bottom-tab-trade-plans"]').first();
  if (await plansTab.isVisible()) {
    await plansTab.click();
    await page.waitForTimeout(500);
  }

  // 4. Capture 3: UI-CONV-P01_03_TERMINAL_ROOT_UNIFIED_SHELL.png
  console.log("Capture 3: Terminal Root in Unified Shell (All 5 Zones in Dark Theme)...");
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P01_03_TERMINAL_ROOT_UNIFIED_SHELL.png"),
    fullPage: false,
  });

  // 5. Capture 4: UI-CONV-P01_04_NON_TERMINAL_ROUTE_UNIFIED_SHELL.png
  console.log("Capture 4: Non-terminal Route (/signals) in Unified Shell...");
  const signalsRailBtn = page.locator('[data-testid="rail-btn-research-advisory-signals"]').first();
  if (await signalsRailBtn.isVisible()) {
    await signalsRailBtn.click();
    await page.waitForTimeout(1500);
  } else {
    await page.goto("http://localhost:5173/signals", { waitUntil: "networkidle" });
    await page.waitForTimeout(1500);
  }
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P01_04_NON_TERMINAL_ROUTE_UNIFIED_SHELL.png"),
    fullPage: false,
  });

  // 6. Capture 5: UI-CONV-P01_05_COMMAND_PALETTE_OPEN_WITH_RESULTS.png (Dark Theme)
  console.log("Capture 5: Command Palette Open with Filter Results (Dark Theme)...");
  await page.keyboard.press("Control+KeyK");
  await page.waitForTimeout(1000);
  const paletteInput = page.locator('.ix-command-palette input').first();
  if (await paletteInput.isVisible()) {
    await paletteInput.fill("Signals");
    await page.waitForTimeout(1000);
  }
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P01_05_COMMAND_PALETTE_OPEN_WITH_RESULTS.png"),
    fullPage: false,
  });
  await page.keyboard.press("Escape");
  await page.waitForTimeout(500);

  // 7. Capture 6: UI-CONV-P01_06_REDUCED_MOTION_OR_LIGHT_THEME.png
  console.log("Capture 6: Light Theme Variant...");
  if (await themeBtn.isVisible()) {
    await themeBtn.click();
    await page.waitForTimeout(1500);
  }
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-CONV-P01_06_REDUCED_MOTION_OR_LIGHT_THEME.png"),
    fullPage: false,
  });

  await browser.close();
  console.log("All 6 CONV-P01 captures complete at 1920x1080!");

  // Copy to /home/user/uploads and /home/user
  const destDirs = ["/home/user/uploads", "/home/user"];
  for (const dir of destDirs) {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    for (let i = 1; i <= 6; i++) {
      const numStr = String(i).padStart(2, "0");
      const files = fs.readdirSync(EVIDENCE_DIR).filter((f) => f.startsWith(`UI-CONV-P01_${numStr}_`));
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
