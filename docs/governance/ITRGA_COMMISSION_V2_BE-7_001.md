# ITRGA-CN-V2-BE-7-001 — Band BE-7 Commissioning Record (opening of the BE-7 chain)

| Item | Value |
|---|---|
| Date | 2026-09-03 |
| Authority | Operator authorization conveyed 2026-09-03 ("next build order authorized, whenever ready you can issue the design request"), received immediately after the BE-6 working-lineage closure. Scope granted by that authorization: (1) ITRGA requests the DA design plan; (2) after full ITRGA verification of the plan, ITRGA issues the Build Order. Implementation itself remains gated downstream per the delivery model. |
| Roadmap default | "forward register: BE-7 (Backtesting, Simulation, Replay, and Governed Research Jobs) per roadmap order" (`ITRGA-DET-V2-BE-6-ACCEPT-001`, accepting determination) |
| Band contract source | `AXIOM-V2-BE-ROADMAP-001`, Band **BE-7 — Backtesting, Simulation, Replay, and Governed Research Jobs** — in-repo custody copy `uploads/V2_BACKEND_ROADMAP.md` §"Band BE-7", lines 281–312 (**present and verified in-workspace this session**; the same file's BE-6 section was proven verbatim against the DA's §0 quotation in the BE-6 chain). Unlike BE-6's commissioning, **no open input is required from the Operator**. |

## 1. Baseline readings (verified this session, cited instruments on the record)

- **Capability rows (BE-7, currently DESIGNED):** `Backtesting Engine`, `Historical Replay`, `Research Job Queue` (family **Simulation**) — `V2_CAPABILITY_MATURITY.md` rows 57–59.
- **Architecture principles:** backtesting and simulation = BE-7, governing note *Simulation engine design* (`V2_ARCHITECTURE_PRINCIPLES.md` row 71); **open decision that the plan MUST resolve: "Message queue technology — BE-7 — Depends on research job requirements"** (row 89).
- **Chain state as floor for BE-7** (per `ITRGA-DET-V2-BE-6-CLOSE-001` and `ITRGA-DET-V2-BE-6-ACCEPT-001`): migration head `20260903_0046` (single head) on the working lineage; **next migration number 0047** (date prefix assigned at issuance; `down_revision = "20260903_0046"`); executed test floor **911 passed / 0 failed** (module itemization 17/7/14/17 for the BE-6 additions; pytest 8.4.2 certified pin); drift declaration = exactly the 9 inherited V1 tokens, zero BE-6/V2 tokens; pinned totals on the lineage: **32** v2 triggers · **41** permission rows · **6** computation-version rows; bands BE-0…BE-6 closed (working lineage at `20260903_0046`; anchor and transcripts hash-pinned in `operator-evidence\BE-6\`); register sync entries supplied to the DA (CLOSE-001 §8; DA office applies).
- **Interfaces BE-7 may consume (verified reviews stand):**
  - From BE-6: versioned-immutable portfolio definitions (`record_seq` + `supersedes`; currency = greatest `record_seq`), immutable research artifacts with **determinism anchors** (inputs hash × engine-versions hash → idempotent return), `engine_versions` provenance on every artifact, typed `insufficient` outcomes, six-class data taxonomy with `synthetic`/`simulated` first landing.
  - From BE-5: predictive-signal governance and versioned promotion vocabulary.
  - From V1 lineage: deterministic dataset snapshot/temporal-split work (W2-U04: random splits and label-horizon leakage rejected) and the execution-research evaluators over **simulated** artifacts (W6-U04) — the plan must declare, per candidate, consume-vs-build.
  - Structural regime: BE-1 columns on every row (mode / operator_id / correlation_id / created_at); audit events; SAL-aligned RBAC with `denied` typed; redaction gate untouched; `historical_real`/`live` remain corpus-gated refusals (V2-TD-18).

## 2. Open input required

**None.** The BE-7 band contract is present verbatim in the workspace custody copy (see header). The REQ is authored directly from it.

## 3. Acts sequenced

1. ITRGA authors **`ITRGA-REQ-V2-BE-7-PLAN-001`** (design-plan request to the DA): band-contract REQ items from the roadmap §BE-7 (objective, scope ×7, controls ×3, exit evidence ×5) + mandatory Pins (P-1…P-7 carry by default; BE-7-specific pins declared in the REQ) + custody/discipline rules + required plan parts (decomposition; DDL/guard/seed/drift declarations per migration unit; mode/audit/security integration; test and evidence plans; register impacts; boundary restatements vs BE-8 / BE-9 / BE-10 / BE-11 / corpus track).
2. DA returns the design plan via the Operator → full-depth ITRGA review (against REQ items, Pins, and the roadmap text, with the REQ numbered map) → scope assessment (+ corrections if any).
3. On verified plan: ITRGA issues **BO-V2-BE-7-001** under this commissioning authorization; Operator decision; implementation begins per the delivery model; the working-DB application of 0047 remains a separate sanctioned act at chain end (instruments ITRGA-authored, per the 0043/0045/0046 lineage — including the E-0046-DUP startup-hygiene rule: a completed-run marker at instrument startup ⇒ STOP, never delete).

**INSCRIBED as `ITRGA-CN-V2-BE-7-001`. No code, migration, repository write, or execution is authorized by this record; it opens the commissioning track only.**

---

### CLOSURE LINE (updated 2026-09-04 — BAND ACCEPTED)

Commissioning act complete: band contract verified in-workspace (§2) → **`ITRGA-REQ-V2-BE-7-PLAN-001`** issued (REQ-1.1…1.13 + Pins P-1…P-7 carried, P-8…P-10 declared) → DA plan `AXIOM-V2-BE-7-DA-PLAN-001` v1.0.0 → **`ITRGA-PRV-V2-BE-7-PLAN-001`**: **ACCEPTED, zero corrections** with two BO-binding conditions plus four non-blocking observations → **`BO-V2-BE-7-001`** issued (single package U-1…U-6; T-1…T-14; normative: six physical tables) → delivery `AXIOM-V2-BE-7-DR-001` → **`ITRGA-INT-V2-BE-7-DR-001`**: **INTAKE PASS** (8/8 checks independently recomputed) → `AXIOM-V2-BE-7-DA-INT-ACK-001` → **`ITRGA-DET-V2-BE-7-FINAL-001`**: full-depth source review — **ACCEPTED WITH CORRECTIONS** (F-1 cost-unit vocabulary; F-2 determinism ×3) → DA correction cycle **CR-V2-BE-7-001** (DR v1.0.1 + bounded 5-file diff, +49/−1; 972/0 full re-run; RJE re-pinned `8f107d17…`, RPE unchanged) → ITRGA targeted re-verification green → **`ITRGA-ACC-V2-BE-7-001`: BAND BE-7 ACCEPTED**. Band floor of record: migration `20260903_0047` (DA test chains) · suite **972 passed/0 failed** · triggers **42** · permissions **49** · compver **8** (rpe-1.0.0 `1499343d…` · rje-1.0.0 `8f107d17…`) · drift = 9 inherited V1 tokens, zero band tokens. Register sync: capability rows → COMPLETE via DA per ACC §4. **Remaining chain act: the 0047 working-DB application instrument — separate sanctioned act, awaiting operator authorization** (startup refuse-if-PASS law; compver pre-declared expectations RPE unchanged/RJE new; transcript-witnessed).
