import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const OUT_DIR = "/home/user/surf_p01_captures";
const JSON_OUT = "/home/user/SURF-P01_CAPTURE_VERIFICATION.json";
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
  { re: /\/api\/v1\/execution-research\/simulated-runs\?/, body: [] },
  { re: /\/api\/v1\/execution-research\/simulated-runs\/[^/]+\/fills/, body: [] },
  { re: /\/api\/v1\/execution-research\/simulated-ledger-entries\?/, body: [] },
  { re: /\/api\/v1\/execution-research\/execution-risk-reports\?/, body: [] },
  { re: /\/api\/v1\/execution-research\/execution-experiments\?/, body: [] },
  { re: /\/api\/v1\/execution-research\/simulated-analytics-reports\?/, body: [] },
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

// OBS-SURF1-2: legibility instrument — record the panel's height, the inner
// grid's height, every card's height, and whether every card rect lies fully
// inside its panel rect. A panel whose cards are clipped or overlapped by the
// next section fails `cardsFullyInsidePanel`.
async function measureLegibility(page, panelSelector, cardSelector) {
  return page.evaluate(
    ([psel, csel]) => {
      const panel = document.querySelector(psel);
      if (!panel) return null;
      const pr = panel.getBoundingClientRect();
      const cards = [...panel.querySelectorAll(csel)];
      const cardRects = cards.map((c) => {
        const r = c.getBoundingClientRect();
        return { top: Math.round(r.top), bottom: Math.round(r.bottom), h: Math.round(r.height) };
      });
      const innerGrid = panel.querySelector(".artifact-source-grid, .metric-card-grid");
      return {
        panelTop: Math.round(pr.top),
        panelBottom: Math.round(pr.bottom),
        panelH: Math.round(pr.height),
        innerGridH: innerGrid ? Math.round(innerGrid.getBoundingClientRect().height) : null,
        cardCount: cardRects.length,
        cardRects,
        cardsFullyInsidePanel:
          cardRects.length > 0 &&
          cardRects.every((r) => r.top >= pr.top - 0.5 && r.bottom <= pr.bottom + 0.5),
      };
    },
    [panelSelector, cardSelector],
  );
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

  // ---------- CAPTURE 01: POPULATED STAGE + M2 LABELS + INTERACTION TRACE ----------
  await page.goto("http://localhost:5173/?view=execution", { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="execution-research-header"]', {
    state: "visible",
    timeout: 15000,
  });
  await page.waitForTimeout(2500);

  const stageAttr = await page
    .locator('[data-testid="trading-terminal-workspace"]')
    .getAttribute("data-stage-view");
  const mainName = await page
    .locator('[data-testid="terminal-slot-centre"]')
    .getAttribute("aria-label");
  const chartStageCount = await page.locator('[data-testid="terminal-chart-stage"]').count();
  const simBadges = await page.locator('[data-testid^="execution-sim-badge-"]').count();
  const regionTestIds = [
    "execution-stage-scroll",
    "execution-research-header",
    "execution-research-refresh",
    "execution-research-disclaimer",
    "execution-investigation-context",
    "execution-source-status",
    "execution-group-runs",
    "execution-group-fills",
    "execution-group-ledger",
    "execution-group-risk",
    "execution-group-experiments",
    "execution-group-analytics",
  ];
  const regions = {};
  for (const id of regionTestIds) {
    regions[id] = (await page.locator(`[data-testid="${id}"]`).count()) > 0;
  }
  const readyRows = await page.locator('[data-testid="exec-source-status-ready"]').count();
  const errorRows = await page.locator('[data-testid="exec-source-status-error"]').count();
  const runCards = await page.locator('[data-testid^="execution-run-card-"]').count();
  record("capture01_stage_view_attr", { value: stageAttr });
  record("capture01_main_aria_label", { value: mainName });
  record("capture01_chart_stage_mounted", { count: chartStageCount });
  record("capture01_sim_badges", { count: simBadges });
  record("capture01_region_testids_present", regions);
  record("capture01_source_status", { ready: readyRows, error: errorRows });
  record("capture01_run_cards", { count: runCards });
  record(
    "capture01_source_status_legibility",
    await measureLegibility(page, '[data-testid="execution-source-status"]', ".artifact-source-card"),
  );
  record(
    "capture01_counts_legibility",
    await measureLegibility(
      page,
      'section[aria-label="Execution research artifact counts"]',
      ".metric-card",
    ),
  );

  // INTERACTION TRACE: real-browser hit-test proof before a real Playwright
  // click on the first run card's detail button (item-4 elementFromPoint
  // method). The click must land on the button and surface the detail record.
  let detailButton = null;
  if (runCards > 0) {
    detailButton = page.locator('[data-testid^="execution-detail-open-run-"]').first();
    await detailButton.scrollIntoViewIfNeeded();
    await page.waitForTimeout(400);
    const hitTestOwnsPointer = await detailButton.evaluate((el) => {
      const r = el.getBoundingClientRect();
      const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      return top === el || el.contains(top);
    });
    record("capture01_hitTestDetailButtonOwnsPointerBeforeClick", { value: hitTestOwnsPointer });
  }

  const scrollMetrics01 = await page
    .locator('[data-testid="execution-stage-scroll"]')
    .evaluate((el) => ({ scrollTop: el.scrollTop, scrollHeight: el.scrollHeight, clientHeight: el.clientHeight }));
  record("capture01_scroll_metrics", scrollMetrics01);
  const p1 = path.join(OUT_DIR, "SURF-P01_01_POPULATED_EXECUTION_STAGE_LABELLED.png");
  await page.screenshot({ path: p1 });
  record("capture01_sha256", { file: path.basename(p1), sha256: sha256(p1) });

  // ---------- CAPTURE 02: DETAIL RECORD VIA THE SURFACED RUN DETAIL GET ----------
  if (detailButton) {
    const detailBefore = await page
      .locator('[data-testid="execution-detail-panel"]')
      .count()
      .catch(() => 0);
    await detailButton.click();
    await page.waitForSelector('[data-testid="execution-detail-record"]', {
      state: "visible",
      timeout: 10000,
    });
    await page.waitForTimeout(700);
    const detailAfter = await page.locator('[data-testid="execution-detail-panel"]').count();
    const detailText = await page
      .locator('[data-testid="execution-detail-record"]')
      .textContent()
      .catch(() => null);
    record("capture02_detail_panel_mounted", {
      before: detailBefore,
      after: detailAfter,
      recordTextSample: (detailText ?? "").slice(0, 220),
    });
    const fillsHeading = await page.getByText(/^Fills \(\d+\)$/).count();
    record("capture02_detail_fills_heading_present", { count: fillsHeading });
    const p2 = path.join(OUT_DIR, "SURF-P01_02_DETAIL_RECORD_SURFACED_GET.png");
    await page.screenshot({ path: p2 });
    record("capture02_sha256", { file: path.basename(p2), sha256: sha256(p2) });
  }

  // ---------- CAPTURE 03: EMPTY BUNDLE (ALL SEAMS EMPTY), SCROLLED ----------
  const pageEmpty = await context.newPage();
  await installEmptySeams(pageEmpty);
  await pageEmpty.goto("http://localhost:5173/?view=execution", { waitUntil: "domcontentloaded" });
  await pageEmpty.waitForSelector('[data-testid="execution-research-header"]', {
    state: "visible",
    timeout: 15000,
  });
  await pageEmpty.waitForTimeout(2200);

  const emptyMarkers = {};
  for (const marker of [
    "No simulated runs returned.",
    "No simulated fills returned.",
    "No simulated ledger rows returned.",
    "No risk reports returned.",
    "No replay experiments returned.",
    "No analytics reports returned.",
  ]) {
    emptyMarkers[marker] = (await pageEmpty.getByText(marker).count()) > 0;
  }
  const zeroRows = await pageEmpty.getByText("0 rows loaded").count();
  record("capture03_empty_absence_markers", emptyMarkers);
  record("capture03_zero_row_counts", { count: zeroRows });
  record(
    "capture03_source_status_legibility",
    await measureLegibility(
      pageEmpty,
      '[data-testid="execution-source-status"]',
      ".artifact-source-card",
    ),
  );
  record(
    "capture03_counts_legibility",
    await measureLegibility(
      pageEmpty,
      'section[aria-label="Execution research artifact counts"]',
      ".metric-card",
    ),
  );

  // Scroll the stage container to the artifact groups region (honest empty).
  await pageEmpty.locator('[data-testid="execution-group-runs"]').scrollIntoViewIfNeeded();
  await pageEmpty.waitForTimeout(500);
  const scrollMetrics03 = await pageEmpty
    .locator('[data-testid="execution-stage-scroll"]')
    .evaluate((el) => ({ scrollTop: el.scrollTop, scrollHeight: el.scrollHeight, clientHeight: el.clientHeight }));
  const markerInViewport = await pageEmpty
    .getByText("No simulated runs returned.")
    .first()
    .evaluate((el) => {
      const r = el.getBoundingClientRect();
      return r.top >= 0 && r.bottom <= window.innerHeight;
    });
  record("capture03_scroll_metrics", scrollMetrics03);
  record("capture03_emptyMarkerVisibleInViewport", { value: markerInViewport });
  const p3 = path.join(OUT_DIR, "SURF-P01_03_EMPTY_BUNDLE_SCROLLED.png");
  await pageEmpty.screenshot({ path: p3 });
  record("capture03_sha256", { file: path.basename(p3), sha256: sha256(p3) });

  // ---------- CAPTURE 04: SINGLE-SEAM FAILURE -> R4 INDEPENDENT DEGRADATION ----------
  const pageError = await context.newPage();
  await pageError.route(
    /\/api\/v1\/execution-research\/simulated-ledger-entries\?/,
    (route) => route.abort(),
  );
  await pageError.goto("http://localhost:5173/?view=execution", { waitUntil: "domcontentloaded" });
  await pageError.waitForSelector('[data-testid="execution-research-header"]', {
    state: "visible",
    timeout: 15000,
  });
  await pageError.waitForTimeout(2500);
  const errorRows04 = await pageError
    .locator('[data-testid="exec-source-status-error"]')
    .count();
  const readyRows04 = await pageError
    .locator('[data-testid="exec-source-status-ready"]')
    .count();
  const ledgerErrorText = await pageError
    .locator('[data-testid="exec-source-status-error"]')
    .first()
    .textContent()
    .catch(() => null);
  const hubStillRenders =
    (await pageError.locator('[data-testid="execution-group-runs"]').count()) > 0;
  record("capture04_single_seam_failure", {
    errorRows: errorRows04,
    readyRows: readyRows04,
    hubStillRenders,
    ledgerErrorText,
  });
  await pageError.locator('[data-testid="execution-source-status"]').scrollIntoViewIfNeeded();
  await pageError.waitForTimeout(500);
  // OBS-SURF1-1 correction (2026-08-16): the previous instrument relied on
  // scrollIntoViewIfNeeded, which does NOT scroll when the section's top edge
  // is already visible, and measured visibility against window.innerHeight
  // instead of the inner scroll container's visible box. The result was a
  // capture whose filename said SCROLLED while scrollTop stayed 0, and a
  // visibility check that affirmed an element below the fold. Corrected
  // instrument: (1) scroll the INNER container explicitly so the error row is
  // centred in it, (2) measure the row against the CONTAINER's clip rect,
  // (3) re-measure scrollTop AFTER the screenshot to prove the rendered frame
  // matches the recorded state.
  const scrollBefore = await pageError
    .locator('[data-testid="execution-stage-scroll"]')
    .evaluate((el) => el.scrollTop);
  await pageError.evaluate(() => {
    const container = document.querySelector('[data-testid="execution-stage-scroll"]');
    const row = document.querySelector('[data-testid="exec-source-status-error"]');
    if (container && row) {
      const cr = container.getBoundingClientRect();
      const rr = row.getBoundingClientRect();
      container.scrollTop += rr.top + rr.height / 2 - (cr.top + cr.height / 2);
    }
  });
  await pageError.waitForTimeout(500);
  const scrollMetrics04 = await pageError
    .locator('[data-testid="execution-stage-scroll"]')
    .evaluate((el) => ({ scrollTop: el.scrollTop, scrollHeight: el.scrollHeight, clientHeight: el.clientHeight }));
  const errorRowWithinContainer = await pageError
    .locator('[data-testid="exec-source-status-error"]')
    .first()
    .evaluate((el) => {
      const r = el.getBoundingClientRect();
      const container = el.closest('[data-testid="execution-stage-scroll"]');
      const cr = container ? container.getBoundingClientRect() : null;
      const withinContainer = cr ? r.top >= cr.top && r.bottom <= cr.bottom : false;
      return { withinContainer, rowTop: r.top, rowBottom: r.bottom, containerTop: cr ? cr.top : null, containerBottom: cr ? cr.bottom : null };
    });
  record("capture04_scroll_before_explicit_scroll", { value: scrollBefore });
  record("capture04_scroll_metrics", scrollMetrics04);
  record("capture04_errorRowWithinContainer", errorRowWithinContainer);
  record(
    "capture04_source_status_legibility",
    await measureLegibility(
      pageError,
      '[data-testid="execution-source-status"]',
      ".artifact-source-card",
    ),
  );
  const p4 = path.join(OUT_DIR, "SURF-P01_04_SINGLE_SEAM_FAILURE_DEGRADATION_SCROLLED.png");
  await pageError.screenshot({ path: p4 });
  const scrollAfterShot = await pageError
    .locator('[data-testid="execution-stage-scroll"]')
    .evaluate((el) => el.scrollTop);
  record("capture04_scrollTop_after_screenshot", { value: scrollAfterShot });
  record("capture04_sha256", { file: path.basename(p4), sha256: sha256(p4) });

  // ---------- CAPTURE 05: /execution-research REDIRECT LANDING ----------
  await page.goto("http://localhost:5173/execution-research", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(2200);
  const finalUrl = page.url();
  const viewMountedAfterRedirect =
    (await page.locator('[data-testid="execution-research-header"]').count()) > 0;
  const stageAttrAfterRedirect = await page
    .locator('[data-testid="trading-terminal-workspace"]')
    .getAttribute("data-stage-view");
  record("capture05_redirect_final_url", { url: finalUrl });
  record("capture05_redirect_target_state", {
    viewMounted: viewMountedAfterRedirect,
    stageView: stageAttrAfterRedirect,
  });
  const p5 = path.join(OUT_DIR, "SURF-P01_05_EXECUTION_RESEARCH_REDIRECT.png");
  await page.screenshot({ path: p5 });
  record("capture05_sha256", { file: path.basename(p5), sha256: sha256(p5) });

  fs.writeFileSync(
    JSON_OUT,
    JSON.stringify(
      { generated_at: new Date().toISOString(), viewport: "1920x1080", records: LOG },
      null,
      2,
    ),
  );
  console.log("[DONE] verification JSON:", JSON_OUT);
  await browser.close();
}

run().catch((err) => {
  console.error("[FATAL]", err);
  process.exit(1);
});
