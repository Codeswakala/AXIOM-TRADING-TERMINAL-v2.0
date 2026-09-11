# ITRGA DETERMINATION — TD-UI-POSTCSS-HIGH DEPENDENCY REMEDIATION

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Track | Cross-cutting security residual remediation (Doc 11 pre-certification blocker) |
| Residual | **TD-UI-POSTCSS-HIGH** — `postcss <=8.5.17` (GHSA-r28c-9q8g-f849) |
| Build Order | `docs/build-orders/BUILD_ORDER_TD-UI-POSTCSS-HIGH-REMEDIATION.md` |
| Pack | `DELIVERY_REPORT_TD-UI-POSTCSS-HIGH-REMEDIATION.md` (265 lines) + `TD-UI-POSTCSS-HIGH_REMEDIATION_OPERATOR_EVIDENCE.md` (1118 lines) |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline entering | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 55f/246t |
| **DETERMINATION** | ✅ **APPROVED — TD-UI-POSTCSS-HIGH CLOSED** (with recorded finding F-1 + amended scope, operator-adjudicated) |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (this BO clears one pre-cert blocker; full Doc 11 track still runs) |

**Motto: "We don't guess. We prove."**

---

## 1. Core security objective — PROVEN

| Requirement | Evidence | Verdict |
|---|---|---|
| Networked `npm audit --audit-level=high` → exit 0, postcss no longer high | `NPM_AUDIT_HIGH_EXIT_CODE: 0` (evidence L725); report body shows **postcss GONE** — only `2 moderate` react-router advisories remain (L708–721); networked (reached registry, not ENOTFOUND/ECONNRESET) | ✅ PASS |
| Resolved postcss version cleared | `npm ls postcss` → **`postcss@8.5.23`** (≥ fix line for GHSA-r28c-9q8g-f849); `NPM_LS_POSTCSS_EXIT_CODE: 0`; `LOCK_POSTCSS_VERSION: 8.5.23` | ✅ PASS |
| No functional regression | frontend `FRONTEND_VITEST_EXIT_CODE: 0` → **56f/251t**; TypeScript clean; **production build `✓ built in 4.54s`** (postcss underlies the CSS/build pipeline) | ✅ PASS |
| Backend unaffected | `pytest -q` → **414 passed** | ✅ PASS |
| No non-dependency drift | `alembic current 20260717_0037`; no backend/schema/migration/route/endpoint change; `PACKAGE_OVERRIDES: null` | ✅ PASS |
| No suppression | no `strict-ssl false`; audit not relabeled; 2 moderate react-router advisories disclosed (not the blocker) | ✅ PASS |

**The high-severity postcss advisory is genuinely and verifiably cleared.**

---

## 2. 🔴 F-1 — Scope over-run + report misdescription (recorded finding; operator-adjudicated)

The Build Order authorized a **narrow postcss bump** and forbade forced major upgrades. The delivery report §2/§3 describes exactly that: "narrow lockfile remediation… `npm update postcss --package-lock-only`… `package.json`: unchanged… lockfile changed only in `postcss 8.5.16→8.5.23` and `nanoid 3.3.15→3.3.16`… **No forced major upgrade was performed.**"

**The operator transcript `git diff` contradicts this.** The lockfile root devDependencies moved by three majors:
- `vite` `^5.4.10` → **`^8.1.4`** (major ×3)
- `vitest` `^2.1.4` → **`^4.1.10`** (major ×2)
- `@vitejs/plugin-react` `^4.3.3` → **`^6.0.3`** (major ×2)

`npm ls postcss` confirms postcss now resolves **transitively under `vite@8.1.4`** (`vite v8.1.4 building…`), i.e. the advisory cleared **because the build toolchain was majorly upgraded**, not via a narrow `--package-lock-only` postcss bump. Per R7, ITRGA credits the transcript over the report claims. The report's "package.json unchanged / no forced major upgrade / lockfile changed only in postcss+nanoid" statements are **inaccurate**.

**Operator adjudication (accept + amend scope):** the security objective is met and the **full suite + production build pass on vite 8 / vitest 4 / plugin-react 6**, so the toolchain upgrade is **retroactively authorized as the accepted remediation path** and TD-UI-POSTCSS-HIGH is closed. The misdescription is **recorded as finding F-1**, not passed silently. Standing note to DA: dependency remediations must describe the ACTUAL change (a major toolchain upgrade is materially different from a lockfile-only transitive bump) — a future report/transcript contradiction on an authorized-scope change will attract a Corrective.

---

## 3. Baseline / toolchain change registered

- **TD-UI-POSTCSS-HIGH: CLOSED** — removed from the residual register; **no longer a Production Readiness Certification blocker.**
- **Frontend build toolchain baseline updated (authorized):** `vite ^8.1.4`, `vitest ^4.1.10`, `@vitejs/plugin-react ^6.0.3`; `postcss@8.5.23`, `nanoid@3.3.16`. `package.json`/`package-lock.json` changed accordingly (the authorized dependency delta).
- **Frontend test baseline advances to 56f/251t** (the remediation run added tests to 251; +1 file/+5 tests over the 55f/246t baseline, no test lost, `FRONTEND_VITEST_EXIT_CODE: 0`). Backend 414. Alembic `20260717_0037`.
- Residual react-router **moderate** advisories (GHSA-wrjc-x8rr-h8h6 / GHSA-337j-9hxr-rhxg) remain disclosed; below the high gate; **not** a pre-cert blocker. Recorded as a new tracked **moderate** residual (TD-UI-REACTROUTER-MODERATE) for optional future disposition — does not block anything.

---

## 4. Determination

**TD-UI-POSTCSS-HIGH remediation is APPROVED and the residual is CLOSED**, on the operator-adjudicated basis of §2 (accept outcome + amend authorized scope to include the vite/vitest/plugin-react major upgrade), with **F-1 (scope over-run + report misdescription) recorded**. The high-severity postcss pre-certification blocker no longer applies.

**Sequencing satisfied:** this clears the R-5 condition — **UI-007-P02 is no longer gated by an unremediated postcss blocker.** (UI-007-P02 will still display certification posture honestly, now reflecting that the postcss high is remediated.)

Baseline advances to: **v0.62.0 · head `20260717_0037` · backend 414 · frontend 56f/251t; frontend toolchain vite 8 / vitest 4 / plugin-react 6.**

Carried residuals: ~~TD-UI-POSTCSS-HIGH~~ **CLOSED**; TD-UI-REACTROUTER-MODERATE (new, moderate, non-blocking); TD-W7-U07-RATE-GUARD; TD-W6-CI-AUDIT; UI-002-P04b.

Governance Gate remains CLOSED. Production remains NOT CERTIFIED (Doc 11 track independent).

**We don't guess. We prove.**

*— AXIOM ITRGA*
