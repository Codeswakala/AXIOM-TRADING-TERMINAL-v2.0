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

  // ---------- CAPTURE 01: EXPANDED SIGNAL CARD WITH THE THREE NEW SECTIONS ----------
  await page.goto("http://localhost:5173/?dock=signals", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(3000);

  // INTERACTION TRACE: real-browser hit-test proof. The click below is a true
  // Playwright hit-test — it fails if any element intercepts the pointer
  // (the exact defect class that made the item-3 overlay click-transparent).
  const firstCard = page.locator('[data-testid^="signal-card-"]').first();
  await firstCard.waitFor({ state: "visible" });
  const hitTestBefore = await firstCard.evaluate((el) => {
    const r = el.getBoundingClientRect();
    const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return top === el || el.contains(top);
  });
  await firstCard.click();
  await page.waitForTimeout(1000);

  const frameVisible = await page.locator('[data-testid="signal-investigation-frame"]').count();
  const reportIdsVisible = await page.locator('[data-testid^="signal-detail-report-ids-"]').count();
  const evidenceLinksVisible = await page.locator('[aria-label="Related investigation evidence links"]').count();
  const intelligenceVisible = await page.locator('[data-testid^="signal-detail-intelligence-"]').count();
  const frameText = await page.locator('[data-testid="signal-investigation-frame"]').textContent().catch(() => null);

  // Scroll the expanded card's new sections into view (bottom of the card).
  const intelSection = page.locator('[data-testid^="signal-detail-intelligence-"]').first();
  await intelSection.scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);
  const listScroll = await page.locator(".signals-cards-list").first().evaluate((el) => ({
    scrollTop: el.scrollTop,
    scrollHeight: el.scrollHeight,
    clientHeight: el.clientHeight,
  }));

  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM6_01_EXPANDED_DRILLDOWN_NEW_SECTIONS.png") });
  await record("01_EXPANDED_DRILLDOWN", {
    url: page.url(),
    hitTestCardOwnsPointerBeforeClick: hitTestBefore,
    frameVisible,
    reportIdsVisible,
    evidenceLinksVisible,
    intelligenceVisible,
    frameTextExcerpt: frameText ? frameText.slice(0, 200) : null,
    listScroll,
  });

  // ---------- CAPTURE 02: /investigate REDIRECT LANDING ----------
  await page.goto("http://localhost:5173/investigate", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(3000);
  const finalUrl = page.url();
  const signalsDockActive = await page.locator('[data-testid="right-dock-tab-signals"]').getAttribute("class");
  await page.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM6_02_INVESTIGATE_ROUTE_REDIRECT.png") });
  await record("02_INVESTIGATE_REDIRECT", {
    finalUrl,
    signalsTabClass: signalsDockActive,
  });

  await browser.close();

  // ---------- CAPTURE 03: EMPTY BUNDLE — "No reports returned." scrolled (OBS-CONV3-5) ----------
  const browser2 = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context2 = await browser2.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const page2 = await context2.newPage();

  // Abort ONLY the intelligence bundle seam: absence renders as
  // "No reports returned." per group — never fabricated report rows (M2).
  await page2.route("**/api/v1/institutional-platform/intelligence-bundle**", (route) => route.abort());
  await page2.route("**/intelligence-bundle**", (route) => route.abort());

  await login(page2);
  await page2.goto("http://localhost:5173/?dock=signals", { waitUntil: "domcontentloaded" });
  await page2.waitForTimeout(3000);

  const card2 = page2.locator('[data-testid^="signal-card-"]').first();
  await card2.click();
  await page2.waitForTimeout(1000);

  const intelSection2 = page2.locator('[data-testid^="signal-detail-intelligence-"]').first();
  await intelSection2.scrollIntoViewIfNeeded();
  await page2.waitForTimeout(400);
  const noReportsCount = await page2.locator('text=No reports returned.').count();
  const sectionText = await intelSection2.textContent().catch(() => null);
  const scrollState = await page2.locator(".signals-cards-list").first().evaluate((el) => ({
    scrollTop: el.scrollTop,
    scrollHeight: el.scrollHeight,
    clientHeight: el.clientHeight,
  }));

  await page2.screenshot({ path: path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM6_03_EMPTY_BUNDLE_SCROLLED.png") });
  await record("03_EMPTY_BUNDLE_SCROLLED", {
    method: "network abort of the intelligence bundle seam (backend otherwise up)",
    noReportsReturnedInstances: noReportsCount,
    intelligenceSectionTextExcerpt: sectionText ? sectionText.slice(0, 300) : null,
    scrollState,
  });

  await browser2.close();
  fs.writeFileSync(path.join(EVIDENCE_DIR, "UI-CONV-P03-ITEM6_CAPTURE_VERIFICATION.json"), JSON.stringify(LOG, null, 2));
  console.log("ITEM6 CAPTURES COMPLETE");
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
