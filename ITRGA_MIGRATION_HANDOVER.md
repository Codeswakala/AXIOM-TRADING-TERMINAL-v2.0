# ITRGA MIGRATION HANDOVER — AXIOM V2 PROGRAMME STATE & EXPECTED ITRGA ACTIONS

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-ITRGA-HANDOVER-001 |
| Date | 2026-09-02 |
| Author | Development Authority (DA) — issued at Operator direction |
| Purpose | Initialize a **replacement ITRGA** into the current programme state and the exact actions pending on the ITRGA side |
| Audience | The incoming ITRGA, via the Operator |
| Authority note | This document confers **no authority** and changes **no record**. It is a DA-authored orientation aid (Level III). The incoming ITRGA must establish every fact below from the governing corpus and the archived evidence, per its own onboarding — a DA declaration is not proof |

**Standing discipline: we don't guess. We prove.**

---

## 1. First actions for the incoming ITRGA (before anything else)

1. **Read your onboarding:** `docs/governance/AXIOM_ITRGA_MASTER_ONBOARDING.md`
   (md5 `7bc6563409b3f6639f7cf017bc3b7830` per the outgoing ITRGA's own
   reaffirmation record `ITRGA-REA-V2-BE-4-001`). It defines your role,
   evidence law (Level I/II/III/IV; NOT PROVEN ≠ FALSE), the three-pass
   review order, the 12-field finding form, the closed determination
   vocabulary (§35), and the no-self-authorization rule (§37).
2. **Read the constitutional corpus in precedence order:**
   `AXIOM-V2-GOV-CHARTER-001` (APPROVED) → `V2_BACKEND_ROADMAP` (Band
   definitions; §3 delivery model) → `AXIOM V2 — PRODUCT & ARCHITECTURE
   SPECIFICATION` → `V2_ARCHITECTURE_PRINCIPLES` → the reasoning
   frameworks → the operational governance registers (all under
   `docs/governance/`).
3. **Re-establish programme state from the latest evidence, not from any
   summary** (onboarding latest-evidence rule). The two authoritative
   closure records are:
   - `ITRGA_DETERMINATION_V2_BE-3_P2_TRANS_APPLY_FINAL.md`
     (`ITRGA-DET-V2-BE-3-P2-TRANS-APPLY-FINAL-001`, 2026-08-31)
   - `ITRGA_DETERMINATION_V2_BE-4_FINAL.md`
     (`ITRGA-DET-V2-BE-4-FINAL-001`, 2026-09-02)
4. **Issue your own role-reaffirmation record** (pattern:
   `ITRGA_ROLE_PROJECT_REAFFIRMATION_V2_BE-4-001.md` /
   `ITRGA-REA-V2-BE-4-001`) so the succession itself is on the record.
5. **Adopt the standing practice commitments** of
   `ITRGA_PRACTICE_NOTE_V2_PACK_DISCIPLINE_001.md` (`ITRGA-PTN-V2-PACK-001`)
   — they bind ITRGA instrument-issuance practice (§2.1 battery floor,
   §2.2 instruction cards, same-session turnaround, up-front dependency
   disclosure, explicit supersession marking).

## 2. Governance model (unchanged by the migration)

Three authorities, strictly separated:

| Authority | Does | Never does |
|---|---|---|
| **Operator** | Issues decisions (ODs); authorizes acts; executes sanctioned console runs; owns repository custody (Git — **deferred**, frozen at a BE-1-era HEAD) | Reviews own work |
| **DA** (me) | Designs, implements, tests, produces evidence, submits Delivery Reports | Self-approves; issues determinations; touches Git; touches the working DB |
| **ITRGA** (you) | Independent review; verification; findings (12-field form); determinations (closed vocabulary); sanctioned instrument issuance (packs) | Writes production code; implements DA corrections; self-authorizes; treats DA declarations as proof |

Chain per act (roadmap §3): Operator direction → scope assessment (ITRGA)
→ Operator scope decision → DA design plan → ITRGA plan review → Operator
authorization → Build Order → DA implementation + evidence → ITRGA
source/evidence review (+ correction cycles) → ITRGA determination.

**Standing laws:** credential law (no secret/account identifier/connection
URL in any artifact; the Four Secrets never shared; scan before every
archive) · evidence law (Level I runtime/DB/file > II executed > III
document > IV assertion; missing = NOT PROVEN, never converted to a
negative finding) · no Git operations by anyone but the Operator ·
fail-atomic sanctioned instruments for any working-DB mutation · one
Operator decision per act · content-based row comparison, never
position-based (PGF-012 lesson).

## 3. Programme state at handover (2026-09-02)

### 3.1 Bands closed (all with ITRGA determinations on record)

| Band | Determination | Key state |
|---|---|---|
| BE-0 | closed (charter approved, OD-001) | Governance baseline |
| BE-1 | ITRGA-DET-V2-BE-1-001 | Audit/lineage/RBAC/mode core; 78 tests |
| BE-2 | ITRGA-DET-V2-BE-2-001 | Normalized market-data read model, W-1/W-2 writers; 45 tests |
| BE-3 P1 | ITRGA-DET-V2-BE-3-P1-FINAL-001 | Provider registry (Twelve Data reserved), fixture-only, network-denied; 33 tests |
| BE-3 P2 | ITRGA-DET-V2-BE-3-P2-FINAL-001 | Contract-test capability; run `a246607c-f0c5-42e9-8f3b-a1e1bd75fa83`; 25 tests |
| BE-3 P2 transition act | ITRGA-DET-V2-BE-3-P2-TRANS-APPLY-FINAL-001 | `architecture_candidate → contract_tested` **applied and IN FORCE** on the working DB; 17 tests |
| **BE-4** | **ITRGA-DET-V2-BE-4-FINAL-001 (2026-09-02) — APPROVED WITH OBSERVATIONS** | Market Context Engine + Chart Intelligence + research read models; 39 tests; maturity registry rows → COMPLETE |

### 3.2 Authoritative baselines (from the BE-4 final determination §8)

- **Test baseline: 789** (552 V1 + 198 V2 pre-BE-4 + 39 BE-4) — executed
  789/0/0, Python 3.13.14, pytest 8.4.2.
- **Working database** (`backend\axiom_dev.db`, Operator machine): in force
  at revision **`20260829_0042`**; byte-identity sha256
  `0483f9fe12e3d71f514811571c64589d72c66ec47fb2a3a1f6e986715ca41006`
  (1,310,720 B; last write 2026-08-31 14:09:55 +03:00); **12 v2 triggers**;
  provider `twelvedata` = `contract_tested` / `verified` /
  `persistence_permitted = 0`; history exactly 2 rows; authority variable
  UNSET; integrity ok; recovery anchor
  `axiom_dev.db.pre-0042-20260831140931.bak` (sha256 `6db478ee…`) valid.
- **Repository head:** `20260831_0043` (BE-4 migration delivered and
  hash-verified, **NOT applied** to the working DB).
- **Drift baseline:** exactly the **9 inherited V1 tokens**
  (`audit_write_failure_records` + 2 added indexes + 6 removed indexes),
  plus — until the 0043 act completes — the expected BE-4 schema set.
- **Migration chain hashes (all VERIFIED, Level I/II on record):**
  0038 `6e071157…f588` · 0039 `bc11cae2…5b19` · 0040 `1332ebf5…` ·
  0041 `d775c34a…dadd` · 0042 `af77a63f…c7d4` · 0043 `ab905762…a84b`.
- **Operator environment (recorded):** alembic **1.19.0** (summary-format
  `alembic check` — PGF-014 lesson: format-independent assertions only);
  PowerShell 5.1 console; SQLite 3.50.4.
- **Findings register: PGF-001…PGF-014 — ALL CLOSED.** Zero open
  instrument defects.
- **Mode scope:** RESEARCH/SIMULATION only. Execution default-deny. FE
  bands blocked (sequencing directive `AXIOM-V2-OD-BE-3-P2-003` §3).

### 3.3 The ONE open observation

**OBS-9** (BE-4 final determination §6): the Operator's one-line accounting
of the 2026-09-01 17:26 +03:00 repository bulk-write event (all 43
migration files re-written in a 3-second window; working DB proven
unaffected — byte-identical in every run since). **Administrative
closure only**; awaiting the Operator's statement. Record it when given.

## 4. THE ACTIVE ACT — 0043 working-DB application (your immediate work)

**This is where the incoming ITRGA picks up mid-chain.** Everything before
instrument issuance is DONE:

| Stage | Instrument | Status |
|---|---|---|
| Operator authorization | `AXIOM-V2-OD-BE-4-009` (verbatim "authorized"; scope = ITRGA's exactly-one-next-action) | **DONE** |
| Scope assessment | `ITRGA-ASS-V2-0043-APPLY-001` — incl. the 0038/0039/0041 re-pin precondition **RESOLVED** (Level II recomputation, 7/7 extraction validation) | **DONE** |
| Instrument-design plan | `ITRGA-PLAN-V2-0043-APPLY-001` — apply pack boundaries A0–A8; verify pack B1–B9; battery spec | **DONE** |
| Build Order | `BO-V2-0043-APPLY-001` — terminal-state contract T-1…T-11 | **ISSUED** |
| **Pack battery + issuance** | apply pack + verify pack | **← YOUR NEXT ACTION (§4.1)** |
| Operator console runs | 2 runs (apply, then verify) | awaits packs |
| Act-closure determination | `ITRGA-DET-V2-0043-APPLY-001` | awaits runs |

### 4.1 Expected ITRGA action 1 — build, battery-test, and issue the two packs

Per `ITRGA-PLAN-V2-0043-APPLY-001` and BO §8 (no execution before
issuance). Requirements distilled:

- **Apply pack** (`ITRGA-V2-0043-APPLY-PACK-V1` suggested ID): PowerShell
  5.1-compatible, pure ASCII, PGF-009 `${}` bracing discipline, UTF-8 +
  `PYTHONIOENCODING`, fail-atomic (verdict only at end), MD5 self-check
  step, embedded five-line Operator instruction card. Boundaries:
  A0 self-ID → A1 baseline byte-identity (`0483f9fe…`; **abort on any
  difference**; abort if `alembic current` ≠ exactly `20260829_0042`) →
  A2 pre-mutation anchor (`axiom_dev.db.pre-0043-<ts>.bak`, integrity ok;
  **mutation may not precede a valid anchor**) → A3 runtime hash re-pins
  (0043 `ab905762…`, 0038/0039/0041 per §3.2; abort on mismatch) →
  A4 exactly one `alembic upgrade 20260831_0043` (never "head") →
  A5 post-state (head 0043; **18 triggers**; 3 tables; constraints/indexes;
  5 permission + 3 computation-version seeds) → A6 six guard refusals with
  the exact R-2 messages → A7 drift re-baseline, **format-independent**
  (9 inherited tokens; no `v2_*` token) → A8 verdict + cleanup.
- **Verify pack** (read-only): B1–B9 re-proof of the terminal state,
  pinned to the apply pack's recorded final file values.
- **Battery before issuance** (PTN-V2-PACK-001 §2.1 floor): `${}` span
  audit; full AST parse (pwsh 7.x); the five-case dry-run matrix W1/W2
  (itemized + summary alembic formats — W2 must replicate the recorded
  operator environment, alembic 1.19.0 class) and N1–N4 negative aborts
  (baseline altered / 0043 hash altered / already-at-0043 / anchor
  integrity fail — each proving **no mutation**); verify-pack dry run
  against the W2 post-apply state; MD5/SHA-256 of issued bytes recorded;
  superseded instruments (verify V1/V2/V3) marked **"do not execute for
  this act"**.

### 4.2 Expected ITRGA action 2 — verify the two console transcripts

The Operator returns one transcript per run. Verify against the T-1…T-11
contract; credential-scan before archiving; content-based comparisons.

### 4.3 Expected ITRGA action 3 — act-closure determination

`ITRGA-DET-V2-0043-APPLY-001`: working DB at head `20260831_0043`; 18 v2
triggers in force; drift re-baselined to exactly the 9 inherited tokens;
report tables empty; residual B-1 of the BE-4 final determination closed.

## 5. Expected ITRGA actions after the 0043 act (each gated on a NEW Operator decision)

Per BE-4 final determination §7 — none may be self-initiated:

| # | Next act (Operator's choice) | Your role when directed |
|---|---|---|
| 1 | **BE-5** — Predictive ML, Signal, Research Governance Expansion (roadmap next) | Scope assessment → (OD) → request DA design plan with pre-registered guardrails → plan review → Build Order → delivery review → determination (the BE-4 chain is the template) |
| 2 | FE band unblock (browser-evidence residual of SD-2 = A lands at the FE/X-01 joint gate) | Same chain pattern; sequencing directive must be explicitly lifted by the Operator first |
| 3 | `integrated` provider-ladder step | New separate chain; the transition authority string `BO-V2-BE-3-P2-TRANS-001` was **consumed** — a new one is required |
| 4 | Persistence permission (Twelve Data payloads) | Separate governed act; `persistence_permitted` is `false` and guarded |
| 5 | Real-data research validation (SD-1 = A residual) | Separate later-governed act |
| 6 | Inherited V1 drift reconciliation (the 9 tokens) | Separate act; until then the 9-token set is the ONLY acceptable `alembic check` drift |
| 7 | Git custody publication | Operator-only; deferred since the BE-1 era; you review nothing until directed |
| 8 | Backup-anchor retention/disposal | Operator discretion; retention recommended pending the 0043 act |

## 6. Institutional lessons the incoming ITRGA inherits (do not relearn these)

- **PGF-009:** PowerShell 5.1 — `${}` bracing only for plain identifier names.
- **PGF-011:** every issued pack carries an MD5 self-check step.
- **PGF-012:** never position-based row assertions — content-based always
  (uuid4 TEXT PKs make ordering undefined).
- **PGF-014:** never format-dependent `alembic check` parsing — assert
  exit code + "not up to date"; itemize only when the format provides it.
- **REM-001 (DA-side but you enforce it):** source transcripts carry
  literal contents of EVERY changed file, regardless of change class.
- **DEL-004:** migration seeds are revision-local literal rows, never
  imports from live modules.
- **OBS-5 pattern:** DA test harnesses may set the consumed transition
  authority variable for **dedicated test databases only** — accepted;
  the governed record is untouched.
- **Instruction cards + explicit supersession** eliminate console
  file-selection slips (the run-4 class).
- **Credential classification:** test-fixture placeholders
  (`admin/admin123`, JWT dev-markers, fixture passwords) confined to test
  databases are CLEAN-with-classification — the established standard.

## 7. Where everything lives

| Artifact class | Location |
|---|---|
| Constitutional + governance corpus, registers, ODs, BOs, ITRGA records | `docs/governance/` |
| Approved design plans | `docs/plans/` |
| Evidence (source transcripts, API/test-run transcripts, CARs, runbooks) | `docs/evidence/` |
| Delivery Reports | repository root (`DELIVERY_REPORT_V2_*.md`) |
| Programme state (DA-maintained; v22.0.0 at handover) | `V2_CURRENT_STATE.md` |
| Operator-machine evidence (apply/verify transcripts, anchors) | `operator-evidence\` (Operator machine) |
| Backend source + migrations + tests | `backend/` |

## 8. Handover integrity statement (DA)

This document was prepared by the DA from the archived record. Every
factual claim above traces to a named determination, review, decision, or
hash on the record; nothing herein is new authority. Where the incoming
ITRGA's own verification differs from this document, **the record and your
verification prevail — not this document.** The DA's own state file
(`V2_CURRENT_STATE.md`) remains Level III to you, per custody independence.

**We don't guess. We prove.**

**End of AXIOM-V2-ITRGA-HANDOVER-001**
