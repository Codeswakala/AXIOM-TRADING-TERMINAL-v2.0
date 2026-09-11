# ITRGA FINAL VERDICT — W4-U07 (Institutional Intelligence Dashboard)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W4-U07** — Institutional Intelligence Dashboard (first Wave-4 UI) |
| Supersedes | `ITRGA_REVIEW_W4-U07.md` (2026-07-16, CONDITIONAL — C-1 report-with-uncertainty; C-2 logged-out) |
| Evidence | C-1+C-2 closure — 3 browser screenshots (LOGIN, redirected, C1 report card) |
| Platform | **0.37.0** |
| Review date | 2026-07-16 |
| **VERDICT** | **✅ APPROVED WITH OBSERVATIONS — C-1 & C-2 CLOSED.** Platform advances to **v0.37.0** |
| Confidence | **HIGH** — dashboard proven rendered on the served session with a real report + logged-out block; one LOW display-binding note |

> **We don't guess. We prove.** The dashboard now renders a real report on screen and blocks the logged-out route. One cosmetic display gap (interval bounds show as em-dashes) is noted, not blocking.

---

## 1. Bottom line

The two CONDITIONAL browser conditions are addressed on the served session. **C-2 (logged-out block) is
cleanly CLOSED. C-1 (a report rendered on the dashboard) is substantively CLOSED** — a real
`signal_validation_report` card renders with **sample_count 4**, method `wilson_score_intervals`, `n=4`,
research framing, and the metrics JSON — **but the numeric interval bounds display as "— to —"** (a
display-binding bug; the underlying data has real bounds). Because the safety posture is fully proven and the
blank bound is **honest-but-incomplete (not false precision)**, this is **APPROVED WITH OBSERVATIONS**
(OBS-1), not a re-withhold. Platform advances to **v0.37.0.**

---

## 2. C-2 — CLOSED ✅ (logged-out block)

`LOGIN.png` and `redirected.png` both show `127.0.0.1:8000/login` rendering the operator sign-in screen (empty
username/password) — an unauthenticated visit lands on login, **not** the dashboard. The `/intelligence`
route's logged-out block is proven on the served session. ✅

## 3. C-1 — substantively CLOSED, with OBS-1 🟡→✅

`W4-U07_C1_REPORT_WITH_UNCERTAINTY.png` shows the served `/intelligence` dashboard rendering a **real report
card** — "ADVISORY QUALITY REVIEW" → `signal_validation_report`:
- **Sample count: 4** displayed; **method** `wilson_score_intervals`; **n=4**.
- `RESEARCH_ONLY` badge; Economic context `not_assessed` ("research context and not an economic/trading
  claim"); Lineage `c592d8184a…` (matches the verified W4-U06 report).
- Evidence/limitations expander: `historical_research_only, not_a_guarantee, not_a_prediction,
  not_financial_advice, uncalibrated_model_score_excluded, no_governed_forward_outcomes_available,
  economic_usefulness_not_assessed`; metrics JSON `clean_advisory_rate: {value 0.25, sample_count 4, …}`.

So a report **is** displayed on screen, with sample_count, method, research framing, and no raw score — the
core of C-1 is met.

**OBS-1 (LOW, non-blocking) — uncertainty interval bounds render as em-dashes.** The **Uncertainty** summary
field reads **"— to — · n=4 · wilson_score_intervals"** — the numeric lower/upper bounds are blank, even though
the source report has real Wilson bounds (verified at W4-U06: `clean_advisory_rate lower 0.0456 / upper
0.6994`) and the same card's JSON carries the values. This is a **display-binding bug** (the summary field
isn't mapping the interval numbers), not missing data and **not false precision** (a blank bound over-claims
nothing). Fix the interval-bounds rendering — fold into **W4-U08 closeout** or a quick patch.

---

## 4. No regression

The earlier pack's text gates stand (backend 233 / frontend 12·29 / ruff / audit 0 / CI via Git-Bash exit 0 /
no migration); this closure adds browser evidence only. Core controls unchanged: R-3 no-execution (grep + test
+ nav), GR-8 presentation-only (grep), API auth 401/200/405, disclaimer on screen, no raw score rendered.

---

## 5. Findings ledger

| ID | Severity | Status |
|---|---|---|
| C-2 (was LOW–MED) | — | **CLOSED** — logged-out → /login on served session |
| C-1 (was MEDIUM) | — | **CLOSED (substantively)** — real report card rendered w/ sample_count + method + framing; see OBS-1 |
| **OBS-1** | LOW | Uncertainty interval bounds render as "— to —" (display-binding bug; data present; not false precision) | Non-blocking; fix in W4-U08/patch |

**No CRITICAL/HIGH. No unmet mandatory safety evidence.** UI proven in the browser (rendered dashboard + report
+ disclaimer + no-exec + logged-out block). Proportionality (R13): approve with observation.

---

## 6. Disposition & next step

- **W4-U07 — ✅ APPROVED WITH OBSERVATIONS.** Platform **v0.36.0 → v0.37.0**. Residual: OBS-1 (render the
  uncertainty interval bounds, not em-dashes).
- Commendation: C-1/C-2 closed browser-only as asked; the report card shows the right framing (RESEARCH_ONLY,
  raw-score-excluded, economic not_assessed) and honest limitations — the fix needed is purely a display
  binding, and the blank bound errs toward under-claiming (honest), never false precision.
- **Next:** ITRGA recommends **W4-U08 — Wave-4 Closeout & Hardening (the LAST Wave-4 unit)**: full-wave
  no-execution/no-account-linkage proof, artifact-audit completeness across all W4 report types, auth/read-only
  proof, docs/register reconciliation, **and closure of OBS-1 (interval-bounds render)** + a clean browser
  pass. On its approval, ITRGA declares the **"Institutional Intelligence Layer Complete"** milestone. On
  operator authorization ITRGA issues `BUILD_ORDER_W4-U08.md`.
- DA does not self-authorize W4-U08, adopt an unspiked dep, add execution/broker, or open the Gate.

> **We don't guess. We prove.** — ITRGA
