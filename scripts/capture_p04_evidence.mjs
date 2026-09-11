import { chromium } from "playwright";
import fs from "fs";
import path from "path";

const EVIDENCE_DIR = "/home/user/axiom/docs/evidence/uinew";

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

  // Check if we are redirected to login
  if (page.url().includes("/login")) {
    console.log("On login page. Submitting credentials...");
    const userField = page.locator('label:has-text("Username") input, input:not([type="password"])').first();
    const passField = page.locator('label:has-text("Password") input, input[type="password"]').first();
    await userField.fill("admin");
    await passField.fill("AxiomSecurePass2026!");
    await page.click('button[type="submit"]');
    console.log("Waiting for navigation after login...");
    await page.waitForURL("http://localhost:5173/", { timeout: 10000 });
    await page.waitForTimeout(2000);
  }

  console.log("Current URL:", page.url());

  // 1. Capture 1: UI-NEW-P04_01_SIGNAL_STREAM_WITH_UNCERTAINTY.png
  console.log("Capture 1: Right dock tab SIGNALS...");
  const signalsTab = page.locator('[data-testid="right-dock-tab-signals"], button:has-text("SIGNALS")').first();
  if (await signalsTab.isVisible()) {
    await signalsTab.click();
  }
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P04_01_SIGNAL_STREAM_WITH_UNCERTAINTY.png"),
    fullPage: false,
  });

  // 2. Capture 2: UI-NEW-P04_02_WITHHELD_OR_EXPIRED_SIGNAL.png
  console.log("Capture 2: Click EXPIRED filter...");
  const expiredChip = page.locator('[data-testid="signal-filter-expired"]').first();
  if (await expiredChip.isVisible()) {
    await expiredChip.click();
  }
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P04_02_WITHHELD_OR_EXPIRED_SIGNAL.png"),
    fullPage: false,
  });

  // 3. Capture 3: UI-NEW-P04_03_CHART_SIGNAL_OVERLAYS_OVER_SEEDED_WALK.png
  console.log("Capture 3: Center chart with signal overlays...");
  const allChip = page.locator('[data-testid="signal-filter-all"]').first();
  if (await allChip.isVisible()) {
    await allChip.click();
  }
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P04_03_CHART_SIGNAL_OVERLAYS_OVER_SEEDED_WALK.png"),
    fullPage: false,
  });

  // 4. Capture 4: UI-NEW-P04_04_INTELLIGENCE_CARDS_CALIBRATION_CORRELATION.png
  console.log("Capture 4: Right dock tab INTELLIGENCE...");
  const intelTab = page.locator('[data-testid="right-dock-tab-intelligence"], button:has-text("INTELLIGENCE")').first();
  if (await intelTab.isVisible()) {
    await intelTab.click();
  }
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P04_04_INTELLIGENCE_CARDS_CALIBRATION_CORRELATION.png"),
    fullPage: false,
  });

  // 5. Capture 5: UI-NEW-P04_05_SIGNAL_UNCERTAINTY_UNAVAILABLE_QUALIFIER.png
  console.log("Capture 5: Switch back to SIGNALS and show unavailable qualifier...");
  if (await signalsTab.isVisible()) {
    await signalsTab.click();
  }
  await page.waitForTimeout(1000);
  await page.screenshot({
    path: path.join(EVIDENCE_DIR, "UI-NEW-P04_05_SIGNAL_UNCERTAINTY_UNAVAILABLE_QUALIFIER.png"),
    fullPage: false,
  });

  await browser.close();
  console.log("Done taking screenshots!");

  // Copy to uploads and user root
  const destDirs = ["/home/user/uploads", "/home/user"];
  for (const dir of destDirs) {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    for (let i = 1; i <= 5; i++) {
      const numStr = String(i).padStart(2, "0");
      const files = fs.readdirSync(EVIDENCE_DIR).filter((f) => f.startsWith(`UI-NEW-P04_${numStr}_`));
      for (const f of files) {
        fs.copyFileSync(path.join(EVIDENCE_DIR, f), path.join(dir, f));
      }
    }
  }
  console.log("Copied all 5 screenshots to /home/user/uploads/ and /home/user/");
}

run().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
