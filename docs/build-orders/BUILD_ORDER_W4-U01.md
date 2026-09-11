# AXIOM BUILD ORDER — W4-U01

## Institutional Intelligence: Scientific Dependency Compatibility + Intelligence Artifact Foundation

**Build Order ID:** W4-U01
**Wave:** 4 — Institutional Intelligence · **Unit:** 01 (foundation; no analytical feature)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **Wave-4 Design Plan ACCEPTED WITH REFINEMENTS (R-1…R-8)** + operator
authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07/08_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A** (market-agnostic); Wave-4 guardrails **GR-1…GR-8**; plan
refinements **R-1…R-8** (`ITRGA_REVIEW_WAVE4_DESIGN_PLAN.md`).
**Governing plan:** `WAVE4_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §3 (bounded context), §4.1 (artifact
contract), §6 (dependency/spike), §9/§10 (W4-U01 scope).
**Baseline to meet/exceed:** backend **192** / frontend **11 files · 25 tests**; Platform **v0.30.1**; Alembic
head **20260715_0018**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

W4-U01 is the **foundation** of Wave 4 — it builds the safety/engineering base **before any analytical
feature.** Two jobs only:

1. **Discharge TD-065 as a HARD GATE (R-1):** prove, on the exact target (Windows + Python 3.14.6, PostgreSQL),
   whether the candidate compiled scientific dependencies install/import/smoke cleanly — and pin exactly which
   are approved for later Wave-4 use. Where a candidate fails, commit the pure-Python fallback path.
2. **Establish the Institutional Intelligence bounded context + the common artifact/report contract** (05 v2.0
   §3/§13 single ownership; plan §3/§4.1) with lineage/uncertainty/audit designed in — so W4-U02+ persist
   governed, traceable, inert artifacts from day one.

**No operator-facing analytical capability is authorized** (no correlation/regime/scenario/risk feature, no
new dashboard beyond what is strictly needed for evidence). This is scaffolding + a spike, proven safe.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution / order / broker / paper-trade / position / autonomy path anywhere** (GR-1/GR-3). The
  Constitutional Governance Gate stays **CLOSED**; no code path opens it. Prove by **R-3 wave-wide grep**
  (command + output) incl. `place_order|cancel_order|order_payload|\bexecute\b|\bbuy\b|\bsell\b|\bposition\b|broker\.|paper.?trade|auto_retrain|model\.status\s*=|advisory_status\s*=|remediation_payload|gate_open|allow_execution`.
- ❌ **No analytical feature / no guaranteed-return framing / no signal emission.** This unit computes no
  correlation/regime/scenario/risk result for operator consumption. The artifact contract may exist; it is
  **inert** (no artifact carries an order payload or remediation directive).
- ❌ **No adoption of a compiled dependency the spike did not pass (R-1).** An import of an unspiked/failed
  compiled lib is an automatic FAIL. If a candidate fails, the **pure-Python fallback** for that capability is
  committed and the register records it.
- ❌ **No un-audited persisted artifact (R-4).** If a `scientific_dependency_spikes` table (or any table) is
  added, it triggers the **persistence-capture control**: committing script + raw `psql SELECT ≥1 row` on the
  CORRECT table + a matching immutable audit event, in this first submission. If the spike evidence is
  file-only (no table), state that explicitly — no silent choice.
- ❌ **No cross-context ownership violation** (05 v2.0 §13). `institutional_intelligence` **reads** from
  Market/ML/Trading Intelligence; it owns no feeds, order flow, broker abstraction, or auth.
- ❌ **No D-W2-001 breach.** Nothing here learns symbol identity or introduces a per-market specialized model.
- ❌ **No regression** (Wave-0/1/2/3 + W3-U08.1). Full suite green + **green CI (`LOCAL_CI_EXIT_CODE: 0`
  inline — now the established standard)** + parity smoke.
- ✅ **Preserve:** advisory/research-first, presentation-only UX, tz-UTC, all prior hardening, npm-audit 0,
  ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.**

---

## 3. Scope (Components A–C only)

### A. Scientific dependency compatibility spike (R-1 — the hard gate; discharges TD-065)
- On the target (**Windows + Python 3.14.6**, PowerShell, the project venv), for each candidate compiled
  dependency the DA intends to rely on in Wave 4 (per plan §6.1: e.g. **numpy, scipy, pandas**; scikit-learn
  only if intended): **install → import → a minimal numeric smoke** (e.g. build a small array/series, compute a
  mean/correlation-primitive, assert a known value). Record **exact resolved versions** and raw console output.
- Produce a decision record: **which deps PASS (approved for Wave-4 use) and which FAIL.** For any FAIL,
  define and commit the **pure-Python fallback** for the dependent capability and note it in the register.
- Persist or file-record the spike evidence (see §B/R-4). Add a wheel-compat policy note/ADR:
  *"No Wave-4 unit may import a compiled dependency not passed by this spike."*

### B. Institutional Intelligence bounded context + artifact contract (plan §3/§4.1)
- Create the backend package skeleton `backend/app/institutional_intelligence/` with clear single ownership
  (reads Market/ML/Trading Intelligence; owns no feeds/order/broker/auth).
- Define the **common intelligence artifact/report base contract** carrying at least (plan §4.1):
  `id · created_at(UTC) · artifact_type · method_version · config · input_lineage · source_artifact_ids ·
  market_scope · as_of_start · as_of_end · sample_count · uncertainty · results · limitations · report_hash ·
  research_status · created_by/actor · audit_correlation_id`.
- Define the **audit + persistence pattern** every future artifact will use (immutable audit event on
  create; correlation id; no-orphan by construction). No feature artifact is produced yet.
- If a persisted table is introduced now (e.g. `scientific_dependency_spikes`), add the Alembic migration and
  satisfy **R-4**. If not, spike evidence is a governed file — state which, explicitly.

### C. Policy tests + register/docs
- Named tests proving the **no-execution/no-guarantee policy** structurally: the new context has no
  execution/order/broker path; the artifact base cannot carry an order payload/remediation directive; the Gate
  is untouched. (These are the W4 analogues of the W3 inert-schema/keystone tests.)
- Update registers/docs: **TD-065** updated to reflect exactly which deps are discharged (and any residual
  fallback owed); RISK_REGISTER (Wave-4 rows per plan §8 that apply to the foundation); GOVERNANCE_AMENDMENTS
  (no amendment; Option A stands; Gate CLOSED); CHANGELOG → **v0.31.0**; PROJECT_STATE; ADR for the
  foundation + wheel-compat policy.

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL)

Report `DELIVERY_REPORT_W4-U01.md` + raw `operator results.md`. **Prove build identity first** (Test-Path the
new files/ADR; git HEAD; v0.31.0 stamp) — the W3-U07/U08.1 precedent.

1. **Build identity** — new package/ADR files exist; v0.31.0; `git log -1 --oneline`.
2. **Wheel-compat spike (R-1)** — raw install/import/smoke output per candidate dep with **resolved versions**;
   an explicit PASS/FAIL list; the committed fallback for any FAIL. (Python 3.14.6 confirmed.)
3. **Artifact contract** — show the base contract fields; a unit test constructing an artifact and asserting
   the mandatory fields (lineage/uncertainty/sample_count/research_status/audit) are present and that no
   order/remediation field exists.
4. **Persistence (R-4, if a table is added)** — Alembic `upgrade head` + `alembic current`; committing script;
   raw `psql SELECT ≥1 row` on the correct table; matching audit event (no orphan). If file-only, say so.
5. **R-3 wave-wide grep** — backend + frontend, command + output; residual hits disclosed + shown benign.
6. **Full regression** — backend `pytest` **≥192** (0 failed), frontend **11 files · 25 tests** (or higher if
   tests added), ruff/tsc/build clean, npm audit 0.
7. **CI** — `local_ci.sh` → `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** inline.
8. **Parity smoke** (ws-ticket 200, persist_errors 0).

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.31.0.
- [ ] **R-1 spike discharged:** each candidate dep has raw install/import/smoke output + resolved version + a
      PASS/FAIL verdict; fallback committed for any FAIL; policy note present ("no unspiked compiled dep in
      Wave 4"). TD-065 updated to the exact deps discharged.
- [ ] Institutional Intelligence context skeleton with single ownership; **artifact base contract** carries all
      §4.1 fields incl. lineage/uncertainty/sample_count/research_status/audit; artifact is **inert** (no
      order/remediation field) — proven by test.
- [ ] **R-4** satisfied for any new table (committing script + raw SELECT + audit event, correct table) OR an
      explicit file-only statement.
- [ ] **R-3** grep empty/benign (command+output); no execution/broker/gate path; Gate CLOSED.
- [ ] No analytical feature / no guaranteed-return framing / no signal emission / no D-W2-001 breach.
- [ ] No regression; full suite green; **`LOCAL_CI_EXIT_CODE: 0`**; parity smoke clean.
- [ ] Registers/docs reconciled (TD-065, RISK, GOVERNANCE_AMENDMENTS Option A/Gate CLOSED, CHANGELOG v0.31.0,
      ADR).
- [ ] DA does not self-approve, self-advance, build a W4-U02+ feature, adopt an unspiked dep, or open the Gate.

**A single CRITICAL, unmet mandatory evidence, or a red gate ⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA
approves W4-U01, advances to **v0.31.0**, and (on operator authorization) issues `BUILD_ORDER_W4-U02.md`
(Correlation Intelligence Reports) carrying **R-2/R-4/R-6**.

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Any correlation/regime/scenario/portfolio-risk/signal-validation **analytical result** for operator
  consumption (those are W4-U02…U06, each with its own Build Order).
- Any execution/order/broker/paper-trade/account/position linkage; opening the Gate.
- Adoption of any compiled dependency the spike did not pass.
- Any per-market specialized model or symbol-identity feature (D-W2-001 Option A; would need an amendment).
- Any Wave-5/6 work.

---

## 7. Notes to the Development Authority

Foundation units are judged on **safety and reproducibility, not surface.** The two things that must be
incontrovertible here: (1) **exactly which compiled deps are proven to work on Windows + Python 3.14.6**, with
raw versions and output — so no later unit builds on an unproven stack; and (2) **an artifact contract that
structurally cannot carry an action**, with lineage/uncertainty/audit designed in. Prove build identity first;
keep the CI exit code inline; disclose grep residuals with output. Nothing operator-facing analytical yet.

DA does not self-approve, self-advance the version, build a Wave-4 feature unit, adopt an unspiked dependency,
or open the Gate. The next unit follows ITRGA's verdict + a new Build Order + operator authorization.

> **We don't guess. We prove.** — ITRGA
