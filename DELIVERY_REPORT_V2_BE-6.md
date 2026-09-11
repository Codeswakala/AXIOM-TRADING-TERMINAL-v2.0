# DELIVERY REPORT — AXIOM V2 BE-6: Portfolio and Risk Research Domain

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-6-DR-001 |
| Revision | **v1.0.2** — C-1 applied (route (a) + cluster 2; suite 906 → **911**); **C-2 re-stamp applied** (`ITRGA-DET-V2-BE-6-FINAL-001` §4: T-9/§3/T-8 cells re-stamped to the 911 floor and the amended audit enumeration — presentation-class, zero substance change) |
| Build Order | BO-V2-BE-6-001 |
| Governing plan | AXIOM-V2-BE-6-DA-PLAN-001 v1.0.0 (ACCEPTED — ITRGA-PRV-V2-BE-6-PLAN-001, zero corrections) |
| Review contract | ITRGA-REQ-V2-BE-6-PLAN-001 REQ §1.1–§1.11 · Pins P-1…P-7 · roadmap Band BE-6 §0 |
| Date | 2026-09-03 |
| Author | Development Authority (DA) |
| Status | **RE-SUBMITTED (v1.0.1) — C-1 closed; Rev-2 evidence attached with full hashes** |
| Baseline in | head `20260902_0045` · 856 tests · 28 triggers · 35 permissions · 5 compver |
| Baseline out | migration `20260903_0046` (**DA test chains only** — working-DB application is a separate sanctioned act) · **911 tests** · triggers **32** · permissions **41** · compver **6** — all P-5-style pins hit exactly |

**Standing discipline: we don't guess. We prove.**

---

## 1. Executive Summary

Band BE-6 implemented in full: 4 units, all 12 terminal-state items
T-1…T-12 satisfied with executed evidence, all 7 Pins honored.
**911 executed, 911 passed, 0 failed** = 856 baseline + **55 new tests**
(50 plan budget + 5 C-1 probe tests; itemization §3). Zero V1 diffs; BE-2…BE-5
protected state proven untouched; zero network attempts; **no credential
prompted for or used anywhere in the band**.

**Hypothetical-vs-account separation is structural (P-6):** `basis` CHECK
admits only `hypothetical`; `basis_label` CHECK admits only
`hypothetical-research` and appears on every artifact and response; no
account/order/position/broker vocabulary exists in schema or permissions
(forbidden-marker guard green). **Validation tier: pipeline-validation**
on labelled synthetic input — **no risk conclusion about real markets is
claimed or claimable** (NOT PROVEN until the corpus track).

## 2. Terminal-state contract T-1…T-12 (item-for-item)

| T | Evidence (executed) |
|---|---|
| T-1 | Chain at `20260903_0046 (head)` single head (API transcript §5 direct run); literal-revision upgrades throughout; models registered same-unit (PG-002) |
| T-2 | Both tables with the exact DDL pins — columns asserted; `uq_v2_pfdef_id_seq` proven **behaviorally** (dup (id,seq) refused, next seq allowed); `uq_v2_pfrisk_determinism_anchor` exercised by the idempotency test; the two **single-value CHECKs refuse** `real`/`live_account`/`account-state` (executed) |
| T-3 | Trigger census **32** (28+4); all 4 guard messages **byte-exact** (`test_0046_guard_messages_verbatim`) |
| T-4 | Permissions **41**, 6 new rows content-exact incl. SAL, zero duplicates; forbidden-vocabulary scan over ALL 41 rows (no account/order/position/broker/execution token); marker guard green at import |
| T-5 | compver **6**; `portfolio_risk_engine = pre-1.0.0`, source hash computed at migration time over the 4 co-delivered engine files (P-4; C-2 re-pin obligation recorded for the application act) |
| T-6 | Drift direct run at the 0046 head: **9 distinct tokens = exactly the inherited V1 set, zero BE-6/V2 tokens — PASS** (API transcript §5) + `test_drift_gate_head` |
| T-7 | No-touch: BE-3 provider rows + BE-4/BE-5 compver rows content-identical across 0046; trigger delta = exactly the 4 new |
| T-8 | Six states reachable (`available`/`degraded`/`unavailable` executed; `stale`/`unknown` in the status CHECK + writer paths; `denied` executed via RBAC 403 generic); typed `insufficient` per metric (never fabricated — `value=None`); `historical_real` define-refusal executed; `hypothetical-research` label on every artifact response (Level I); **all compute-side refusals durably audited (C-1): `portfolio_risk.compute.unknown` with typed `refusal_class` ∈ {as_of_in_future, definition_not_found, definition_superseded, source_unknown_or_inactive, unknown_instrument}, committed before the HTTP error raises** |
| T-9 | Level I API transcript (**15/15** inline ASSERTs True — Rev 2; path pinned `/api/v1/v2/portfolio-research/*`); raw `pytest -v` **911/0** (= 856 + 55; itemization 17/7/14/17); **worked-sample annex** shipped (`V2_BE-6_WORKED_SAMPLE_ANNEX.md`) with hand-computable expected values matched by 17 executed annex tests; REM-001 transcript with full hashes; credential scans CLEAN |
| T-10 | Registers staged honestly: maturity rows → IMPLEMENTED only (COMPLETE = acceptance's); risk +2; debt +2; 30.x serialization |
| T-11 | Construction-token scan test: no `recommendation`/`rebalance`/`hedge`/`action` vocabulary in band modules; no preview/export surface; RESEARCH-only writers; socket guard on every test |
| T-12 | No credentials (none prompted — stated); no Git operations; full-depth review posture acknowledged |

## 3. Test accounting (fail-first; 856 + 55 = 911, itemized)

| Module | Count | Content |
|---|---|---|
| `test_v2_be6_metrics.py` | 17 | per-metric correctness vs hand-computed values; typed insufficiency; both-VaR-separate; determinism; construction-token scan; weights contract; taxonomy shared with BE-5 (no fork) — **authored first, failed on missing module (fail-first evidence)** |
| `test_v2_be6_migration.py` | 7 | DDL/seeds/triggers; guard messages verbatim; single-value CHECK refusals; behavioral uniqueness; no-touch; downgrade cycle (content-based; compver guard restored); drift gate |
| `test_v2_be6_api.py` | 9 | define accept/refusals (weights, data-class, assumptions, unknown instrument); versioning + supersede + current-only projection; compute available/unavailable/idempotent; superseded-generation 409; as_of 400; RBAC + labels |
| `test_v2_be6_annex.py` | 17 | **the worked-sample annex executed** (9 exact-value tests) + boundary coverage (norm-ppf reference values; CI-width monotonicity; VaR observation boundary; weight-sum tolerance boundary; duplicate refusal; insufficient-contract completeness; vocabulary integrity) |
| C-1 probes (in `test_v2_be6_api.py`) | 5 | one per refusal class + the cluster-2 registry-drift probe |
| **Total** | **55** | Full suite **911 passed, 0 failed** (V1 552 intact) |

One generational scoping disclosed (4th modified file): the BE-5 drift
test became format-independent since 0045 is no longer head — the exact
PGF-014 pattern the BE-4 test received last band; zero-token assertion
retained.

## 4. Pin satisfaction (P-1…P-7)

- **P-1** — `record_seq` + `supersedes` (C-1 vocabulary from birth);
  currency = greatest-seq projection (reads + compute writer both enforce
  it; superseded-generation compute → 409, executed Level I).
- **P-2** — determinism anchor on the report table; same inputs+versions ⇒
  existing report returned (executed twice: test + Level I transcript).
- **P-3/P-4** — typed permanent outcomes + 6-class taxonomy **imported
  from the BE-5 contracts module** (single taxonomy, no fork — asserted by
  test); compver provenance with co-delivered engine hashing.
- **P-5** — structural proof over vocabulary: refusals executed, not
  asserted.
- **P-6** — hypothetical-only separation structural: single-value CHECKs
  refuse foreign values (executed); labels on every response (Level I).
- **P-7** — worked-sample annex shipped as a standalone evidence file with
  the recomputation procedure; the engine's own 17 annex tests pin the
  same values (executed).

## 4b. C-1 closure (route (a), both clusters)

**Cluster 1 — declaration/implementation agreement:** the plan-enumerated
`portfolio_risk.compute.unknown` event is now emitted on ALL four
compute-refusal classes (`as_of_in_future` 400 · `definition_not_found`
404 · `definition_superseded` 409 · `source_unknown_or_inactive` 404),
each with a typed `refusal_class` in `details`, **committed before the
HTTP error raises** — the request dependency rolls back on exception, so
the helper commits the audit independently; durability is what the five
probes prove. Per-event live probes: 4 executed in the Level I transcript
§6 (all four classes present in the durable audit table after failed
requests) + 5 suite tests.

**Cluster 2 — dropped credited weight can never be silent:** the
`continue`-on-unknown-instrument path is REPLACED by a typed
`unknown_instrument` refusal (409) whose durable audit NAMES the dropped
instrument and its credited weight; zero side effects (no report row).
Probe: `test_c1_dropped_weight_refused_never_silent` (registry-drift
simulation; executed).

The audit-event enumeration now agrees exactly with plan Part 4; the DR §2
T-8 row is amended accordingly. No schema, metric, or permission change.

## 5. Evidence package (full hashes; intake-§4 law)

All artifacts Revision 2 except the annex (unchanged — no metric change):

| Artifact | MD5 | SHA-256 |
|---|---|---|
| `docs/evidence/V2_BE-6_SOURCE_TRANSCRIPT.md` (Rev 2; §0 revision note itemizing the C-1 scope) | `5c4d0f4edaf254a91792d4e3b2fd5c67` | `8f134b229f2651a7228c2ab7a702952c404364b53ffb8ae297aca8102bd01bd4` |
| `docs/evidence/V2_BE-6_API_TRANSCRIPT.txt` (Rev 2; **15/15 ASSERTs** incl. §6 C-1 durable-audit probes; drift PASS at head) | `4b6a9067b38c439e7394fb4d1054d50c` | `4a2937fea487227ec4d242461692032ca421e77f16ca0a4762fd0cda60c94d77` |
| `docs/evidence/V2_BE-6_TESTRUN_TRANSCRIPT.txt` (Rev 2; raw `-v`; **911/0**) | `6f7911c8ab118e9e15197e9a1fe35b90` | `8b875d046fab2e4c3d5f6671ef57c64a7c7c524efa249988ed2dcefc32add0ab` |
| `docs/evidence/V2_BE-6_WORKED_SAMPLE_ANNEX.md` (P-7; **unchanged Rev 1**) | `6727334e26c77e08348442e18006938d` | `4c2bfe99f1074208f75889877200fb21649e7b2759a40698ff6b4eafdf98cf02` |

Credential scans CLEAN on all artifacts. No commits — custody is the
Operator's.

## 6. Register impacts

State → v32.0.0. Maturity: `Portfolio Research` + `Risk Research` →
**IMPLEMENTED** (COMPLETE is the acceptance act's). Risk +2:
hypothetical-mistaken-for-account (mitigated structurally);
metric-overtrust (mitigated by mandatory uncertainty/limitations). Debt
+2: long-only v1 allocations; grouping-not-regression factors.

## 7. Known limitations (honest)

1. Long-only, sum-to-1 allocations; short/leveraged = future band (debt).
2. Factor decomposition is market-class grouping, not regression (debt;
   declared in every output's limitations).
3. Parametric VaR carries the declared normality assumption; the
   chi-square CI uses the Wilson–Hilferty closed form (accuracy declared
   in the citation).
4. `stale`/`unknown` statuses are schema-reachable with writer paths but
   no band-local producer transitions reports into them (no staleness
   clock in v1 scope) — the O-5-class structural-completeness posture,
   disclosed.
5. Working-DB application of 0046: **not performed** — separate sanctioned
   act (C-2-pattern engine-file re-pins recorded for its instrument).
6. All evidence pipeline-validation tier; real-market risk conclusions
   NOT PROVEN and not claimed.

**We don't guess. We prove.**

**End of Delivery Report AXIOM-V2-BE-6-DR-001**
