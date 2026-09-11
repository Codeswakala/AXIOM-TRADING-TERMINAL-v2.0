# DA DELIVERY NOTE — SUITE-ISOLATION CORRECTION (ITRGA-CB-V2-0047-SUITE-ISOLATION-001)
# AXIOM-V2-BE-7-DA-CB-001 · v1.0.0 · 2026-09-04 · AXIOM Trading Terminal v2.0
# Responds to: ITRGA-CB-V2-0047-SUITE-ISOLATION-001 (blocks the 0047 act's suite gate)
# Class per the brief: TEST-ISOLATION DEFECT in pre-BE-7 code — NOT a BE-7
# regression, NOT an instrument defect, NO schema or product behavior change.
# Author: Replacement Development Authority (DA)
# Status: SUBMITTED FOR ITRGA FULL-DEPTH VERIFICATION (brief R-5)

---

## §1 — Root cause confirmed on DA disk (Level I)

The brief's line-exact diagnosis reproduces here byte-for-byte:
`app/main.py::create_app()` registers the SPA catch-all
(`/{full_path:path}`, endpoint name `spa_fallback`) only when
`frontend/dist/index.html` exists (main.py L378–398); the
`error_probe_client` fixture adds its `/api/v1/v2/_test/*` probe routes
AFTER `create_app()`; Starlette matches in registration order, so with the
dist present the catch-all shadows the probes and serves index.html →
HTTP 200, the raise never executes.

**DA independent repro (the brief's Proof-2 form, executed here):** with a
stub `frontend/dist/index.html` present and the PRE-FIX fixture, both
tests fail exactly as the operator transcript shows — `assert 200 == 503`
and `assert 200 == 500`. Failing-run witness shipped (§4) — this also
serves the standing OBS-E commitment (a dedicated failing-run transcript
as fail-first evidence).

## §2 — Resolution implemented (R-1…R-3, exactly as ordered)

**R-1 — fixture-scope isolation repair.** In
`tests/test_v2_integration.py::error_probe_client`, immediately after
`create_app()` and before the probe routes are added, the fixture now
strips any route named `spa_fallback` from **that throwaway app
instance only**:

```python
application.router.routes[:] = [
    route
    for route in application.router.routes
    if getattr(route, "name", None) != "spa_fallback"
]
```

A docstring documents the conditional-registration law and cites the
brief by ID. With the dist absent the filter is a no-op (nothing named
`spa_fallback` exists); with it present the catch-all is removed from the
probe instance only — both tests now pass deterministically in BOTH arms.

**R-2 — zero application-code change.** `app/main.py` untouched
(`create_app()` and the SPA fallback semantics are contracted product
behavior for the terminal UI and remain exactly as accepted). The CB diff
surface is ONE file: `tests/test_v2_integration.py` — the fixture
docstring + the 5-line route filter. No other file changed; no BE-7
band file touched; **compver file sets unaffected** (RPE/RJE members do
not include any test file): RPE `1499343d…b178` and RJE `8f107d17…0598`
expectations for the 0047 act are UNMOVED.

**R-3 — cardinality held.** Full suite re-run **with the dist present**
(the operator-workstation condition): **972 collected, 972 passed, 0
failed, 0 skipped** — the BO floor exactly. (The stub dist used for the
proof was removed afterwards; the DA workspace carries no
`frontend/dist`, and the pre-existing `frontend/` source tree is
untouched.)

## §3 — Executed proof matrix

| Arm | Fixture | frontend/dist/index.html | Result |
|---|---|---|---|
| Failing-run witness | pre-fix | PRESENT (stub) | both tests FAIL — `assert 200 == 503` / `assert 200 == 500` (= operator field transcript) |
| Arm 1 | fixed | ABSENT | 2/2 PASS |
| Arm 2 | fixed | PRESENT (stub) | 2/2 PASS |
| Full suite | fixed | PRESENT (stub) | **972 passed / 0 failed** (raw `-v`, 494.30s) |

Ruff clean on the corrected file.

## §4 — Delivered file + evidence identities (R-4; full hashes, intake law)

| Artifact | Bytes | MD5 | SHA-256 |
|---|---|---|---|
| **`backend/tests/test_v2_integration.py`** (the corrected file — the only change) | 28,322 | `8269d2d5f7ef6817d74abc34b14ac216` | `84ac22435a73f402274c508edc31a657fb2424a49ea659f0164c18ed8257000b` |
| `docs/evidence/V2_BE-7_CB1_TESTRUN_DIST_PRESENT.txt` (full raw `-v`, 972/0, dist present) | 96,090 | `5583ac0cf3d0cab1252044c7af91292b` | `ba761a56a30e3d88cd91296a0bce1695f11b24a252b1b1f8c4f4afedc47e2808` |
| `docs/evidence/V2_BE-7_CB1_FAILING_RUN_WITNESS.txt` (pre-fix + dist present: the 200==503/500 failures) | 3,258 | `3dfe5506d8b70bcf21f76d238bb4c632` | `9b0fef58492a8a0efde2fb49e5f3bc53b26c39a525008e40dadd5e8d5a4e1e63` |

Credential scan CLEAN (household test-fixture placeholders only). No Git
operations; custody Operator-only.

## §5 — Operator landing instruction (through the standard channel)

Replace `backend\tests\test_v2_integration.py` on the workstation with
the delivered file and verify its SHA-256 equals
`84ac22435a73f402274c508edc31a657fb2424a49ea659f0164c18ed8257000b`
before any rerun. Per the brief's state-safety note: the working DB is
valid at `20260903_0047`, the rollback anchor is intact, and the resume/
verify instruments are inert — no other action until ITRGA verifies this
fix full-depth (R-5) and re-issues the completion instruction for
`ITRGA_V2_0047_APPLY_RESUME_PACK_V1.ps1` + `ITRGA_V2_0047_VERIFY_PACK_V5.ps1`
(edition 2).

**We don't guess. We prove.**

— AXIOM-V2-BE-7-DA-CB-001 · v1.0.0 · 2026-09-04
