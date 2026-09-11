# ITRGA REVIEW — BE-4 DELIVERY (SOURCE/EVIDENCE) (001)

| Field | Value |
|---|---|
| Review ID | `ITRGA-REV-V2-BE-4-DELIVERY-001` |
| Date | 2026-08-31 |
| Reviewer | ITRGA |
| Subject | BE-4 delivery package: `AXIOM-V2-BE-4-DR-001` (`DELIVERY_REPORT_V2_BE-4.md`) + `AXIOM-V2-BE-4-TRANSCRIPT-001` (`V2_BE-4_SOURCE_TRANSCRIPT.md`) |
| Authority | `BO-V2-BE-4-001` (issued per `AXIOM-V2-OD-BE-4-008`); roadmap §3 delivery model — stage 8 |
| Governing instruments | `AXIOM-V2-BE-4-DA-PLAN-001` v1.0.0 + R-1…R-5 · `ITRGA-REQ-V2-BE-4-001` BG-1…BG-12 · charter invariants 1–9 · onboarding (evidence law; §17 test-evidence discipline; §35 closed vocabulary) |
| Determination | **CLOSED — FINAL: APPROVED (2026-09-01; §10 dated closure note).** v1.0.0: RETURN FOR RE-SUBMISSION (CG-1, CG-2; no source-side defect; V-1…V-13 all pass) |

---

## 1. Evidence received

| Item | Identification | Credential scan | Archive |
|---|---|---|---|
| Delivery Report | `DELIVERY_REPORT_V2_BE-4.md` — md5 `6d1fe7d99ff65f67ff082e4cc49520bf`, 12,416 B, 192 lines, `AXIOM-V2-BE-4-DR-001`, dated 2026-08-31 | **CLEAN** (only the concept string "credential scan" in the checklist) | `docs/evidence/BE-4/DELIVERY_REPORT_V2_BE-4.md` (byte-identical, md5 verified) |
| Source Transcript | `V2_BE-4_SOURCE_TRANSCRIPT.md` — md5 `e8b22ca0ee4f8070053dbcf5065a1fd4`, 137,662 B, 3,626 lines, `AXIOM-V2-BE-4-TRANSCRIPT-001` | **CLEAN with classification** (OBS-2): the flagged lines are test-fixture placeholders confined to test databases — a JWT test placeholder, an operator-fixture password with random fixture usernames, an admin dev-default login, a runtime Bearer token from a test login, and the `AXIOM_ALLOW_INSECURE_DEV` test-environment marker. No real credential of the Four Secrets, no account identifier, no provider key, no production secret, in either artifact | `docs/evidence/BE-4/V2_BE-4_SOURCE_TRANSCRIPT.md` (byte-identical, md5 verified) |

No repository change and no working-database modification accompany this submission (as the BO requires).

## 2. Evidence classification

- Both submitted artifacts are **Level III** (documents) at the tier of their claims, **except** where ITRGA itself recomputed values from the submitted artifact (below — those recomputations are **Level II on the submitted artifact**).
- The DR's executed-run claims ("789 executed, 789 passed"; "executed proof: repeat POST returned `reused_existing: true`"; "drift gate … direct run") are **Level III as submitted**: the corresponding run outputs are **not in the channel** (CG-1, CG-2). Per onboarding §17, a test count is not a test result; per §5, a DA declaration is not proof. These are recorded **NOT PROVEN — not FALSE**.
- The DA's Level II attestations (read-only `git status`/`git diff --stat` inspection; SHA-256 manifest "recomputed against the working tree") remain independent of ITRGA: no DA workspace access (custody independence). The manifest's internal integrity, however, **is** independently verifiable from the submitted artifact — and was (below).

## 3. ITRGA-performed verification (recomputed from the submitted transcript)

| # | Check (ITRGA recomputation) | Result |
|---|---|---|
| V-1 | **Manifest integrity:** SHA-256 of the literal content of all 15 files (12 new + 3 modified) vs the transcript §2 manifest | **15/15 MATCH** |
| V-2 | **R-2 pins in migration 0043:** all six trigger names present as literals; all six guard messages present **byte-exact** (e.g. `V2 market context reports are immutable; UPDATE prohibited`) | **6/6 + 6/6 MATCH** |
| V-3 | **Trigger DDL structure:** deterministic loop over the literal 6-tuple table (SQLite `RAISE(ABORT, message)`); PostgreSQL deployment-dialect branch parameterized to the identical messages; downgrade drops this revision's triggers | **COMPLIANT** (OBS-4) |
| V-4 | **Migration identity:** `revision = "20260831_0043"`, `down_revision = "20260829_0042"` | **MATCH** |
| V-5 | **OBS-3 pin:** `engine_versions_hash` column present; determinism anchor `UNIQUE(instrument_id, input_content_hash, engine_versions_hash)` present | **MATCH** |
| V-6 | **Seeds:** 5 permission rows present as **revision-local literals** (admin×3, operator×2; SAL-2/SAL-3 per DR); **no import from the live permissions module** (DEL-004 / R-5 pattern) | **MATCH** |
| V-7 | **No-touch in migration:** zero references to `v2_md_provider` / history / any BE-1–BE-3 object | **CLEAN** |
| V-8 | **Test inventory:** `test_v2_be4_research.py` 22 · `test_v2_be4_migration.py` 5 · `test_v2_be4_api.py` 12 (async) = **39** — matches DR §4 itemization and `789 = 750 + 39` | **MATCH** (inventory tier) |
| V-9 | **V1 surface pin (closes OBS-1 at attestation tier):** full SHA-256 of the three reused V1 files extends the plan §1.1 16-char prefixes exactly (`af661b52edd15e44…`, `bd83c67279ba2e26…`, `02d2e98185bb89b4…`) | **MATCH** (full hashes now pinned) |
| V-10 | **R-4 rule table:** `typing.py::TIMEFRAME_RELATIONSHIP_RULES` = exactly the five pinned classes (3 `derived`/`derived_observation` + 2 `contextual`/`contextual_interpretation`), "anything not listed is refused" | **MATCH** DR §3 R-4 |
| V-11 | **R-1 writer (source):** compute endpoint gated by `require_v2_permission("v2.research.market_context.compute")`; `_ALLOWED_MODES = ("RESEARCH", "SIMULATION")`; `reused_existing` response field; audit actions `research.market_context.computed` / `research.chart_intelligence.computed` | **PRESENT** (executed tier pending CG-1) |
| V-12 | **Append-only repositories:** repository surface = `list_all/get/append/find_by_anchor/list_reports/get_by_market_context` — **no update/delete methods** | **MATCH** (defense-in-depth per R-2) |
| V-13 | **Deterministic core:** `uuid4(` count = 0 in `market_context.py`, `chart_intelligence.py`, `repositories.py` (DR: ids are deterministic sequences) | **MATCH** (source tier; the token-scan test re-proves it at execution) |

## 4. Investigation

### Pass 1 — Authority and scope
Authorizing instrument `BO-V2-BE-4-001` cited in the DR header with the correct authority chain (OD-008 → review → plan). Deliverables D-1…D-7 each mapped (DR §2). Fixed parameters SD-1 = A / SD-2 = A carried (DR §1 declarations, verbatim tier: "It substantiates no market conclusion"; "BE-4 read models produce correct market analysis" remains **NOT PROVEN and is not claimed** — the correct epistemic posture). **Pass 1: PASS.**

### Pass 2 — Evidence and implementation
Source side: V-1…V-13 all pass — the delivered source is internally consistent, pin-exact, and BO-conformant at the source tier. Modified files: 3, all additive V2 (router mount; `rbac/permissions.py` permission constants + grants + SAL entries; `models/__init__.py` registry imports) — see OBS-1 (compliant; precision noted). **Missing from the channel:** the Level I API transcript and the executed full-suite output (CG-1/CG-2). **Pass 2: INCOMPLETE — evidence gaps, not source defects.**

### Pass 3 — Governance and risk
- BG-1…BG-12 on the source side: no actuation surface; read-only endpoints + the single R-1 writer; no-touch list honored (V-7); data basis §8 of the plan carried (DR §1 + §6); typing at schema level (V-10 + CHECK mirrors per DR §4); determinism/temporal design (V-13 + tests); lineage (DR §3/R-1 + `v2_lineage_record` rows per DR §3); dialect/migrations (V-4…V-7); V1 preservation (V-9 + zero V1 diffs attested, OBS-3); exit-evidence mapping with the browser residual (DR §5.12); boundaries (DR §7); evidence discipline (DR §5 — with the two missing artifacts).
- DR §6 known limitations: honest and correctly scoped — the 0042 test-chain authority note (OBS-5), the 0043 working-DB application deferred (BO §9 — honored), the declared `stale` bound, v1-scope family vocabularies, `structure_nesting` without a v1 emitter, the SD-1/SD-2 residuals, and unchanged inherited V1 debt. No concealment detected.
- DR §7 security attestation is consistent with the source (V-11, V-12) — at the source tier.
- **Pass 3: PASS at the source tier; completion blocked by CG-1/CG-2.**

## 5. Completeness gaps (NOT PROVEN — not defects; onboarding §15)

**CG-1 — Level I API transcript not submitted (roadmap exit-evidence item 4; BO §6.4; DR §5.4 names the artifact).**
`V2_BE-4_API_TRANSCRIPT.txt` is cited by the DR but is not in the channel. Consequently: the final endpoint path `/api/v1/v2/market-context/*` (R-3) and the claim_type separation shown "verbatim" are **Level III claims — NOT PROVEN**. The executed R-1 idempotency proof (repeat POST → `reused_existing: true`, same report id, count 1, reuse audited) is likewise NOT PROVEN at the Level I tier.

**CG-2 — Executed full-suite test output not submitted (onboarding §17; BO §6.1; DR §1, §5.8).**
"789 tests executed, 789 passed, 0 failed" and the drift gate's "direct run" have **no run output in the channel** — the transcript is literal file contents only (it ends "End of Source Transcript"). The 39-test inventory is verified (V-8); the **executed result is NOT PROVEN**.

Per onboarding §15, missing evidence is recorded NOT PROVEN; it is not converted into a negative finding, and no defect is manufactured.

## 6. Observations

- **OBS-1 (modified-files precision — compliant, recorded):** BO §5 enumerated the primary modified file (the V2 aggregate router). The DA additionally modified two V2 files, both **additive** and both **directly required by the BO**: `app/v2/rbac/permissions.py` (BO §7's three additive SAL-aligned permissions; R-1's RBAC gate) and `app/db/models/__init__.py` (registry imports so Alembic `target_metadata` includes the three new models — without which the drift gate would be broken; the transcript's "PG-002 lesson" note). Zero V1 lines touched. **Future BOs should enumerate permitted modified files exhaustively** (ITRGA process note).
- **OBS-2 (credential-scan classification):** as recorded in §1 — test-fixture placeholders only; no real credential exposure; consistent with previously accepted bands.
- **OBS-3 (read-only Git inspection):** the V1-preservation attestation used read-only `git status` / `git diff --stat` ("no Git write operation performed"). The custody prohibition targets repository-state mutation; read-only inspection changes no repository state. **Compliant; recorded.**
- **OBS-4 (deployment-dialect branch):** 0043 carries a PostgreSQL branch (`prevent_v2_research_mutation` + the six triggers), parameterized to the identical pinned messages. It is not executed in the DA workspace (SQLite-only posture); an ITRGA PostgreSQL gate could prove it if the Operator ever directs one. Recorded.
- **OBS-5 (0042 test-chain note, DR §6.1):** the BE-4 migration test harness sets `AXIOM_TD_TRANSITION_AUTHORITY_REF` **for its own dedicated test databases only** — the accepted transition-test pattern; the working database is untouched (BO §9); the governed act is not re-executed anywhere governed. Recorded as appropriate and honestly disclosed.

## 7. Determination

**RETURN FOR RE-SUBMISSION.**

The source (15 files) is **accepted at the source tier**: BO-conformant, pin-exact, internally consistent — with ITRGA's own recomputation proving the manifest's internal integrity (V-1…V-13). The delivery **cannot close** because two required evidence artifacts are missing from the channel (CG-1, CG-2). This is an evidence-completeness determination, not a source-quality one.

### Re-submission requirements (minimal; nothing else is requested)

- **RSR-1 (closes CG-1):** submit **`V2_BE-4_API_TRANSCRIPT.txt`** — a single Level I transcript of the executed API surface against the delivered tree, containing: the final endpoint path; the full R-1 compute flow (first POST → report created; repeat POST → `reused_existing: true`, same report id, report count still 1, reuse audited); the report and chart-intelligence GET responses showing the `claim_type` separation **verbatim** (`fact` / `derived_observation` / `contextual_interpretation`; predictions = 0); a representative response for each of the six BE-1 states; and the drift direct-run output (`alembic check` at the 0043 head: exactly the 9 inherited tokens, zero BE-4 tokens). No credential of any kind in the transcript (the standing scan list applies before archiving).
- **RSR-2 (closes CG-2):** submit **`V2_BE-4_TESTRUN_TRANSCRIPT.txt`** — the raw full-suite pytest execution output: the command line; the environment (including no-network posture); the full `-v` pass list; and the summary line showing **789 passed, 0 failed** — consistent with the DR §4 itemization (750 + 39, no double counting).

Constraints on re-submission: **no repository changes; no working-database modification; no code change** — the transcripts are evidence of the already-delivered tree. Single transcript per artifact; standing evidence discipline (BO §6) applies.

### After re-submission (stage 8 completion path)

1. ITRGA closes this review on the complete package (verdict on the executed tier).
2. Working-database no-touch re-verification by a proven ITRGA instrument (the working DB must remain at head 0042 with the in-force state byte-intact; mechanics per the standing verification discipline — no new working-DB writes).
3. ITRGA determination closes the band. The 0043 working-DB application remains a **separate, later-governed act** (BO §9).

## 8. Baseline registration

No baseline change: working DB head `20260829_0042`; test baseline **750**; drift = exactly the 9 inherited V1 tokens; the in-force provider state untouched; Four Secrets untouched. The DA-workspace state (revision 0043 present; 789-test suite) is **verified at the source tier (V-1…V-13)** and **NOT PROVEN at the executed tier** until CG-2 closes.

## 9. Document control

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-31 | Issued — **RETURN FOR RE-SUBMISSION** (CG-1, CG-2; RSR-1, RSR-2; V-1…V-13 all pass; OBS-1…OBS-5; no source-side defect) |

*We don't guess. We prove.*
— ITRGA, 2026-08-31

---

## 10. Dated note — re-submission verified; review closed (2026-09-01)

**Re-submission received (2026-09-01):** `AXIOM-V2-BE-4-RESUB-001` cover (md5 `e0fb087408ebd82b621f13b6ba65f2c6`, 5,287 B) + `AXIOM-V2-BE-4-API-TRANSCRIPT-002` (md5 `85f9ad33a1ccfe7f0924891f066ca749`, 8,601 B) + `AXIOM-V2-BE-4-TESTRUN-TRANSCRIPT-001` (md5 `110d9475f97f35679ee22c14a60eab20`, 81,936 B). All three archived **byte-identical** in `docs/evidence/BE-4/`. Credential scans: **CLEAN** on all three (API transcript: zero bearer/token/password/connection-URL values; test-run header: JWT value redacted as `<test dev-marker constant, 40 chars>`; remaining hits are V1 security-test names — conceptual). Scope discipline honored: exactly the two requested artifacts; no repository change, no working-DB modification, no code change.

### CG-1 — CLOSED (Level I, verified by ITRGA against the submitted transcript)

| RSR-1 item | Verification |
|---|---|
| Final endpoint path (R-3) | Every call verbatim under **`/api/v1/v2/market-context/*`** — pin now Level I |
| R-1 compute flow | first POST → `reused_existing: false`, id `2c287eeb-c354-46af-a530-f632cdfbf603`; repeat POST → `reused_existing: true`, **same id**; `GET /reports` → `total: 1`; audit action list contains `research.market_context.compute.reused`; inline ASSERTs all True |
| claim_type separation verbatim | distribution `{fact: 9, derived_observation: 6, contextual_interpretation: 1}`; **predictions = 0 asserted**; verbatim samples per claim class + annotation/interpretation samples; the interpretation carries the epistemic note ("Interpretation of deterministic observations on labelled synthetic input; no market conclusion, no prediction"); the V1 liquidity disclosure is propagated verbatim (band control) |
| Six BE-1 states | all six executed with representative responses + ASSERTs: `available` (9 families) · `degraded` (typed `insufficient_data`: `required_bars` vs `available_bars`) · `unavailable` (0 families) · `stale` (disclosure bound 2700 s = 3 × M15 periods — consistent with the DR) · `unknown` (`report_id: null`, count 0 — nothing persisted) · `denied` (HTTP 403 generic; operator read still 200; unauthenticated 401) |
| Drift direct run | fresh dedicated chain: `alembic current` = `20260831_0043 (head)`; distinct tokens = **exactly the 9 inherited V1 set** (names identical to the record: `audit_write_failure_records`; `ix_audit_write_failures_category_action`, `ix_audit_write_failures_created`; the six removed V1 indexes), **zero BE-4/V2 tokens** — DRIFT GATE PASS; the double-print note (ERROR log + FAILED summary; accounting over distinct tokens) is honest and correct |

### CG-2 — CLOSED (Level II, ITRGA recomputation from the raw output)

- Command line `python -m pytest -v`; environment printed: `testing`, in-memory SQLite per test, socket guards in the BE-4/BE-3 P2 modules, **`AXIOM_TD_TRANSITION_AUTHORITY_REF` NOT SET in the runner environment** (per-invocation, dedicated test DBs only — OBS-5 pattern).
- **789 PASSED / 0 FAILED / 0 ERROR** (ITRGA recomputed line counts); summary line `789 passed, 2 warnings in 262.39s`.
- Itemization recomputed: `test_v2_be4_research` 22 + `test_v2_be4_migration` 5 + `test_v2_be4_api` 12 = **39** → 789 − 39 = 750. **Full reconciliation against the authoritative 750 composition:** the non-BE-4 V2 modules sum to 198 = 78 (BE-1) + 45 (BE-2) + 33 (P1) + 25 (P2) + 17 (transition), and V1 = 552 — exact, no double counting.
- Execution environment: DA workspace (platform linux, Python 3.13.14, pytest 8.4.2) — the DA's own environment, consistent with prior bands; the Operator-machine state is established separately by ITRGA's own instrument (next step).

### Final determination on the complete package: **APPROVED**

Source tier (V-1…V-13, 2026-08-31) **and** executed tier (CG-1 Level I; CG-2 Level II) both verified. The band exit evidence is satisfied per SD-2 = A: direct API evidence of facts vs interpretation is now Level I; **browser evidence remains the recorded residual** (SD-2 = A), to be verified at the FE band / X-01 joint gate. Real-data research validation remains the recorded residual of SD-1 = A (separate, later-governed act).

### Observations (non-blocking; for the record)

- **OBS-6:** the API transcript's `/versions` print shows one of the three registered components (the `indicator_engine` row). Full seed registration is proven at the source tier (migration literal: all three component tuples present, revision-local, hashes computed/recorded at seed time per plan §1.2) and the executed tier (`test_upgrade_creates_tables_seeds_and_triggers` PASSED). The transcript print is a partial sample — recorded, no action.
- **OBS-7:** the cover characterizes both warnings as starlette/httpx deprecations; the transcript's second warning is a pre-existing V1 `@pytest.mark.asyncio` PytestWarning (`test_b_audit_concurrency`). Both pre-existing, non-BE-4, no impact; the summary line is authoritative.
- **OBS-8:** re-submission runs were generated 2026-09-01 (~11:00 UTC, DA workspace clock) — cross-midnight delivery of the 2026-08-31 package; recorded for accuracy.

### Chain state (review §7 completion path)

Step 1 (review closure on the executed tier) — **DONE**. **Step 2 (working-DB no-touch re-verification) is the single next action:** re-issue of the **proven, read-only** instrument `ITRGA_V2_BE-3_P2_TRANS_VERIFY_PACK_V1.ps1` (MD5 `00ffe783aa3dcdbb5515d2d0a35fa2ea`; proven on the machine 2026-08-31 — verify run 1 PASS) to re-prove the in-force state on the working database (head `20260829_0042`; the four guard trigger names; provider/history/audit exact; 5/5 refusals; authority UNSET; drift = exactly the 9 inherited tokens; recovery anchor present + integrity ok) and to record the file state for ITRGA's cross-check against the recorded sha256 `0483f9fe…`. A file-level delta (e.g. V1 application runtime writes) would be **recorded in the determination and is not per se a BE-4 violation** — the v2-state assertions are authoritative for the band. Step 3: ITRGA band-closure determination. The 0043 working-DB application remains a separate, later-governed act (BO §9).

— ITRGA, 2026-09-01
