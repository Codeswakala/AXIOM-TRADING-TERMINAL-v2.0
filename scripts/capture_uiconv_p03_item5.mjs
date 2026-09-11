import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";

const EVIDENCE_DIR = "/home/user/axiom/docs/evidence/uiconv";
const LOG = [];

async function record(label, data) {
  LOG.push({ label, ...data });
  console.log(`[VERIFY] ${label}: ${JSON.stringify(data)}`);
}

async function login(page) {
  await page.goto("http://localhost:5173/login", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(900);
  await page.locator('input[data-testid="login-username-input"], input#username-input').first().fill("admin");
  await page.locator('input[data-testid="login-password-input"], input#password-input').first().fill("AxiomSecurePass2026!");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2500);
}

async function run() {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await login(page);

  // ---------- CAPTURE 01: AUDIT EXPLORER WITH REFUSAL REASON-CODE VISIBLE ----------
  await page.goto("http://localhost:5173/?open=governance", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(3000);
  const overlay = await page.locator('[data-testid="governance-overlay"]').count();
  // Select the refusal event (newest-first ordering puts the just-inserted row first).
  const refusalCard = page.locator('button.artifact-catalog-card', { hasText: "assistant.response_refused" }).first();
  const refusalExists = await refusalCard.count();
  if (refusalExists) {
    await refusalCard.click();
    await page.waitForTimeout(700);
  }
  // Scroll the refusal viewer region into view.
  const refusalViewer = page.locator('[data-testid="governance-refusal-reason-viewer"]').first();
  if (await refusalViewer.count()) {
    await refusalViewer.scrollIntoViewIfNeeded();
    await page.waitForTimeout(400);
  }
  const reasonText = await refusalViewer.textContent().catch(() => null);
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM5_01_AUDIT_EXPLORER_REFUSAL_CODE.png") });
  await record("01_AUDIT_EXPLORER_REFUSAL", {
    url: page.url(),
    overlayOpen: overlay,
    refusalCardSelected: refusalExists,
    refusalViewerText: reasonText,
  });

  // ---------- CAPTURE 02: FOUR CONSTITUTIONAL DECLARATIONS IN FRAME ----------
  const certPanel = page.locator('[data-testid="governance-certification-status"]').first();
  await certPanel.scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  const certVisible = await page.locator('[data-testid="governance-certification-status"]').count();
  const residualsVisible = await page.locator('[data-testid="governance-standing-residuals"]').count();
  const boundaryVisible = await page.locator('[data-testid="governance-readonly-boundary"]').count();
  const inertVisible = await page.locator('[data-testid="governance-inert-display-rules"]').count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM5_02_CONSTITUTIONAL_DECLARATIONS.png") });
  await record("02_CONSTITUTIONAL_DECLARATIONS", {
    certificationStatusInDom: certVisible,
    standingResidualsInDom: residualsVisible,
    readOnlyBoundaryInDom: boundaryVisible,
    inertDisplayRulesInDom: inertVisible,
  });

  // ---------- CAPTURE 03: PLATFORM POSTURE SECTION (certification boundary card) ----------
  const posturePanel = page.locator('[data-testid="governance-platform-posture"]').first();
  await posturePanel.scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  const certBoundaryCard = await page.locator('[aria-label="Production certification remains separate"]').count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM5_03_PLATFORM_POSTURE.png") });
  await record("03_PLATFORM_POSTURE", {
    posturePanelVisible: await posturePanel.count(),
    certificationBoundaryCard: certBoundaryCard,
  });

  // ---------- CAPTURE 04: /governance LEGACY ROUTE REDIRECT ----------
  await page.goto("http://localhost:5173/governance", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(3000);
  const finalUrl = page.url();
  const overlayAfterRedirect = await page.locator('[data-testid="governance-overlay"]').count();
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM5_04_GOVERNANCE_ROUTE_REDIRECT.png") });
  await record("04_GOVERNANCE_ROUTE_REDIRECT", {
    finalUrl,
    overlayOpen: overlayAfterRedirect,
  });

  await browser.close();
  fs.writeFileSync(path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM5_CAPTURE_VERIFICATION.json"), JSON.stringify(LOG, null, 2));
  console.log("ITEM5 POPULATED CAPTURES COMPLETE");
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
