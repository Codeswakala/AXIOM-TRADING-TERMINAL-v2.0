import { chromium } from "playwright";
import fs from "fs";
import path from "path";

const EVIDENCE_DIR = "/home/user/axiom/docs/evidence/uinew";

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

  // 1. Capture 4: Logged-out redirect at /login
  console.log("Capture 4: Logged-out redirect at /login...");
  await page.goto("http://localhost:5173/", { waitUntil: "networkidle" });
  await page.waitForTimeout(1000);
  console.log("Logged out URL:", page.url());
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P06_04_LOGGED_OUT_REDIRECT.png"),
    fullPage: false,
  });

  // 2. Login to Terminal
  console.log("Logging into Terminal...");
  const userField = page.locator('label:has-text("Username") input, input:not([type="password"])').first();
  const passField = page.locator('label:has-text("Password") input, input[type="password"]').first();
  await userField.fill("admin");
  await passField.fill("AxiomSecurePass2026!");
  await page.click('button[type="submit"]');
  await page.waitForURL("http://localhost:5173/", { timeout: 10000 });
  await page.waitForTimeout(2000);

  // Seed chart history for EUR/USD
  const seedBtn = page.locator('[data-testid="chart-seed-btn"]').first();
  if (await seedBtn.isVisible()) {
    await seedBtn.click();
    await page.waitForTimeout(1000);
  }

  // 3. Capture 1: UI-NEW-P06_01_WHOLE_ASSEMBLED_TERMINAL.png
  console.log("Capture 1: Whole Assembled Terminal (EUR/USD, Chart Candles, Trade Plans Tab)...");
  const eurRow = page.locator('[data-testid="watchlist-row-eur-usd"]').first();
  if (await eurRow.isVisible()) {
    await eurRow.click();
    await page.waitForTimeout(500);
  }
  const plansTab = page.locator('[data-testid="bottom-tab-trade-plans"]').first();
  if (await plansTab.isVisible()) {
    await plansTab.click();
  }
  const signalsTab = page.locator('[data-testid="right-dock-tab-signals"]').first();
  if (await signalsTab.isVisible()) {
    await signalsTab.click();
  }
  await page.waitForTimeout(1500);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P06_01_WHOLE_ASSEMBLED_TERMINAL.png"),
    fullPage: false,
  });

  // 4. Capture 2: UI-NEW-P06_02_SYMBOL_SELECTION_PROPAGATION.png
  console.log("Capture 2: Switching symbol to GBP/USD and viewing telemetry...");
  const gbpRow = page.locator('[data-testid="watchlist-row-gbp-usd"]').first();
  if (await gbpRow.isVisible()) {
    await gbpRow.click();
  }
  await page.waitForTimeout(1000);
  const telemetryTab = page.locator('[data-testid="right-dock-tab-telemetry"]').first();
  if (await telemetryTab.isVisible()) {
    await telemetryTab.click();
  }
  await page.waitForTimeout(1500);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P06_02_SYMBOL_SELECTION_PROPAGATION.png"),
    fullPage: false,
  });

  // 5. Capture 3: UI-NEW-P06_03_BOTTOM_DOCK_TAB_SWITCHING.png
  console.log("Capture 3: Bottom dock tab RISK & DRAWDOWN with intact EUR/USD chart stage...");
  if (await eurRow.isVisible()) {
    await eurRow.click();
    await page.waitForTimeout(500);
  }
  const riskTab = page.locator('[data-testid="bottom-tab-risk"]').first();
  if (await riskTab.isVisible()) {
    await riskTab.click();
  }
  await page.waitForTimeout(1500);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P06_03_BOTTOM_DOCK_TAB_SWITCHING.png"),
    fullPage: false,
  });

  // 6. Capture 5: UI-NEW-P06_05_GOVERNANCE_CHIPS_FULL_BLEED.png
  console.log("Capture 5: Governance chips full-bleed view (Journal Tab)...");
  const journalTab = page.locator('[data-testid="bottom-tab-journal"]').first();
  if (await journalTab.isVisible()) {
    await journalTab.click();
  }
  if (await signalsTab.isVisible()) {
    await signalsTab.click();
  }
  await page.waitForTimeout(1500);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P06_05_GOVERNANCE_CHIPS_FULL_BLEED.png"),
    fullPage: false,
  });

  await browser.close();
  console.log("All 5 P06 captures complete at 1920x1080!");

  // Copy to /home/user/uploads and /home/user
  const destDirs = ["/home/user/uploads", "/home/user"];
  for (const dir of destDirs) {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    for (let i = 1; i <= 5; i++) {
      const numStr = String(i).padStart(2, "0");
      const files = fs.readdirSync(EVIDENCE_DIR).filter((f) => f.startsWith(`UI-NEW-P06_${numStr}_`));
      for (const f of files) {
        fs.copyFileSync(path.join(EVIDENCE_DIR, f), path.join(dir, f));
      }
    }
  }
  console.log("Copied all 5 P06 screenshots to /home/user/uploads/ and /home/user/");
}

run().catch((err) => {
  console.error("Capture failed:", err);
  process.exit(1);
});
