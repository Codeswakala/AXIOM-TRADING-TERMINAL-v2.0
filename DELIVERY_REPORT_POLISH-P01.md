# DELIVERY REPORT — POLISH-P01 (final phase: open observations, simulator realism, evidence confluence)

**Delivered by:** AXIOM Development Authority
**To:** ITRGA
**Date:** 2026-08-18
**Build Order:** `BUILD_ORDER_POLISH-P01.md` (sha256 `450c60ced03f97277abe5846af97940a1391280cfa3e645cd4d2715effddf1a3`)
**Base:** 15-element chain (through `chart_p03`)

| Artifact | sha256 |
|---|---|
| `polish_p01.patch` (== `.txt`, `cmp`-identical) | `598d2ac91142f403c467a32ccc17b6fe64dad5e1943c36c251f0efd5a49384e2` |
| Patch format | 1,480 lines · 20 files · LF-only (CR bytes: 0) · terminating newline |
| Pristine apply | 16th element of the chain; `git apply --check` exit 0 in a fresh clone |

## 1. Requirement mapping — M1–M7

| Req | Delivered | Where |
|---|---|---|
| M1 — drift removed | ✅ **Model stated: zero-mean.** The three idio means were zeroed (crypto 0.0004→0, JPY 0.004→0, forex 0.00004→0); sigmas, per-symbol seeds, class factor streams, betas, `_base_price` and provenance markers are untouched (pinned verbatim by `test_polish_p01_mean_terms_are_zero_and_nothing_else_moved`; the DATA-P01 determinism test re-ran UNMODIFIED and green; no CHART expected value edited — the DATA-P01 crypto property test still passes). Measured: six-day EURUSD total return **+30.66% → −0.17%**. The adapter's alternating ticks were already zero-mean — untouched. |
| M2 — code splitting | ✅ Route-level: four workspace pages (LiveMarket, InstitutionalIntelligence, TradePlanning, ManualJournal) and two stage views (ResearchHubView, ExecutionResearchView) are lazy chunks. **Initial chunk 748.05 → 626.51 kB (−121.5 kB, −16.2%)**; split chunks: Intelligence 45.21 · ResearchHub 37.72 · ExecutionResearch 20.67 · TradePlanning 10.16 · ManualJournal 9.44 · LiveMarket 6.15 kB. **RBAC-before-chunk PROVEN**: `GatedRouteElement` checks the registry's existing `allowedRoles` before rendering the lazy component (rendering is what triggers the fetch); unit test mocks the page module and asserts it is never imported for a denied role; capture 07 network-trace shows only the initial bundle fetched with ACCESS DENIED rendered. |
| M3 — watchlist clip | ✅ **Stated choice: labels wrap within the column; values are never wrapped, truncated or ellipsised** (the order barred truncation). The chip, the sparkline provenance tag and the price row wrap; `.item-price-val` stays nowrap. Proven in the MIXED state (long tag machine-recorded): BTC price ink 119.6→197.6, change 188.2→222, range 230→275 — all inside the 239px clip. |
| M4 — orphan | ✅ `ChartPlaceholderPage.tsx` deleted (0 references verified before deletion). |
| M5 — confluence | ✅ **Evidence aggregation only**, per the Operator decision: `computeConfluence` classifies the operator's ACTIVE indicators (declared rule per type — slopes for SMA/EMA/HMA, close-vs-middle for the bands, RSI vs 50, MACD histogram sign, Stochastic %K vs 50, CCI/ROC sign; exclusions STATED, never silent: ADX/ATR/Supertrend/Ichimoku/levels/structure/stats), presents score + Wilson-95% uncertainty band + NON-ACTUATING + "aggregates the operator's currently active indicators over simulated data — not a market opinion." **Refused and absent:** Trade Eligibility, Risk/Reward, Setup Quality as recommendation, entry/stop/target output. Band math pinned by unit test (3/4 → ±0.424). |
| M6 — login + logo | ✅ Login: the existing dimensional scene was strengthened (perspective-tilted frosted card — machine-recorded computed transform `matrix3d`, gradient sheen, reduced-motion fallback). **Logo: a drawing compass with an epsilon symbol beside it** — inline SVG `LogoMark` (no new dependency, currentColor tokens), mounted on the login and the shell brand block, replacing the placeholder AX monogram. |
| M7 — guard | ✅ Anchor pinned; `CONFLUENCE_FORBIDDEN_TERMS` adds `eligible`, `eligibility`, `risk/reward`, `r:r`, `setup quality`, `take the trade`, `high probability setup` plus the standing actuation/institutional vocabulary; asserted at source residue AND at render; discrimination recorded (0/6 pre-fix → 6/6 post-fix). |

## 2. Constraints — R1–R6

R1 ✅ the seeder opened for the mean term ONLY (pinned by the source test); aggregation and all 29 formulae untouched. R2 ✅ 16 routes, registry structure unchanged — the gate ENFORCES the existing `allowedRoles` metadata at render time (a stated consequence: a role outside the list now receives an explicit denial page instead of a page whose APIs 403 — enforcement, not new policy). R3 ✅ no recommendations/verdicts/actuation; the confluence vocabulary is refused at source and render. R4 ✅ vocabulary unchanged. R5 ✅ zero new dependencies — splitting is bundler configuration; the logo is inline SVG. R6 ✅ **initial 626.51 kB · total 755.86 kB** (the split adds ~9 kB of chunk overhead; reported plainly) against 748.05 kB.

## 3. Fail-first demonstration (acceptance 11)

```
pytest tests/test_polish_p01_drift.py  (PRE-FIX)  exit 1 — drift property FAILS:
        EURUSD six-day drift 30.66%  (matches ITRGA's 31.4% measurement)
        + the mean-term pin fails (old means present)
vitest terminalPolishP01.test.tsx     (PRE-FIX)  exit 1 — confluence module absent
guard-extension (PRE-FIX) 0/6 confluence-forbidden terms under test → FAILS; (POST-FIX) 6/6 → PASSES
```

## 4. Executed-test position (fresh transcripts, both trees)

| Run | DA tree | Pristine clone (chain + polish_p01) |
|---|---|---|
| pytest | **476 passed** (`pytest_polish_p01_r1.log`) | **476 passed** (`pytest_polish_p01_verify.log`) |
| vitest | **175 files · 859 passed** (`vitest_polish_p01_r1.log`) | **175 files · 859 passed** (`vitest_polish_p01_verify.log`) |
| tsc -b --force | 0 errors | 0 errors |
| npm run build | `index-N7jYdIYC.js` 626.51 kB | identical hash `1eea48fe…` |

Suite position: **1,335 (476 backend / 859 frontend)** — baseline 1,326 + **9** (+3 backend: drift property, determinism re-run pin, mean-term source pin; +6 frontend: chunk gating ×2, confluence ×2, M7 guard, watchlist CSS anchors). Build JS sha256 identical in both trees.

## 5. Level-I captures (image primary; instruments corroborate)

| Capture | sha256 | Gate result |
|---|---|---|
| 01 drift fixed | `30244fd0cd8fcc503d5faaa6abea01fd2438b273a4039d3a54e0bc63a78eb9a5` | D1 envelope: 5 bars, total return −0.17% (pre-fix +30.7%) ✅ |
| 02 watchlist clip | `f60453e6f3e5387d7329c0dba32faa13edbca2306ff8fe01fbcb32bfb255cca` | MIXED state (long tag recorded); BTC row fully inside the clip ✅ |
| 03 confluence | `a8841236dcfa064cf2626f5a54f365dcaf9b7814fabac0e241bc0b4371a49d4` | score + band + NON-ACTUATING + simulated-data statement; forbidden vocabulary absent ✅ |
| 04 login | `90a6e2e3d18aa20c668949906aa2365a6003625d6b6ac24c9393e4cf3e8e4a50` | logo mounted; card transform `matrix3d` recorded ✅ |
| 05 logo | `ae638b98dc3bf43caf92b85dd3563f06b813007bebe7f753db59db1717f922c0` | compass + epsilon mark legible ✅ |
| 06 route split | `3f581c2a60cb694d49c9de7e16bf6aec5587548a973aebb4e4a877ea93879df` | initial bundle + `InstitutionalIntelligencePage-vt6XKB-Z.js` fetched on navigation ✅ |
| 07 RBAC before chunk | `493256ea975a9702da1a1030f8fcbb29e164533db74d36e00088ea12d42e6b8` | ACCESS DENIED; `intelligenceChunkFetched: false` ✅ |

- `POLISH-P01_CAPTURE_VERIFICATION.json` (Rev A) sha256 `70b4ceef94b54984bfb370a78d2d5c144efe885404df5424d011d025583992d6` (`.txt` `cmp`-identical)
- `POLISH-P01_CAPTURES.html` (self-contained gallery) sha256 `c503c28c430b6a6a4d83b1851dd1cec02aaab784711552265678b6c2e82fcebb`
- Captures 06/07 were taken against the **production build** (`vite preview`, port 4173) — the only way a chunk-level network trace can show real chunk files; a preview proxy block mirroring the dev proxy was added (bundler configuration, stated in the register row).

## 6. Deviations disclosed unprompted (including failed attempts)

1. **Three capture-script defects caught by its own gates:** capture 02's gate measured against the whole dock while the rows container scrolls (BTC row below the fold — the gate now scrolls the rows and asserts the horizontal clip, the actual defect axis); capture 06 recorded zero chunks against the DEV server (dev serves no chunk files — the captures moved to the production preview build); capture 07's unprivileged page shared the admin context's cookies and never reached the login surface (fresh browser context per role — the standing multi-user capture lesson, hit a third time).
2. **Fixture regeneration:** the six-day seed was regenerated with the zero-mean walk (the old fixture carried the +31% drift this phase removes); the feed was stop/cleared/restarted before capture 02 so the watchlist rendered the MIXED provenance state the clip fix exists for (register row `TD-UI-POLISH-P01-EVIDENCE-FIXTURE`).
3. **Sandbox clock jumps** occurred repeatedly during the phase (the sandbox wall clock advanced ~1h between operations), which aged JWT tokens and let the live feed outgrow the 30-bar window; both were re-seeded/re-authenticated and are stated here.
4. **Two test-contract updates caused by M2:** the deep-link tests now await the lazy stage chunks (same assertions, async); the F-BRAND-1 monogram pin now asserts the compass+epsilon mark instead of the retired AX text (the old pin would have been wrong by design).
5. **The Build Order's M6 inventory claim ("no 3D/gradient/perspective treatment") did not match the tree** — the login page already carried a 3D candlestick scene (21 perspective/gradient/transform rules). The DA strengthened the interactive card's depth treatment and added the required logo; the discrepancy is stated rather than argued.
6. **The route gate strengthens existing enforcement:** roles outside a route's `allowedRoles` (e.g. the unprivileged fixture role) now receive an explicit denial page at the route level instead of a page whose APIs 403 — enforcement of the registry metadata that already existed (register row `TD-UI-POLISH-P01-LAZY-ROUTES`).
7. **Dev-environment observation, disclosed:** during capture 07's unprivileged login the backend logged one `audit append failed … no such savepoint: sa_savepoint_1` error (SQLite concurrency in the dev harness — the registered TD-031 class). The login succeeded (HTTP 200), the denial rendered and the capture recorded correctly; nothing in the shipped artifacts depends on that audit row. Not a product defect; noted because the log line is visible in the capture evidence window.

## 7. Acceptance criteria

1–15 addressed as mapped; criterion 14 (patch applies clean on the 15-element chain, sha256 declared and matching) verified in a pristine clone; criterion 15 (bundle initial + total) reported in §2. The artifact of record is the verified patch, not a commit — no commits, pushes or pulls.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This delivery implements POLISH-P01 only. Programme closure is a separate determination after this review.

**We don't guess. We prove.**
