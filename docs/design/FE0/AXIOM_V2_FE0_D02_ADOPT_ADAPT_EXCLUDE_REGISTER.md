# FE-0 / D0-2 — Adopt / Adapt / Exclude Register (Framework + Seed Entries)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-FE0-D02-001 |
| Parent | AXIOM-V2-FE0-DESIGN-PLAN-001 (under AXIOM-V2-DPR-001) |
| Author | DA · 2026-09-10 |
| **HOLD (binding, Operator ruling §9)** | The visual-reference consultation set is ABSENT from the corpus. **No entry below cites it.** All reference-derived entries are structurally reserved as PENDING (§4) until transmission and absorption. AXIOM identity and existing approved design rules govern as defaults |

## 1. Register schema (the framework every future entry uses)

| Column | Meaning |
|---|---|
| Entry id | `AAE-NNN`, append-only |
| Subject | The concrete artifact/pattern (file-cited where it exists) |
| Source class | `V1-AS-BUILT` · `APPROVED-DESIGN-RULE` · `REFERENCE-SET (PENDING)` |
| Disposition | **ADOPT** (use as-is) · **ADAPT** (use with named changes) · **EXCLUDE** (do not carry) · **PENDING** (reference-set entries only) |
| Rationale | One evidence-cited sentence |
| Binding unit | Where the disposition takes effect (unit id) |

Rules: dispositions bind only when the naming unit's BO adopts them; EXCLUDE entries also name what replaces the excluded thing (or "nothing"); reference-set entries may not leave PENDING except by an instrument recording absorption.

## 2. Seed entries — V1 as-built (from D0-1)

| Id | Subject | Source | Disposition | Rationale | Unit |
|---|---|---|---|---|---|
| AAE-001 | 5-tier token hierarchy `tokens.css` (282 props) + `theme.ts` typed access + brand palette | V1-AS-BUILT / APPROVED-DESIGN-RULE (Doc 16 conformance recited in-file) | **ADOPT** | Existing approved AXIOM identity; WCAG AA notes in-file; every later unit consumes it (U2 R-3: tokens are U02's foundation) | FE-U02 (consumed from U01) |
| AAE-002 | 21 `components/ui` primitives with co-located tests | V1-AS-BUILT | **ADOPT** (per-unit reuse assessment per §E) | Tested, token-conformant primitive base; rewriting is the v1 wave-batching failure mode U3 exists to prevent | all units |
| AAE-003 | `WORKSPACE_REGISTRY` contract incl. `requiresAuth:true` / `noActuation:true` guard literals, RBAC gate + truthful ACCESS DENIED element | V1-AS-BUILT | **ADOPT** | The denial text ("access restriction, not an empty result") is already §B.3-conformant; registry is the single route source of truth | FE-U02 |
| AAE-004 | Auth session mechanics (`AuthContext` + `tokenStorage` + `ProtectedRoute`) | V1-AS-BUILT | **ADAPT** | Flow is backend-true, but D0-1 F-4 (no rotation despite backend support) and F-5 (localStorage) are named adaptation candidates — backend-coupled parts go to findings, not FE scope | FE-U01 |
| AAE-005 | `LoginPage` layout family (split hero/form composition) | V1-AS-BUILT | **ADAPT** | Composition serviceable; hardcoded governance literals (F-1), dead checkbox (F-2), and missing coupon (F-3) must be resolved by the D0-4 contract | FE-U01 |
| AAE-006 | LoginPage hardcoded posture strings (`GATE: CLOSED`, `SAL-2 …`, `RESEARCH-ONLY · NON-ACTUATING` as static text) | V1-AS-BUILT | **EXCLUDE** — replaced by the D0-4 truthful-posture pattern (backend-sourced or honestly-unverified presentation) | §B.2/§B.3: no fabricated or unverifiable state at the door | FE-U01 |
| AAE-007 | `rememberWorkstation` dead control | V1-AS-BUILT | **EXCLUDE** — replaced by nothing (remove) unless a real persistence semantic is BO'd | A control that does nothing is fabricated UI state | FE-U01 |
| AAE-008 | Decorative pre-auth market-like scene (candles/waves/particles, `aria-hidden`) | V1-AS-BUILT | **ADAPT** | Lawful while value-free and decorative; the D0-4 contract pins "no real or realistic quote/level/symbol content" + reduced-motion behavior | FE-U01 |
| AAE-009 | Relative-URL API client with typed error status (SURF-P03) | V1-AS-BUILT | **ADOPT** | §B.5-conformant (no direct provider/broker contact; single client seam) | all units |
| AAE-010 | React Router v7 future-flags OPTION A | V1-AS-BUILT | **ADOPT** | Explicit early pin, recorded in source | FE-U02 |
| AAE-011 | Dormant `featureFlag` registry field | V1-AS-BUILT | **ADOPT** (dormant) | Needed by §E route/flag gates when a unit first uses a flag | as first used |
| AAE-012 | `/chart` alias of `/charts` | V1-AS-BUILT | **ADAPT** (keep functioning; do not extend) | V1 preservation (§A.6); consolidation would be a breaking change needing explicit approval | FE-U04 |

## 3. Approved-design-rule entries

| Id | Subject | Disposition | Rationale | Unit |
|---|---|---|---|---|
| AAE-020 | AXIOM brand palette + logo assets (`branding/`, `frontend/public/branding/axiom-logo.png`) | **ADOPT** | The governing identity default under the §9 HOLD | all |
| AAE-021 | WCAG 2.1 AA floor as recited in tokens.css | **ADOPT** | §B.8 baseline-not-polish | all |
| AAE-022 | Truthful-state vocabulary (loading/empty/error/denied/stale/degraded/unknown) | **ADOPT** | §A.4 state matrix is per-unit BO law | all |

## 4. Reference-set section — FIRST ABSORPTION (REF-001, 2026-09-10)

> Status change: the Operator transmitted the first visual reference **during the FE-U01
> corrective cycle** (visual rejection of FEPACK-FEU01-001's door, §A.5): `REF-001`
> `docs/design/references/REF-001_Login_Signup_Screens.jpg` (md5
> `24aff50af75cec0be35c4b5bd3537b15` / sha256 `6007a3da…84cd9a1`, 88,108 B) with the
> instruction "professional 3D animated trading terminal, use the attached image as a
> template". Absorbed under invariant §B.9: composition language adapted to AXIOM identity;
> every backend-unsupported affordance excluded. The broader consultation-set HOLD remains
> for any references not yet transmitted.

| Id | Subject (from REF-001) | Disposition | Rationale | Unit |
|---|---|---|---|---|
| AAE-030 | Floating rounded glass-shell card over a full-bleed dramatic backdrop | **ADAPT** | Composition adopted; backdrop becomes the AXIOM 3D market scene (value-free), not the reference's figure imagery | FE-U01 |
| AAE-031 | Top slim identity/nav strip inside the card | **ADAPT** | Becomes AXIOM brand (left) + truthful posture/reachability chips (right); the reference's Home/About/Blog nav and Sign in/Register controls are not adopted (no such routes/flows) | FE-U01 |
| AAE-032 | Split hero-left / form-right inner layout with soft depth | **ADAPT** | Kept; hero = brand copy over the animated scene, form = frosted card | FE-U01 |
| AAE-033 | SSO row ("continue with" Google/Apple/Facebook) | **EXCLUDE** — replaced by nothing | Backend supports no SSO (D0-1); §B.9 forbids implying it; C9 scan-enforced | FE-U01 |
| AAE-034 | "Recover Password ?" link | **EXCLUDE** — replaced by nothing | No reset flow exists on the backend; ruling §2 | FE-U01 |
| AAE-035 | "Create Account!" / Register affordances | **EXCLUDE** — replaced by nothing | No self-registration exists | FE-U01 |
| AAE-036 | Email-placeholder identity ("Enter Email") | **EXCLUDE** | The backend contract is operator username, not email | FE-U01 |
