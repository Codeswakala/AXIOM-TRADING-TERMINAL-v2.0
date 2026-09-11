# AXIOM V2 — FE-0 DESIGN PLAN (Design Foundation) — DELIVERED FOR OPERATOR ABSORPTION

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-FE0-DESIGN-PLAN-001 |
| Version | 1.0.1 (correction filing under OD-FE0-001 §1; v1.0.0 identities preserved in §2a) |
| Author | Replacement Development Authority (DA) |
| Date | 2026-09-10 |
| Authorizing request | `AXIOM-V2-DPR-001` (`docs/governance/V2_DESIGN_PLAN_REQUEST_001.md`, md5 `f2b582e44256db2e56fe9935123c698e` / sha256 `177d7034…d916fe`), issued under Operator direction of 2026-09-10 |
| Programme frame | Roadmap CORRECTED EDITION U3 (`AXIOM-V2-FE-ROADMAP-003`, md5 `c45ce9abe8813000a510555e424c31db`) — formal adoption pending; this plan is docs-only either way |
| Authority conferred by this plan | **NONE.** Documents only. No code, styles, routes, assets, or configuration were created or modified. Discovered code needs are FINDINGS for future Build Orders (DPR §3.1) |
| Status | **DELIVERED — ready for Operator absorption/acceptance (DPR §4.2), then ITRGA determination (§4.3)** |

---

## 1. Delivery statement

FE-0's full scope (roadmap U3 §D: inventory · Adopt/Adapt/Exclude register · personas/journeys
· page-contract format + FE-U01 contract · evidence-baseline · sequence confirmation) is
delivered as a six-document cited set under `docs/design/FE0/`. The frontend tree was read
as-is at the clean baseline and was not disturbed (verified §4).

## 2. The document set (identities measured from final bytes)

| ID | Deliverable | File | md5 | sha256 | Bytes |
|---|---|---|---|---|---|
| D0-1 | Existing-frontend inventory (register-true; 17 routes, 81 client functions, 282 tokens, 21 primitives, 188 test files / 975 cases; **8 debt/drift findings F-1…F-8**) | `docs/design/FE0/AXIOM_V2_FE0_D01_FRONTEND_INVENTORY.md` | `ba389d1708ee6bf14d4eee2a633f0778` | `79f3e6062dfb3e37a801ec725349f2955e5cef8b448a0e7940dfc093bb7e8cb0` | 8,837 |
| D0-2 | Adopt/Adapt/Exclude register — framework + 15 seed entries; **reference-set section structurally PENDING per the §9 HOLD (zero entries, zero citations)** | `docs/design/FE0/AXIOM_V2_FE0_D02_ADOPT_ADAPT_EXCLUDE_REGISTER.md` | `5e4755267539e1d3709dd287c6f0b530` | `bb91fdeb59abfc7490019cfca0c5baf5a2ab70f491b1edac3e64d342744edefd` | 5,600 |
| D0-3 | Personas (P-1…P-5, Operator-as-approver included) + journey map J-1…J-8, classification-lawful | `docs/design/FE0/AXIOM_V2_FE0_D03_PERSONAS_JOURNEYS.md` | `13a656783491a31e846ff3635c8596b8` | `a0c1a043f593e4fb4ba6bd46016e469eb251a5d6335806ace184f4a85e8b6600` | 5,712 |
| D0-4 | Page-contract format PCF-1 (12 sections C1–C12) + **FE-U01 sign-in contract COMPLETE** (PC-FEU01-1) | `docs/design/FE0/AXIOM_V2_FE0_D04_PAGE_CONTRACT_FORMAT_AND_FEU01_SIGNIN.md` | `4521605b108b818a36c9488a77d70294` | `118a845736c81e89c9e365b2c2d2c174a7a61d141ef2891b1428fe7e755ca4b1` | 9,952 |
| D0-5 | Evidence-baseline definition (`FEPACK-*` standard E-1…E-9; capture, citation, determination-ready format; E-8 re-keyed per §1.2b with the dual-template disclosure CF-1) | `docs/design/FE0/AXIOM_V2_FE0_D05_EVIDENCE_BASELINE.md` | `78a7d079645423951bc285cfe78095d5` | `06ec0c2c14b677c1fcf74cfeae5648168879058529625e3b1c78b9280bfa5fac` | 4,543 |
| D0-6 | Final sequence confirmation (exit evidence; FE-U17 exception rule as binding text; dependency recital) | `docs/design/FE0/AXIOM_V2_FE0_D06_SEQUENCE_CONFIRMATION.md` | `2f3705f284fad6856956fc094f20def9` | `7b9d02a7e1237567db57567a972b23aa6af180a46b987cc7d6339e757e0adab0` | 3,442 |

### 2a. Correction-filing record (OD-FE0-001 §1, executed 2026-09-10)

| Item | Disposition |
|---|---|
| §1.1 custody | The six-document set was already at `docs/design/FE0/` from first filing; custody re-verified, no move needed |
| §1.2a HEAD id | All 3 citations re-keyed: canonical custody id `fd8d649` named, DA-station clone id `9c78afa` retained as the disclosed measurement plane (`fd8d649` is not an object in the DA clone — both facts recorded; no hash is written that was not measured) |
| §1.2b template path | E-8 re-keyed to `docs/templates/DELIVERY_REPORT_TEMPLATE.md` (md5 `5c8e9de9983cb3ddaec623722fb1d1ec`) with disclosure **CF-1**: custody holds BOTH templates (the 17-section `AXIOM_DA_DELIVERY_REPORT_TEMPLATE.md`, md5 `e54e0dc2…`, was used for all BE-12 DRs) — one-word clarification requested at BO adoption |
| §1.2c §2 path rows | Verified true custody at v1.0.0 already; unchanged |
| §1.3 re-publish | Executed — this table. **Bounded diff: exactly 3 documents moved (D0-1, D0-5, D0-6) + this report. D0-2 `5e475526…` / D0-3 `13a65678…` / D0-4 `4521605b…` BYTE-STILL — the BO's pinned contract identity is unmoved** |

v1.0.0 identities of the moved files, preserved for the record: D0-1 `5bd5dd7d4932eaaf27b4cb86d0cd387a`/8,711 B · D0-5 `69a444bdf16e6e98b001241e0b295e91`/4,100 B · D0-6 `1f7b6c9885121af6ebaf3d05d6caf928`/3,336 B.

## 3. Decisions the plan surfaces for the Operator (absorption items)

1. **The truthful-posture pattern at the door (D0-4 C3).** The as-built LoginPage hardcodes
   `GATE: CLOSED` / `SAL-2…` — excluded as fabricated-looking state (D0-1 F-1, AAE-006). The
   contract offers two lawful forms: (a) facts from an unauthenticated endpoint, or (b) the
   honest `POSTURE: VERIFIED AFTER SIGN-IN` label. Asserted pre-auth posture requires backend
   finding **FE0-BF-1** (public read-only posture fact endpoint) — its own future backend BO.
2. **Removals inside FE-U01's scope:** dead `rememberWorkstation` control (F-2/AAE-007);
   SSO/reset/sign-up affordances stay absent and scan-enforced (backend supports none).
3. **Untouched debts, named:** no token rotation (F-4), localStorage tokens (F-5) — both
   backend-coupled hardening candidates for later BOs, not silent U01 changes.
4. **DPR §3.5 held:** exactly ONE page contract written (FE-U01). U02 is next-on-request.

## 4. Constraint compliance (measured this turn)

- **Docs-only:** every delivered byte lives under `docs/design/FE0/` + this report + register
  files. `git status --short -- frontend/` → **empty**; `frontend/` remains BYTE-CLEAN at head
  `fd8d649` (canonical custody id per OD-FE0-001 §1.2a; DA-station clone id `9c78afa`) after
  the work. Zero code/style/route/asset/config changes.
- **Register-true language:** backend states cited at DPR §3.4 values throughout; §C.1
  semantics used everywhere (DEPENDENCY SATISFIED never read as authorization).
- **No Git write operations.** Workspace `backend/axiom_dev.db` ABSENT (checked this turn).
- **Invariants §B** bound the drafting: no fabricated state survives into the D0-4 contract;
  presentation-is-not-authority is C3's table law; §B.5 is C11 + C9 needles; §B.8 is C8;
  §B.9 governs D0-2 §4's structural PENDING.

## 5. Acceptance path position (DPR §4)

1. ✅ **§4.1 executed** — this cited document set is the return.
2. ⏳ **§4.2 — Operator absorption and acceptance**: awaits an Operator Decision naming this
   plan (`AXIOM-V2-FE0-DESIGN-PLAN-001` v1.0.0 and/or its md5, measured below at filing).
3. ⏳ **§4.3 — ITRGA determination** on the plan file.
4. ⏳ **§4.4 — only then**: `BO-FE-U01` drafted against D0-4. Implementation remains
   unauthorized until that BO is itself adopted.

## 6. DA sign-off

Implemented: N/A (docs-only band). Documents delivered: 6 + this plan report.
Verified-by-DA: every count in D0-1 measured from the tree this turn; every hash in §2
measured from final bytes; frontend tree byte-clean before and after.
Ready-for-review. We don't guess. We prove.

— Replacement Development Authority, 2026-09-10
