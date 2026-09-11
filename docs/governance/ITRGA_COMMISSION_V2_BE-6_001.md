# ITRGA-CN-V2-BE-6-001 — Band BE-6 Commissioning Record (opening of the BE-6 chain)

| Item | Value |
|---|---|
| Date | 2026-09-03 |
| Authority | Operator authorization of Band **BE-6**, conveyed 2026-09-03 ("BE-6 is authorized to proceed, you can request the design plan and once fully verified you can issue the build order"). Scope granted by that authorization: (1) ITRGA requests the DA design plan; (2) after full ITRGA verification of the plan, ITRGA issues the Build Order. Implementation itself remains gated downstream per the delivery model. |
| Roadmap default | "Next per the forward register: BE-6 (Portfolio/Risk Research)" (`V2_CURRENT_STATE.md` Active Band row, verified at Rev-13 post-sync) |

## 1. Baseline readings (verified this session, cited instruments on the record)

- **Capability rows (BE-6, currently DESIGNED):** `Portfolio Research` and `Risk Research` (family Portfolio) — `V2_CAPABILITY_MATURITY.md`.
- **Architecture principle:** portfolio-and-risk research = BE-6, governing note *Risk methodology design* (`V2_ARCHITECTURE_PRINCIPLES.md` row 70).
- **Chain state as floor for BE-6:** migration head `20260902_0045` (single head); next migration number **0046**; executed test floor **856 passed / 0 failed** (Rev-2 testrun transcript, pytest 8.4.2 certified pin); drift declaration = exactly the 9 inherited V1 tokens, zero BE-4/BE-5 tokens; bands BE-0…BE-5 closed; registers synced (Rev-13 verification complete, `ITRGA-DET-V2-BE-5-ACCEPT-001`).
- **BE-5 interfaces BE-6 may consume (verified reviews stand):** predictive-signal and model-governance surface with typed permanent states (`withheld`/`refused_expired`/`refused_ineligible`), six-class data taxonomy (`synthetic · simulated · historical_real · live · stale` absorbs as two classes + unknown), versioned promotion (`supersedes`), lineage-bearing diagnostic/research reports. `historical_real`/`live` remain corpus-gated refusals (V2-TD-18) — evidence tiers must be declared accordingly.

## 2. Open input required before the design-plan request is authored

The §1.x required-content checklist of the design-plan request (the REQ set the DA's plan will be reviewed against) must enumerate the **Band BE-6 contract from `AXIOM-V2-BE-ROADMAP-001`** — the same authoritative source used for BE-5's §1.2 REQ items (BE-5's were built from that roadmap's BE-5 section; see `ITRGA-REQ-V2-BE-5-PLAN-001`). The in-workspace governing corpus contains only one-line BE-6 references (architecture row 70; charter bullet) — insufficient to enumerate the band contract without risking roadmap divergence, which the standing review rule forbids.

**Requested from the Operator:** transmission of `AXIOM-V2-BE-ROADMAP-001` (the whole document again, or at minimum the complete Band BE-6 section, verbatim) through the custody channel.

## 3. Acts sequenced on receipt

1. ITRGA authors `ITRGA-REQ-V2-BE-6-PLAN-001` (design-plan request to the DA): band-contract REQ items from the roadmap section + mandatory Pins (P-series; BE-5 pins P-1…P-5 carry by default, BE-6-specific pins added per the band contract), custody/discipline rules, and the plan's required parts (decomposition into separately-orderable units; DDL/guard/seed/drift declarations per migration unit; mode/audit/security integration; test and evidence plans; register impacts; boundary restatements vs BE-7 / BE-8…BE-10 / BE-11 / corpus track).
2. DA returns the design plan via the Operator → full-depth ITRGA review → scope assessment (+ corrections if any).
3. On verified plan: ITRGA issues **BO-V2-BE-6-001** under this commissioning authorization; Operator decision; implementation begins per the delivery model.

**INSCRIBED as `ITRGA-CN-V2-BE-6-001`. No code, migration, repository write, or execution is authorized by this record; it opens the commissioning track only.**

---

### CLOSURE LINE (2026-09-03, same day)

Commissioning act complete in one day: the DA's `AXIOM-V2-BE-6-DA-PLAN-001` v1.0.0 arrived (§0 roadmap quote verified verbatim against the in-repo `uploads/V2_BACKEND_ROADMAP.md` Band BE-6 section — §2's "open input" resolved by the DA's verbatim quotation discipline, with the file itself independently located and diffed). Chain issued: **`ITRGA-REQ-V2-BE-6-PLAN-001`** (review contract REQ §1.1–§1.11 + Pins P-1…P-7) → **`ITRGA-PRV-V2-BE-6-PLAN-001`** (full-depth verdict ACCEPTED, zero corrections; independent corroborations: roadmap quote verbatim, four V1 file pins byte-matched, cited config existent, chain arithmetic consistent) → **`BUILD_ORDER_V2_BE6_PORTFOLIO_RISK_RESEARCH.md` / BO-V2-BE-6-001** (scope U-1…U-4 single package; terminal state T-1…T-12; pins P-1…P-7). Implementation begins under the Operator's execution authorization per the delivery model; the working-DB application of 0046 remains a separate sanctioned act.
