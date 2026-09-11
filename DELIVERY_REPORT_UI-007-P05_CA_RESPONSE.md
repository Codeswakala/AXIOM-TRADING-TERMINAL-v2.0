# DELIVERY REPORT — UI-007-P05 Corrective Response

## Evidence Integrity and Authenticated Read-Capture Correction

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P05 corrective response** |
| ITRGA determinations | `ITRGA_REVIEW_UI-007-P05.md` and `ITRGA_REVIEW_UI-007-P05_ATTEMPT2.md` |
| Scope | Evidence capture, evidence runner, and delivery-record correction only; no P05 product re-implementation |
| Baseline | **Unchanged: v0.62.0 · head `20260717_0037` · backend 414 · frontend 59 files / 266 tests** |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |
| DA status | Corrective package prepared; not self-approved |

---

## 1. Findings accepted

| Finding | DA response |
|---|---|
| CA-P05-1 wrong P04 transcript | Closed by ITRGA attempt-2 review after the correct P05 transcript was supplied. |
| CA-P05-3 blank-token raw captures | Accepted. Six authenticated files were 30-byte `Not authenticated` responses; their secret-marker scan was a non-result. |
| CA-P05-4 backend manifest drift | Accepted. `backend/pyproject.toml` diff must be displayed and reconciled with the P04 conflict-repair record. |
| CA-P05-5 backend/Alembic/CI absent | Accepted. The P05 v1 runner did not complete its terminal evidence sequence. |
| CA-P05-2 logged-out P05 capture absent | Accepted. A P05-specific `/login` capture remains required. |

No P05 product code is changed by this corrective response.

---

## 2. Authenticated API-capture correction

Created:

```text
scripts/capture_ui007_p05_api_evidence.ps1
```

The script:

1. writes the login JSON through a UTF-8 no-BOM temporary body file and sends it with `curl.exe --data-binary @body.json`, eliminating PowerShell inline-JSON quote loss;
2. captures the login HTTP status to an artifact;
3. requires `HTTP 200` and a non-empty access token before any authenticated read request;
4. deletes the temporary body and login response before successful completion so the token is never preserved or printed;
5. requires each target endpoint to return HTTP 200;
6. creates a direct raw-value comparison file for system version, persistence counts, and API catalogue Alembic head;
7. runs `SECRET_MARKER_COUNT` only over real, authenticated response payloads;
8. emits a terminal clean sentinel only when all capture and secret checks pass.

A failed login now stops the capture utility before downstream error bodies can be written as false API evidence.

---

## 3. P05 evidence-runner v2.0.0

Updated:

```text
scripts/run_ui007_p05_evidence.ps1
docs/evidence/UI-007-P05_OPERATOR_EVIDENCE_COMMANDS.md
```

The v2.0.0 runner retains non-halting per-gate capture and now explicitly records:

- a final terminal summary after the automated gate sequence;
- per-gate exit codes;
- named P05 test transcript;
- full frontend/backend/Alembic/CI artifacts;
- no-control/no-actuation/no-recompute/no-external-AI source checks;
- the exact backend manifest diff alongside registry and frontend-manifest deltas.

The corrected command pack directs the Operator to execute scripts rather than continue hand-entered commands after a thrown token validation error.

A final single-transcript wrapper, `scripts/run_ui007_p05_final_evidence.ps1`, is also provided. It relays the existing audit artifact, runs only the remaining verified-token capture, pauses for the P05 logged-out screenshot, and writes every remaining output to `UI-007-P05_OPERATOR_RESULTS.txt` without repeating accepted full regression gates. Its root resolution is performed after parameter binding, avoiding Windows PowerShell `-File` evaluation of an empty `$PSScriptRoot` default.

---

## 4. `backend/pyproject.toml` reconciliation

The checked worktree diff is:

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

This is the disclosed P04 conflict-repair resolution, not a P05 dependency or tool-configuration change. The selected `HEAD` version remains `0.56.0`; no dependency section changed. The v2 evidence runner now captures this exact diff rather than emitting a false clean manifest-drift result.

ITRGA must independently confirm this context from the target evidence; DA does not self-approve the reconciliation.

---

## 5. Required remaining evidence

The corrective P05 submission must include:

- verified-token raw responses for `/api/v1/system/info`, `/api/v1/persistence/stats`, and the other existing P05 read APIs;
- screenshot/raw comparison of at least two direct values;
- meaningful `SECRET_MARKER_COUNT: 0` over real HTTP-200 payloads;
- displayed `backend/pyproject.toml` diff;
- backend 414, Ruff, target Alembic head, networked CI output, and P05 runner terminal summary;
- P05-specific logged-out `/login` capture.

---

## 6. Files created or modified

```text
scripts/capture_ui007_p05_api_evidence.ps1
scripts/run_ui007_p05_evidence.ps1
scripts/run_ui007_p05_final_evidence.ps1
docs/evidence/UI-007-P05_OPERATOR_EVIDENCE_COMMANDS.md
docs/evidence/UI-007-P05_FINAL_EVIDENCE_COMMANDS.md
DELIVERY_REPORT_UI-007-P05_CA_RESPONSE.md
docs/build-orders/ITRGA_REVIEW_UI-007-P05.md
docs/build-orders/ITRGA_REVIEW_UI-007-P05_ATTEMPT2.md
```

No backend application behaviour, schema, migration, dependency, route, registry, or P05 presentation capability was changed by the corrective response.

---

## 7. DA disposition

P05 remains **Corrective Actions Required** on evidence integrity, not product implementation. The next action is one verified-token target capture plus the v2.0.0 automated evidence runner and P05 logged-out browser proof, followed by ITRGA re-review.

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**
