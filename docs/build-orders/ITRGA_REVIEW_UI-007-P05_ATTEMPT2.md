# ITRGA DETERMINATION — UI-007-P05 (Attempt 2 — correct transcript)

**Platform Health, System Readiness, Version & API Posture** — *(Read-Only)*

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P05** |
| Supersedes | `ITRGA_REVIEW_UI-007-P05.md` (wrong-pack transcript — now resolved) |
| Pack | `DELIVERY_REPORT_UI-007-P05.md` + **correct** `OPERATOR_RESULTS.md` (519 lines, runner v1.0.0) + 5 served screenshots |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 59f/266t |
| **DETERMINATION** | 🟡 **CORRECTIVE ACTIONS REQUIRED** |
| Baseline | **UNCHANGED — v0.62.0** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build identity — ✅ PASS (the relay error is resolved)

| Check | Result |
|---|---|
| Phase references | **`UI007_P05`: 83** · `UI007_P04`: 6 (contextual citations only) | ✅ |
| Size | 519 lines / 65,554 bytes — **not** the 2270-line / 162,572-byte P04 file | ✅ |
| Sentinels | `UI007_P05_EVIDENCE_STARTED: 2026-07-28T17:32:53`; `UI007_P05_RUNNER_VERSION: 1.0.0`; `UI007_P05_BUILD_IDENTITY_CONFIRMED` | ✅ |
| Repo root | `C:\Users\Swakala\.vscode\AXIOM\axiom` | ✅ |

**Pack confirmed OF UI-007-P05.** The prior determination's sole finding (CA-P05-1, wrong-pack) is **CLOSED**. The correct transcript now permits substantive review — and that review surfaces three genuine findings the stale file had concealed.

---

## 2. ✅ What is proven at Level-I

| # | Item | Evidence | Verdict |
|---|---|---|---|
| (b) | **5 P05 named tests DISPLAYED passing** | All five by name with timings (L75–79); `Test Files 1 passed (1)` / `Tests 5 passed (5)`; `UI007_P05_NAMED_VITEST_EXIT_CODE: 0` | ✅ |
| (c) | 🔴 **H-1 forbidden-label grep** | `production\.ready\|all systems go\|fully operational\|production_ready` → no hits; `UI007_P05_FORBIDDEN_RUNTIME_LABEL_EXIT_CODE: 0`; `UI007_P05_RUNTIME_CERTIFICATION_LABEL_GREP_CLEAN` | ✅ |
| (c) | 🔴 **H-1 positive proof** | Source shows `Production NOT CERTIFIED` at 6 sites, `Doc 11 HELD`, and the literal `<strong>Runtime readiness is not production certification.</strong>` callout; `UI007_P05_CERTIFICATION_VOCABULARY_IS_STORED_DOC11_TEXT` | ✅ **Exemplary** |
| (d) | 🔴 **H-2 residual honesty** | Source grep confirms all six rendered: `TD-UI-REACTROUTER-MODERATE`, `TD-W7-U07-RATE-GUARD`, `TD-W6-CI-AUDIT`, `UI-002-P04b`, `TD-UI005-COMPLETION-TIMEOUT`, **`TD-AXIOM-GIT-PROVENANCE`**; browser shows correct severities incl. OPEN·HIGH·PRE-CERT BLOCKER | ✅ |
| (H-3) | `admin/admin123` as-stored | `ADMIN_DEFAULT_CREDENTIAL_REJECTED_WITH_INSECURE_DEV_OFF` rendered verbatim | ✅ |
| (f) | 🔴 G-2 governance-control grep | `UI007_P05_GOVERNANCE_CONTROL_EXIT_CODE: 0` | ✅ |
| (g) | 🔴 M-4 + ops-actuation grep | `UI007_P05_NO_ACTUATION_EXIT_CODE: 0` | ✅ |
| (h) | 🔴 No-recompute + external-AI | `UI007_P05_R6_NO_RECOMPUTE_EXIT_CODE: 0`; `UI007_P05_EXTERNAL_AI_EXIT_CODE: 0` | ✅ |
| (j) | No new endpoint | `UI007_P05_ROUTE_DECLARATIONS_EXIT_CODE: 0`; `UI007_P05_ROUTE_DECLARATION_GREP_CLEAN` | ✅ |
| (k) | Frontend regression | `FRONTEND_VITEST_EXIT_CODE: 0`; **`Test Files 60 passed (60)` / `Tests 271 passed (271)`** — baseline 59f/266t **+5** = exactly the P05 tests, no test lost | ✅ |
| — | TypeScript / build | `UI007_P05_TYPESCRIPT_EXIT_CODE: 0`; `UI007_P05_FRONTEND_BUILD_EXIT_CODE: 0` | ✅ |
| — | npm audit high gate | `NPM_AUDIT_HIGH_EXIT_CODE: 0`; 2 moderate react-router advisories disclosed | ✅ |

The report's claimed 60f/271t is now **Level-I confirmed on target**. H-1 — this phase's spine — is proven in both source and browser.

---

## 3. 🔴 CA-P05-3 (CRITICAL) — the as-returned proof is a non-result: blank-token captures

Item (e) — **raw API response compared against rendered value** — was the central G-5 requirement of this phase. It did not succeed.

**The login failed and the run continued anyway:**

```
$login = curl.exe -sS -X POST "$baseUrl/api/v1/auth/login" -d '{"username":"admin","password":"admin123"}'
$token = ($login | ConvertFrom-Json).tokens.access_token
if (-not $token) { throw 'UI007_P05_LOGIN_TOKEN_MISSING' }

UI007_P05_LOGIN_TOKEN_MISSING          ← THREW: token was empty
  + CategoryInfo : OperationStopped
```

The `throw` fired, but because these were **interactive line-by-line commands rather than a guarded script block**, execution continued to the next prompt. Every subsequent authenticated capture ran with `Authorization: Bearer ` — an empty token.

**The file sizes prove the consequence:**

| Raw capture | Bytes | Reading |
|---|---:|---|
| `RAW_HEALTH.json` | 191 | ✅ Real payload (unauthenticated endpoint) |
| `RAW_READY.json` | 1100 | ✅ Real payload (unauthenticated endpoint) |
| `RAW_METRICS.json` | **30** | ❌ |
| `RAW_PERSISTENCE_STATS.json` | **30** | ❌ |
| `RAW_SYSTEM_INFO.json` | **30** | ❌ |
| `RAW_ROUTE_INVENTORY.json` | **30** | ❌ |
| `RAW_RBAC.json` | **30** | ❌ |
| `RAW_API_CATALOGUE.json` | **30** | ❌ |
| `RAW_PLUGIN_CONTRACTS.json` | **30** | ❌ |

`{"detail":"Not authenticated"}` is **exactly 30 bytes**. Six authenticated endpoints returned byte-identical 30-byte error bodies. These are not API responses — they are auth rejections.

**Three consequences:**

1. **Item (e) is unproven.** No raw-vs-rendered comparison exists for `/api/v1/system/info` (version, alembic head) or `/api/v1/persistence/stats` — the two surfaces the Build Order named. `/health` and `/ready` captured real payloads, but they are the unauthenticated pair and were never displayed side-by-side with rendered values.
2. **`SECRET_MARKER_COUNT: 0` is a false-clean.** The secret scan ran over these nine files — six of which contain only `{"detail":"Not authenticated"}`. **A secret scan over error bodies proves nothing.** The pattern itself is sound; the corpus was empty. This is item (i) unmet.
3. **This is the W7-U02 blank-token lesson, exactly.** That precedent is recorded in the onboarding standard: *"for any auth probe, FIRST verify each `/auth/login` returned 200 with a non-empty token before trusting downstream status codes; a blank-token result is an R7 non-result, not a pass."* The runner correctly detected the condition and threw — the interactive invocation simply failed to halt on it.

**Note:** this does **not** indicate an auth defect. The most likely cause is the API server running without `AXIOM_BOOTSTRAP_ADMIN_ENABLED` / `AXIOM_ALLOW_INSECURE_DEV` set in that shell, or a differently-shaped login response. It is an evidence-harness fault, not a product fault.

---

## 4. 🟠 CA-P05-4 (HIGH) — manifest drift gate FAILED, and it contradicts the delivery report

```
UI007_P05_NO_MANIFEST_OR_REGISTRY_DRIFT_EXIT_CODE: 1
=== REGISTRY DELTA ===        (empty — good)
=== MANIFEST DELTA ===
backend/pyproject.toml
```

The delivery report §10 states:

> *"No backend production source, API route, database schema, migration, **package manifest**, dependency, workspace registry, or application route was modified for P05."*

**The evidence contradicts the report.** `backend/pyproject.toml` is a package manifest and it appears in the delta. Under **R12**, evidence that contradicts a report claim is a higher-severity finding.

**Mitigating context, stated fairly:** the transcript emits a Git line-ending warning for that same file (`LF will be replaced by CRLF`), and `pyproject.toml` was one of the 25 files repaired during the P04 conflict-resolution event. The delta may well be a CRLF-only artifact carried from that repair, with no semantic change. **But no diff was shown**, so I cannot distinguish a whitespace artifact from a dependency or tool-configuration change — and P05 is a presentation-only phase with a hard no-backend-manifest boundary.

**Required:** `git diff -- backend/pyproject.toml` displayed. If line-endings only, that closes it. If any content changed, it is an unauthorized backend modification in a presentation phase.

---

## 5. ❌ CA-P05-5 (HIGH) — backend regression, alembic, and CI absent; transcript ended early

Searched the full 519 lines:

| Required | Present? |
|---|---|
| Backend `pytest -q` ≥414 passed | ❌ No `414 passed`, no `collected 414` |
| `BACKEND_PYTEST_EXIT_CODE: 0` | ❌ Never printed |
| Backend Ruff | ❌ Absent |
| `alembic current` = `20260717_0037` | ❌ Absent (only a citation of the P04 review header at L28) |
| Networked CI `LOCAL_CI_EXIT_CODE` | ❌ Absent |
| Final summary sentinel | ❌ Absent — no `EVIDENCE_COMPLETED_CLEAN` / `WITH_FINDINGS` |

The transcript ends after the H-1 label greps. **The P04 corrective runner (v2.0.0) printed a per-gate summary table and a terminal completion sentinel; this P05 runner is v1.0.0 and does neither.** That regression in harness discipline is why an incomplete run reads as if it simply stopped.

**Also missing: (m) logged-out `/login` capture for P05** — carried from the prior determination as CA-P05-2, still open.

---

## 6. Findings

| ID | Severity | Status |
|---|---|---|
| CA-P05-1 | CRITICAL | ✅ **CLOSED** — correct P05 transcript supplied |
| **CA-P05-3** | **CRITICAL** | **OPEN** — as-returned proof (e) is a blank-token non-result; six 30-byte `Not authenticated` bodies; `SECRET_MARKER_COUNT: 0` is a false-clean over error payloads (i) |
| **CA-P05-4** | **HIGH** | **OPEN** — `backend/pyproject.toml` in manifest delta; drift gate exit 1; **contradicts report §10** (R12). Diff required |
| **CA-P05-5** | **HIGH** | **OPEN** — backend pytest / ruff / `alembic current` / CI absent; no completion sentinel |
| CA-P05-2 | MEDIUM | **OPEN** — logged-out `/login` capture for P05 |
| OBS-P05-2 | OBSERVATION | Vite chunk-size advisory (>500 kB), non-failing. Carried |
| **OBS-P05-3** | OBSERVATION (new) | P05 runner is **v1.0.0**; adopt the **v2.0.0** pattern (per-gate exit table, terminal completion sentinel, guarded script block so a `throw` halts rather than falling through to the next interactive prompt) |
| — | **COMMENDATION** | **H-1 is the best-executed requirement in this workstream.** The certification boundary is stated in source at six sites and in the browser four ways, the forbidden-label grep is clean, and Doc-11 vocabulary is rendered as stored. **H-2 likewise** — both residuals I opened during this review cycle, including the HIGH pre-certification blocker against the repository itself, are displayed at honest severity. The DA also correctly declared local validation as local and never claimed target evidence it did not have |

---

## 7. Required corrections

1. **CA-P05-3** — re-run the API capture **with a verified token**: print the login HTTP status and assert a non-empty token *before* any authenticated call (fail loudly, do not continue). Then show, for **≥2 surfaces** (`/api/v1/system/info` version + alembic head; `/api/v1/persistence/stats` a count), **the raw JSON beside the rendered UI value**, proving they match. Re-run the secret scan over the **real** payloads so `SECRET_MARKER_COUNT: 0` means something.
2. **CA-P05-4** — display `git diff -- backend/pyproject.toml`. Confirm line-endings-only, or justify the change.
3. **CA-P05-5** — backend `pytest -q` ≥414 with `BACKEND_PYTEST_EXIT_CODE: 0`; ruff; `alembic current 20260717_0037`; networked CI (a named tracked flake is acceptable if disclosed after gates are green).
4. **CA-P05-2** — logged-out `/login` capture (the P04 Incognito shot was exemplary).
5. **OBS-P05-3** — adopt the v2.0.0 runner pattern.

**No re-implementation.** Do not re-run the already-proven gates: the 5 named tests, frontend 60f/271t, tsc, build, and all boundary greps stand.

---

## 8. Disposition

**UI-007-P05 is CORRECTIVE ACTIONS REQUIRED.**

The wrong-pack finding is closed and the substantive review is now possible — and it shows a phase whose *hardest* requirement is met with real distinction. H-1 is proven: runtime readiness is fenced from production certification in source and on screen, with no forbidden label anywhere. H-2 is proven: every residual, including the HIGH pre-certification blocker, renders honestly. The five named tests pass, the frontend suite advances to 60f/271t with the +5 reconciling exactly, and every governance-boundary grep is clean.

What blocks approval is **evidence integrity, not engineering**. The as-returned proof — the one item that makes "displayed as returned" a verified claim rather than a design intention — captured six authentication errors instead of six API payloads, and the secret scan then ran over those errors and reported clean. That is a false-clean of exactly the kind this project has ruled against since W7-U02, and I will not accept it merely because the surrounding work is strong. Compounding it, the drift gate failed against a backend manifest while the report asserts no manifest changed, and the backend, alembic and CI gates never ran.

The corrections are mechanical and narrow. The product is not in question.

Verification is limited to supplied evidence. Direct validation of the authenticated read payloads, backend suite, migration head, and CI was not possible.

**Baseline does NOT advance — v0.62.0 · head `20260717_0037` · backend 414 · frontend 59f/266t.** UI-007-P06 remains unauthorized. Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**.

Carried residuals: TD-UI-REACTROUTER-MODERATE · TD-W7-U07-RATE-GUARD · TD-W6-CI-AUDIT · UI-002-P04b · TD-UI005-COMPLETION-TIMEOUT · **TD-AXIOM-GIT-PROVENANCE** (pre-certification). *(TD-UI-POSTCSS-HIGH CLOSED.)*

---

## 9. Evidence Confidence Statement

- **Evidence reviewed:** correct `OPERATOR_RESULTS.md` (519 lines, read in full); `DELIVERY_REPORT_UI-007-P05.md` (220 lines); 5 served `/governance` screenshots.
- **Confidence:** **HIGH** that H-1, H-2, H-3, the five named tests, the frontend suite (60f/271t), tsc/build, and all boundary greps are proven at Level-I. **HIGH** that the as-returned proof failed on a blank token — the `LOGIN_TOKEN_MISSING` throw and six byte-identical 30-byte captures are conclusive. **HIGH** that backend/alembic/CI are absent. **LIMITED** on whether the `pyproject.toml` delta is semantic or line-endings-only — no diff was shown.
- **Remaining unknowns:** authenticated payload values vs rendered; `pyproject.toml` diff content; backend/alembic/CI state on target; logged-out behaviour this phase.
- **Additional evidence required:** §7 items 1–5.

---

*A secret scan that finds nothing in an empty file is not a clean result — it is no result. The distinction is the whole discipline.*

**We don't guess. We prove.**

*— AXIOM ITRGA*
