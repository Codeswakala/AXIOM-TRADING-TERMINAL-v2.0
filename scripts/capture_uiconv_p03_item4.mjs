import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const OUT_DIR = "/home/user/uiconv_p03_item4_captures";
const JSON_OUT = "/home/user/UI-CONV-P03-ITEM4_CAPTURE_VERIFICATION.json";
const LOG = [];

fs.mkdirSync(OUT_DIR, { recursive: true });

function record(label, data) {
  LOG.push({ label, ...data });
  console.log(`[VERIFY] ${label}: ${JSON.stringify(data)}`);
}

function sha256(filePath) {
  const h = crypto.createHash("sha256");
  h.update(fs.readFileSync(filePath));
  return h.digest("hex");
}

async function login(page) {
  await page.goto("http://localhost:5173/login", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(900);
  await page
    .locator('input[data-testid="login-username-input"], input#username-input')
    .first()
    .fill("admin");
  await page
    .locator('input[data-testid="login-password-input"], input#password-input')
    .first()
    .fill("AxiomSecurePass2026!");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2500);
}

const EMPTY_SEAMS = [
  { re: /\/api\/v1\/institutional-platform\/research-management/, body: { collections: [], members: [], tags: [] } },
  { re: /\/api\/v1\/intelligence\/scenario-reports/, body: [] },
  { re: /\/api\/v1\/signals\/history/, body: [] },
  { re: /\/api\/v1\/intelligence\/correlation-reports/, body: [] },
  { re: /\/api\/v1\/intelligence\/regime-reports/, body: [] },
  { re: /\/api\/v1\/intelligence\/portfolio-risk-reports/, body: [] },
  { re: /\/api\/v1\/intelligence\/signal-validation-reports/, body: [] },
  { re: /\/api\/v1\/collaboration\/trade-plans/, body: [] },
  { re: /\/api\/v1\/collaboration\/journal-entries/, body: [] },
  { re: /\/api\/v1\/execution-research\/simulated-runs/, body: [] },
  { re: /\/api\/v1\/execution-research\/simulated-ledger-entries/, body: [] },
  { re: /\/api\/v1\/execution-research\/execution-risk-reports/, body: [] },
  { re: /\/api\/v1\/execution-research\/execution-experiments/, body: [] },
  { re: /\/api\/v1\/execution-research\/simulated-analytics-reports/, body: [] },
  { re: /\/api\/v1\/institutional-platform\/portfolio-research\/dashboard/, body: null },
  { re: /\/api\/v1\/institutional-platform\/portfolio-research\/report/, body: null },
  { re: /\/api\/v1\/collaboration\/chart-annotations/, body: [] },
];

async function installEmptySeams(page) {
  for (const seam of EMPTY_SEAMS) {
    await page.route(seam.re, (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(seam.body),
      }),
    );
  }
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
  await login(page);

  // ---------- CAPTURE 01: POPULATED RESEARCH STAGE WITH INTERACTION TRACE ----------
  await page.goto("http://localhost:5173/?view=research", { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="research-hub-view"]', { state: "visible", timeout: 15000 });
  await page.waitForTimeout(2500);

  const stageAttr = await page
    .locator('[data-testid="trading-terminal-workspace"]')
    .getAttribute("data-stage-view");
  const mainName = await page
    .locator('[data-testid="terminal-slot-centre"]')
    .getAttribute("aria-label");
  const chartStageCount = await page.locator('[data-testid="terminal-chart-stage"]').count();
  const regionTestIds = [
    "research-stage-scroll",
    "research-hub-view",
    "research-hub-header",
    "artifact-explorer-frame",
    "artifact-explorer-guardrail",
    "artifact-explorer-completion-guardrails",
    "artifact-source-counts",
    "artifact-source-status",
    "artifact-source-inventory",
    "artifact-catalog",
    "artifact-filter-panel",
    "artifact-catalog-list",
    "artifact-detail-card",
    "collection-organization-controls",
    "tag-organization-controls",
    "organization-records-preview",
  ];
  const regions = {};
  for (const id of regionTestIds) {
    regions[id] = (await page.locator(`[data-testid="${id}"]`).count()) > 0;
  }
  const sourceReady = await page.locator('[data-testid="source-status-ready"]').count();
  const sourceError = await page.locator('[data-testid="source-status-error"]').count();
  record("capture01_stage_view_attr", { value: stageAttr });
  record("capture01_main_aria_label", { value: mainName });
  record("capture01_chart_stage_mounted", { count: chartStageCount });
  record("capture01_region_testids_present", regions);
  record("capture01_source_status", { ready: sourceReady, error: sourceError });

  // INTERACTION TRACE: real-browser hit-test proof (document.elementFromPoint)
  // before a real Playwright click on a catalog card — the same defect class
  // check that caught the item-3 click-transparent overlay. The click targets
  // a non-active card so the detail pane provably changes.
  const cardCount = await page.locator(".artifact-catalog-card").count();
  record("capture01_catalog_card_count", { count: cardCount });
  if (cardCount > 0) {
    const targetCard = page.locator(".artifact-catalog-card:not(.active)").first();
    const targetCount = await targetCard.count();
    const clickCard = targetCount > 0 ? targetCard : page.locator(".artifact-catalog-card").first();
    await clickCard.scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    const targetLabel = await clickCard.locator("strong").first().textContent();
    const hitTestOwnsPointer = await clickCard.evaluate((el) => {
      const r = el.getBoundingClientRect();
      const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      return top === el || el.contains(top);
    });
    record("capture01_hitTestCardOwnsPointerBeforeClick", {
      value: hitTestOwnsPointer,
      targetLabel,
    });
    const detailBefore = await page.locator('[data-testid="artifact-detail-card"]').textContent();
    await clickCard.click();
    await page.waitForTimeout(700);
    const detailAfter = await page.locator('[data-testid="artifact-detail-card"]').textContent();
    const activeCount = await page.locator(".artifact-catalog-card.active").count();
    record("capture01_click_landed", {
      detailChanged: detailBefore !== detailAfter,
      activeCardCount: activeCount,
    });
  }

  const scrollMetrics01 = await page.locator('[data-testid="research-stage-scroll"]').evaluate((el) => ({
    scrollTop: el.scrollTop,
    scrollHeight: el.scrollHeight,
    clientHeight: el.clientHeight,
  }));
  record("capture01_scroll_metrics", scrollMetrics01);

  const p1 = path.join(OUT_DIR, "UI-CONV-P03-ITEM4_01_POPULATED_RESEARCH_STAGE.png");
  await page.screenshot({ path: p1 });
  record("capture01_sha256", { file: path.basename(p1), sha256: sha256(p1) });

  // ---------- CAPTURE 02: LEGACY ROUTE REDIRECT ----------
  await page.goto("http://localhost:5173/research-management", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(2200);
  const finalUrl = page.url();
  const hubVisibleAfterRedirect =
    (await page.locator('[data-testid="research-hub-view"]').count()) > 0;
  const stageAttrAfterRedirect = await page
    .locator('[data-testid="trading-terminal-workspace"]')
    .getAttribute("data-stage-view");
  record("capture02_redirect_final_url", { url: finalUrl });
  record("capture02_redirect_target_state", {
    hubMounted: hubVisibleAfterRedirect,
    stageView: stageAttrAfterRedirect,
  });
  const p2 = path.join(OUT_DIR, "UI-CONV-P03-ITEM4_02_RESEARCH_MANAGEMENT_REDIRECT.png");
  await page.screenshot({ path: p2 });
  record("capture02_sha256", { file: path.basename(p2), sha256: sha256(p2) });

  // ---------- CAPTURE 03: EMPTY BUNDLE (ALL SEAMS FULFILLED EMPTY), SCROLLED ----------
  const pageEmpty = await context.newPage();
  await installEmptySeams(pageEmpty);
  await pageEmpty.goto("http://localhost:5173/?view=research", { waitUntil: "domcontentloaded" });
  await pageEmpty.waitForSelector('[data-testid="research-hub-view"]', {
    state: "visible",
    timeout: 15000,
  });
  await pageEmpty.waitForTimeout(2200);

  const emptyMarkers = {};
  for (const marker of [
    "No collections returned for this operator.",
    "No membership references returned.",
    "No tags returned.",
    "No artifact metadata matches these filters.",
  ]) {
    emptyMarkers[marker] = (await pageEmpty.getByText(marker).count()) > 0;
  }
  const zeroRowCount = await pageEmpty.getByText("0 rows loaded").count();
  record("capture03_empty_absence_markers", emptyMarkers);
  record("capture03_zero_row_counts", { count: zeroRowCount });

  // Scroll the stage container to the organization records region (bottom).
  await pageEmpty
    .locator('[data-testid="organization-records-preview"]')
    .scrollIntoViewIfNeeded();
  await pageEmpty.waitForTimeout(500);
  const scrollMetrics03 = await pageEmpty
    .locator('[data-testid="research-stage-scroll"]')
    .evaluate((el) => ({ scrollTop: el.scrollTop, scrollHeight: el.scrollHeight, clientHeight: el.clientHeight }));
  const previewRect = await pageEmpty
    .locator('[data-testid="organization-records-preview"]')
    .evaluate((el) => {
      const r = el.getBoundingClientRect();
      return { top: r.top, bottom: r.bottom, height: r.height, width: r.width };
    });
  const emptyMarkerInViewport = await pageEmpty
    .getByText("No collections returned for this operator.")
    .first()
    .evaluate((el) => {
      const r = el.getBoundingClientRect();
      return r.top >= 0 && r.bottom <= window.innerHeight;
    });
  record("capture03_scroll_metrics", scrollMetrics03);
  record("capture03_organization_preview_rect", previewRect);
  record("capture03_emptyMarkerVisibleInViewport", { value: emptyMarkerInViewport });

  const p3 = path.join(OUT_DIR, "UI-CONV-P03-ITEM4_03_EMPTY_BUNDLE_SCROLLED.png");
  await pageEmpty.screenshot({ path: p3 });
  record("capture03_sha256", { file: path.basename(p3), sha256: sha256(p3) });

  // ---------- CAPTURE 04: SINGLE-SEAM FAILURE -> M5 PER-SOURCE DEGRADATION ----------
  // M5 (directive §6): abort ONE seam (the research-management bundle). The hub
  // must not blank — the failed family reports its own error row while the
  // other nine sources keep their genuine rows. Scrolled to the affected region.
  const pageError = await context.newPage();
  await pageError.route(
    /\/api\/v1\/institutional-platform\/research-management/,
    (route) => route.abort(),
  );
  await pageError.goto("http://localhost:5173/?view=research", { waitUntil: "domcontentloaded" });
  await pageError.waitForSelector('[data-testid="research-hub-view"]', {
    state: "visible",
    timeout: 15000,
  });
  await pageError.waitForTimeout(2500);
  const errorRows = await pageError.locator('[data-testid="source-status-error"]').count();
  const readyRows = await pageError.locator('[data-testid="source-status-ready"]').count();
  const bundleErrorText = await pageError
    .locator('[data-testid="source-status-error"]')
    .first()
    .textContent()
    .catch(() => null);
  const hubStillRenders = (await pageError.locator('[data-testid="artifact-catalog"]').count()) > 0;
  record("capture04_m5_single_seam_failure", {
    errorRows,
    readyRows,
    hubStillRenders,
    bundleErrorText,
  });
  await pageError
    .locator('[data-testid="artifact-source-status"]')
    .scrollIntoViewIfNeeded();
  await pageError.waitForTimeout(500);
  const scrollMetrics04 = await pageError
    .locator('[data-testid="research-stage-scroll"]')
    .evaluate((el) => ({ scrollTop: el.scrollTop, scrollHeight: el.scrollHeight, clientHeight: el.clientHeight }));
  const errorRowInViewport = await pageError
    .locator('[data-testid="source-status-error"]')
    .first()
    .evaluate((el) => {
      const r = el.getBoundingClientRect();
      return r.top >= 0 && r.bottom <= window.innerHeight;
    });
  record("capture04_scroll_metrics", scrollMetrics04);
  record("capture04_errorRowVisibleInViewport", { value: errorRowInViewport });
  const p4 = path.join(OUT_DIR, "UI-CONV-P03-ITEM4_04_SINGLE_SEAM_FAILURE_DEGRADATION_SCROLLED.png");
  await pageError.screenshot({ path: p4 });
  record("capture04_sha256", { file: path.basename(p4), sha256: sha256(p4) });

  // ---------- CAPTURE 05: MUTATION CONTROL INTERACTION (directive §8.7) ----------
  // A real collection-organization write: hit-test trace, then a true Playwright
  // click on "Save collection record" with a unique name; the created row must
  // appear in the organization preview (POST to the existing W7 store).
  const pageMutation = await context.newPage();
  await pageMutation.goto("http://localhost:5173/?view=research", { waitUntil: "domcontentloaded" });
  await pageMutation.waitForSelector('[data-testid="collection-organization-controls"]', {
    state: "visible",
    timeout: 15000,
  });
  await pageMutation.waitForTimeout(2000);
  const uniqueName = `DA capture review set ${Date.now()}`;
  const nameInput = pageMutation
    .locator('[data-testid="collection-organization-controls"] input')
    .first();
  await nameInput.fill(uniqueName);
  const saveButton = pageMutation
    .locator('[data-testid="collection-organization-controls"]')
    .getByText("Save collection record");
  // Scroll the button into view BEFORE the hit-test so the trace measures the
  // actual click-time geometry (the prior run measured a pre-scroll point and
  // reported false while the subsequent auto-scrolling click landed — a
  // measurement flaw, disclosed and corrected in this script).
  await saveButton.scrollIntoViewIfNeeded();
  await pageMutation.waitForTimeout(400);
  const mutationHitTest = await saveButton.evaluate((el) => {
    const r = el.getBoundingClientRect();
    const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return top === el || el.contains(top);
  });
  record("capture05_mutation_hitTestBeforeClick", { value: mutationHitTest, uniqueName });
  await saveButton.click();
  await pageMutation.waitForTimeout(1500);
  const previewHasRow = await pageMutation
    .locator('[data-testid="organization-records-preview"]')
    .getByText(uniqueName)
    .count();
  record("capture05_created_collection_visible_in_preview", {
    name: uniqueName,
    visible: previewHasRow > 0,
  });
  await pageMutation
    .locator('[data-testid="collection-organization-controls"]')
    .scrollIntoViewIfNeeded();
  await pageMutation.waitForTimeout(400);
  const scrollMetrics05 = await pageMutation
    .locator('[data-testid="research-stage-scroll"]')
    .evaluate((el) => ({ scrollTop: el.scrollTop, scrollHeight: el.scrollHeight, clientHeight: el.clientHeight }));
  record("capture05_scroll_metrics", scrollMetrics05);
  const p5 = path.join(OUT_DIR, "UI-CONV-P03-ITEM4_05_MUTATION_CONTROL_SAVED.png");
  await pageMutation.screenshot({ path: p5 });
  record("capture05_sha256", { file: path.basename(p5), sha256: sha256(p5) });

  fs.writeFileSync(JSON_OUT, JSON.stringify({ generated_at: new Date().toISOString(), viewport: "1920x1080", records: LOG }, null, 2));
  console.log("[DONE] verification JSON:", JSON_OUT);
  await browser.close();
}

run().catch((err) => {
  console.error("[FATAL]", err);
  process.exit(1);
});
