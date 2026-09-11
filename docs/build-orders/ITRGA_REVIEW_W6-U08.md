# ITRGA REVIEW — W6-U08 (Wave-6 Closeout & Hardening)

## Execution Research Environment — Closeout, Whole-Wave Proof & Milestone

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Unit:** W6-U08 (closeout — last unit) · **Reviewed pack:** `DELIVERY_REPORT_W6-U08.md` + `operator results.md` + 5 screenshots
**Build Order:** `BUILD_ORDER_W6-U08.md`
**Review date:** 2026-07-18
**Platform of record (pre-unit):** v0.53.0 · head `20260717_0033` · backend 345 / frontend 18f·58t
**Verdict:** 🟡 **CONDITIONAL APPROVAL** — whole-wave soundness largely proven; the named six-table no-orphan **completeness** proof is missing (C-1). **Milestone "Execution Research Environment Complete" and v0.54.0 are HELD** until closure.
**Confidence:** HIGH on what was proven; C-1 is a named-evidence gap (each table's no-orphan was already proven at its own unit), C-2 is a diagnosed environmental CI condition.
**Governance Gate:** CLOSED (verified). **Motto:** *We don't guess. We prove.*

---

## 0. Build-identity check (done FIRST)

- `DELIVERY_REPORT_W6-U08.md`: Unit W6-U08, cites Build Order + W6-U07 FINAL prerequisite; target v0.54.0, head `20260717_0033` unchanged. DA explicitly does **not** self-declare the milestone (`PROJECT_STATE.md`: "Milestone candidate … not declared by DA"). ✔
- `operator results.md`: fresh closeout pack (`test_wave6_closeout.py`, six-table SQL, browser captures, docs reconciliation). ✔

---

## 1. What is PROVEN (Level-I, operator-run + browser)

| Requirement | Evidence | Result |
|---|---|---|
| Whole-wave closeout tests | `test_wave6_closeout.py`: `test_wave6_bright_line_grep_no_live_execution_path`, `test_governance_gate_remains_closed_for_wave6`, `test_broker_logic_contained_in_external_integration`, `test_all_wave6_simulated_tables_labelled_and_inert` all **PASSED** (5 passed) | ✅ |
| Full backend regression | **350 passed** (+5 over 345); broker+safety suite **13 passed** | ✅ |
| Frontend | **18 files / 58 tests passed** | ✅ |
| Migration state | `alembic current = 20260717_0033` unchanged (no closeout migration) | ✅ |
| **SIMULATED-everywhere (6 tables)** | per-table `bad_count = 0` (rows deviating from `SIMULATED`/`research_only`) for runs/fills/ledger/risk/experiments/analytics | ✅ |
| Whole-wave bright-line grep | over `execution_research` + routes → "no output" | ✅ |
| §16 broker containment grep | `MetaTrader\|BrokerClient\|broker_endpoint\|broker_credentials…` outside External Integration → "no output" | ✅ |
| Gate CLOSED wave-wide | closeout gate test + broker suite green; Ops Dashboard states "Execution remains governance-gated", `live_streams:false` | ✅ |
| Browser E2E | served `localhost:8000/execution-research`: SIMULATED banner + disclaimer, artifact cards (Runs 9/Fills 10/Ledger 8/Risk 3/Experiments 5/Analytics 4), SIMULATED detail cards, analytics uncertainty + `economic usefulness: not_assessed`; no actuation controls; Ops Dashboard v0.54.0 "Wave-6 Closeout & Hardening" | ✅ |
| Docs reconciliation | README/PROJECT_STATE/CHANGELOG v0.54.0; roadmap/risk/TD registers updated (TD-090 = TD-W6-CI-AUDIT) | ✅ |

---

## 2. CONDITIONS (must close before milestone)

### 🟡 C-1 — The six-table **no-orphan audit JOIN** completeness proof was not operator-run in the closeout pack.
BO §5(d) named, for **each of the six** W6 tables: `SELECT COUNT(*)` (row_count ≥1) **and** its **no-orphan audit JOIN** (`LEFT JOIN audit_events … WHERE ae.id IS NULL`) → **`orphan_count 0`**. The pack proves **SIMULATED/inert** via `bad_count = 0` and the `test_all_wave6_simulated_tables_labelled_and_inert` test — but the **no-orphan audit JOIN** (`orphan_count 0`) for the six tables is **not present** in the operator transcript (the only `orphan`/`LEFT JOIN audit_events` strings are inside the RISK/TD register file-dumps, not executed queries). The DR §7 lists "no-orphan audit joins" as delivered, but the transcript does not contain them.
**This is the defining proof of a closeout** — the whole-wave audit-completeness assertion. It is not a suspected orphan (each table's no-orphan JOIN was independently proven at its own unit: U02 runs/fills, U03 ledger, U04-FINAL risk, U05 experiments, U06 analytics), but the *named* wave-wide re-consolidation must be shown.
**To close C-1:** run, on target PostgreSQL, the six per-table `row_count ≥1` + no-orphan audit JOIN queries in one transcript; each `orphan_count 0`.

### 🟡 C-2 — CI `LOCAL_CI_EXIT_CODE: 1` persists — DIAGNOSED as a TLS-intercept on the `npm audit` endpoint (not a code/vuln issue).
Despite the operator confirming network connectivity, the CI still fails at the `npm audit` step with:
`write EPROTO … SSL routines:tls_validate_record_header:wrong version number`.
**Diagnosis:** `wrong version number` means npm sent a TLS/HTTPS request to `registry.npmjs.org:443` but received a **plain-text (non-TLS) response** — the signature of a **proxy / TLS-inspection appliance / antivirus HTTPS interception / captive portal** sitting in the path. Connectivity exists; the **advisory endpoint is being intercepted**. This is the same environmental class already **operator-waived at W6-U07** (TD-W6-CI-AUDIT). All substantive CI gates pass (backend 350, frontend 18/58, build). See §4 for concrete fixes.
**Disposition:** carried as TD-W6-CI-AUDIT (operator-waived precedent). Not blocking on its own; folded into the closeout so the wave doesn't close with an unexplained red — **investigated, diagnosed, not relabeled green.**

---

## 3. Classification

- **C-1** — MEDIUM (named whole-wave completeness proof missing; underlying per-table no-orphan already proven at each unit; must be re-shown for a milestone).
- **C-2** — LOW / environmental (diagnosed TLS-intercept on `npm audit`; substantive gates green; operator-waived precedent; TD carried).
- No CRITICAL, no HIGH. No live-execution path, no broker logic outside External Integration, no Gate mutation, no actuation control, SIMULATED-everywhere — all proven. **Milestone is HELD** only because a closeout's defining artifact (six-table no-orphan) must be on record before I declare "Complete." Per proportionality (R13): every *risk* item proven ⇒ **CONDITIONAL**, not WITHHELD; **v0.54.0 + milestone HELD**, platform stays **v0.53.0**.

---

## 4. Concrete fix for the CI `npm audit` failure (operator-requested)

The `EPROTO / wrong version number` is a **TLS-path interception**, not a code bug. Any ONE of these resolves C-2 to a clean `LOCAL_CI_EXIT_CODE: 0`:

1. **Run the CI off the intercepting network** (home/mobile-hotspot or a network without a TLS-inspection proxy) — `npm audit` will then reach `registry.npmjs.org` and return `0 vulnerabilities` (as the online DR run already showed).
2. **Point npm at the registry over a trusted path / proxy:**
   `npm config set registry https://registry.npmjs.org/` and, if behind a corporate proxy, set `npm config set proxy http://<proxy>:<port>` and `https-proxy` accordingly (and ensure the proxy's CA is trusted, e.g. `npm config set cafile <corp-ca.pem>`). Do **not** use `strict-ssl false` as a fix — that hides the interception.
3. **Make the audit step degrade gracefully in `scripts/local_ci.sh`** so an unreachable advisory endpoint does not fail the gate: e.g. run `npm audit --audit-level=high || echo "npm audit endpoint unreachable — env, not a vulnerability"` guarded by a connectivity check, so CI yields exit 0 while still running audit when the endpoint is reachable. (Preferred for a reproducible local CI; keeps the gate meaningful online, non-fatal offline.)

Any of these + a re-run capturing `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` closes C-2/TD-W6-CI-AUDIT.

---

## 5. Not a finding (disclosed)

- The CI red is **diagnosed and recorded** (C-2/TD-W6-CI-AUDIT), not relabeled green; substantive gates (350 backend, 18/58 frontend) independently pass.
- Logged-out browser item: not re-litigated — accepted at W6-U07 FINAL by operator authorization on the passing auth test; closeout auth/route protection re-confirmed by the suite.
- Artifact counts grew since U07 (Runs 8→9, Ledger 7→8, Experiments 4→5, Analytics 3→4) from closeout seeds — expected, all SIMULATED.

---

## 6. Path to milestone (FINAL)

On receipt of **C-1** (six-table `row_count ≥1` + no-orphan audit JOIN `orphan_count 0`, raw psql on target) — and ideally **C-2** resolved via §4 (or formally re-waived) — I will write `ITRGA_VERDICT_W6-U08_FINAL_AND_WAVE6_CLOSURE.md`, bump to **v0.54.0**, declare **WAVE 6 CLOSED** and 🏛️ **"EXECUTION RESEARCH ENVIRONMENT COMPLETE."** A milestone is the highest-stakes approval in a wave; its defining whole-wave proof must be on record. Nothing here is relabeled green.

---

## 7. Posture note

The closeout is strong — whole-wave bright-line clean, Gate proven CLOSED wave-wide, SIMULATED across all six tables, browser E2E research-framed and non-actuating, docs reconciled, and the DA correctly did **not** self-declare the milestone. The one thing standing between here and "Complete" is the closeout's signature artifact: the six-table no-orphan audit JOIN. Show it, resolve/rewaive the diagnosed CI env-flake, and Wave 6 closes.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
