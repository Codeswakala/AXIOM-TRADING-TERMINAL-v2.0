# DA ACKNOWLEDGMENT — BE-7 INTAKE VERIFICATION RECORD
# AXIOM-V2-BE-7-DA-INT-ACK-001 · v1.0.0 · 2026-09-04 · AXIOM Trading Terminal v2.0
# Band: BE-7 (Backtesting, Simulation, Replay, and Governed Research Jobs)
# Acknowledges: ITRGA-INT-V2-BE-7-DR-001 (INTAKE VERDICT: PASS — admitted to full-depth source review)
# Chain: CN-V2-BE-7-001 → REQ → PRV (ACCEPTED) → BO-V2-BE-7-001 → AXIOM-V2-BE-7-DR-001 → INT (PASS) → THIS ACK
# Author: Replacement Development Authority (DA)
# Reading rule: this is a DA acknowledgment and observation response. It contains
# no ruling, no approval claim, and no change to the under-review package.

---

## §1 — Receipt and filing

`ITRGA-INT-V2-BE-7-DR-001` received 2026-09-04 via Operator relay and filed at
`docs/governance/ITRGA_INT_V2_BE-7_DR_001.md`
(md5 `f4789585d06e7e4486457616b7c3cdff` as filed).

The DA acknowledges the intake verdict as written by ITRGA: **PASS — package
admitted to full-depth source review. No blocking findings. No corrections
issued at intake.** The DA notes this is *not* the FINAL determination and
claims nothing beyond the record's own words.

## §2 — DA cross-verification of §1 package identity (Level I, recomputed on disk 2026-09-04)

| Artifact | Bytes (disk) | MD5 (disk) | SHA-256 (disk) | vs ITRGA §1 |
|---|---|---|---|---|
| `DELIVERY_REPORT_V2_BE-7.md` | 9,737 | `67e84a6e1915e2d374916d4a547d51da` | `d707697c15a9c2b30e762dbade87c0acddef79cfc94887b6d7825553577feb59` | byte-match |
| `docs/evidence/V2_BE-7_SOURCE_TRANSCRIPT.md` | 161,210 | `8156c081367c95925b53f82940ba46bf` | `2d496225da00c9c9fde743d868fdd2eb90b1a0ea2c91e4925878f74a00825f5d` | byte-match |
| `docs/evidence/V2_BE-7_API_TRANSCRIPT.txt` | 4,870 | `8c8e0084c8e1b33c88d9f7fe8a8c64a7` | `4f73511b06bbbb48268733e28329bab549d210f4ebf60365e844af20a0f4f752` | byte-match |
| `docs/evidence/V2_BE-7_TESTRUN_TRANSCRIPT.txt` | 96,636 | `69294b316fdcc625c9e97fb0d9daa2ca` | `1da03bce19ede13f6e51738560ea43aba592f5251a8090ffdbb92406c6aad177` | byte-match |

The reviewed package and the workspace package are the same bytes. Nothing has
been modified since transmission, and nothing will be modified while the
full-depth review is in flight.

Counting-convention note (not a discrepancy): ITRGA §1 records the DR at 123
lines; `wc -l` on disk reports 122 newline-terminated lines. MD5 and SHA-256
byte-match, so this is a line-counting convention difference only (final-line
handling), asserted here so the FINAL reviewer does not have to chase it.

**INT-6 independent confirmation.** The DA re-executed the migration-0047
rolling-hash recipe (`SHA-256 over ref‖0x00‖bytes‖0x00 per file in tuple
order`) against the live files on disk:

- RPE (`__init__.py`, `leakage.py`, `replay.py`):
  `1499343d48b778af17065e8bf1eaabcffc116880fa6967ab442db1255992b178`
- RJE (`queue.py`, `runner.py`):
  `f01e3041a060e96cfcdcc9650d2458f84512e2d1bb2e2509fe668a9d3704ed7c`

Both match ITRGA's replicated prefixes (`1499343d…`, `f01e3041…`) — the
transcript literals, the disk files, and the ITRGA replication agree; full
values are placed on the record here.

## §3 — Response to OBS-A (disclosure completeness — U-3 module merge)

ITRGA is correct: the divergence exists and DR §7 did not disclose it. The DA
supplies the missing disclosure **on this record now**, and accepts the process
observation without qualification.

**The one-line disclosure that should have appeared in DR §7:**

> Plan U-3 named `app/v2/research_jobs/{registry,costs,strategy}.py`; the
> delivery implements all three U-3 scopes (input registration, cost-model
> configuration with the citation law, strategy lifecycle) in a single module
> `app/v2/research_jobs/registry.py` — a packaging merge only, with no scope
> change and no compver engine file-set impact (RPE/RJE tuples unchanged from
> the migration declaration).

**Substantiation for the full-depth reviewer (where each U-3 scope lives and is tested):**

| U-3 scope | Implementation (all in `registry.py`, 218 lines) | Level-II tests |
|---|---|---|
| Input registration | `register_input` (line 42): first-landing data-class gate (V2-TD-18), `ReplayWindow.validate()` inverted-window refusal via `LeakageRefused`, empty-`series_refs` refusal, content-hash dedupe → `input.reused` audit, write-once row + `input.registered` audit | `test_v2_be7_jobs.py` registration-outcome block (registered/reused/refused + durable audits) |
| Cost-model configuration | `register_cost_model` (line 110): citation law — every component requires `value+unit+citation`, refused typed otherwise; citations persisted on the row; `cost_model.registered` audit | `test_cost_model_requires_citations` (jobs line 154) |
| Strategy lifecycle | `register_strategy` (line 162): `LIFECYCLE_STATES` gate (draft/registered/retired), registered-rule-vocabulary gate (threshold/crossover only), forbidden-parameter-key refusal predicate (credential/api_key/broker/account/adapter — the sole `broker` token ITRGA classified in INT-7), generation supersede chain, `strategy.registered`/`strategy.superseded` audits | `test_strategy_unregistered_rule_refused` (166), `test_strategy_forbidden_parameter_keys_refused` (177), `test_strategy_versioning_supersede` (187), `test_submit_draft_strategy_refused` (351), `test_submit_superseded_strategy_refused` (369) |

**On amending the DR:** the DA does **not** re-stamp `DELIVERY_REPORT_V2_BE-7.md`
while it is under active full-depth review — a mid-review hash churn of the
reviewed artifact is worse than the omission (pack discipline,
ITRGA-PTN-V2-PACK-001). If the FINAL determination directs a DR revision
carrying this disclosure, the DA will issue v1.0.1 with the §0 revision note
and full re-hashes within the FINAL's correction cycle.

## §4 — Response to OBS-B (informational — `_RPE_FILES` includes `__init__.py`)

Acknowledged; no action, per ITRGA's own disposition. Rationale placed on the
record for completeness: `__init__.py` carries the package's public export
surface for the replay engine; including it makes any export-surface change
move the pinned engine hash (fail-loud), at the cost of a broader-than-plan
file set. The broadening is deterministic and disclosed by the migration
source itself (`_RPE_FILES` literal). The apply-time-computed compver hash is
correct-by-construction as ITRGA states; §2 above additionally pins the
concrete current values so the 0047 working-DB application act has a
pre-declared expectation to verify against.

## §5 — DA posture while full-depth review is in flight

- **No writes** to any file named in the SOURCE_TRANSCRIPT manifest, the DR,
  or the evidence artifacts. The reviewed bytes stay frozen.
- No Git operations (standing prohibition; custody Operator-only).
- Working DB untouched; 0047 application remains a separate sanctioned act,
  explicitly NOT authorized by the intake record.
- OBS-9 (Operator one-line accounting) remains open, administrative,
  Operator-side.
- BE-6 DR v1.0.2 re-stamp (C-2 editorial) rode with the BE-7 transmission;
  the DA treats it as delivered unless ITRGA states otherwise.

Next expected act (ITRGA's words): full-depth source review of all 17
delivered files against BO-V2-BE-7-001 T-1…T-14, then the FINAL determination.
The DA stands ready for corrections if any issue.

**We don't guess. We prove.**

— AXIOM-V2-BE-7-DA-INT-ACK-001 · v1.0.0 · 2026-09-04
