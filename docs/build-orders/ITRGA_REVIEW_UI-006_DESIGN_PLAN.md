# ITRGA REVIEW — UI-006 ENGINEERING DESIGN PLAN

**Unified Research Artifact Explorer**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | **UI-006 — Unified Research Artifact Explorer** (NEW) |
| Document reviewed | `UI-006_ENGINEERING_DESIGN_PLAN.md` (655 lines) |
| ITRGA request | `docs/ITRGA_REQUEST_UI-006_DESIGN_PLAN.md` |
| Governing docs | Doc 12 §8, Doc 13, completed UI-001…UI-005 foundations, Doc 16 Part XIV |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 49f/216t |
| **DETERMINATION** | ✅ **APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS R-1…R-8** |
| Authorizes | Issuance of `BUILD_ORDER_UI-006-P01` (on operator "authorized") — NOT implementation |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Build-identity verification (performed FIRST)

| Check | Result |
|---|---|
| Plan header | `# UI-006 Engineering Design Plan — Unified Research Artifact Explorer`; "pre-Build-Order; no implementation authorization" — OF the workstream |
| Plan length | 655 lines — substantive |
| References request + correct baseline + residual | Yes (`ITRGA_REQUEST_UI-006_DESIGN_PLAN.md`, UI-001…UI-005 COMPLETE, 49f/216t, TD-UI-POSTCSS-HIGH carried in header) |

**Pack confirmed OF the UI-006 Design Plan.**

---

## 2. Assessment against the mutation-boundary (M-1…M-5) — the defining risk

| Line | Plan coverage | Verdict |
|---|---|---|
| **M-1 organization-only** | §2 M-1 enumerates permitted org mutations (collection name/desc, empty-collection delete if API-supported, membership add/remove, tag label create, tag delete if API-supported) AND the **17 underlying-artifact tables that must NOT be mutated** (advisory_signals…operator_workspace_preferences) | ✅ Met (exemplary) |
| **M-2 no verdict mutation** | §2 M-2 enumerates the exact stored fields that must never change (research_status/calibrated_confidence/economic_verdict/validation/sample count/uncertainty/limitations/report_hash/lineage/scenario results/SIMULATED); "no control may relabel a stored artifact as approved/tradable/live/real/reliable/economically-useful/production-ready" | ✅ Met |
| **M-3 store + persistence discipline** | §2 M-3: reuse W7-U03 (`research_collections`/`research_collection_members`/`research_tags`); no new table/migration/dep; persistence-capture verbatim ("API read-back never substitutes… `(0 rows)` is disproof"); any new relationship table = separately-justified heightened-evidence sub-decision | ✅ Met |
| **M-4 no actuation** | §2 M-4 expanded forbidden list incl. position/balance/margin/capital/allocation/real_pnl/open_gate/allow_execution | ✅ Met |
| **M-5 no external AI / analytics engine / recompute** | §2 M-5 full prohibition list (openai/gpt/external_llm/…/generateScenario) | ✅ Met |

All five mutation-boundary lines are pre-registered and testable. The plan correctly identifies UI-006 as the first mutation-bearing workstream and isolates mutation to dedicated late phases.

---

## 3. Assessment against ITRGA request §4 questions

| Q | Plan answer | ITRGA finding |
|---|---|---|
| 1 Route/registry | §3: enhance existing `/research-management` host; no new route in P01 | ✅ Accepted (R-1) |
| 2 Mutation model | §5: enumerated mutations, each mapped to existing W7-U03 endpoint, first mutation isolated to **P04** (collections) then **P05** (tags), after P01–P03 read-only; M-1/M-2 enforced by named tests | ✅ Accepted (R-4/R-5) |
| 3 Persistence/schema | §4/§2 M-3: reuse W7-U03, **no new table/migration** | ✅ Accepted (R-3) |
| 4 Read surfaces | §6 mapped to existing read APIs; §7 verbatim preservation | ✅ Accepted (R-6) |
| 5 Verbatim + no-cherry-picking | §7 explicit | ✅ Accepted (R-6) |
| 6 Phase split | §10: P01 frame → P02 catalog/metadata → P03 lineage/relationships/filtering → **P04 collections mutation → P05 tags mutation** → P06 completion | ✅ Accepted (R-5) |
| 7 UI-002-P04b / UI-009 | §8: advanced filtering in-memory; UI-002-P04b stays independent; first-party components flagged for UI-009 | ✅ Accepted (R-8) |

---

## 4. Binding refinements (R-1…R-8) — conditions on every UI-006 phase

- **R-1 — Route/registry no-drift.** Enhance existing `/research-management`; **no new route** without ITRGA pre-approval; 14-field registry contract unchanged; no duplicate navigation. (Q2 alias `/artifacts` deferred — not authorized now.)
- **R-2 — Read-only P01–P03 (HARD).** P01 (frame/inventory/guardrails), P02 (catalog/metadata), P03 (lineage/relationships/filtering) are **strictly read-only** — no mutation, no persistence write. Prove no mutation control present.
- **R-3 — No new table/migration/dependency (default).** Reuse W7-U03. Alembic stays `20260717_0037`. Any proposed new relationship table is a **separate, heightened-evidence sub-decision requiring explicit ITRGA authorization before implementation** (not granted by this review).
- **R-4 — Mutation is ORGANIZATION-ONLY (M-1/M-2 HARD).** No underlying-artifact mutation; no stored-verdict/confidence/validation/economic/lineage change. Every mutation phase MUST carry: (a) a **`..._does_not_modify_underlying_artifact_values`** named test, and (b) a **forbidden-field-rejection** named test (`..._reject_order_account_execution_and_verdict_fields`).
- **R-5 — Mutation split confirmed: P04 = Collections & Memberships, P05 = Tags.** Mutation only after P01–P03 read-only evidence is Approved. **Create/add-first (Q5):** collection/tag **deletion is authorized only if existing backend AND client API support is proven inline** in that phase; otherwise implement create/add/remove-membership only and defer deletion. No rename/edit-label (backend change) without separate ITRGA authorization.
- **R-6 — Verbatim + no-cherry-picking + no-recompute SPINE (every phase).** Whole-surface grep clean (`inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|generateScenario|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders`) + external-AI grep; displayed artifact values verbatim; filtered/aggregated views never claim full-scope truth unless the stored artifact declares it.
- **R-7 — Persistence-capture control (mutation phases).** Inline raw psql save→SELECT ≥1 row on the CORRECT W7 table + `operator_id → operators.id` no-orphan join + forbidden-field-present=false + `alembic current` = head. **API/in-process read-back NEVER substitutes; `(0 rows)` = disproof.** Also prove the source artifact's stored values are unchanged after the org mutation.
- **R-8 — Level-I + Doc-16 + regression + CI.** Build-identity FIRST; named tests DISPLAYED passing; whole-surface no-actuation grep (M-4 expanded); no-drift substitute (head `20260717_0037`, manifests unchanged, no-endpoint, no registry/route change unless R-1-approved); full suite ≥ **49f/216t** no test lost + backend ≥414; **Doc-16 brand B-1…B-7 (never color alone; material violation ⇒ Corrective)**; served browser evidence; networked CI exit 0 + sentinel, OR TD-W6-CI-AUDIT env-flake waiver, OR `LOCAL_CI_EXIT_CODE:1` solely the tracked TD-UI-POSTCSS-HIGH after substantive gates green — any other nonzero cause is a finding. UI-002-P04b stays independent (Q7). Advanced filtering in-memory; saved filters deferred (Q6).

---

## 5. Observations (non-blocking)

- **OBS-DP-1 (Q8 — postcss remediation timing, ITRGA decision):** The DA asked whether to schedule the TD-UI-POSTCSS-HIGH remediation before mutation phases, before completion, or only before Production Readiness Certification. **ITRGA decision:** it does **not** need to precede the read-only phases or the mutation phases (no dependency change in scope), BUT a **dependency-remediation Build Order SHOULD be scheduled at or before the UI-006-P06 completion checkpoint** — the residual has now recurred across UI-005-P02/P03/P05 and should not be carried indefinitely. At UI-006-P06, the DA must either present remediation or an explicit re-acceptance; carrying it silently past a second workstream completion will attract a Corrective. (Recorded; not blocking any UI-006 phase before P06.)
- **OBS-DP-2 (deletion gating):** Per R-5, any collection/tag deletion in P04/P05 requires **inline proof of existing backend + client API support**; absent that proof, deletion is out of scope for that phase and its inclusion would be Corrective.

---

## 6. Disposition

**UI-006 Design Plan is APPROVED WITH OBSERVATIONS + BINDING REFINEMENTS R-1…R-8.** This is the most disciplined design plan of the programme on its defining risk (artifact mutation). On operator "authorized", ITRGA will issue **`BUILD_ORDER_UI-006-P01` — Explorer Frame, Existing Route Posture, Data-Source Inventory & Guardrails** (per §10 P01 / §14), carrying R-1…R-8 and the P01 named-test anchors, and holding all mutation to P04/P05 under the persistence-capture + no-underlying-artifact-mutation discipline.

No implementation is authorized by this review. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.

**We don't guess. We prove.**

*— AXIOM ITRGA*
