# AXIOM BUILD ORDER — W4-U06

## Institutional Intelligence: Professional Signal Validation Extension (research, uncertainty-mandatory, raw-score-excluded, no cherry-picking)

**Build Order ID:** W4-U06
**Wave:** 4 — Institutional Intelligence · **Unit:** 06
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **W4-U05 APPROVED — CLEAN** (Platform v0.35.0; portfolio/risk no-linkage) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07/08_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-4 guardrails **GR-1…GR-8**; this unit carries
**R-2, R-4, R-5, R-6** + **raw-score-exclusion** + **no-cherry-picking (R18)** (`ITRGA_REVIEW_WAVE4_DESIGN_PLAN.md`, plan §5.5).
**Governing plan:** `WAVE4_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §4.1 (artifact contract), §5.5
(signal-validation methodology/controls), §9.
**Builds on:** W4-U01…U05 (context/contract/approved deps, inline raw-SELECT + no-orphan audit standard) +
W2-U07/U08 (uncertainty/calibration precedent) + W3-U02/U07 (advisory signals + raw-score-stripped precedent).
**Baseline to meet/exceed:** backend **225** / frontend **11 files · 25 tests**; Platform **v0.35.0**; head
**20260716_0022**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver a **Professional Signal Validation Extension** — a research artifact that **evaluates the quality of
persisted advisory signals** (from W3-U02+) over an **as-of-bounded, honestly-scoped** set of records, **with
uncertainty**, persisted and auditable. It is **research context for the operator** about how the advisory has
behaved — **not** a promise of future performance, **not** a signal, and it **never** treats a raw model score
as confidence (plan §5.5).

**Honesty about outcome data (critical):** validation may only use **governed outcome data where it exists.**
If governed forward-outcome/label data does not yet exist, the unit must **say so explicitly** and validate
only what is legitimately available (e.g. guardrail/state distribution, calibration-report linkage, coverage)
— it must **not fabricate or imply realized performance/returns.**

It reads persisted records read-only, emits the W4-U01 `IntelligenceArtifactContract`, and is read-only. It
uses the **W4-U01-approved deps (numpy/pandas/scipy) or the pure-Python fallback** — nothing else.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No cherry-picking / no selective window (R18 — KEYSTONE). MANDATORY NAMED TEST.** Validation runs over a
  **declared, honestly-scoped** record set (as-of-bounded; the scope/filters stored in `config`). No
  post-hoc window/metric selection that flatters the advisory. Prove by: (a) the scope/filters persisted in
  the artifact; (b) a **named test** that the validation includes the full declared set (no silent
  exclusions), and that the same declared scope yields the same result (deterministic, no selective drop). The
  W2-U07 lesson applies: a suspiciously-good stat gets a base-rate/leakage sanity check.
- ❌ **Raw model score NOT treated as confidence (raw-score-exclusion — KEYSTONE). MANDATORY TEST.** The
  validation output uses **calibrated** confidence / governed metrics; the **raw model score is excluded** from
  the validation payload. Prove by: a **test** that no raw-score field appears in the artifact/output, and — if
  raw_score exists on the source signals — that it is **stripped** (the W3-U07 "present upstream, absent
  downstream" standard).
- ❌ **No guaranteed/expected future performance (§5.5).** Every result is **historical/research with
  uncertainty**; `limitations` state not-a-guarantee / not-a-prediction / not-financial-advice. No language
  implying future returns. Prove by test.
- ❌ **No uncertainty-free metric (GR-7).** Every validation metric carries **uncertainty + sample_count**
  (Wilson/CI as appropriate). No bare point estimate. **Economic usefulness REPORTED independently (R-5)** —
  "statistical/quality signal ≠ tradable"; honest (`not_assessed` + reason acceptable).
- ❌ **No look-ahead (R-2 — MANDATORY NAMED NEGATIVE TEST).** Validation of a signal uses only data available
  as of that signal's decision time / `as_of_end`; no future outcome leaks into a metric it shouldn't. Named
  test (inject future record → excluded/unchanged).
- ❌ **Not a signal / triggers nothing (R-6 standing).** A validation report is not a signal/instruction and
  mutates/triggers nothing (no re-emit, no model/advisory-status change). Inert contract + "changes-nothing"
  named test; grep `auto_retrain|model.status =|advisory_status =|emit_signal` benign.
- ❌ **No un-audited persisted report (R-4 — INLINE).** New `signal_validation_reports` table triggers the
  persistence-capture control with the reinforced proof: Alembic head advance + committing script + **raw
  `psql SELECT ≥1 row` on `signal_validation_reports`** + **no-orphan audit JOIN** (`signal_validation_report.
  created`, `orphan_count 0`) — inline in the first submission. `research_status` mandatory; validation scope +
  source signal ids in lineage.
- ❌ **No execution / order / broker / gate path** (GR-1/GR-3). Gate CLOSED. **R-3 wave-wide grep** (command +
  output, incl. `raw_score|score(|gate_open|allow_execution`), residuals disclosed + benign.
- ❌ **No unspiked compiled dependency** (R-1); numpy/pandas/scipy or pure-Python only. **No D-W2-001 breach.**
- ❌ **No client-side authoritative recompute** (GR-8) if any UI; presentation-only; browser screenshots
  mandatory if UI. If no UI, state so.
- ❌ **No regression** (Wave-0…W4-U05). Full suite green + **CI via documented Git-Bash path →
  `LOCAL_CI_EXIT_CODE: 0`** + parity smoke (Tee/marker-check at the **W4-U06** transcript).
- ✅ **Preserve:** advisory/research-first, tz-UTC, market-agnostic, all prior hardening, npm-audit 0,
  ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.** The **no-cherry-picking** and **raw-score-exclusion** proofs are the
keystones.

---

## 3. Scope (Components A–D)

### A. Signal-validation service (backend, `institutional_intelligence`)
- Read persisted advisory signals (W3-U02+) read-only over a **declared, as-of-bounded scope** (stored in
  `config`); compute quality/validation metrics that are **legitimately supported by governed data**
  (e.g. guardrail-state distribution, calibration-report linkage/coverage, clean-vs-withheld rates) **with
  uncertainty + sample_count**. **Exclude raw model score** from the output.
- If governed forward-outcome/label data does not exist, **explicitly report that** and validate only what is
  available — do **not** synthesize realized performance.
- Attach `limitations` (historical/research, not a guarantee/prediction; outcome-data availability stated) and
  an independent **economic_usefulness** field (R-5).
- Emit `IntelligenceArtifactContract` (`artifact_type = "signal_validation_report"`): metrics, uncertainty,
  declared scope/filters, source signal ids (lineage), calibration linkage, `economic_usefulness`,
  `research_status`, report_hash, audit_correlation_id. **No raw_score, no order/signal/sizing field.**

### B. Persistence + audit (R-4 — inline)
- New `signal_validation_reports` table + Alembic migration; committing repository/script; immutable
  `signal_validation_report.created` audit event; no orphan by construction.

### C. Read-only API
- `GET /api/v1/intelligence/signal-validation-reports` (list) + `GET …/{report_id}` (detail) — authenticated,
  read-only. Unauth → **401**; POST → **405/404**. No emit/execute endpoint.

### D. (Optional) presentation-only surface
- If any UI: presentation-only, metrics with uncertainty + sample_count, **calibrated confidence (no raw
  score)**, historical/not-guaranteed labels, **no execution controls (R-3)**; **browser screenshots** from a
  reachable served session. If no UI, state so.

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL)

Report `DELIVERY_REPORT_W4-U06.md` + raw `operator results.md`. **Prove build identity first.**

1. **Build identity** — new files/ADR exist; v0.36.0; `git log -1 --oneline`.
2. **No-cherry-picking (R18)** — named test that validation covers the full declared scope (no silent
   exclusions); scope/filters persisted; deterministic on same scope.
3. **Raw-score-exclusion** — named test that no raw-score field is in the validation artifact/output; if source
   signals carry raw_score, show it is stripped (present-upstream/absent-downstream).
4. **No guaranteed performance** — `limitations` state historical/not-a-guarantee/outcome-data status; test;
   grep for guaranteed/expected-return language benign.
5. **GR-7 + R-5** — each metric has uncertainty + sample_count; independent `economic_usefulness`; bare
   point-estimate rejected.
6. **R-2 no-look-ahead** — named negative test PASSED.
7. **R-6 non-signal / no mutation** — named "changes-nothing" test; grep benign.
8. **R-4 persistence (inline)** — Alembic `upgrade head` + `alembic current` (new head); committing script;
   **raw `psql SELECT ≥1 row` on `signal_validation_reports`**; **no-orphan audit JOIN**
   (`signal_validation_report.created`, `orphan_count 0`).
9. **API** — unauth **401**; **list 200** + **detail 200** (non-blank echoes); POST → **405/404**.
10. **Dependency discipline** — approved deps or fallback only; grep no unspiked import; **grep confirms no
    `raw_score` in the validation module output path.**
11. **R-3 wave-wide grep** — command + output; residuals disclosed + benign; Gate CLOSED (broker gate tests).
12. **Full regression** — backend `pytest` **≥ (225 + new)**, 0 failed; frontend green; ruff/tsc/build clean;
    npm audit 0.
13. **CI** — **documented Git-Bash invocation** → `==> Local CI equivalent complete` +
    **`LOCAL_CI_EXIT_CODE: 0`** (transcript labelled W4-U06).
14. **Browser screenshots** if any UI; else explicit "no UI this unit." **Parity smoke.**

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.36.0.
- [ ] **No-cherry-picking (keystone):** named test — full declared scope, no silent exclusions; scope persisted;
      deterministic. Suspiciously-good stats get a base-rate/leakage sanity note.
- [ ] **Raw-score-exclusion (keystone):** no raw-score in output; stripped from source if present (test).
- [ ] No guaranteed/expected future-performance framing; historical/research labels; outcome-data status stated
      honestly (no fabricated performance).
- [ ] **GR-7 + R-5:** every metric uncertainty + sample_count; independent economic_usefulness; no bare
      point-estimate.
- [ ] **R-2** named no-look-ahead negative test PASSED.
- [ ] **R-6** non-signal / no-mutation (named test + benign grep).
- [ ] **R-4** `signal_validation_reports`: Alembic head advanced; committing script + **raw SELECT ≥1 row** +
      no-orphan audit JOIN — inline.
- [ ] Read-only API 401 / list-200 / detail-200 / POST-405; non-blank detail echoes.
- [ ] Only approved deps or fallback; no unspiked import; no D-W2-001 breach.
- [ ] **R-3** grep empty/benign (command+output); Gate CLOSED.
- [ ] No regression; full suite green; **CI via Git-Bash → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke; browser
      evidence if UI.
- [ ] DA does not self-approve, self-advance, build W4-U07+, adopt an unspiked dep, or open the Gate.

**A single CRITICAL, unmet mandatory evidence, or a red gate ⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA
approves W4-U06, advances to **v0.36.0**, and (on operator authorization) issues `BUILD_ORDER_W4-U07.md`
(Institutional Intelligence Dashboard / Chart Context — presentation-only, **browser evidence mandatory**).

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Dashboard / closeout (W4-U07/U08, each own Build Order).
- Any execution/order/broker/account/position/sizing path; opening the Gate.
- Any unspiked compiled dependency; any per-market model / symbol-identity feature.
- Raw-score-as-confidence; guaranteed/expected future performance; cherry-picked windows; **fabricated
  realized-outcome data** where none is governed.
- Any Wave-5/6 work.

---

## 7. Notes to the Development Authority

Two keystones here, both learned earlier in this project: **(1) no cherry-picking (R18)** — validate over a
**declared, honestly-scoped** set with the scope persisted, and give any strong stat a base-rate/leakage
sanity check (W2-U07); and **(2) raw-score-exclusion** — the validation output uses calibrated/governed
metrics, never the raw model score (W3-U07 "present upstream, absent downstream"). Be honest about
**outcome-data availability** — if governed forward-outcomes don't exist yet, say so and validate only what's
legitimately there; never fabricate realized performance. Carry uncertainty on every metric, report
economic-usefulness independently (R-5), deliver the **raw SELECT + no-orphan audit inline**, and run CI via
the **documented Git-Bash path** for a clean exit 0 (transcript labelled W4-U06). Prove build identity first;
disclose grep residuals with output.

DA does not self-approve, self-advance the version, build W4-U07+, adopt an unspiked dependency, add
execution/broker, or open the Gate. The next unit follows ITRGA's verdict + a new Build Order + operator
authorization.

> **We don't guess. We prove.** — ITRGA
