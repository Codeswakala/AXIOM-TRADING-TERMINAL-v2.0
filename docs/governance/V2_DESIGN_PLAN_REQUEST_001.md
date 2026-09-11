# DESIGN PLAN REQUEST — DPR-001 (FE-0 Design Foundation)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-DPR-001 |
| Authorization | **Operator direction of 2026-09-10** — *"you are authorized to issue the first design plan request"* |
| Commissioned program state | Corrected roadmap edition **U3** (`AXIOM-V2-FE-ROADMAP-003`), its fourteen adjudication rulings incorporated; formal adoption word of U3 stands **pending** — this request is docs-only and confers no implementation authority either way |
| Addressee | **DA (Delivery Agent)** |
| Band / unit | **FE-0 — V2 UX governance, research, design plan** (docs-only band); lead unit-scope: **FE-U01 sign-in surface** |
| Issuer | ITRGA hand (instrument drafted and issued under the cited Operator authorization) |
| Implementation authority | **NONE. This request authorizes research, inventory, and documents only. No code, styles, routes, assets, or configuration may be created or modified. No implementation is authorized by this request, by U3, or by anything short of a unit Build Order adopted by the Operator.** |

## 1. PURPOSE

Produce the V2 frontend design foundation — the documents from which every subsequent unit design plan and Build Order will be drafted — with the **FE-U01 sign-in surface** as the first fully-written page contract. This closes FE-0's scope as defined in roadmap U3 §D: inventory; Adopt/Adapt/Exclude register; personas/journeys; page contracts; final confirmation of the §C sequence; evidence-baseline definition. FE-0 excludes all visual implementation.

## 2. DELIVERABLES

| ID | Deliverable | Specification |
|---|---|---|
| D0-1 | **Existing-frontend inventory** | Complete register-true map of the current V1 application's surfaces: routes, pages, components, design tokens/primitives, the as-implemented authentication flow, the API client surface and contracts, RBAC/feature-flag behavior, test posture. Truthful — what IS, including debt and drift, not what should be. |
| D0-2 | **Adopt / Adapt / Exclude register — framework** | The register structure and its entries from **existing approved AXIOM design rules and inventory findings**. **HOLD (Operator ruling §9, binding): the visual-reference consultation set is absent from the corpus; no entry may cite it; all its entries remain PENDING until it is transmitted and absorbed. AXIOM identity and existing approved design rules remain the governing defaults.** |
| D0-3 | **Personas + journey map** | Research-grade operator/user types (notably including the Operator himself as approver) and the core journey flows, classification-lawful (research/simulation/paper vocabulary only). |
| D0-4 | **Page contract format + FE-U01 sign-in page contract (complete)** | The contract format that every future unit will use, then the sign-in contract written in full: purpose; AXIOM identity expression; identity/mode/posture visibility at the door; **approved authentication behaviour as actually supported by the backend auth service — no SSO, password-reset, or identity claims that the backend does not support (ruling §2; invariant §B.9)**; full state matrix (loading / empty / error / denied / stale / degraded / unknown); viewport pins (**1440×900 desktop, 390×844 narrow**, unless a later instrument amends); interaction script; accessibility requirements (keyboard, focus, screen-reader announcements, contrast, reduced motion); prohibition scans; V1 regression notes. |
| D0-5 | **Evidence-baseline definition** | The evidence-pack structure every unit will ship: capture spec, naming/register discipline, citation requirements, determination-ready format. This is what makes your visual approvals evidence-shaped (cadence §A.4). |
| D0-6 | **Final sequence confirmation (exit evidence)** | The §C.4 sequence mirrored at closing edition state, including the FE-U17 exception rule as binding text. |

## 3. BINDING CONSTRAINTS ON THE PLANNING WORK

1. **Docs-only.** The DA's work products are documents and reviews. Any code change discovered to be necessary is recorded as a finding for a future Build Order — never executed.
2. **Invariants §B bind the plan as they will bind the build** — truthful mode/provenance, no fabricated state, presentation-is-not-authority, browser never touching broker/provider/AI secrets, execution controls absent until authority exists, assistant non-actuating, accessibility/responsive baseline, §B.9 reference law.
3. **Frontend tree is clean** (custody resolved 2026-09-10, U3 §G.3). The plan must not disturb it; the inventory reads the tree as-is.
4. **Register-true state language.** Backend states are cited at current authoritative values: BE-9 broker visibility OPERATING · BE-11 paper bridge OPERATING · SEEDS ARMED (first cited paper intent witnessed) · BE-12 CLOSED, REGISTERED-LOCKED · live-activation campaign F01 parked/unadjudicated. Dependency semantics per U3 §C.1: DEPENDENCY SATISFIED never means implementation authorized.
5. **Serial cadence law (§A) governs what this plan may not pre-decide:** page contracts beyond FE-U01 are NOT deliverables of FE-0; each later unit receives its contract inside its own loop (Build Order → design plan → …). D0-4 defines the format and the U01 contract only; U02 is next-on-request.

## 4. ACCEPTANCE PATH

1. DA executes and returns the FE-0 design plan (D0-1 … D0-6) as a cited document set.
2. **Operator absorption and acceptance** — recorded as an **Operator Decision naming the plan** (same evidence discipline the visual gates will use).
3. ITRGA determination on the plan file.
4. Only then: the **FE-U01 sign-in Build Order** is drafted (ITRGA hand, adjudicable instrument) against D0-4 — implementation remains unauthorized until that BO is itself adopted.

## 5. RECORD

This request, its authorization, and its eventual acceptance/closure belong to the V2 frontend register trail alongside `AXIOM-V2-FE-ROADMAP-003` and the custody record (U3 §G.3).
