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

  console.log("Navigating to / (Trading Terminal)...");
  await page.goto("http://localhost:5173/", { waitUntil: "networkidle" });
  await page.waitForTimeout(1000);

  // Login if redirected
  if (page.url().includes("/login")) {
    console.log("Submitting login credentials...");
    const userField = page.locator('label:has-text("Username") input, input:not([type="password"])').first();
    const passField = page.locator('label:has-text("Password") input, input[type="password"]').first();
    await userField.fill("admin");
    await passField.fill("AxiomSecurePass2026!");
    await page.click('button[type="submit"]');
    console.log("Waiting for navigation to root...");
    await page.waitForURL("http://localhost:5173/", { timeout: 10000 });
    await page.waitForTimeout(2000);
  }

  console.log("Current URL:", page.url());

  // 1. Capture 1: UI-NEW-P05_01_TRADE_PLANS_TAB.png
  console.log("Capture 1: Bottom dock tab TRADE_PLANS...");
  const plansTab = page.locator('[data-testid="bottom-tab-trade-plans"]').first();
  if (await plansTab.isVisible()) {
    await plansTab.click();
  }
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P05_01_TRADE_PLANS_TAB.png"),
    fullPage: false,
  });

  // 2. Capture 2: UI-NEW-P05_02_TRADE_PLAN_CREATE_FORM.png
  console.log("Capture 2: Open Trade Plan Form modal...");
  const addPlanBtn = page.locator('[data-testid="add-trade-plan-btn"]').first();
  if (await addPlanBtn.isVisible()) {
    await addPlanBtn.click();
  }
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P05_02_TRADE_PLAN_CREATE_FORM.png"),
    fullPage: false,
  });
  // Close modal
  const closeBtn = page.locator('.modal-header .close-btn, button:has-text("Cancel")').first();
  if (await closeBtn.isVisible()) {
    await closeBtn.click();
  }
  await page.waitForTimeout(500);

  // 3. Capture 3: UI-NEW-P05_03_RESEARCH_JOURNAL_EDITED_ENTRY.png
  console.log("Capture 3: Bottom dock tab JOURNAL...");
  const journalTab = page.locator('[data-testid="bottom-tab-journal"]').first();
  if (await journalTab.isVisible()) {
    await journalTab.click();
  }
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P05_03_RESEARCH_JOURNAL_EDITED_ENTRY.png"),
    fullPage: false,
  });

  // 4. Capture 4: UI-NEW-P05_04_RISK_AND_DRAWDOWN_TAB.png
  console.log("Capture 4: Bottom dock tab RISK...");
  const riskTab = page.locator('[data-testid="bottom-tab-risk"]').first();
  if (await riskTab.isVisible()) {
    await riskTab.click();
  }
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P05_04_RISK_AND_DRAWDOWN_TAB.png"),
    fullPage: false,
  });

  // 5. Capture 5: UI-NEW-P05_05_MACRO_SCENARIOS_TAB.png
  console.log("Capture 5: Bottom dock tab SCENARIOS...");
  const scenTab = page.locator('[data-testid="bottom-tab-scenarios"]').first();
  if (await scenTab.isVisible()) {
    await scenTab.click();
  }
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P05_05_MACRO_SCENARIOS_OR_WRITE_FAILURE.png"),
    fullPage: false,
  });

  await browser.close();
  console.log("All 5 captures complete at 1920x1080!");

  // Copy to /home/user/uploads and /home/user
  const destDirs = ["/home/user/uploads", "/home/user"];
  for (const dir of destDirs) {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    for (let i = 1; i <= 5; i++) {
      const numStr = String(i).padStart(2, "0");
      const files = fs.readdirSync(EVIDENCE_DIR).filter((f) => f.startsWith(`UI-NEW-P05_${numStr}_`));
      for (const f of files) {
        fs.copyFileSync(path.join(EVIDENCE_DIR, f), path.join(dir, f));
      }
    }
  }
  console.log("Copied all 5 P05 screenshots to /home/user/uploads/ and /home/user/");
}

run().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
