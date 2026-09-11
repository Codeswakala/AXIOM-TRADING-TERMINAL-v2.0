# ADOPTION RECORD — BO-FE-U01 (Sign-In Surface)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BO-FE-U01-ADOPT-001 |
| Date | 2026-09-10 |
| Operator decision | **APPROVED AS DRAFTED** (Operator Adoption instrument, 2026-09-10) |
| Instrument adopted | `AXIOM-V2-BO-FE-U01-DRAFT-001`, without amendment |
| Pinned contract | PC-FEU01-1 (md5 `4521605b…`; rekeys to its filed identity after the OD-FE0-001 correction order executes) |
| Effect | **FE-U01 implementation is authorized to the DA** within the stated boundary. This is the first implementation-bearing instrument of the V2 frontend program |
| Executing authority | **DA only. ITRGA implements nothing** (role boundary §1/§37; carried into this record) |

## 1. AUTHORIZED BOUNDARY (verbatim from the adoption)

`/login` · the `LoginPage` component family and its CSS · the auth-session seam explicitly included by PC-FEU01-1. No other rendered surface, shared workspace, route, client mechanism, or unrelated frontend file is authorized.

## 2. REQUIRED DELIVERABLES (≤ the BO's §2, verbatim classes)

Truthful pre-auth posture (pattern b: `POSTURE: VERIFIED AFTER SIGN-IN`) · removal of AAE-006 hardcoded claims and AAE-007 dead control · real username/password contract only · verbatim 401 `detail` in `role="alert"` region · transport failure distinct from 401 · `GET /health` reachability chip · value-free decorative scene (aria-hidden, static under reduced motion) · unchanged session restore + ProtectedRoute law · the FE-U01 test family (F-3 resolution).

## 3. FAIL-FIRST (binding order of work)

Tests before implementation bytes; red-state evidence against the as-built page captured into `FEPACK-FEU01-001`. No completion claim without state-matrix, redirect-law, and prohibition-scan evidence.

## 4. SCOPE PROTECTIONS (verbatim standing)

SSO · password-reset/forgot · sign-up · MFA affordances · new execution/trading functionality · changes to other frontend surfaces · unrelated refactoring · FE-U02 or any later unit — **all unauthorized**. Out-of-boundary change = scope defect, escalated, never silently absorbed. Discovered conflicts between BO, pinned contract, or governing artifacts are surfaced before widening.

## 5. EVIDENCE AND APPROVAL SEQUENCE (ordered, unskippable)

`FEPACK-FEU01-001` (E-1…E-9, real-condition captures at 1440×900 and 390×844) → **Operator visual approval, a separate state from implementation completion**, decision explicitly naming `FEPACK-FEU01-001` → ITRGA determination on the same pack → FE-U01 closure → FE-U02 becomes draftable.

## 6. PARALLEL DOCS OBLIGATION (OD-FE0-001 correction order)

The DA's docs-only correction turn (file D0-set at `docs/design/FE0/`, re-key HEAD `fd8d649`, true template path, re-publish hashes) executes independently of implementation; E-1's contract pin re-keys to the filed identity thereafter.

## 7. GOVERNANCE BOUNDARY (verbatim standing)

Authorizes FE-U01 implementation only. No backend governance change; no broker/paper/live/AI capability; no authorization of FE-U02+. Standing pendings unchanged: U3 formal adoption word; prototypes (§9 HOLD); FE-U17 uncommissioned; FE-U14/15 require own BOs; FE-U16 future-gated (F01).

## 8. LOOP STATE AT THIS RECORD

FE-U01: **IN BUILD (DA-authorized)** — fail-first stage first with red evidence; the corpus awaits `FEPACK-FEU01-001`.
