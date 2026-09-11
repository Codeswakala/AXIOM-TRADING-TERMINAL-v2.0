# ITRGA REVIEW — W7-U06

## Portfolio Research Dashboard / Advanced Reporting

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Unit:** W7-U06 (Wave 7) · **Reviewed pack:** `operator results.md` + 4 screenshots (no separate DELIVERY_REPORT file this turn)
**Build Order:** `BUILD_ORDER_W7-U06.md`
**Review date:** 2026-07-19
**Platform of record (pre-unit):** v0.59.0 · head `20260717_0037` · backend 391 / frontend 20f·64t
**Verdict:** 🟡 **CONDITIONAL APPROVAL** — every risk control proven at Level-I; one named item open (C-1: CI exit-code output not captured). **Version bump to v0.60.0 HELD.**
**Confidence:** HIGH. **Governance Gate:** CLOSED. **Motto:** *We don't guess. We prove.*

---

## 0. Build-identity check (done FIRST)

- `operator results.md`: fresh pack opening with W7-U06-specific `Test-Path` (ADR-069, `portfolio_research.py`, `test_portfolio_research.py`, `PortfolioResearchPage.tsx`, seed). ✔ No separate `DELIVERY_REPORT_W7-U06.md` attached this turn — reviewed against operator evidence + screenshots (Level-I; the DR is a claim-tier doc anyway).
- Screenshots dated 2026-07-19; Ops Dashboard shows `W7-U06`, v0.60.0. ✔

---

## 1. What is PROVEN (Level-I)

| # | Requirement | Evidence | Result |
|---|---|---|---|
| b | Named tests | `test_portfolio_research.py` **8/8 PASSED** (all §4 backend tests) | ✅ |
| — | Full backend regression | **399 passed** (+8 over 391); broker suite in-suite green | ✅ |
| — | Frontend | **21 files / 67 tests passed** (+1 file, +3 tests) | ✅ |
| c | Migration state | `alembic current = 20260717_0037` unchanged; `REPORT_PERSISTED: False` (generated report — no table) | ✅ |
| **d** | **No real account/P&L (CENTRAL)** | forbidden-marker grep over dashboard/report JSON + `PortfolioResearchPage.tsx` incl. `P&L\|Balance\|Account` → "no output"; **`REAL_ACCOUNT_OR_PNL_MARKER_FILE_MATCH_COUNT: 0`** | ✅ |
| e | GR7-4 uncertainty + stat≠economic | `DASHBOARD_ECONOMIC_USEFULNESS: not_assessed`, `REPORT_ECONOMIC_USEFULNESS: not_assessed`; **`FIGURES_MISSING_UNCERTAINTY_OR_SAMPLE_COUNT: 0`**; `REPORT_HASH_PRESENT: True`; full-scope no-cherry-picking (`test_report_full_scope_included_no_cherry_picking` PASS + `included_scope: full_current_operator_scope_no_cherry_picking`) | ✅ |
| f | Operator scoping (R7-3, valid tokens) | `LOGIN_A/B 200`; **`B_VISIBLE_A_DASHBOARD_SOURCE_COUNT: 0`** / `B_VISIBLE_B: 1`; **`B_VISIBLE_A_REPORT_SOURCE_COUNT: 0`**; mutation surface 404/405 | ✅ |
| g | No secrets/PII | **`SECRET_OR_PII_MARKER_FILE_MATCH_COUNT: 0`** | ✅ |
| i | Browser (GR7-10) | served `localhost:8000/portfolio-research`: "Hypothetical research only… AXIOM does not act and this view is not a live venue record"; **HYPOTHETICAL RESEARCH** labels; per-figure sample_count + uncertainty; `economic usefulness: not_assessed`; report hash; `Persisted: false`; **no actuation/real-P&L controls**; logged-out `/login` | ✅ |
| j | No barred dependency | grep clean | ✅ |
| m | Gate CLOSED | `test_gate_remains_closed_for_wave7` PASS; broker suite green | ✅ |

**The red line — a portfolio dashboard that is a RESEARCH view, not a real account — is proven:** zero real-account/P&L fields or labels, every figure hypothetical and uncertainty-bearing with `economic_usefulness = not_assessed`, full-scope (no cherry-picking), operator-scoped with zero cross-operator leakage.

---

## 2. CONDITION

### 🟡 C-1 — CI exit-code output not captured (§5(k)).
The operator pack **ends at the CI command line** — the `& "…\git\bin\bash.exe" scripts/local_ci.sh` command + `Write-Host LOCAL_CI_EXIT_CODE` + the `Select-String "Local CI equivalent complete"` are entered, but the **transcript was cut before their output**: `LOCAL_CI_EXIT_CODE: [0-9]` appears **0 times** and there is no `==> Local CI equivalent complete` line. Frontend build succeeded (`✓ built in 3.00s`) just above, and the full backend 399 + frontend 21/67 are green — but the named §5(k) CI gate evidence (`LOCAL_CI_EXIT_CODE: 0`) is not on record.
**To close C-1:** submit the CI tail showing `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** (apply the TD-W6-CI-AUDIT fix if the offline `npm audit` condition recurs — trusted path/CA or graceful audit; if it does recur, an operator waiver per precedent is acceptable).

---

## 3. Classification

- **C-1** — LOW (transcript truncation of the CI output; all substantive gates — 399 backend, 21/67 frontend, build — independently green; only the named exit-0 line is missing).
- No CRITICAL, no HIGH. No real-account/P&L, uncertainty+economic separation, full-scope, operator scoping (0 leakage), no secret/PII, browser hypothetical framing, Gate CLOSED — all proven Level-I. Per proportionality (R13): every *risk* item proven, one *named* CI item missing ⇒ **CONDITIONAL**, not WITHHELD. **v0.60.0 HELD** (platform stays v0.59.0).

---

## 4. Not a finding / disclosed

- No separate `DELIVERY_REPORT_W7-U06.md` this turn — not required for the verdict (operator evidence + screenshots are Level-I; the DR is claim-tier). Recommend the DA still file it for the record.
- `REPORT_PERSISTED: False` → no report table → no persistence-capture owed; correct (head 0037 unchanged).
- Browser logged-out is `/login`; acceptable (auth/route protection consistent with the passing tests).

---

## 5. Path to FINAL

On C-1 (CI transcript tail with `LOCAL_CI_EXIT_CODE: 0` / `Local CI equivalent complete`, or an operator waiver if the offline-`npm audit` condition recurs), I will write `ITRGA_VERDICT_W7-U06_FINAL.md` superseding this CONDITIONAL, bump to **v0.60.0** (head `20260717_0037`), update onboarding, and W7-U07 (Enterprise Scalability & Multi-User Readiness Hardening — incl. the deferred abuse/rate guard + admin/admin123 disposition, R7-6) becomes authorizable.

---

## 6. Posture note

A clean portfolio-research unit: the dashboard is unmistakably a hypothetical research view (banner + HYPOTHETICAL RESEARCH labels + `not_assessed` economics + per-figure uncertainty), carries zero real-account/P&L fields or labels (marker count 0), is operator-scoped with zero leakage, and leaks no secrets. The only gap is the CI transcript being cut before its exit line — capture it (or waive per the standing CI-env precedent) and this unit is FINAL.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
