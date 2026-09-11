import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const OUT_DIR = "/home/user/surf_p03_captures";
const JSON_OUT = "/home/user/SURF-P03_CAPTURE_VERIFICATION.json";
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

async function login(page, username, password) {
  await page.goto("http://localhost:5173/login", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(900);
  await page
    .locator('input[data-testid="login-username-input"], input#username-input')
    .first()
    .fill(username);
  await page
    .locator('input[data-testid="login-password-input"], input#password-input')
    .first()
    .fill(password);
  await page.click('button[type="submit"]');
  await page.waitForTimeout(2500);
}

async function openGovernance(page) {
  await page.goto("http://localhost:5173/?open=governance", { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="governance-overlay-body"]', {
    state: "visible",
    timeout: 15000,
  });
  await page.waitForSelector('[data-testid="platform-records-section"]', {
    state: "attached",
    timeout: 20000,
  });
  await page.waitForTimeout(2500);
}

// OBS-SURF1-2 legibility instrument: containment of cards within a panel.
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
      return {
        panelH: Math.round(pr.height),
        cardCount: cardRects.length,
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

  // Each role logs in with a FRESH browser context (auth state is per-origin
  // and shared across pages of one context — a second login on the same
  // context is already authenticated and never reaches the login form).
  async function newSession(username, password) {
    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      deviceScaleFactor: 1,
    });
    const page = await context.newPage();
    await login(page, username, password);
    return page;
  }

  // ---------- CAPTURE 01: ADMIN — POPULATED PLATFORM RECORDS ----------
  const pageAdmin = await newSession("admin", "AxiomSecurePass2026!");
  await openGovernance(pageAdmin);
  const routeEntries = await pageAdmin.locator('[data-testid^="platform-route-entry-"]').count();
  const roleEntries = await pageAdmin.locator('[data-testid^="platform-role-"]').count();
  const catalogueEntries = await pageAdmin.locator('[data-testid^="platform-catalogue-entry-"]').count();
  const contractEntries = await pageAdmin.locator('[data-testid^="platform-contract-entry-"]').count();
  const scopeRecords = await pageAdmin.locator('[data-testid^="platform-scope-record-"]').count();
  const readyRows = await pageAdmin.locator('[data-testid="platform-source-status-ready"]').count();
  const deniedRows = await pageAdmin.locator('[data-testid="platform-source-status-denied"]').count();
  record("capture01_admin_counts", {
    routeEntries,
    roleEntries,
    catalogueEntries,
    contractEntries,
    scopeRecords,
    readyRows,
    deniedRows,
  });
  await pageAdmin.locator('[data-testid="platform-records-section"]').scrollIntoViewIfNeeded();
  await pageAdmin.waitForTimeout(400);
  record(
    "capture01_source_status_legibility",
    await measureLegibility(pageAdmin, '[data-testid="platform-source-status"]', ".artifact-source-card"),
  );
  const p1 = path.join(OUT_DIR, "SURF-P03_01_PLATFORM_RECORDS_POPULATED.png");
  await pageAdmin.screenshot({ path: p1 });
  record("capture01_sha256", { file: path.basename(p1), sha256: sha256(p1) });

  // ---------- CAPTURE 02: ADMIN — SCOPE DETAIL INTERACTION ----------
  const scopeDetailButton = pageAdmin.locator('[data-testid^="platform-scope-detail-open-"]').first();
  await scopeDetailButton.scrollIntoViewIfNeeded();
  await pageAdmin.waitForTimeout(400);
  // INTERACTION TRACE: elementFromPoint at click-time geometry before the
  // real Playwright click (item-4 method).
  const hitTestOwnsPointer = await scopeDetailButton.evaluate((el) => {
    const r = el.getBoundingClientRect();
    const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return top === el || el.contains(top);
  });
  record("capture02_scope_detail_hitTestBeforeClick", { value: hitTestOwnsPointer });
  const detailBefore = await pageAdmin.locator('[data-testid="platform-scope-detail-record"]').count();
  await scopeDetailButton.click();
  await pageAdmin.waitForSelector('[data-testid="platform-scope-detail-record"]', {
    state: "visible",
    timeout: 10000,
  });
  await pageAdmin.waitForTimeout(600);
  const detailAfter = await pageAdmin.locator('[data-testid="platform-scope-detail-record"]').count();
  const detailText = await pageAdmin
    .locator('[data-testid="platform-scope-detail-record"]')
    .textContent()
    .catch(() => null);
  record("capture02_scope_detail_landed", {
    detailBefore,
    detailAfter,
    detailTextSample: (detailText ?? "").slice(0, 160),
  });
  await pageAdmin.locator('[data-testid="platform-scope-records"]').scrollIntoViewIfNeeded();
  await pageAdmin.waitForTimeout(300);
  const p2 = path.join(OUT_DIR, "SURF-P03_02_SCOPE_DETAIL_INTERACTION.png");
  await pageAdmin.screenshot({ path: p2 });
  record("capture02_sha256", { file: path.basename(p2), sha256: sha256(p2) });

  // ---------- CAPTURE 03: OPERATOR ROLE — REAL BACKEND PARTIAL DENIAL ----------
  const pageOperator = await newSession("w7-u06-a-0a16e141", "operator-pass-123");
  await openGovernance(pageOperator);
  const opErrorRows = await pageOperator.locator('[data-testid="platform-source-status-error"]').count();
  const opReadyRows = await pageOperator.locator('[data-testid="platform-source-status-ready"]').count();
  const routeErrorText = await pageOperator
    .locator('[data-testid="platform-route-inventory-error"]')
    .textContent()
    .catch(() => null);
  const rbacErrorText = await pageOperator
    .locator('[data-testid="platform-rbac-error"]')
    .textContent()
    .catch(() => null);
  const opScopeVisible = await pageOperator
    .locator('[data-testid="platform-scope-list"]')
    .count();
  record("capture03_operator_role_real_backend_denial", {
    errorRows: opErrorRows,
    readyRows: opReadyRows,
    routeErrorText,
    rbacErrorText,
    scopeListRendered: opScopeVisible > 0,
  });
  await pageOperator.locator('[data-testid="platform-source-status"]').scrollIntoViewIfNeeded();
  await pageOperator.waitForTimeout(300);
  const p3 = path.join(OUT_DIR, "SURF-P03_03_OPERATOR_ROLE_REAL_403_PARTIAL_DENIAL.png");
  await pageOperator.screenshot({ path: p3 });
  record("capture03_sha256", { file: path.basename(p3), sha256: sha256(p3) });

  // ---------- CAPTURE 04: UNPRIVILEGED — M3 SCOPE ACCESS-DENIED NOTICE ----------
  const pageUnpriv = await newSession("surf-p03-unprivileged-028efc57", "operator-pass-123");
  await openGovernance(pageUnpriv);
  const deniedNotice = await pageUnpriv
    .locator('[data-testid="platform-scope-access-denied"]')
    .textContent()
    .catch(() => null);
  const deniedSourceRows = await pageUnpriv
    .locator('[data-testid="platform-source-status-denied"]')
    .count();
  const scopeErrorRows = await pageUnpriv.locator('[data-testid="platform-source-status-error"]').count();
  const scopeEmptyPresent = (await pageUnpriv.locator('[data-testid="platform-scope-empty"]').count()) > 0;
  record("capture04_unprivileged_m3_access_denied", {
    deniedNoticeText: (deniedNotice ?? "").slice(0, 200),
    deniedSourceRows,
    errorSourceRows: scopeErrorRows,
    emptyStateRendered: scopeEmptyPresent,
  });
  await pageUnpriv.locator('[data-testid="platform-scope-records"]').scrollIntoViewIfNeeded();
  await pageUnpriv.waitForTimeout(300);
  const p4 = path.join(OUT_DIR, "SURF-P03_04_UNPRIVILEGED_SCOPE_403_ACCESS_DENIED.png");
  await pageUnpriv.screenshot({ path: p4 });
  record("capture04_sha256", { file: path.basename(p4), sha256: sha256(p4) });

  // ---------- CAPTURE 05: EMPTY (ALL SEAMS FULFILLED EMPTY), SCROLLED ----------
  const pageEmpty = await newSession("admin", "AxiomSecurePass2026!");
  const emptyRoute = {
    service: "institutional_platform",
    version: "v1",
    routes: [],
    actuation_surface_present: false,
    governance_gate_capability_present: false,
  };
  const emptyRbac = { policy: "default_deny", roles: {}, forbidden_capabilities_present: false };
  const emptyCatalogue = {
    service: "institutional_platform",
    catalogue_version: "v1",
    api_version: "v1",
    routes: [],
    route_count: 0,
    actuation_surface_present: false,
    governance_gate_capability_present: false,
    abuse_guard: { status: "engaged", reason: "default_deny_abuse_guard" },
    persistence: { catalogue_table_persisted: true, alembic_head_expected: "20260717_0037" },
  };
  const emptyPlugins = {
    service: "institutional_platform_plugin_contracts",
    contract_version: "v1",
    contracts: [],
    capability_allowlist: [],
    dynamic_code_execution_enabled: false,
    third_party_plugin_execution_enabled: false,
    plugin_execution_audit_table_present: false,
    governance_gate_capability_present: false,
  };
  await pageEmpty.route(/\/api\/v1\/institutional-platform\/route-inventory/, (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(emptyRoute) }),
  );
  await pageEmpty.route(/\/api\/v1\/institutional-platform\/rbac\/permissions/, (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(emptyRbac) }),
  );
  await pageEmpty.route(/\/api\/v1\/institutional-platform\/api-catalogue/, (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(emptyCatalogue) }),
  );
  await pageEmpty.route(/\/api\/v1\/institutional-platform\/plugin-contracts/, (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(emptyPlugins) }),
  );
  await pageEmpty.route(/\/api\/v1\/institutional-platform\/operator-scope-records\??/, (r) =>
    r.fulfill({ status: 200, contentType: "application/json", body: "[]" }),
  );
  await openGovernance(pageEmpty);
  const emptyMarkers = {};
  for (const marker of [
    "No route inventory records returned.",
    "No role permission records returned.",
    "No API catalogue records returned.",
    "No plugin contract records returned.",
    "No scope records returned for this operator.",
  ]) {
    emptyMarkers[marker] = (await pageEmpty.getByText(marker).count()) > 0;
  }
  record("capture05_empty_absence_markers", emptyMarkers);
  await pageEmpty.locator('[data-testid="platform-route-inventory-empty"]').scrollIntoViewIfNeeded();
  await pageEmpty.waitForTimeout(300);
  const emptyInViewport = await pageEmpty
    .locator('[data-testid="platform-route-inventory-empty"]')
    .evaluate((el) => {
      const r = el.getBoundingClientRect();
      return r.top >= 0 && r.bottom <= window.innerHeight;
    });
  record("capture05_emptyMarkerVisibleInViewport", { value: emptyInViewport });
  const p5 = path.join(OUT_DIR, "SURF-P03_05_EMPTY_COLLECTIONS_SCROLLED.png");
  await pageEmpty.screenshot({ path: p5 });
  record("capture05_sha256", { file: path.basename(p5), sha256: sha256(p5) });

  // ---------- CAPTURE 06: SINGLE-SEAM FAILURE — INDEPENDENT DEGRADATION ----------
  const pageError = await newSession("admin", "AxiomSecurePass2026!");
  await pageError.route(/\/api\/v1\/institutional-platform\/api-catalogue/, (r) => r.abort());
  await openGovernance(pageError);
  const errRows = await pageError.locator('[data-testid="platform-source-status-error"]').count();
  const readyRows06 = await pageError.locator('[data-testid="platform-source-status-ready"]').count();
  const catalogueErrorText = await pageError
    .locator('[data-testid="platform-api-catalogue-error"]')
    .textContent()
    .catch(() => null);
  const othersRender =
    (await pageError.locator('[data-testid^="platform-route-entry-"]').count()) > 0 &&
    (await pageError.locator('[data-testid^="platform-role-"]').count()) > 0;
  record("capture06_single_seam_failure", {
    errorRows: errRows,
    readyRows: readyRows06,
    catalogueErrorText,
    othersRender,
  });
  await pageError.locator('[data-testid="platform-source-status"]').scrollIntoViewIfNeeded();
  await pageError.waitForTimeout(300);
  const p6 = path.join(OUT_DIR, "SURF-P03_06_SINGLE_SEAM_FAILURE_DEGRADATION.png");
  await pageError.screenshot({ path: p6 });
  record("capture06_sha256", { file: path.basename(p6), sha256: sha256(p6) });

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
