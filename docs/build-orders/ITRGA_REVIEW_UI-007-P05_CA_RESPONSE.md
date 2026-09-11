# ITRGA DETERMINATION — UI-007-P05 (Corrective Response)

**Platform Health, System Readiness, Version & API Posture — Evidence Integrity Correction**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P05 — corrective response** |
| Supersedes | `ITRGA_REVIEW_UI-007-P05_ATTEMPT2.md` (CA-P05-2/-3/-4/-5) |
| Pack | `DELIVERY_REPORT_UI-007-P05_CA_RESPONSE.md` (131 lines) + `OPERATOR_RESULTS.md` (**935 lines**, runner v2.0.0) + 2 served screenshots |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 59f/266t |
| **DETERMINATION** | 🟡 **CORRECTIVE ACTIONS REQUIRED (CA-P05-4 ✅ · CA-P05-5 ✅ · CA-P05-3 ❌ · CA-P05-2 ❌)** |
| Baseline | **UNCHANGED — v0.62.0** |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build identity — ✅ PASS

New, genuine P05 run: **935 lines / 97,098 bytes** (vs the 519-line attempt-2), `UI007_P05_EVIDENCE_STARTED: 2026-07-28T19:29:59`, **67 P05 references**, runner **v2.0.0**. Browser metrics show `Uptime 5084.911s` against attempt-2's `1875.625s` — a genuinely fresh session, not a re-attachment.

---

## 2. ✅ CA-P05-5 — CLOSED. Backend, Alembic and CI now complete.

Every gate absent last turn is now present and green:

| Gate | Evidence | Verdict |
|---|---|---|
| Backend full suite | **`414 passed, 1919 warnings in 547.75s`** (L603); `BACKEND_PYTEST_EXIT_CODE: 0` (L324) | ✅ |
| Ruff | `UI007_P05_RUFF` exit **0** | ✅ |
| Alembic on target | **`20260717_0037 (head)`** (L607); exit 0 | ✅ |
| **Networked CI** | **`LOCAL_CI_EXIT_CODE: 0`** (L611) — clean, no waiver needed | ✅ |
| Frontend full suite | **`Test Files 60 passed (60)` / `Tests 271 passed (271)`**; `FRONTEND_VITEST` exit 0 | ✅ |
| TypeScript / build | Both exit 0 | ✅ |
| Terminal summary | Per-gate exit-code table + `UI007_P05_EVIDENCE_COMPLETED_WITH_FINDINGS: NPM_AUDIT_HIGH=1` + `EVIDENCE_FINISHED` + `RUNNER_INVOCATION_EXIT_CODE: 1` | ✅ |

**OBS-P05-3 is also CLOSED** — the v2.0.0 runner restores the per-gate table and terminal sentinel, and closes with *"All raw evidence artifacts were collected. Do not relabel a nonzero result green."*

Note `LOCAL_CI_EXIT_CODE: 0` is the **first fully clean networked CI in this workstream** — `TD-UI005-COMPLETION-TIMEOUT` did not recur.

---

## 3. ✅ CA-P05-4 — CLOSED. The manifest delta is a leftover conflict marker, version-only.

The diff I demanded is supplied:

```diff
 [project]
 name = "axiom-backend"
-<<<<<<< HEAD
 version = "0.56.0"
-=======
-version = "0.35.0"
->>>>>>> 7aff710a248d8ec2451040b3e023391cb04908c1
 description = "AXIOM institutional trading research platform — backend foundation"
```

**Assessment:** this is not a P05 change. It is the removal of an unresolved merge-conflict block left in `backend/pyproject.toml` — residue of the **56-block / 25-file conflict repair disclosed at P04**. The retained `HEAD` value `0.56.0` is unchanged; **no dependency, tool-configuration, or build section was touched.** The referenced SHA `7aff710a…` is the **old pre-re-initialisation commit** identified in the UI-002-P05 provenance precedent, which corroborates the account exactly.

The apparent contradiction with report §10 ("no package manifest was modified") is resolved: the file was *repaired*, not *modified for P05*. **Under R12 the contradiction is dissolved by evidence, not by assertion** — and the drift gate now reports exit **0** with the diff captured rather than a bare failure.

**A note for the record:** this is the second time conflict residue from that committed baseline has surfaced inside a phase review. It reinforces **`TD-AXIOM-GIT-PROVENANCE`** as a genuine pre-certification blocker.

---

## 4. ❌ CA-P05-3 — STILL OPEN. Login failed again, with a different root cause.

The as-returned proof — the defining G-5 requirement of this phase — did not succeed:

```
UI007_P05_LOGIN_HTTP_STATUS: 422
{"detail":[{"type":"json_invalid","loc":["body",1],"msg":"JSON decode error",
 "ctx":{"error":"Expecting property name enclosed in double quotes"}}]}
UI007_P05_LOGIN_HTTP_STATUS_UNEXPECTED:422  → THROW → capture halted
```

**What changed, and what did not:**

| | Attempt 2 | This attempt |
|---|---|---|
| Failure | Empty token, run **continued** | HTTP **422**, capture **halted** |
| Artifacts written | Six 30-byte `Not authenticated` bodies | **None** |
| `SECRET_MARKER_COUNT: 0` | **False-clean over error bodies** | **Not claimed** |

**The harness fix is correct and I credit it fully.** The new `capture_ui007_p05_api_evidence.ps1` asserts HTTP 200 and a non-empty token *before* any authenticated call, and it stopped dead rather than manufacturing evidence. **The false-clean failure mode is eliminated** — that was the substance of CA-P05-3's criticism, and it is fixed.

**But the proof itself still does not exist.** No raw payload for `/api/v1/system/info` or `/api/v1/persistence/stats`; no raw-vs-rendered comparison; no meaningful secret scan. Item (e) and item (i) remain unmet.

**Root cause is a shell-quoting defect, not a product defect.** The 422 is `json_invalid` at `body` position 1 — the JSON body reached FastAPI malformed. This is the well-known PowerShell single-quote/`curl.exe` interaction: `-d '{"username":"admin",...}'` loses its quoting through the native-command boundary. The API is behaving correctly by rejecting a malformed body. **Auth is not broken.**

**Suggested fix (evidence tooling only):** write the JSON to a temp file and use `curl.exe -d "@body.json"`, or use `Invoke-RestMethod -Body (@{username='admin';password="<REDACTED_DEV_PASSWORD>"} | ConvertTo-Json) -ContentType 'application/json'`. Also confirm `AXIOM_BOOTSTRAP_ADMIN_ENABLED=true` and `AXIOM_ALLOW_INSECURE_DEV=true` are set in the capture shell.

---

## 5. ❌ CA-P05-2 — STILL OPEN. No logged-out capture.

Both screenshots are authenticated `/governance` (admin + Sign out visible). No P05 `/login` capture. Under **R4** this remains outstanding. The P04 Incognito shot was exemplary — repeat that pattern.

---

## 6. 🟡 New finding — OBS-P05-4: `NPM_AUDIT_HIGH = 1` disclosed but not detailed

The gate table shows `NPM_AUDIT_HIGH  1`, and the runner honestly surfaced it in the terminal sentinel rather than hiding it. **That is correct conduct.** However, the audit output was written to `UI-007-P05_NPM_AUDIT.txt` and **not echoed into the transcript**, so I cannot see what tripped it.

This matters because attempt-2 recorded `NPM_AUDIT_HIGH_EXIT_CODE: 0` with only 2 *moderate* react-router advisories. **A high-or-critical advisory appearing between runs is a material change I must see, not infer.** It could be a newly-published advisory against an existing dependency — but no dependency changed, so this needs its content displayed.

**Required:** echo the npm audit output inline. If a genuine high/critical advisory has appeared, it needs a tracked residual and a disposition.

---

## 7. Findings

| ID | Severity | Status |
|---|---|---|
| CA-P05-1 | CRITICAL | ✅ CLOSED (attempt 2) |
| **CA-P05-4** | HIGH | ✅ **CLOSED** — conflict-marker residue, version-only, no dependency change |
| **CA-P05-5** | HIGH | ✅ **CLOSED** — backend 414, ruff, alembic head, **CI exit 0**, terminal summary |
| OBS-P05-3 | OBSERVATION | ✅ **CLOSED** — v2.0.0 runner restored |
| **CA-P05-3** | **CRITICAL** | ❌ **OPEN** — login HTTP 422 (`json_invalid`); no authenticated payloads; items (e) and (i) unmet. **Harness now fails correctly instead of false-cleaning** |
| **CA-P05-2** | MEDIUM | ❌ **OPEN** — logged-out `/login` capture |
| **OBS-P05-4** | OBSERVATION (new) | `NPM_AUDIT_HIGH = 1` disclosed but content not echoed; was 0 last run. Display it |
| OBS-P05-2 | OBSERVATION | Vite chunk-size advisory, non-failing. Carried |
| — | **COMMENDATION** | The corrective response **accepts all five findings without relabeling any**, fixes the exact defect criticised — a harness that continued past a failed login — and produces the `pyproject.toml` diff that dissolved CA-P05-4 honestly. `RUNNER_INVOCATION_EXIT_CODE: 1` and the `WITH_FINDINGS` sentinel are reported plainly. **The DA has now twice built tooling whose purpose is to make its own failures impossible to conceal.** That is the standard functioning as intended |

---

## 8. Required to close — two items

1. **CA-P05-3** — re-run `capture_ui007_p05_api_evidence.ps1` with the login body correctly quoted (temp-file `@body.json` or `Invoke-RestMethod`). Show `LOGIN_HTTP_STATUS: 200`, a non-empty token assertion, then **raw JSON beside rendered UI value for ≥2 surfaces** (`/api/v1/system/info` version + alembic head; `/api/v1/persistence/stats` a count), and `SECRET_MARKER_COUNT: 0` over **real HTTP-200 payloads**.
2. **CA-P05-2** — logged-out `/login` capture (Incognito, URL bar visible).
3. *(OBS-P05-4, same run)* — echo the npm audit output.

**Do not re-run anything else.** Backend 414, alembic head, CI exit 0, frontend 60f/271t, the 5 named tests, tsc, build, all boundary greps and the manifest diff are **proven and stand**. This is one capture script and one screenshot.

---

## 9. Disposition

**UI-007-P05 remains CORRECTIVE ACTIONS REQUIRED — but two of the four findings are closed and the critical one has been materially de-fanged.**

CA-P05-4 and CA-P05-5 are discharged: the manifest delta proved to be conflict residue from the P04 repair with no dependency change, and the full backend/Alembic/CI envelope is now green — including the first clean networked CI of this workstream.

CA-P05-3 stays open, but its character has changed. Last turn the harness manufactured a false-clean: six 30-byte error bodies scanned for secrets and reported clean. This turn the harness **detected the failure and stopped**, writing nothing. The proof is still missing, so I cannot approve — but the *evidence-integrity defect* that made the earlier submission dangerous is fixed. What remains is a shell-quoting bug in a capture script, not a product or governance problem.

Everything substantive about P05 is proven: H-1 in source and browser, H-2 residual honesty, H-3 as-stored, the five named tests, the full regression envelope, and every governance-boundary grep. **Two mechanical artifacts stand between this phase and approval.**

Verification is limited to supplied evidence. Direct validation of authenticated read payloads and logged-out behaviour was not possible.

**Baseline does NOT advance — v0.62.0 · head `20260717_0037` · backend 414 · frontend 59f/266t.** UI-007-P06 remains unauthorized. Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**.

Carried residuals: TD-UI-REACTROUTER-MODERATE · TD-W7-U07-RATE-GUARD · TD-W6-CI-AUDIT · UI-002-P04b · TD-UI005-COMPLETION-TIMEOUT · **TD-AXIOM-GIT-PROVENANCE** (pre-certification, reinforced by §3). *(TD-UI-POSTCSS-HIGH CLOSED.)*

---

## 10. Evidence Confidence Statement

- **Evidence reviewed:** `OPERATOR_RESULTS.md` (935 lines, read in full); `DELIVERY_REPORT_UI-007-P05_CA_RESPONSE.md` (131 lines); 2 served `/governance` screenshots.
- **Confidence:** **HIGH** that CA-P05-5 is closed — backend 414, alembic head, and `LOCAL_CI_EXIT_CODE: 0` are directly evidenced. **HIGH** that CA-P05-4 is closed — the diff shows conflict-marker removal with an unchanged version and no dependency section. **HIGH** that CA-P05-3 remains unmet and that its cause is shell quoting (`json_invalid` at body position 1), not auth. **LIMITED** on `NPM_AUDIT_HIGH = 1` — disclosed, content not shown.
- **Remaining unknowns:** authenticated payload values vs rendered; npm audit advisory content; logged-out behaviour this phase.
- **Additional evidence required:** §8 items 1–3.

---

*Last turn the harness invented a clean result. This turn it refused to. The proof is still owed — but the instrument can now be trusted, and that was the harder half.*

**We don't guess. We prove.**

*— AXIOM ITRGA*
