# BUILD ORDER — UI-006-P01

**Explorer Frame · Existing Route Posture · Data-Source Inventory · Guardrails** — *(Read-Only)*

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P01** |
| Design-plan review | `docs/ITRGA_REVIEW_UI-006_DESIGN_PLAN.md` — ✅ Approved w/ Obs + R-1…R-8 |
| Governing docs | Doc 12 §8, `UI-006_ENGINEERING_DESIGN_PLAN.md` §10 (P01), Doc 16 Part XIV |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend **49f/216t** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose & scope

Establish the UI-006 Unified Research Artifact Explorer **frame** on the existing `/research-management` host, prove **every artifact family maps to an existing governed store/read API**, and lay down the **no-actuation / no-recompute / no-mutation guardrail** BEFORE any read-detail or mutation work. **This phase is strictly READ-ONLY (R-2).** Presentation/navigation/integration only.

**IN scope:**
1. Explorer frame on existing `/research-management` (no new route — R-1).
2. **Data-source inventory** covering the artifact families (advisory signals, intelligence/validation/economic/correlation/regime/scenario/portfolio-risk reports, chart annotations, trade plans, journal, execution research, collections, tags, memberships) — each mapped to its existing store + existing read seam.
3. No-actuation / no-recompute / no-external-AI / **mutation-deferral** guardrail framing (GATE CLOSED · RESEARCH-ONLY; collection/tag mutation explicitly deferred to P04/P05).

**OUT of scope (do NOT build):**
- Read-detail catalog/metadata (P02), lineage/relationships/filtering (P03), **any mutation** (P04 collections / P05 tags), completion (P06).
- Any collection/tag/membership create/update/delete (R-2/R-4 — P01 is read-only).
- Any persistence / saved-view state; any new table / migration / dependency / endpoint / **registry route** change (R-1/R-3).
- Any recompute / inference / re-derivation / reclassification / analytics engine / external AI-LLM (R-6/M-5).
- Any order/broker/account/position/balance/margin/capital/allocation/real-P&L/live/go-live/execute/Gate path (M-4).

---

## 2. Binding refinements applied (R-1…R-8)

- **R-1** — Enhance existing `/research-management`; **no new route** (no `/artifacts`/`/artifact-explorer`); 14-field registry contract unchanged; no duplicate navigation.
- **R-2** — **P01 is strictly READ-ONLY** — no mutation control present, no persistence write.
- **R-3** — No new table/migration/dependency; alembic `20260717_0037`.
- **R-4** — Mutation deferred to P04/P05; P01 exposes no create/update/delete.
- **R-6** — no-recompute + external-AI grep clean; verbatim posture on any displayed artifact value.
- **R-8** — Level-I evidence + Doc-16 brand + regression ≥ baseline, no test lost + whole-surface no-actuation grep (M-4 expanded).

---

## 3. Mandatory named tests (MUST be DISPLAYED passing by name — verbose reporter)

1. `test_ui006_explorer_mounts_inside_single_ui001_shell`
2. `test_ui006_explorer_uses_existing_route_and_registry_only`
3. `test_ui006_explorer_maps_every_artifact_family_to_existing_sources`
4. `test_ui006_explorer_contains_no_mutation_actuation_or_gate_path`
5. `test_ui006_explorer_preserves_research_only_verbatim_and_doc16_branding`

---

## 4. Full mandatory evidence checklist (Level-I, operator-run on target)

Windows/PowerShell `C:\Users\Swakala\.vscode\AXIOM\axiom`; PostgreSQL `axiom`/`axiom_dev_password` db `axiom`; admin `admin`/`admin123`.

- (a) **Build identity** — delivery report + transcript header grep proving pack is OF UI-006-P01.
- (b) **5 named tests DISPLAYED passing** by name (verbose reporter).
- (c) **🔴 R-2/R-4 read-only proof** — no collection/tag/membership create/update/delete control present in the P01 explorer (grep + named test #4); mutation deferral stated in UI.
- (d) **🔴 R-6 no-recompute grep CLEAN** — `inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|generateScenario|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders`; **AND external-AI grep CLEAN** — `openai|gpt|external_llm|llm_summary|ai_summary`.
- (e) **🔴 Whole-surface no-actuation grep CLEAN** (M-4 expanded): `buy|sell|place_order|execute|go-live|connect-broker|broker|account_id|order_ticket|position|balance|margin|capital|allocation|real_pnl|open_gate|allow_execution`.
- (f) **Data-source inventory proof** — each artifact family maps to an existing store + existing read seam (source grep + named test #3).
- (g) **No-drift substitute** — `alembic current` = `20260717_0037`; `package.json`/`package-lock.json` content unchanged (no new dep); no new endpoint grep; **no registry/route change** (R-1: existing `/research-management` only, no `/artifacts`/`/artifact-explorer`); **no persistence** (R-3).
- (h) **Regression** — frontend Vitest **≥49f/216t** all passing (no test lost; verify FULL total; print the vitest sentinel alongside the CI sentinel); backend `pytest -q` **≥414 passed**; TS clean; production build + bundle delta. **Gated full run must exit 0.**
- (i) **🔴 Doc 16 brand B-1…B-7** — palette / `--font-mono` / `.mono` numerics (artifact/collection/tag ids) / no hardcoded color in production TSX / unified iconography / institutional-not-retail / brand a11y (never color alone).
- (j) **Browser served-session screenshots** — logged-in `/research-management` explorer frame with the data-source inventory + explicit mutation-deferral copy; GATE CLOSED / RESEARCH-ONLY framing; logged-out `/login` block.
- (k) **Networked local CI** `LOCAL_CI_EXIT_CODE: 0` + sentinel; OR the TD-W6-CI-AUDIT offline npm-audit env-flake after substantive gates green → waiver; OR `LOCAL_CI_EXIT_CODE: 1` attributable **solely** to the tracked TD-UI-POSTCSS-HIGH after substantive gates green — disclosed, not relabeled. **Any other nonzero cause is a finding.**
- (l) **TD-UI-POSTCSS-HIGH note** — P01 introduces no dependency change; the residual does not gate it but remains OPEN (dependency-remediation Build Order to be scheduled at/before UI-006-P06 per OBS-DP-1).

---

## 5. Determination rule

A single CRITICAL, any mutation control present in this read-only phase, or any unmet mandatory evidence item ⇒ Corrective Actions Required / Rejected. Only **Approved** or **Approved with Observations** authorizes the next Build Order (UI-006-P02 — Unified Artifact Catalog & Metadata Detail, read-only).

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
