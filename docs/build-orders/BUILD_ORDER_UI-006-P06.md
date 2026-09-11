# BUILD ORDER — UI-006-P06

## UI-006 Completion Checkpoint (integration evidence · mutation-boundary + constitutional + Doc 16 brand validation)

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P06 — Completion Checkpoint** |
| Predecessor verdict | `docs/ITRGA_REVIEW_UI-006-P05.md` — ✅ Approved with Observations |
| Governing docs | Doc 12 §8, `UI-006_ENGINEERING_DESIGN_PLAN.md` §10 (P06)/§11, `ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` (R-1…R-8 + M-1…M-5), Doc 16 Part XIV |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **54f/241t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose

Provide **final integration evidence** and bring UI-006 to its **completion checkpoint**: the Unified Research Artifact Explorer makes every research artifact discoverable, interconnected, and traceable on the existing `/research-management` host — read-only catalog/metadata/lineage/relationships/filtering plus **organization-only** collection/tag/membership mutation over existing W7 stores, constitutionally clean (no underlying-artifact/verdict mutation, no actuation, no recompute, no external AI, no new table), verbatim, no-cherry-picking, and brand-compliant. **No new capability.** On Approved, ITRGA declares 🏛️ UI-006 COMPLETE.

---

## 2. Scope

**IN scope:**
1. Route/browser integration evidence across the explorer (catalog · metadata detail · lineage/relationships · filtering · collection/tag/membership organization).
2. Whole-surface no-actuation **and** no-recompute/no-inference/no-external-AI grep.
3. Full regression (backend + frontend, no loss).
4. **Mutation-boundary completion validation** — organization-only, existing-store-bound, no underlying-artifact/verdict mutation, no new table (M-1…M-3).
5. Final constitutional self-check + Doc 16 brand self-check (B-1…B-7).
6. Browser-served workflow proof (incl. organization mutation + logged-out block).
7. **🔴 TD-UI-POSTCSS-HIGH decision (mandatory — see §5).**

**OUT of scope:** any new capability / recompute / analytics engine / external AI / live data / broker-execution-Gate / **new artifact-organization mutation beyond the P04/P05 slices** / new table / migration / dependency (except a §5(A) authorized remediation) / endpoint / registry-route change / Production Readiness Certification (Doc 11, HELD).

---

## 3. Constitutional & architectural guardrails (binding)

- Gate CLOSED; no live broker/order/account/position/balance/margin/capital/allocation/real-P&L path anywhere.
- No external LLM/AI; no client-side analytics engine; no recompute/inference/relationship-inference/re-derivation/reclassification.
- **Mutation is organization-only (M-1/M-2):** collection/tag/membership actions never mutate underlying artifacts or their stored verdict/confidence/validation/economic/lineage values; references are ids only, no source payload.
- **Existing-store-bound (M-3):** mutation writes only to existing W7 `research_collections` / `research_collection_members` / `research_tags`; **no new table/migration**; alembic `20260717_0037`.
- **Verbatim + no-cherry-picking preserved** across catalog/metadata/lineage/filtering.
- No-drift: package manifests unchanged (no new dependency, except a §5(A) authorized remediation); no new endpoint; **no registry/route change** (R-1: `/research-management` only).
- **🔴 Doc 16 brand gate (B-1…B-7)** — never color alone; material violation ⇒ Corrective (Part XIV).

---

## 4. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui006_completion_artifact_explorer_discovery_organization_and_traceability_hold`
2. `test_ui006_completion_mutations_are_organization_only_and_existing_store_bound`
3. `test_ui006_completion_no_actuation_recompute_external_ai_schema_or_route_drift`
4. `test_ui006_completion_verbatim_no_cherry_picking_and_relationship_boundaries_hold`
5. `test_ui006_completion_accessibility_doc16_brand_and_ui001_ui002_integration_hold`

---

## 5. 🔴 TD-UI-POSTCSS-HIGH DECISION (mandatory at this checkpoint)

The high-severity transitive advisory `postcss <=8.5.17` (GHSA-r28c-9q8g-f849) has been carried since UI-004-P06 (Path-B accepted) and is now at a **second** workstream completion. The delivery MUST take one of two paths, **explicitly stated in the delivery report and adjudicated by ITRGA**:
- **(A) Remediate:** a separately-authorized dependency remediation (`npm audit fix` / bump) — being a dependency change, it requires its own evidence: manifest diff, full suite still green (no functional regression), and a **networked `npm audit --audit-level=high` exit 0**; OR
- **(B) Re-accept (explicit):** declare UI-006 COMPLETE with TD-UI-POSTCSS-HIGH **explicitly re-accepted** as a pre-certification residual, on the standing condition it is remediated before Production Readiness Certification (Doc 11).

**Silently relabeling the audit green is prohibited. Carrying it without an explicit decision at this checkpoint ⇒ Corrective.** ITRGA strongly prefers (A) at or before this point given the recurrence, but will adjudicate the chosen path.

---

## 6. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-006-P06.
- (b) **5 named completion tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 Whole-surface no-recompute/no-inference/no-external-AI grep CLEAN** — `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|generateScenario|inferRelationship|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders` + `openai|gpt|external_llm|llm_summary|ai_summary`.
- (d) **🔴 Whole-surface no-actuation grep CLEAN** (M-4 expanded): `buy|sell|place_order|execute|go-live|connect-broker|broker|account_id|order_ticket|position|balance|margin|capital|allocation|real_pnl|open_gate|allow_execution`.
- (e) **🔴 Mutation-boundary completion proof** — organization-only, existing-store-bound (M-1/M-2/M-3): re-affirm (raw psql or referenced from P04/P05) that collection/tag/membership mutation touches only `research_collections`/`research_collection_members`/`research_tags` with refs only, no underlying-artifact/verdict mutation, `forbidden_*_column_count = 0`; named test #2.
- (f) **Verbatim + no-cherry-picking reaffirmed** (named test #4).
- (g) **No-drift substitute** — `alembic current` = `20260717_0037` (**no new migration** unless §5(A)); `package.json`/`package-lock.json` content unchanged (unless §5(A) remediation → supply manifest diff); no new endpoint grep; **no registry/route change** (R-1); named test #3.
- (h) **Completion regression** — backend `pytest -q` **≥414 passed**; frontend Vitest **≥54f/241t** all passing (no test lost). **Gated full run must exit 0.**
- (i) **🔴 Doc 16 brand self-check + browser proof (B-1…B-7).**
- (j) **Browser served-session** — the explorer end-to-end (discovery → catalog/metadata → lineage/relationships → filtering → organization mutation), organization-only + operator-scoped; GATE CLOSED / RESEARCH-ONLY framing; logged-out `/login` block.
- (k) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel; OR TD-W6-CI-AUDIT env-flake waiver; OR (only if §5(B) chosen) `LOCAL_CI_EXIT_CODE: 1` solely the tracked TD-UI-POSTCSS-HIGH after substantive gates green — disclosed. If §5(A) remediation chosen, a networked audit-high exit 0 is expected. **Any other nonzero cause is a finding.**
- (l) **🔴 UI-006 COMPLETION VALIDATION** — the delivery report presents the DA's completion self-check; ITRGA independently applies the **constitutional validation** (governing hierarchy Docs 00–16 · no scope expansion · mutation organization-only & existing-store-bound · no underlying-artifact/verdict mutation · no new table · no actuation/recompute/external-AI · UI-001/UI-002 unmodified · single shell · **Gate CLOSED**) **AND the Doc 16 brand validation (B-1…B-7)** — plus the §5 residual decision.

---

## 7. Determination rule

**Approved** requires: build-identity confirmed; (b) all five named completion tests displayed passing; (c) whole-surface no-recompute + external-AI grep clean; (d) whole-surface no-actuation grep clean; (e) mutation-boundary completion proof (organization-only, existing-store-bound, no underlying-artifact/verdict mutation, no new table); (f) verbatim + no-cherry-picking reaffirmed; (g) no-drift + head unchanged (or a clean §5(A) remediation with green suite); (h) completion regression green (gated exit 0); (i) Doc 16 brand pass; (j) browser workflow + logged-out; (k) CI exit 0 or the pre-authorized/waived exception; (l) constitutional + brand completion validation clean **and** the §5 TD-UI-POSTCSS-HIGH decision explicitly stated and adjudicated.

A single CRITICAL, an undeclared/silently-carried postcss decision, any underlying-artifact/verdict mutation, a new table/migration, a red gated run, or any unmet mandatory evidence item ⇒ Corrective Actions Required / Rejected.

**On Approved: ITRGA will declare 🏛️ UI-006 — UNIFIED RESEARCH ARTIFACT EXPLORER — COMPLETE** (every research artifact discoverable/interconnected/traceable on the UI-001/UI-002 shell; read-only discovery + organization-only mutation over existing W7 stores; no underlying-artifact mutation; Doc 12 §8 / Doc 16 conformant; regression passed; ITRGA review complete). **UI-006 completion does NOT open the Gate or authorize execution.**

Future after UI-006: **UI-007 — Governance & Evidence Workspace** (Doc 12 §9 — NEW workstream → request Design Plan first), then UI-008 (Institutional AI — constitutionally scoped, no external LLM without a governance amendment), UI-009 (Design System), UI-010 (Accessibility); and separately the Production Readiness Certification track (Doc 11, HELD — gated by TD-UI-POSTCSS-HIGH remediation).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
