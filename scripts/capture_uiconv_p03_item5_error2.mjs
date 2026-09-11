import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";

const EVIDENCE_DIR = "/home/user/axiom/docs/evidence/uiconv";

const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const page = await context.newPage();

// M5 demonstration: abort ONLY the audit seam. The other two sections must
// load normally and the constitutional declarations must remain visible.
await page.route("**/api/v1/persistence/audit-events**", (route) => route.abort());

await page.goto("http://localhost:5173/login", { waitUntil: "domcontentloaded" });
await page.waitForTimeout(900);
await page.locator('input[data-testid="login-username-input"], input#username-input').first().fill("admin");
await page.locator('input[data-testid="login-password-input"], input#password-input').first().fill("AxiomSecurePass2026!");
await page.click('button[type="submit"]');
await page.waitForTimeout(2500);

await page.goto("http://localhost:5173/?open=governance", { waitUntil: "domcontentloaded" });
await page.waitForTimeout(4000);

const auditError = await page.locator('text=Audit Error').count();
const auditErrorText = await page.locator('[data-testid="governance-audit-explorer"]').textContent().catch(() => null);
const validationLoaded = await page.locator('[data-testid="governance-validation-panels"]').count();
const platformLoaded = await page.locator('[data-testid="governance-platform-posture"]').count();
const certVisible = await page.locator('[data-testid="governance-certification-status"]').count();

// OBS-CONV3-5: scroll to the affected region (audit explorer with its error banner).
const auditExplorer = page.locator('[data-testid="governance-audit-explorer"]').first();
await auditExplorer.scrollIntoViewIfNeeded();
await page.waitForTimeout(400);
const bodyScroll = await page.locator(".ix-governance-body").evaluate((el) => ({
  scrollTop: el.scrollTop,
  scrollHeight: el.scrollHeight,
  clientHeight: el.clientHeight,
}));

await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM5_05_AUDIT_ERROR_STATE_SCROLLED.png") });
console.log(JSON.stringify({
  auditErrorBannerVisible: auditError,
  auditSectionTextExcerpt: auditErrorText ? auditErrorText.slice(0, 300) : null,
  validationSectionLoaded: validationLoaded,
  platformSectionLoaded: platformLoaded,
  certificationStatusStillVisible: certVisible,
  bodyScroll,
}, null, 2));

await browser.close();
console.log("ITEM5 ERROR-STATE CAPTURE COMPLETE");
