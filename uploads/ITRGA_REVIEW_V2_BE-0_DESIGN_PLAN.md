# ITRGA Review — AXIOM V2 BE-0 DA Design Plan

| Field | Value |
|---|---|
| Review ID | ITRGA-REV-V2-BE-0-001 |
| Review date | 2026-08-23 |
| Submission reviewed | `AXIOM-V2-BE-0-DA-PLAN-001`, version 1.0.0 |
| Governing request | `ITRGA-REQ-V2-BE-0-001` |
| Determination | **CORRECTION REQUIRED** |
| Review scope | Plan authority, scope, provenance, architecture, security, regression, evidence, and alignment with current Operator V2 decisions |

---

## 1. Evidence received

| Level | Evidence | Assessment |
|---|---|---|
| III | Submitted V2 BE-0 DA Design Plan | Complete structure and substantial planning detail received |
| III | V2 Product & Architecture Specification | Proposed design-stage direction; not implementation authority |
| III | V2 Backend/Frontend Roadmaps | Approved planning/decomposition artifacts; no implementation authority by themselves |
| III | `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md` | Active Operator V2 transition-precedence decision |
| I | Current cloned repository measurement | Current commit is `9ab91e76b3ac5f6a42c3066f022700489c214a29`; backend test-file count is 83; frontend test-file count is 188; migration chain visibly reaches `20260717_0037` |

No V1 regression execution output, exact test-result inventory, tag evidence, or Delivery Report was submitted. That absence is expected at plan-review stage and is not itself a defect in the plan.

## 2. Scope assessment

### Verified strengths

The plan is well structured and responds to the ITRGA request. It correctly:

- treats BE-0 as a governance/baseline/architecture band rather than feature work;
- prohibits providers, credentials, brokers, accounts, orders, paper trading, external AI, real-data claims, production deployment, code changes, migrations, and frontend redesign;
- preserves V1 historical records, Git history, migrations, tests, and evidence;
- recommends continued use of the same repository, matching the Operator decision;
- identifies clear V2 domains, versioned APIs, schema ownership, audit/correlation/lineage, feature maturity, mode, degraded-state, and security concepts;
- preserves the frontend-to-broker prohibition;
- includes a V1 regression baseline plan and additive-file scope;
- includes risk, debt, provenance, architecture, current-state, ADR, and capability-maturity artifacts.

### Assessment

The plan is a strong basis for BE-0 after the corrections below. It must not proceed to a Build Order in its submitted form because it conflicts with current Operator V2 governance decisions in several material places.

## 3. Findings

### Finding V2-BE0-PLAN-001 — Proposed fractional constitutional tiers conflict with the active V2 precedence decision

| Field | Detail |
|---|---|
| Severity | High — governance/authority integrity |
| Status | Open |
| Governing rule | `V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md`: all active V1 governing documents remain binding; a V2 document may amend a V1 requirement only by explicit affected document/section, replacement rule, effective scope, approval, and V2 amendment-register entry. |
| Observed condition | Part B.1 proposes a new Tier 2.5 V2 Product & Architecture Specification, Tier 3.5 roadmaps, and Tier 4.5 V2 architecture. This implicitly changes the established constitutional hierarchy and the operative precedence model. |
| Impact | Fractional tiers could cause V2 planning documents to appear superior to active V1 roadmap/architecture rules without the explicit amendment process required by the Operator. |
| Required correction | Remove the proposed Tier 2.5/3.5/4.5 hierarchy from the BE-0 plan. Replace it with the active Operator rule: V1 governing documents remain binding; V2 documents are proposed/approved within their stated domain and may amend V1 only through a specific recorded amendment. The future V2 Programme Charter must be described as an Operator-owned draft requiring explicit approval, not as a mechanism that unilaterally reorders tiers. |
| Expected closure evidence | Revised Part A/B plus an explicit reference to `docs/governance/V2_DOCUMENT_PRECEDENCE_ADOPTION_RECORD.md`. |
| Closure criterion | No V2 document has implied precedence over V1 merely because it is labelled V2 or assigned a fractional tier. |

### Finding V2-BE0-PLAN-002 — The plan has not incorporated current Operator decisions on repository, precedence, and BE-0 modes

| Field | Detail |
|---|---|
| Severity | High — current-state accuracy |
| Status | Open |
| Governing/Operator decisions | V2 continues in the same repository; V2 precedence decision is recorded and active; BE-0 implementation scope is governance/provenance artifacts only; BE-0 design scope is Research and Simulation only. |
| Observed condition | A.5 and I.3 classify repository/custody and document precedence as **PENDING**. Part D proposes a duplicate `V2_DOCUMENT_PRECEDENCE.md` despite the active adoption record. C.7 and D-10 define all four modes (`RESEARCH`, `SIMULATION`, `PAPER`, `LIVE`) as BE-0 work. |
| Impact | The plan is stale against Operator decisions and expands BE-0 design beyond the authorized Research/Simulation scope. A duplicate precedence artifact risks conflict. |
| Required correction | Update the plan to: (1) record same repository as an Operator decision; (2) cite the existing precedence adoption record as the controlling transition-precedence artifact; (3) remove duplicate V2 precedence deliverable from BE-0; (4) constrain BE-0 operational mode classification to `RESEARCH` and `SIMULATION`; (5) record Paper and Live only as future, explicitly out-of-scope concepts requiring later amendments and bands. |
| Expected closure evidence | Updated Parts A, C.7, D, G, and I, including an authoritative-decision table. |
| Closure criterion | The plan’s stated current state agrees with the active Operator decisions and does not establish Paper/Live as BE-0 design deliverables. |

### Finding V2-BE0-PLAN-003 — Baseline claims are not sufficiently exact and conflict with current repository/capability evidence

| Field | Detail |
|---|---|
| Severity | Medium — provenance/regression integrity |
| Status | Open |
| Governing rule | BE-0 requires a V1 parent baseline and regression baseline that are reproducible and traceable. |
| Observed condition | B.4/F.1 use `Current HEAD`, approximate file/test counts, and state ~1,017 tests (415 backend + 603 frontend). The current repository measurement establishes the full SHA `9ab91e76b3ac5f6a42c3066f022700489c214a29`, 83 backend test files, and 188 frontend test files. The current verified capability catalogue states 1,336 tests (476 backend + 860 frontend); the submitted figures conflict with it. The proposed V2 baseline tag is named but has no approved creation/record semantics. |
| Impact | An inaccurate or non-specific baseline weakens reproducibility, regression accounting, and later provenance claims. Test-file count is not executed-test count. |
| Required correction | Replace `Current HEAD` with the full commit SHA in the plan. Do not claim an exact test-case count until it is measured by the prescribed commands and captured as Level-II evidence. Distinguish test-file inventory from executed results. Define the baseline tag as an intended BE-0 artifact, with creation only after the Build Order authorizes it and its final SHA recorded. Reconcile or explicitly mark the capability-catalogue test-count discrepancy for measurement during BE-0. |
| Expected closure evidence | Revised B.4/B.5/F.1/F.5/H.3 language and baseline measurement protocol. |
| Closure criterion | Future baseline reporting can reproduce commit, migration head, commands, environment, executed result, file inventory, and tag/ref without ambiguity. |

### Finding V2-BE0-PLAN-004 — BE-0 architecture material is appropriate, but it must not pre-authorize future capability models or permissions

| Field | Detail |
|---|---|
| Severity | Medium — scope discipline |
| Status | Open |
| Governing rule | BE-0 is governance/provenance artifacts only; active V1 documents remain binding. |
| Observed condition | The plan’s conceptual package/module topology, API prefixes, tables, error codes, environment modes, and permission map include future `paper_trading.trade`, `execution.trade`, broker management, `LIVE` configuration, `v2_orders`, `v2_positions`, and AI-provider domains. Although marked later bands, the detail can be read as a preselected implementation/design decision beyond Research/Simulation BE-0 scope. |
| Impact | It risks prematurely constraining security/execution architecture before the required future specialist security, paper, broker, and execution design reviews. |
| Required correction | Retain a high-level future-domain inventory only. Label all Paper, Live, Broker, Execution, and external AI shapes as **non-binding future candidates**, not approved architecture. Remove future trade permissions and production-facing table/configuration specifics from the BE-0 canonical decision set. Keep BE-0 architecture binding only for V1 preservation, domain-boundary principles, audit/provenance principles, Research/Simulation boundary, and deferral mechanism. |
| Expected closure evidence | Revised Part C/E with a clear `Binding BE-0 decisions` versus `Deferred/non-binding V2 candidates` separation. |
| Closure criterion | No BE-0 artifact can be cited to justify later paper/live/broker/execution implementation without its own authorized design and Build Order. |

### Finding V2-BE0-PLAN-005 — Required Operator charter handling needs an explicit approval and amendment-register workflow

| Field | Detail |
|---|---|
| Severity | Medium — governance completeness |
| Status | Open |
| Governing rule | A V2 document may amend V1 only via explicit section-level amendment, scope, approval, and V2 amendment-register record. |
| Observed condition | The plan proposes a V2 Programme Charter but does not fully specify how its provisions will identify affected V1 sections, state replacement rules/effective scope, obtain Operator approval, and be entered in a V2 amendment register. |
| Required correction | Add the amendment-register artifact/process to the BE-0 inventory or expressly establish it as a section of the V2 Current State/Charter with immutable IDs. Define DA drafting, Operator approval, ITRGA review, and record publication responsibilities. The BE-0 Build Order must make clear that the DA drafts but cannot self-adopt the charter. |
| Expected closure evidence | Revised artifact inventory and charter workflow. |
| Closure criterion | Every prospective V1 amendment is traceable to exact old/new language, scope, approval, and V2 register entry. |

## 4. Non-finding observations

1. The single FastAPI modular-monolith recommendation is proportionate for the present stage. The plan correctly defers any execution-service extraction decision.
2. Preserving `/api/v1/` and using additive `/api/v2/` endpoints is a sound candidate strategy, but it remains an architecture proposal subject to a later authorized architecture decision.
3. The audit-event and correlation/causation model is valuable. `details` must later have redaction/classification rules; it must not become a secret-bearing general payload.
4. The shared-table proposal (`operators`, `audit_events`, `refresh_tokens`) needs a later data-ownership/security review before any schema work. It is acceptable only as a non-binding candidate at BE-0.
5. The plan correctly identifies the V1 production-not-certified and gate-closed facts as inherited constraints.

## 5. Required resubmission scope

The DA must resubmit a corrected BE-0 design plan addressing Findings V2-BE0-PLAN-001 through V2-BE0-PLAN-005 only. No expansion, runtime code, migrations, provider/broker activity, paper/live capability, external AI, or frontend implementation is requested.

## 6. Determination and next state

**Determination: CORRECTION REQUIRED.**

The plan is structurally strong and conditionally suitable for BE-0, but it cannot support a Build Order until it aligns with the active Operator V2 transition-precedence decision, same-repository decision, governance/provenance-only BE-0 scope, and Research/Simulation-only BE-0 design scope.

After correction, the next sequence is:

```text
DA corrected plan
→ ITRGA closure review
→ Operator approval of any required V2 Programme Charter/amendment
→ bounded BE-0 Build Order
→ governance/provenance artifact implementation only
```

No V2 runtime implementation is authorized by this review.
