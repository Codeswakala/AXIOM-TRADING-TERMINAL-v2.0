# ITRGA_INT_V2_BE-6_DR_001 — Intake review, full-depth: `AXIOM-V2-BE-6-DR-001` + evidence package

| Item | Value |
|---|---|
| Date | 2026-09-03 |
| Reviewed | `AXIOM-V2-BE-6-DR-001` + 4 evidence artifacts (all revision-stamped 2026-09-03) |
| Review contract | BO-V2-BE-6-001 T-1…T-12; REQ §1.1–§1.11; Pins P-1…P-7; roadmap §0 |
| Review depth | **Full-depth** — every metric function, both writers, the migration, the tests, both transcripts, the annex, and the manifest read and machine-checked |

## 1. Identity verification (intake law — recomputed, not trusted)

- All four evidence artifacts: my MD5/SHA-256 recomputations **byte-match the DR §5 table** exactly (source `76114657…/2efbf777…5093`; api `c55204da…/dccf31d6…fa93b`; testrun `15ad6a96…/553ea36b…/…`; annex `6727334e…/4c2bfe99…`).
- Manifest self-consistency (REM-001 recipe): extracted all 15 literal file bodies from the source transcript and re-hashed: **15/15 match** their declared full SHA-256.
- V1 attestation: the four `app/execution_research/*` pins and `app/ml/validation/service.py` (`029f3f36…`) recomputed against the frozen review clone: **5/5 byte-match**. Reuse-only claim proven.

## 2. Pin satisfaction (independently executed where possible)

- **P-7 EXECUTED by ITRGA recomputation (no engine code):** from the pinned ANNEX-A inputs I computed HHI 0.3450 ✓, top-2 0.7500 ✓, gross/net 1.0/1.0 ✓, MaxDD −0.0388349515 ✓, scenario −0.1750 ✓, factor shares ✓ — all inside stated tolerance 1e-12 — plus the un-stated anchors: vol 0.034494498661, VaR-hist 0.020202707318, VaR-param 0.053454090, matching the formulas both artifacts implement. Runtime sample cross-check: scenario {crypto:−0.3} → −0.12 = 0.40×−0.3 ✓.
- **P-1/P-2:** superseding-version chain executed (seq 2; compute-vs-superseded → 409); determinism anchor idempotency executed twice (test + Level I, same report id).
- **P-3/P-4:** taxonomy shared by **structural import** from the BE-5 contracts module (no fork, verified in source); compver `pre-1.0.0` co-delivery hash recipe re-pinnable at the application act (C-2 disclosure embedded in the migration docstring).
- **P-5:** refusals are executed, not asserted (single-value CHECK probes; behavioral uniqueness; 9-token itemized drift — **the exact inherited set verified byte-for-byte against the BE-5-era record**).
- **P-6:** hypothetical-only proven structurally (CHECK probes refuse `real`/`live_account`/`account-state`; label on every artifact and response at Level I).

## 3. Test accounting (bookkeeping proven)

- Final line **906 passed / 0 failed** (388.45s); PASSED-line count = 906 ✓; BE-6 itemization **17+7+9+17 = 50** per-module in both the source transcript (`def`/`async def` counts verified) and the executed transcript = the exact plan budget; aggregate arithmetic 552 V1 + 354 V2 = 906 ✓; fail-first disclosed; generational scoping of `test_v2_be5_migration.py` (format-independent drift gate; zero-token assertion retained) disclosed and consistent with the PGF-014 precedent.

## 4. Registered claims → verdicts on the map

REQ §1.1–§1.11, T-1…T-12, roadmap §0: every item has executed, transcript-visible evidence (DR §2 map verified against the artifacts, not accepted on face). **All items: satisfied on the evidence plane.**

## 5. Finding — Correction C-1 (MANDATORY; bounded)

**Plan-vs-delivery delta in the compute-writer's audit surface.** The authorized plan (Part 4) enumerates the audit event `portfolio_risk.compute.unknown`; the delivered code emits **no such event on any path** (verified absence across `api.py`, the migration, and all test modules). More materially, the compute writer's compute-side refusal classes today end in typed HTTP outcomes with **no domain audit entry**: unknown/inactive source (404), definition-not-found (404), superseded-generation (409), as_of-in-future (400). The define-writer's refusal path IS audited (`portfolio.define.refused`) — the asymmetry departs from the authorized enumeration and from the BE-1 refusal-audit law (denied/refusal decisions auditable). Reachable-today risk: low; the governing-contract risk: real.

**Required correction (DA chooses the route; the closed loop is what I verify):**
1. Bring declaration and implementation into exact agreement — either **(a) emit `portfolio_risk.compute.unknown`** (the promised event) on the compute-refusal classes with typed `details` covering the refusal class (recommended), with per-event live probes; or **(b) amend plan §4** to the shipped enumeration with a written audit posture for compute-side refusals under the BE-1 contract, and have the corrected DR restate the final enumeration with transcript probes.
2. **Same cluster, same fix window** (currently unreachable-by-construction, still a fabrication vector by design): the compute writer's `continue`-on-unknown-instrument silently drops credited weight from the value series with no marker — no insufficient metric, no degraded status, no audit. Closed rule: **any dropped credited weight must surface as a typed outcome** (refuse with `unknown_instrument` reason + audit, or degrade with an explicit marker naming the dropped instrument). Choose and prove.

No schema change, no metric change, no permission change is requested. If code changes: re-run the full suite (floor restated 906 + Δ), re-ship the affected evidence (append §0 revision notes; full hashes — intake law), and add the probes. If plan-routed: the amended plan §4 + corrected DR + probe evidence per final event.

## 6. Observations (non-blocking; on the record)

- **O-1** Annex vol/VaR expecteds are formula-inline in the test file; independence is supplied by my recomputation (executed, matching). Acceptable per the annex design; recorded so future bands don't cite the test file alone as an independence source.
- **O-2** `ix_v2_pfdef_portfolio` (definition index) is additive-benign and justified by the current-only projection, but not itemized in plan §1.2's DDL enumeration; the 0046-application act's schema census will verify the settled set.
- **O-3** Runtime literals from the 119-obs seeded series are execution artifacts, not annex pins (independent-recompute plane = the annex; recorded to keep the distinction hard).
- **O-4** `stale`/`unknown` report statuses producerless-by-design (DR §7.4 disclosure; schema-reachable, writer-path-present, no clock in v1 scope).

## 7. Disposition

- DR: face-consistent; arithmetic exact; evidence plane independently verified in the large part; **review OPEN on C-1 only.** Not a rejection — the delivery is of the honest class, the disclosure discipline is exact, and the fault is a declaration-vs-implementation delta of the kind the correction mechanism exists to close cheaply.
- Level-I/Level-II verdict: T-1…T-12 satisfied on the executed evidence presented (856→906 floor; P5-style totals hit) — the full-verify determination issues after C-1 closes (per the standing rule: nothing contrary/uncorrected proceeds).
- Working-DB application of 0046 remains an unopened, separate sanctioned act; its instrument inherits C-2-era practice (engine-file re-pins; behavioral probes; `sqlite_master` name-scoped introspection).

— ITRGA, 2026-09-03. We don't guess. We prove.

---

## ADDENDUM (same day) — Correction register, final state

- **C-1: CLOSED 2026-09-03.** Route (a), both clusters: `portfolio_risk.compute.unknown` emitted and durably committed (commit-before-raise; call-site safety reviewed) on all four compute-refusal classes with typed `refusal_class`; the silent dropped-weight path replaced by typed `unknown_instrument` 409 naming the credited weight, side-effect-free. Executed: 4 Level-I §6 probes + 5 suite probes incl. registry-drift simulation; suite restated **911**. Verified in `ITRGA-DET-V2-BE-6-FINAL-001`.
- **C-2 (new, deferred, editorial):** DR v1.0.1 stale cells (§2 T-9 "906/0"; §3 heading "856 + 50 = 906"; T-8 cell lacking the amended audit enumeration). Re-stamp at the next evidence-channel transmission; registers carry **911**. Recorded in the final determination §4.
