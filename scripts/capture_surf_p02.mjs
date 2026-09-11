import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const OUT_DIR = "/home/user/surf_p02_captures";
const JSON_OUT = "/home/user/SURF-P02_CAPTURE_VERIFICATION.json";
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

// OBS-SURF1-2 legibility instrument: card/panel containment within a selector.
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
        panelTop: Math.round(pr.top),
        panelBottom: Math.round(pr.bottom),
        panelH: Math.round(pr.height),
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

  // ---------- CAPTURE 01: RAIL BADGE WITH GENUINE UNREAD COUNT ----------
  await page.goto("http://localhost:5173/", { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="rail-btn-alerts"]', { state: "visible", timeout: 15000 });
  await page.waitForTimeout(2500);
  const badgeText = await page
    .locator('[data-testid="rail-alerts-badge"]')
    .textContent()
    .catch(() => null);
  const alertsAria = await page
    .locator('[data-testid="rail-btn-alerts"]')
    .getAttribute("aria-label");
  record("capture01_rail_badge", { badgeText, ariaLabel: alertsAria });
  const p1 = path.join(OUT_DIR, "SURF-P02_01_RAIL_BADGE_GENUINE_UNREAD_COUNT.png");
  await page.screenshot({ path: p1 });
  record("capture01_sha256", { file: path.basename(p1), sha256: sha256(p1) });

  // ---------- CAPTURE 02: POPULATED ALERTS DOCK, ALL SEVERITIES ----------
  await page.goto("http://localhost:5173/?dock=alerts", { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="monitoring-alerts-panel"]', {
    state: "visible",
    timeout: 15000,
  });
  await page.waitForTimeout(2200);
  const tabSelected = await page
    .locator('[data-testid="right-dock-tab-alerts"]')
    .getAttribute("aria-selected");
  const itemCount = await page.locator('[data-testid^="alert-item-"]').count();
  const severities = await page.locator('[data-testid^="alert-severity-"]').allTextContents();
  const ackButtons = await page.locator('[data-testid^="alert-ack-"]').count();
  record("capture02_dock_state", {
    tabSelected,
    itemCount,
    severities,
    ackButtons,
  });
  record(
    "capture02_panel_legibility",
    await measureLegibility(page, '[data-testid="monitoring-alerts-panel"]', ".alert-list-item"),
  );
  const p2 = path.join(OUT_DIR, "SURF-P02_02_ALERTS_DOCK_POPULATED_SEVERITIES.png");
  await page.screenshot({ path: p2 });
  record("capture02_sha256", { file: path.basename(p2), sha256: sha256(p2) });

  // ---------- CAPTURE 03: ACKNOWLEDGE INTERACTION — BEFORE / AFTER ----------
  const warningAlert = page.locator('[data-testid^="alert-ack-"]').first();
  const warningId = await warningAlert.getAttribute("data-testid");
  await warningAlert.scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);
  // INTERACTION TRACE (mandatory — this control writes): elementFromPoint on
  // click-time geometry before a real Playwright click.
  const hitTestOwnsPointer = await warningAlert.evaluate((el) => {
    const r = el.getBoundingClientRect();
    const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return top === el || el.contains(top);
  });
  const badgeBefore = await page
    .locator('[data-testid="rail-alerts-badge"]')
    .textContent()
    .catch(() => null);
  const itemBefore = await page
    .locator(`[data-testid="${warningId.replace("alert-ack-", "alert-item-")}"]`)
    .textContent();
  record("capture03_before", {
    targetTestId: warningId,
    hitTestOwnsPointer,
    badgeBefore,
    itemAckState: itemBefore ? itemBefore.slice(-20) : null,
  });
  const p3a = path.join(OUT_DIR, "SURF-P02_03a_ACKNOWLEDGE_BEFORE.png");
  await page.screenshot({ path: p3a });
  record("capture03a_sha256", { file: path.basename(p3a), sha256: sha256(p3a) });

  await warningAlert.click();
  await page.waitForTimeout(1800);
  const badgeAfter = await page
    .locator('[data-testid="rail-alerts-badge"]')
    .textContent()
    .catch(() => null);
  const itemAfter = await page
    .locator(`[data-testid="${warningId.replace("alert-ack-", "alert-item-")}"]`)
    .textContent();
  const ackButtonsAfter = await page.locator('[data-testid^="alert-ack-"]').count();
  record("capture03_after", {
    badgeAfter,
    itemAckState: itemAfter ? itemAfter.slice(-20) : null,
    ackButtonsRemaining: ackButtonsAfter,
  });
  const p3b = path.join(OUT_DIR, "SURF-P02_03b_ACKNOWLEDGE_AFTER.png");
  await page.screenshot({ path: p3b });
  record("capture03b_sha256", { file: path.basename(p3b), sha256: sha256(p3b) });

  // ---------- CAPTURE 04: EMPTY STATE (SEAM FULFILLED EMPTY), SCROLLED ----------
  const pageEmpty = await context.newPage();
  await pageEmpty.route(/\/api\/v1\/alerts\?/, (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: "[]" }),
  );
  await pageEmpty.goto("http://localhost:5173/?dock=alerts", { waitUntil: "domcontentloaded" });
  await pageEmpty.waitForSelector('[data-testid="monitoring-alerts-panel"]', {
    state: "visible",
    timeout: 15000,
  });
  await pageEmpty.waitForTimeout(2000);
  const emptyVisible = await pageEmpty
    .locator('[data-testid="alerts-empty"]')
    .textContent()
    .catch(() => null);
  const badgeAbsentWhenZero = (await pageEmpty.locator('[data-testid="rail-alerts-badge"]').count()) === 0;
  record("capture04_empty_state", { emptyText: emptyVisible, badgeAbsentWhenZero });
  await pageEmpty.locator('[data-testid="alerts-empty"]').scrollIntoViewIfNeeded();
  await pageEmpty.waitForTimeout(400);
  const emptyInViewport = await pageEmpty
    .locator('[data-testid="alerts-empty"]')
    .evaluate((el) => {
      const r = el.getBoundingClientRect();
      return r.top >= 0 && r.bottom <= window.innerHeight;
    });
  record("capture04_emptyMarkerVisibleInViewport", { value: emptyInViewport });
  const p4 = path.join(OUT_DIR, "SURF-P02_04_EMPTY_STATE_SCROLLED.png");
  await pageEmpty.screenshot({ path: p4 });
  record("capture04_sha256", { file: path.basename(p4), sha256: sha256(p4) });

  // ---------- CAPTURE 05: LOAD FAILURE — INDEPENDENT DEGRADATION ----------
  const pageError = await context.newPage();
  await pageError.route(/\/api\/v1\/alerts\?/, (route) => route.abort());
  await pageError.goto("http://localhost:5173/?dock=alerts", { waitUntil: "domcontentloaded" });
  await pageError.waitForSelector('[data-testid="alerts-load-error"]', {
    state: "visible",
    timeout: 15000,
  });
  await pageError.waitForTimeout(1800);
  const errorText = await pageError
    .locator('[data-testid="alerts-load-error"]')
    .textContent()
    .catch(() => null);
  const badgeAbsent = (await pageError.locator('[data-testid="rail-alerts-badge"]').count()) === 0;
  const shellIntact =
    (await pageError.locator('[data-testid="trading-terminal-workspace"]').count()) > 0 &&
    (await pageError.locator('[data-testid="terminal-chart-stage"]').count()) > 0;
  record("capture05_load_failure", { errorText, badgeAbsent, shellIntact });
  const p5 = path.join(OUT_DIR, "SURF-P02_05_LOAD_FAILURE_DEGRADATION.png");
  await pageError.screenshot({ path: p5 });
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
