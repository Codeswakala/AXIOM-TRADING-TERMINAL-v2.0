// DA page-capture tooling — Operator request (2026-08-19): capture every
// webpage of the running AXIOM app into .html files.
//
// Each capture is the SERIALIZED RENDERED DOM (post-hydration, post-data):
//   - dev-mode styles are injected <style> blocks, so the snapshots ARE styled
//   - the Operator-supplied logo is inlined as a data URI so it displays
//   - <script src> tags are stripped (they would 404 when opened standalone)
// A capture is a static record of what rendered, not a runnable app.
// A manifest (JSON) lists every file with its requested URL, final URL,
// capture time and sha256.
import { chromium } from "../frontend/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const BASE = "http://localhost:5173";
const OUT_DIR = "/home/user/axiom_page_captures";
const MANIFEST = "/home/user/axiom_page_captures_manifest.json";
const manifest = [];

fs.mkdirSync(OUT_DIR, { recursive: true });

function sha256(text) {
  return crypto.createHash("sha256").update(text).digest("hex");
}

async function login(page, username = "admin") {
  await page.goto(`${BASE}/login`, { waitUntil: "domcontentloaded" });
  await page.waitForSelector('input[data-testid="login-username-input"], input#username-input', {
    timeout: 20000,
  });
  await page
    .locator('input[data-testid="login-username-input"], input#username-input')
    .first()
    .fill(username);
  await page
    .locator('input[data-testid="login-password-input"], input#password-input')
    .first()
    .fill(username === "admin" ? "AxiomSecurePass2026!" : "operator-pass-123");
  await page.click('button[type="submit"]');
  await page.waitForTimeout(3000);
}

async function capture(page, entry) {
  const { file, url, waitSelector, waitClass, settleMs = 2500, note, expect: expectMarker, postAction } = entry;
  const maxAttempts = 3;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const errors = [];
    page.removeAllListeners("pageerror");
    page.on("pageerror", (e) => errors.push(String(e).slice(0, 160)));
    await page.goto(`${BASE}${url}`, { waitUntil: "domcontentloaded", timeout: 60000 });
    if (waitSelector) {
      await page.waitForSelector(waitSelector, { timeout: 20000 }).catch(() => {});
    }
    if (waitClass) {
      await page.waitForSelector(waitClass, { timeout: 20000 }).catch(() => {});
    }
    // Allow lazy chunks + data fetches to settle.
    await page.waitForTimeout(settleMs);
    await page
      .waitForSelector('[data-testid="route-loading"]', { state: "detached", timeout: 15000 })
      .catch(() => {});

    // Post-action hook: build indicator state AFTER the navigation (a pre-go
    // click would be wiped by the page load).
    if (postAction === "activate-sma20") {
      await page.click('[data-testid="overlay-sma20"]').catch(() => {});
      await page
        .waitForSelector('[data-testid="indicator-status-sma20"]', { timeout: 15000 })
        .catch(() => {});
      await page
        .waitForSelector('[data-testid="confluence-strip"]', { timeout: 15000 })
        .catch(() => {});
      await page.waitForTimeout(1000);
    }

    const finalUrl = page.url().replace(BASE, "");
    // Inline the logo (so the captured file shows the mark standalone) and
    // strip broken module scripts (dev-server URLs 404 outside the server).
    const html = await page.evaluate(async () => {
    const doc = document;
    const logo = doc.querySelector('img[src="/branding/axiom-logo.png"]');
    let logoData = null;
    if (logo) {
      try {
        const res = await fetch("/branding/axiom-logo.png");
        const blob = await res.blob();
        logoData = await new Promise((resolve) => {
          const r = new FileReader();
          r.onloadend = () => resolve(r.result);
          r.readAsDataURL(blob);
        });
        logo.setAttribute("src", logoData);
      } catch {
        logoData = null;
      }
    }
    const clone = doc.documentElement.cloneNode(true);
    // Revert the live DOM mutation so the running page is unaffected.
    if (logo && logoData) logo.setAttribute("src", "/branding/axiom-logo.png");
    // Serialize from the clone (with the inlined logo).
    const serializer = new XMLSerializer();
    let out = "<!DOCTYPE html>\n" + serializer.serializeToString(clone);
    // Strip external module scripts (would 404 standalone); keep everything else.
    out = out.replace(/<script\b[^>]*>[\s\S]*?<\/script>/g, "");
    return out;
  });

    const metaComment = `<!-- AXIOM PAGE CAPTURE
  requested: ${url}
  final URL: ${finalUrl}
  captured: ${new Date().toISOString()}
  note: ${note}
  page errors: ${errors.length ? errors.join(" | ") : "none"}
-->`;
    const finalHtml = metaComment + "\n" + html;

    // Verification gate: if a required marker is missing (empty root from a
    // transient dev-server race, or a state that never rendered), retry.
    if (expectMarker && !finalHtml.includes(expectMarker)) {
      console.log(
        `[RETRY]  ${file} attempt ${attempt}/${maxAttempts} — expected marker "${expectMarker}" absent (${(Buffer.byteLength(finalHtml) / 1024).toFixed(0)} kB)`,
      );
      if (attempt < maxAttempts) continue;
      throw new Error(`CAPTURE GATE FAILED for ${file}: "${expectMarker}" never appeared`);
    }

    const outPath = path.join(OUT_DIR, file);
    fs.writeFileSync(outPath, finalHtml);
    manifest.push({
      file,
      requestedUrl: url,
      finalUrl,
      capturedAt: new Date().toISOString(),
      sha256: sha256(finalHtml),
      bytes: Buffer.byteLength(finalHtml),
      pageErrors: errors,
      note,
    });
    console.log(
      `[CAPTURE] ${file.padEnd(46)} | ${finalUrl.padEnd(26)} | ${(Buffer.byteLength(finalHtml) / 1024).toFixed(0)} kB | errors: ${errors.length}`,
    );
    return;
  }
}

async function run() {
  const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });

  // --- Logged-out page -----------------------------------------------------
  {
    const page = await context.newPage();
    await page.goto(`${BASE}/login`, { waitUntil: "domcontentloaded" });
    await page.waitForSelector('[data-testid="login-page-container"]', { timeout: 20000 });
    await page.waitForTimeout(1500);
    const html = await page.evaluate(async () => {
      const logo = document.querySelector('img[src="/branding/axiom-logo.png"]');
      let logoData = null;
      if (logo) {
        try {
          const blob = await (await fetch("/branding/axiom-logo.png")).blob();
          logoData = await new Promise((resolve) => {
            const r = new FileReader();
            r.onloadend = () => resolve(r.result);
            r.readAsDataURL(blob);
          });
        } catch { /* keep as-is */ }
      }
      const clone = document.documentElement.cloneNode(true);
      if (logo && logoData) clone.querySelector('img[src="/branding/axiom-logo.png"]')?.setAttribute("src", logoData);
      let out = "<!DOCTYPE html>\n" + new XMLSerializer().serializeToString(clone);
      out = out.replace(/<script\b[^>]*>[\s\S]*?<\/script>/g, "");
      return out;
    });
    const finalUrl = page.url().replace(BASE, "");
    const meta = `<!-- AXIOM PAGE CAPTURE
  requested: /login
  final URL: ${finalUrl}
  captured: ${new Date().toISOString()}
  note: Logged-out sign-in surface (governance chips + Operator logo)
  page errors: none
-->`;
    const finalHtml = meta + "\n" + html;
    fs.writeFileSync(path.join(OUT_DIR, "01-login-logged-out.html"), finalHtml);
    manifest.push({
      file: "01-login-logged-out.html", requestedUrl: "/login", finalUrl,
      capturedAt: new Date().toISOString(), sha256: sha256(finalHtml),
      bytes: Buffer.byteLength(finalHtml), pageErrors: [], note: "Logged-out sign-in surface",
    });
    console.log(`[CAPTURE] 01-login-logged-out.html | logged-out`);
    await page.close();
  }

  // --- Authenticated captures (admin) --------------------------------------
  const page = await context.newPage();
  await login(page, "admin");

  const terminalWait = '[data-testid="terminal-watchlist-dock"]';
  const captures = [
    { file: "02-terminal-home.html", url: "/", waitSelector: terminalWait, note: "Terminal workspace (Operations dashboard)" },
    { file: "03-live-market.html", url: "/live", waitClass: ".panel-grid", expect: "panel-grid", note: "Live Market workspace (lazy chunk)" },
    { file: "04-intelligence.html", url: "/intelligence", waitClass: ".intelligence-card", expect: "intelligence-card", note: "Institutional Intelligence workspace (lazy chunk)" },
    { file: "05-trade-plans.html", url: "/trade-plans", waitClass: ".field", note: "Trade Plans workspace (lazy chunk)" },
    { file: "06-journal.html", url: "/journal", waitClass: ".journal-actions", expect: "journal-actions", note: "Manual Journal workspace (lazy chunk)" },
    { file: "07-redirect-charts.html", url: "/charts", waitSelector: terminalWait, expect: "terminal-watchlist-dock", note: "/charts redirect -> /?view=chart (chart stage)" },
    { file: "08-redirect-chart-alias.html", url: "/chart", waitSelector: terminalWait, note: "/chart alias redirect -> /?view=chart" },
    { file: "09-redirect-signals.html", url: "/signals", waitSelector: terminalWait, note: "/signals redirect -> /?dock=signals" },
    { file: "10-redirect-analytics.html", url: "/analytics", waitSelector: terminalWait, note: "/analytics redirect -> /?dock=intelligence" },
    { file: "11-redirect-investigate.html", url: "/investigate", waitSelector: terminalWait, note: "/investigate redirect -> /?dock=signals" },
    { file: "12-redirect-compare-scenarios.html", url: "/compare-scenarios", waitSelector: terminalWait, note: "/compare-scenarios redirect -> /?panel=scenarios" },
    { file: "13-redirect-execution-research.html", url: "/execution-research", waitSelector: terminalWait, note: "/execution-research redirect -> /?view=execution" },
    { file: "14-redirect-portfolio-research.html", url: "/portfolio-research", waitSelector: terminalWait, note: "/portfolio-research redirect -> /?panel=portfolio" },
    { file: "15-redirect-research-management.html", url: "/research-management", waitSelector: terminalWait, note: "/research-management redirect -> /?view=research" },
    { file: "16-redirect-governance.html", url: "/governance", waitSelector: terminalWait, expect: "governance-overlay", note: "/governance redirect -> /?open=governance" },
    { file: "17-redirect-workspace-settings.html", url: "/workspace", waitSelector: terminalWait, expect: "ix-settings-overlay", note: "/workspace redirect -> /?open=settings" },
    { file: "18-view-research-stage.html", url: "/?view=research", waitSelector: '[data-testid="research-stage-scroll"]', expect: "research-stage-scroll", note: "Research Hub stage view (lazy chunk)" },
    { file: "19-view-execution-stage.html", url: "/?view=execution", waitSelector: '[data-testid="execution-stage-scroll"]', expect: "execution-stage-scroll", note: "Execution Research stage view (lazy chunk)" },
    { file: "20-view-chart-stage.html", url: "/?view=chart", waitSelector: terminalWait, note: "Chart stage view" },
    { file: "21-dock-signals.html", url: "/?dock=signals", waitSelector: terminalWait, note: "Terminal with SIGNALS dock active" },
    { file: "22-dock-telemetry.html", url: "/?dock=telemetry", waitSelector: terminalWait, note: "Terminal with TELEMETRY dock active" },
    { file: "23-dock-intelligence.html", url: "/?dock=intelligence", waitSelector: terminalWait, note: "Terminal with INTELLIGENCE dock active" },
    { file: "24-dock-alerts.html", url: "/?dock=alerts", waitSelector: terminalWait, note: "Terminal with ALERTS dock active" },
    { file: "25-panel-scenarios.html", url: "/?panel=scenarios", waitSelector: terminalWait, note: "Terminal with SCENARIOS panel active" },
    { file: "26-panel-portfolio.html", url: "/?panel=portfolio", waitSelector: terminalWait, note: "Terminal with PORTFOLIO panel active" },
    { file: "27-open-settings.html", url: "/?open=settings", waitSelector: '[data-testid="settings-overlay"], [class*="settings-overlay"]', expect: "ix-settings-overlay", note: "Terminal with workspace settings overlay open" },
    { file: "28-open-governance.html", url: "/?open=governance", waitSelector: '[data-testid="governance-overlay"], [class*="governance-overlay"]', expect: "governance-overlay", note: "Terminal with governance overlay open" },
    { file: "29-indicators-active.html", url: "/", waitSelector: terminalWait, settleMs: 1500, postAction: "activate-sma20", expect: "confluence-strip", note: "Terminal with SMA 20 active + evidence confluence strip" },
  ];

  for (const entry of captures) {
    await capture(page, entry);
  }

  await page.close();

  // --- Unprivileged access-denied capture (fresh context per role) ----------
  {
    const unauthContext = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
    const upage = await unauthContext.newPage();
    await login(upage, "surf-p03-unprivileged-028efc57");
    await upage.goto(`${BASE}/intelligence`, { waitUntil: "domcontentloaded" });
    await upage.waitForSelector('[data-testid="route-access-denied"]', { timeout: 20000 });
    await upage.waitForTimeout(1500);
    const html = await upage.evaluate(() => {
      const clone = document.documentElement.cloneNode(true);
      let out = "<!DOCTYPE html>\n" + new XMLSerializer().serializeToString(clone);
      out = out.replace(/<script\b[^>]*>[\s\S]*?<\/script>/g, "");
      return out;
    });
    const finalUrl = upage.url().replace(BASE, "");
    const meta = `<!-- AXIOM PAGE CAPTURE
  requested: /intelligence (unprivileged role)
  final URL: ${finalUrl}
  captured: ${new Date().toISOString()}
  note: RBAC access-denied page — the intelligence chunk is NEVER fetched for this role
  page errors: none
-->`;
    const finalHtml = meta + "\n" + html;
    fs.writeFileSync(path.join(OUT_DIR, "30-access-denied-unprivileged.html"), finalHtml);
    manifest.push({
      file: "30-access-denied-unprivileged.html", requestedUrl: "/intelligence (unprivileged)",
      finalUrl, capturedAt: new Date().toISOString(), sha256: sha256(finalHtml),
      bytes: Buffer.byteLength(finalHtml), pageErrors: [], note: "RBAC denial page",
    });
    console.log(`[CAPTURE] 30-access-denied-unprivileged.html | denied`);
    await unauthContext.close();
  }

  fs.writeFileSync(MANIFEST, JSON.stringify({ generatedAt: new Date().toISOString(), captures: manifest }, null, 2));
  console.log("[DONE] manifest:", MANIFEST, "| files:", manifest.length);
  await browser.close();
}

run().catch((err) => {
  console.error("[FATAL]", err);
  process.exit(1);
});
