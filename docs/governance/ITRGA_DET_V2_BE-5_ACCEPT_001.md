# ITRGA FINAL ACCEPTANCE RECORD + BUILD-ORDER CLOSURE — V2 BE-5

- **RECORD_ID:** `ITRGA-DET-V2-BE-5-ACCEPT-001`
- **Date:** 2026-09-02
- **Authority:** the Operator's final acceptance authorization of 2026-09-02 ("final acceptance authorized"), received after `ITRGA-DET-V2-0045-APPLY-001` (C-2 CLOSED; terminal state landed on the working lineage).
- **Chain:** BO-V2-BE-5-001 → DR v1.0.1 + REM-001 Rev-2 → C-1/C-2 closed → `ITRGA-DET-V2-BE-5-FINAL-001` (C full-verify PASS) → `ITRGA-DET-V2-0045-APPLY-001` → **this record**.

## 1. Acceptance recorded

The Operator's authorization is recorded verbatim against the recommendation in `ITRGA-DET-V2-BE-5-FINAL-001` §7. With it:

- `AXIOM-V2-BE-5-DR-001` **v1.0.1** stands as the delivery of record.
- **BO-V2-BE-5-001 is CLOSED.** Terminal state T-1…T-12 is complete on both evidence planes: in-band Level I/II (DA executed: 12/12 inline ASSERTs; 856 passed/0 failed; drift gates at both heads) and working-lineage Level I (operator-run apply+verify envelope, all gates PASS).
- Correction registers: **C-1, C-2 — both CLOSED.** No open items in the BE-5 chain.

## 2. Maturity grant

| Register row (V2_CAPABILITY_MATURITY) | Band | New state | Evidence | Date |
|---|---|---|---|---|
| `ML Research Expansion` (6-ML) | BE-5 | **COMPLETE** | DET-V2-BE-5-FINAL-001 + DET-V2-0045-APPLY-001 | 2026-09-02 |
| `Signal Architecture V2` (4-SIGNAL) | BE-5 | **COMPLETE** | same | 2026-09-02 |

The grant is the acceptance act's, not the DA's (DR §7 staged IMPLEMENTED only).

## 3. Evidence inventory (closing the band; full hashes)

| Artifact | MD5 / SHA-256 |
|---|---|
| `V2_BE-5_SOURCE_TRANSCRIPT.md` (Rev 2) | `36e59d51e8f1af32abfd8b21c2b25222` / `e59ee582f069c553e3a7f9bfa0259c547e109cea99ce707f366769d8615fba8d` |
| `V2_BE-5_API_TRANSCRIPT.txt` (Rev 2) | `78f1f65dd69981e90201b9aa91432cc7` / `843bce50c4124a0e08f2592334dcbd73af21acb331edd9de931e4a01d93bbb03` |
| `V2_BE-5_TESTRUN_TRANSCRIPT.txt` (Rev 2) | `ed87d43fc5cd3f9d7d8f8c317db4e2ec` / `c886381eec7045ed8c77cde25ef09f7349745fb27b4c6a257af3324119d2e135` |
| `0045-APPLY-RUN-V1.txt` (run-of-record) | — / `747123cd6b87abeb24dc9c58546259e7ffacbc91e41d67ad921c2224eb657508` |
| `0045-VERIFY-RUN-V2.txt` | — / `dc2fccb1ae27d7a2572849cac119b626cea2e8ed81349e66590dfb28332ac50c` |

Instrument status register (archive): apply-pack V1 USED AND RETIRED (run-of-record); verify-pack V1 SUPERSEDED (never run); verify-pack V2 LIVE → now CLOSED WITH ITS ACT. PGF-015 recorded.

## 4. Registry synchronization package (Operator-applied; Rev 13)

Apply the following to the governed registers (the DR's "Register impacts" set, reviewed; the values here are the reviewed text):

1. **`V2_CURRENT_STATE.md` → v27.0.0.** Chain head `20260902_0045`; totals: 28 v2 triggers (18 inherited + 10 BE-5), 35 permissions, 5 computation-version rows; drift declaration reaffirmed: exactly the 9 inherited V1 tokens, zero BE-5/V2 tokens (itemized at head, executed twice: DA direct run + operator verify pack).
2. **`V2_CAPABILITY_MATURITY.md`:** the two BE-5 rows `ML Research Expansion` and `Signal Architecture V2` → **COMPLETE** with the evidence strings and reference date of §2 above.
3. **Roadmap / milestones documents:** BE-5 paragraph + terminal-state block; BE-5 COMPLETE row with evidence date 2026-09-02; the 6-ML/4-SIGNAL capability rows updated per §2; `02-MACHINE_LEARNING_PREDICTIVE` and `03-SIGNALS_STRATEGY` (roadmap correlation per `ITRGA-DET-V2-BE-5-FINAL-001` §7) marked COMPLETE.
4. **SPECS index:** add `09_EXECUTION_FUTURES_SPEC` (forward reference only).
5. **`V2_RISK_REGISTER.md` +2 rows (both mitigated):**
   - *signal-truthfulness*: predictive signals gated on a current, eligible governance record; timeless refusal-as-record; proven by execution (API transcript; working-DB probes). Status: mitigated/in-force.
   - *governance-writer-bypass*: all artifact surfaces DB-trigger-guarded; promotion/signal writers append-only with generation-currency gates (C-1 regression `test_predictive_superseded_generation_refused`; live guard probes on the working DB). Status: mitigated/in-force.
6. **`V2_TECHNICAL_DEBT_REGISTER.md` +3 rows:**
   - *unreachable data classes*: `historical_real`/`live` first-landing-refused until the corpus-registration track; zero-emission discipline verified. Open by design, corpus-gated.
   - *declared freshness bounds*: 30/90-day staleness/expiry bounds are band-declared (no V1 config citation exists); replaceable later without schema change. Open, documented.
   - *backlink-vs-forward-link naming*: **RESOLVED by C-1** (`supersedes`); record as closed — no open debt.
7. Re-serialize after the last Op-level edit, per the register convention.

## 5. File placement (per DR §9.1)

- Place the three Rev-2 evidence transcripts at their declared destinations under `docs/evidence/` (names exactly as in DR §6 table; hashes as in §3 above — verify on placement).
- The working-DB run transcripts remain in `operator-evidence\BE-5\` (act archive) on the Operator machine; a copy of each is held by the ITRGA office in the review bundle.
- The DR (v1.0.1) placements follow the established deliveries convention.

## 6. Forward register (nothing owed in BE-5)

The roadmap candidates logged by DR §10 for the next commissioning conversation: execution/gate futures spec track; signal-family readiness (withheld-state producers; corpus-gated data classes); corpus-registration track. The ITRGA is in standby for the Operator's next authorization. Until then: no act is pre-authorized.

**INSCRIBED as `ITRGA-DET-V2-BE-5-ACCEPT-001`. Band BE-5: accepted, closed, and synchronized-ready.**

---

### ADDENDUM (same day) — placement verification executed on the Operator machine

Operator ran the placement act; the three Rev-2 transcripts were found already at `docs\evidence\` (placed by the DA) and `Get-FileHash` (SHA-256) on all three **byte-matched the §3 pins** (SOURCE `E59EE582…FBA8D`; API `843BCE50…BB03`; TESTRUN `C886381E…E135`). **File placement act: PASS, complete.** Environment note recorded for the programme (no action gate): the operator venv's entry-point `.exe` launchers carry a stale interpreter path (venv copied from `axiom_certified`); operative rule affirmed for this environment: invoke tools as `python -m alembic` / `python -m pytest`. It implicates neither the delivery, the database, nor this record.

Env-repair follow-up (same day): `python -m alembic current` returned `20260902_0045 (head)` — working lineage confirmed post-restart-check. During the optional launcher repair, an ITRGA-issued pip token lacked a version pin and the runner drifted pytest 8.4.2 → 9.1.1 (off the pinned-evidence environment); the ITRGA issued the restoration (`pytest==8.4.2`) and a one-module smoke check in the same turn. No governance artifact, verdict, or database state is touched: the 856-floor evidence stands as produced under pytest 8.4.2, and the environment is returned to that pin. Rule recorded for the office: **every pip token issued to a governed environment must carry an exact `==` pin, and every command path an ITRGA issues must resolve to a verified on-machine object** (the smoke-module name was corrected to `tests/test_v2_be5_decisions.py` against the sealed evidence manifest).

Smoke result (same day): `python -m pytest tests/test_v2_be5_decisions.py -q` on the operator machine → **24 passed / 0 failed** in 0.86s — identical count to the 24 lines for this module in the sealed 856-floor testrun transcript; warning classes consistent (starlette `httpx2` deprecation, documented). Short-command launchers proven (`alembic current` → `20260902_0045 (head)`; `pytest --version` → 8.4.2). **Environment act CLOSED on the certified pin.** Advisory recorded (non-gating): the `pytest_asyncio` frame in the smoke run cited the parallel `axiom_certified` venv. RESOLVED as benign same day: operator diagnostics showed a clean `sys.path` (operative venv + stdlib only) and `pytest-asyncio 0.26.0` present in the operative venv's tree — the stale string was bytecode `co_filename` carried over from the venv copy, cosmetic only, optional cache purge supplied. No import leak; no environment surgery. App-restart command form fixed by record: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` (backend cwd, per `backend/README.md`), module form because the `uvicorn.exe` launcher was not part of the regenerated pair. Placement act stands PASS.

Restart act (2026-09-03, operator machine): front-end production build clean (vite 8.1.4, 174 modules, 1.77s); backend started per the recorded command form — `AXIOM v0.62.0 env=development db=sqlite`, engine + session factory initialized against the lineage at `20260902_0045`, `V2 mode initialized: RESEARCH`, `Application startup complete` 06:44:01Z. Dev-posture markers (`AXIOM_ALLOW_INSECURE_DEV` escape hatch, bootstrap-admin provisioning) are the app's declared development behavior, outside the migration chain; no anomaly, no gate implicated. **Restart act: PASS.** Band BE-5 operational residue: registry synchronization (Rev 13) only.
