import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";

const EVIDENCE_DIR = "/home/user/axiom/docs/evidence/uiconv";

const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

// Abort all five intelligence bundle seams: the bundle resolves to
// relation/context/hypothetical/risk/validation report fetches. Absence
// renders as "No reports returned." per group — never fabricated rows (M2).
for (const seam of [
  "**/api/v1/intelligence/correlation-reports**",
  "**/api/v1/intelligence/regime-reports**",
  "**/api/v1/intelligence/scenario-reports**",
  "**/api/v1/intelligence/portfolio-risk-reports**",
  "**/api/v1/intelligence/signal-validation-reports**",
]) {
  await page.route(seam, (route) => route.abort());
}

await page.goto("http://localhost:5173/login", { waitUntil: "domcontentloaded" });
await page.waitForTimeout(900);
await page.locator('input[data-testid="login-username-input"], input#username-input').first().fill("admin");
await page.locator('input[data-testid="login-password-input"], input#password-input').first().fill("AxiomSecurePass2026!");
await page.click('button[type="submit"]');
await page.waitForTimeout(2500);

await page.goto("http://localhost:5173/?dock=signals", { waitUntil: "domcontentloaded" });
await page.waitForTimeout(3000);

const card = page.locator('[data-testid^="signal-card-"]').first();
await card.click();
await page.waitForTimeout(1000);

const intelSection = page.locator('[data-testid^="signal-detail-intelligence-"]').first();
await intelSection.scrollIntoViewIfNeeded();
await page.waitForTimeout(400);

const noReportsCount = await page.locator('text=No reports returned.').count();
const sectionText = await intelSection.textContent().catch(() => null);
const groupCount = await intelSection.locator(".investigation-report-group").count();

await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM6_03_EMPTY_BUNDLE_SCROLLED.png") });
console.log(JSON.stringify({
  method: "network abort of all five intelligence bundle seams (backend otherwise up)",
  noReportsReturnedInstances: noReportsCount,
  reportGroupsRendered: groupCount,
  intelligenceSectionTextExcerpt: sectionText ? sectionText.slice(0, 300) : null,
}, null, 2));

await browser.close();
console.log("ITEM6 EMPTY-BUNDLE CAPTURE COMPLETE");
