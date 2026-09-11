# ITRGA DETERMINATION — UI-004-P04

**Validation & Economic-Usefulness Integrity Panels — the Verbatim-Verdict Surface**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Phase | **UI-004-P04** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-004-P04.md` |
| Governing docs | Doc 12 §6/§2.2, `UI-004_ENGINEERING_DESIGN_PLAN.md`, Doc 16 Brand Governance Standard |
| Binding refinements | R-6 (verbatim / no re-derivation), R-7 (Level-I + Doc-16) |
| Evidence standard | Level-I (operator-run on target) — report-claims alone never approve |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 40f/170t |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

| Check | Result |
|---|---|
| Delivery report header | `# DELIVERY REPORT — UI-004-P04` · Phase `**UI-004-P04**` (L1/L10) — OF the unit |
| Delivery report length | 364 lines — substantive, single-phase (not concatenated) |
| Operator transcript header | Same PowerShell session; opens by grepping `DELIVERY_REPORT_UI-004-P04.md` + `BUILD_ORDER_UI-004-P04.md` (L11–14) — OF the unit |
| Transcript length | 2272 lines — full session, not a stale prior-turn paste |
| Unit id in transcript | `UI-004-P04` throughout; predecessor `ITRGA_REVIEW_UI-004-P03.md` referenced |

**Pack is confirmed OF UI-004-P04.** No stale / wrong-phase / concatenated pack detected.

---

## 2. Level-I evidence verification (operator transcript, line-by-line)

| # | Mandatory item | Transcript evidence | Verdict |
|---|---|---|---|
| E-1 | 5 named P04 tests DISPLAYED passing | Isolated run 11:17:28 → **5 passed (5)**, all five named tests `✓` (L138–145) | ✅ PASS |
| E-2 | 🔴 Verbatim / no-re-derivation grep clean | `recompute\|recalculat\|reclassif\|deriveConfidence\|upgrade.*verdict\|normaliz.*(verdict\|status)\|new .*Engine\|/api/v1/orders` on `InstitutionalIntelligencePage.tsx` → **no output** (L239) | ✅ PASS |
| E-3 | 🔴 Named test proving stored verdict NOT reclassified/upgraded | `test_ui004_economic_usefulness_verdicts_are_not_rederived_or_upgraded` passed (isolated + focused runs) | ✅ PASS |
| E-4 | Verbatim rendering at source | Verdict/status values rendered as `<dd className="mono">{value}</dd>` and `{text(...)}` — direct string, no transform; `research_status ?? "research_only"` fallback only supplies a default when field ABSENT (never upgrades a stored value) | ✅ PASS |
| E-5 | No-cherry-picking (sample counts / scope / limitations + warnings) | Panel renders `sample_count`, `market_scope`/`included_scope`, `limitations` array; "No limitations array supplied…" fallback preserves absence honestly; named test `no_cherry_picking_sample_counts_scope_and_limitations_visible` passed | ✅ PASS |
| E-6 | No-actuation grep | `buy\|sell\|place_order\|execute\|go-live\|connect-broker\|account_id\|order_ticket\|open_gate\|allow_execution` → **no output** (L626) | ✅ PASS |
| E-7 | No-drift: Alembic head | `alembic current` → **`20260717_0037 (head)`** (L640) | ✅ PASS |
| E-8 | No-drift: dependencies | package grep → **`lightweight-charts@^4.2.0` only**; no new charting/markdown/fuzzy dep | ✅ PASS |
| E-9 | No-drift: no new endpoint/schema/persistence | grep for `/api/v1/research-intelligence\|/api/v1/validation-economic\|CREATE TABLE\|op.create_table\|createWorkspacePreference…` → no output | ✅ PASS |
| E-10 | No registry / route change (R-1) | Registry shows `research.intelligence` / `/intelligence` only; **no `/research-intelligence` route** (L659–662) | ✅ PASS |
| E-11 | Full-suite regression ≥40f/170t, no test lost | Clean re-run 11:58:57 → **41 files passed / 175 tests passed** (+1 file / +5 tests) | ✅ PASS (see OBS-P04-1) |
| E-12 | Backend ≥414 | `pytest -q` → **414 passed** (two runs) | ✅ PASS |
| E-13 | Doc-16 brand B-1…B-7 (never color alone) | `--ix-color-primary #3d8bfd` / `-success #3dd68c` / `-warning #f5a524` / `-critical #f31260` / `--font-mono` present; `.mono` on verdicts/statuses/sample_count/source-ids; **hardcoded-color grep on production TSX → no output**; ARIA-labelled sections; non-color status text | ✅ PASS |
| E-14 | Browser served-session verbatim verdicts | 5 served screenshots (login + /intelligence P01 inventory + P02 advisory + P02b analytics) — **P04 panel itself NOT captured** | ⚠️ OBS-P04-2 |
| E-15 | Networked CI / npm audit | `npm audit --audit-level=high` → **exit 0**; only 2 *moderate* react-router advisories (no high/critical); **TD-W6-CI-AUDIT flake did NOT recur this turn** (audit reached registry) | ✅ PASS |

---

## 3. Constitutional line

| Property | State |
|---|---|
| Governance Gate | CLOSED (unchanged) |
| Live broker/order/account/position/balance/margin/real-money path | NONE (no-actuation grep clean) |
| External LLM / AI-summary in feature | NONE (no-re-derivation grep clean) |
| Dynamic/third-party plugin execution | NONE |
| Client-side analytics engine | NONE (`no_client_side_analytics_engine` test passed) |
| Verbatim-verdict integrity (§2.2) | HELD — stored `research_only` / `not_assessed` / `warning:POORLY_CALIBRATED` rendered as-stored, never upgraded to tradable/approved/economically-usable |

The single highest-risk requirement of P04 — that stored validation and economic-usefulness verdicts are shown **exactly as stored and never reclassified or upgraded** — is proven at source and by the `not_rederived_or_upgraded` named test. **No reclassified/upgraded verdict was found.**

---

## 4. Observations (non-blocking, operator-adjudicated)

- **OBS-P04-1 (RESOLVED at operator direction — recorded as residual):** The canonical **gated** full-suite frontend run (11:34:40, `npm test` with `throw` on non-zero exit) returned **RED — 2 failed / 173 passed, exit 1**; the DA script threw `FRONTEND_VITEST_FAILED:1`. The two failures were **10 000 ms timeouts** on pre-existing UI-001/UI-002 tests — `InstitutionalWorkspaceShell.test.tsx > WorkspaceHost mounts each existing page content by route` and `WorkflowNavigationCompletion.test.tsx > test_ui002_all_routes_keep_single_ui001_shell_navigation_system` — **not P04 code, not assertion failures.** Root cause: machine load (environment 430.98 s vs 184.49 s on the clean run). A later re-run (11:58:57) was fully green **41f/175t**, with both tests passing (6 049 ms / 10 445 ms — borderline of the 10 s cap). **Operator adjudicated this a timing flake; the green re-run is authoritative.** *A red gate is not a footnote* — it is recorded here as a finding and as a standing residual: **the two shell/nav route-loop tests are timeout-fragile at the 10 s default under load and should be given an explicit `testTimeout` at UI-004-P05** so the gate is deterministic. The DA delivery report also **omitted the red gate** (reported only "41 files / 175 tests passed"); DA is reminded that intervening red gates must be surfaced in the delivery report, not silently superseded.
- **OBS-P04-2 (RESOLVED at operator direction — carried):** No served-session screenshot captured the **new P04 "Validation & Economic-Usefulness Integrity" panel** (Stored Validation Statuses / Stored Economic-Usefulness Verdicts / Scope-Sample-Limitations cards) — the supplied shots stop scrolling at the P02b analytics section. The panel's verbatim rendering is proven in **source** (lines 902–963) and by the **five named tests**. **Operator accepted the named-test + source proof this once.** DA must supply a served-session screenshot of the P04 panel showing at least one verbatim `research_only` / `not_assessed` / `warning:POORLY_CALIBRATED` verdict at the **UI-004-P05** intake to close this observation.
- **OBS-P04-3 (evidence-form, non-blocking):** The final `LOCAL_CI_EXIT_CODE` sentinel printed empty due to a variable-name typo (`$LASTEXITCODEnb`, L2271). All constituent CI gates were individually green (41f/175t, tsc clean, build success, npm-audit high exit 0). Fix the sentinel variable at P05.

---

## 5. Carried standing residuals (non-blocking)

- TD-W7-U07-RATE-GUARD (API rate guard deferred)
- TD-W6-CI-AUDIT (offline npm-audit CI exit-1 env-flake — **did not recur this turn**)
- UI-002-P04b (remaining global-search adapters — independent)

---

## 6. Disposition

**UI-004-P04 is APPROVED WITH OBSERVATIONS.** This authorizes issuance of the next Build Order (**UI-004-P05 — Research Artifacts, Collections & Saved-View Preferences**) upon operator "authorized". P05 binds: R-2 (if saved-state persisted → one inline raw psql save→SELECT ≥1 populated row on `operator_workspace_preferences`, ids only, no forbidden fields, + alembic head), R-4 (collections/tags READ-ONLY), and carries OBS-P04-1/-2/-3 closure conditions.

Baseline advances to: **v0.62.0 · head `20260717_0037` · backend 414 · frontend 41f/175t.**

Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
