# AXIOM — BUILD ORDER B-00
## Backend Integrity & Reproducible Baseline

| Item | Value |
|------|-------|
| Build Order ID | `BO-B-00` |
| Programme | Backend Operationalization (reconciled v2) |
| Authorizing authority | **Operator** (directive of 2026-08-19: "first build order authorized") |
| Governing documents | `BACKEND_ROADMAP_v2.md` §B-00 · `05_SYSTEM_ARCHITECTURE.md` (v2.0) · `07_ML_SPEC.md` · `17_INSTITUTIONAL_SECURITY_STANDARD.md` · `10_CONSTITUTIONAL_HIERARCHY.md` |
| Implementer | Development Authority (DA) |
| Reviewer | Independent Technical Review & Governance Authority (ITRGA) |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged by this order) |
| Production | NOT CERTIFIED (unchanged by this order) |

---

## 1. Objective

Establish a **provable, honest baseline** before any new capability work proceeds. This order fixes one known data-integrity defect, installs a security-severity/exception policy, records the true executed test baseline, and formalizes a provenance/landing protocol that every subsequent unit must follow.

This is **not** a capability feature. It produces no new analytical output. It makes the foundation trustworthy.

---

## 2. Scope (in scope)

### B-00.1 — Simulated clock chronology fix
- **Problem (verified, FIND-5):** `backend/app/market/adapters/simulated.py` advances bar `open_time` one M1 bar per ~2 s tick (~30× real time), producing **future-dated bars** (observed `open_time` 17:57Z against ~15:05Z wall clock). Violates the project's own as-of / no-look-ahead discipline and can corrupt downstream datasets and model validation.
- **Required outcome (choose exactly one, state which):**
  - **(a)** bind simulated bar time to wall-clock such that **no** generated bar has `open_time > utc_now()`; **or**
  - **(b)** label the feed as an explicit **accelerated synthetic clock** — a distinct, non-live data state that is never presented or persisted as live, and is excluded from any downstream validation tier above "pipeline validation" (per `BACKEND_ROADMAP_v2.md` §B-01.1a).
- **Binding invariant:** zero persisted candles with `open_time > utc_now()` for the chosen model, enforced by the existing chronology guard.

### B-00.2 — Dependency & supply-chain severity/exception policy
- Replaces any prior unconditional "audit clean" expectation with the severity/exception acceptance model.
- Applies to backend dependencies (`backend/requirements.txt`, `backend/pyproject.toml`).

### B-00.3 — True executed test baseline
- Run the backend test suite; record **executed** pass/fail counts; reconcile against the `PROJECT_STATE.md` claim (162 suites / 736 tests; 415 backend). Distinguish **inventory** from **executed result**.

### B-00.4 — Provenance / landing protocol
- Define and enforce: "a unit is landed only when its SHA is cited and its Delivery Report references the canonical registers." Applied to every subsequent unit.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** new analytical features, signals, intelligence reports, alerts, ML training, or assistant endpoints.
- **No** frontend changes (frontend dependency remediation is owned by **F-00**, not this order).
- **No** live/real market-data source. The simulated feed remains simulated.
- **No** governance-gate opening, no actuation, no broker/account/execution/trading state of any kind.
- **No** ML threshold tuning, model training, or promotion.
- **No** modification of the governance hierarchy or constitutional documents.
- **No** reopening of closed experiments.
- **No** repository publication — publication remains an Operator-controlled custody action. The DA works in its own workspace and submits evidence through the established review channel.

---

## 4. Exact deliverables

1. `simulated.py` clock model corrected (option (a) or (b) above, explicitly stated), plus the chronology-guard invariant test.
2. Backend dependency audit run (e.g. `pip-audit`) with findings classified per §B-00.2 acceptance model.
3. Executed backend test-run output with pass/fail/skip totals, reconciled against `PROJECT_STATE.md`.
4. A written **Provenance & Landing Protocol** (can be a short Markdown addition or ADR-style record) stating the SHA-citation and register-reference rules.
5. A **Delivery Report** for this unit (see §8), including a deviation register if any acceptance criterion is adjusted.

---

## 5. Dependencies

- None upstream. This is the programme's first unit.
- Downstream: **all** subsequent B-units (B-01 → B-07) and X-01 depend on B-00's baseline, provenance protocol, and test baseline being in place.

---

## 6. Allowed files / components

- `backend/app/market/adapters/simulated.py` and its test files.
- `backend/app/ml/dataset/chronology_guard.py` (test invocation only — do not weaken it).
- `backend/requirements.txt`, `backend/pyproject.toml` (audit/pinning only; no scope creep into frontend).
- `backend/tests/**` (add/churn tests only for the clock invariant and baseline).
- A new documentation file for the Provenance & Landing Protocol (e.g. under `backend/docs/` or `docs/`), and the Delivery Report.

Anything outside this list is **not authorized** by this order and must be separately requested.

---

## 7. Security constraints (binding)

- No secrets, tokens, or credentials in any changed file or in the Delivery Report.
- No weakening of `17_INSTITUTIONAL_SECURITY_STANDARD.md`; no new network surface; no new endpoints.
- The chronology fix must **not** introduce nondeterminism into inference ordering or the as-of discipline.
- Any dependency change must respect the existing pin-range policy (`requirements.txt` / `pyproject.toml` ranges) unless a specific advisory forces a targeted bump, which must be justified and evidenced.

---

## 8. Acceptance criteria (per sub-unit)

### B-00.1
- [ ] Clock model explicitly stated as (a) or (b).
- [ ] Soak run shows **zero** candles with `open_time > utc_now()`.
- [ ] Chronology guard passes against the corrected feed.
- [ ] Invariant test exists and is pinned (Level II: executed output).

### B-00.2
- [ ] No **unaccepted** critical/high findings.
- [ ] All remaining findings classified (transitive / dev-only / no-fix / false-positive).
- [ ] Any permitted exceptions documented and formally noted (not silently waived).
- [ ] Lockfiles/pins updated where applicable.

### B-00.3
- [ ] Executed test-run output supplied (Level II), not a count assertion.
- [ ] Executed counts reconciled against `PROJECT_STATE.md`; any discrepancy **explicitly reported** (the roadmap forbids inferring fabrication — report the discrepancy accurately).
- [ ] Pass/fail/skip breakdown provided.

### B-00.4
- [ ] Provenance & Landing Protocol written and stated as binding for all future units.

---

## 9. Evidence requirements (what the DA must supply)

| Item | Class | Form |
|------|-------|------|
| Diff/SHA of the `simulated.py` change | Level I | commit ref + diff |
| Soak-run output showing no future-dated bars | Level I | command output |
| Chronology-guard + invariant test run | Level II | executed test output |
| Dependency audit output + classification table | Level II | audit output + table |
| Backend test-run output (executed) | Level II | full/representative run output with totals |
| Provenance & Landing Protocol | Level III | document content |
| Delivery Report | Level III | §10 structure |

Evidence is submitted through the **established review channel**; no direct repository access to the DA workspace is assumed or granted (custody model, `BACKEND_ROADMAP_v2.md` §0.1.6).

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files, with SHAs)
3. Chosen clock model (a or b) and rationale
4. Test evidence (executed)
5. Dependency findings and classification
6. Reconciliation against `PROJECT_STATE.md`
7. Deviations register (if any)
8. Known limitations / remaining risk
9. Technical-debt entries (if any)

---

## 11. Rollback / containment

- The chronology change is local to `simulated.py` and its tests; revert is a single-file/commit revert.
- No schema migration is involved.
- If option (b) (accelerated synthetic clock label) is chosen, the label must be applied consistently; a partial label is a defect.
- No data produced by this order affects production (none is produced).

---

## 12. Completion condition

The unit is complete when: all acceptance criteria are met, evidence is supplied, the Delivery Report is submitted, **and ITRGA issues its independent determination** (APPROVED / APPROVED WITH OBSERVATIONS / CORRECTION REQUIRED / …). A DA declaration of completion is **not** evidence of completion and does **not** close this unit.

**Next authorization state:** upon ITRGA approval of B-00, the next bounded Build Order (B-01, Data Foundation) may be issued. Nothing downstream is authorized by this order.

---

**End of Build Order B-00**
