// OBS-SURF1-2 diagnostic: measure computed geometry of the execution stage
// panels and the research stage panels BEFORE any fix.
import { chromium } from "../frontend/node_modules/playwright/index.mjs";

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

async function probe(page, url, label) {
  await page.goto(url, { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(2600);
  const data = await page.evaluate(() => {
    const scroll = document.querySelector(
      '[data-testid="execution-stage-scroll"], [data-testid="research-stage-scroll"]',
    );
    const panels = [...document.querySelectorAll(".panel")].map((el) => {
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      const innerGrid = el.querySelector(".artifact-source-grid, .metric-card-grid");
      const cards = el.querySelectorAll(".artifact-source-card, .metric-card");
      const cardRects = [...cards].map((c) => {
        const cr = c.getBoundingClientRect();
        return { w: Math.round(cr.width), h: Math.round(cr.height) };
      });
      return {
        label: (el.getAttribute("aria-label") || el.querySelector("h2")?.textContent || el.className)
          .slice(0, 48),
        panelH: Math.round(r.height),
        display: cs.display,
        flexShrink: cs.flexShrink,
        minHeight: cs.minHeight,
        innerGridH: innerGrid ? Math.round(innerGrid.getBoundingClientRect().height) : null,
        cardRects,
      };
    });
    return {
      scrollDisplay: scroll ? getComputedStyle(scroll).display : null,
      scrollH: scroll ? Math.round(scroll.getBoundingClientRect().height) : null,
      scrollTop: scroll ? scroll.scrollTop : null,
      scrollHeight: scroll ? scroll.scrollHeight : null,
      panels,
    };
  });
  console.log(`=== ${label} ===`);
  console.log(JSON.stringify(data, null, 2));
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
  await probe(page, "http://localhost:5173/?view=execution", "EXECUTION STAGE (pre-fix)");
  await probe(page, "http://localhost:5173/?view=research", "RESEARCH STAGE (pre-fix, comparison)");
  await browser.close();
}

run().catch((err) => {
  console.error("[FATAL]", err);
  process.exit(1);
});
