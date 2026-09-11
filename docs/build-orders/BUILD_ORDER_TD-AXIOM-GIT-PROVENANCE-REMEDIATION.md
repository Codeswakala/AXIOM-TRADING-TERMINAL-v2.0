# BUILD ORDER — TD-AXIOM-GIT-PROVENANCE REMEDIATION

**Permanent Governance Baseline & Repository Provenance Correction**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation — governance-integrity track |
| Unit | **TD-AXIOM-GIT-PROVENANCE-REMEDIATION** |
| Predecessor | `ITRGA_REVIEW_UI-007-P06_FINAL_AND_UI-007_COMPLETION.md` — 🏛️ UI-007 COMPLETE |
| Operator directive | Execute before UI-007-P07; UI-008 gated behind both governance-integrity items |
| Governing docs | Doc 11 §5 (Deployment) / §8 (Operational Readiness), `03_AXIOM_SPEC` (Technical Debt Policy, Security Standards), `05_SYSTEM_ARCHITECTURE` §77, `10_CONSTITUTIONAL_HIERARCHY` Tier 7 |
| Baseline of record | **v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 61f / 276t** |
| Governance Gate | **CLOSED** (must remain closed) |
| Production | **NOT CERTIFIED** (unchanged — this unit does not certify) |

**Motto: "We don't guess. We prove."**

---

## 1. Purpose

Close **`TD-AXIOM-GIT-PROVENANCE`** — the standing HIGH pre-certification blocker.

**The deficiency, stated precisely:**

- The implementation repository contains **exactly one commit** (`22c735a`, "AXIOM TRADING PLATFORM v1.0") for a platform spanning Waves 0–7 and seven completed UI workstreams.
- Everything from Wave 0 through UI-007 exists as **uncommitted working-tree state**.
- That single committed baseline contained **56 unresolved merge-conflict blocks across 25 tracked files**, including Tier-3 `04_PROJECT_ROADMAP.md` and three Tier-7 registers. **A conflicted tree was the committed state of record.**

**Consequences already realised, twice each:**
- Phase-isolating diffs proved structurally impossible (UI-002-P05, UI-007-P04).
- Conflict residue surfaced *inside* phase reviews (UI-007-P04 §6, UI-007-P05 CA-P05-4).
- No approved-baseline anchor exists for any verdict in the ledger.
- Months of delivered work sit unprotected against a single accidental loss.

Under **Doc 11 §5/§8**, a platform with no commit history and no reproducible baseline is **not certifiable**, however green its tests.

---

## 2. Scope

### IN scope
1. **Establish an anchored, tagged baseline commit** representing the approved v0.62.0 state.
2. **Retrospective phase tags** for completed workstreams, to the extent the single-commit history permits (see §4).
3. **Conflict-marker prevention** — verified absence at commit time, plus a guard against recurrence.
4. **`.gitignore` hygiene** so evidence artifacts and local secrets are never committed.
5. Registers/docs reconciliation recording the closure.

### OUT of scope — do NOT do
- **Any product source change.** No feature, fix, refactor, dependency, migration, schema, route, or test change. **This unit changes repository metadata only.**
- Rewriting or fabricating history — no invented per-phase commits, no back-dated authorship, no synthetic Wave-0…Wave-7 reconstruction. **A fabricated history is worse than no history.**
- Force-pushing over, deleting, or amending the existing `22c735a` commit.
- Any Gate / certification / execution / production posture change.

---

## 3. 🔴 CRITICAL PRE-CONDITION — credential scrub before ANY commit

**This is the highest-risk step in the unit and it is non-negotiable. Git history is permanent; a committed secret is not undone by a later deletion.**

I verified against the evidence corpus: **operator transcripts and Build Orders across UI-004, UI-005 and later phases contain live dev credentials in plaintext**, including:

```
PGPASSWORD = "<REDACTED_DEV_PASSWORD>"
AXIOM_JWT_SECRET_KEY = "<REDACTED_JWT_SECRET>"
AXIOM_BOOTSTRAP_ADMIN_PASSWORD = "<REDACTED_DEV_PASSWORD>"
```

Committing `docs/evidence/**` or any transcript containing these into a permanent baseline would **embed development credentials into immutable history** — a direct §77 violation and a Doc 11 §2 (Secret & Credential Management) certification failure. It would convert a provenance fix into a security defect.

**Mandatory before the baseline commit:**

- **(P-1)** Add `docs/evidence/**`, `**/OPERATOR_RESULTS*.md`, `**/*_OPERATOR_RESULTS*.md`, `**/UI-*_RAW_*.json`, and `scripts/*_evidence*.ps1` output paths to `.gitignore`. Evidence artifacts are **review inputs, not source of record**.
- **(P-2)** Run a credential scan across **everything staged for commit**:
  ```
  PGPASSWORD|JWT_SECRET|SECRET_KEY|BOOTSTRAP_ADMIN_PASSWORD|admin123|axiom_dev_password|
  postgresql(\+asyncpg)?://[^ ]*:[^ @]*@|Bearer [A-Za-z0-9._-]{20,}|access_token|refresh_token
  ```
  Print the command and its output. **Required result: `STAGED_SECRET_MARKER_COUNT: 0`.** A non-zero count **halts the unit** — unstage, remediate, re-scan.
- **(P-3)** If any Build Order or governance document already tracked in the repo contains a credential literal, **redact it to a placeholder** (e.g. `<REDACTED_DEV_PASSWORD>`) before committing, and list every file redacted. Governance documents are permanent records; they must not carry secrets forward.

**No commit is authorized until P-1, P-2 and P-3 are evidenced.**

---

## 4. Required work

- **(W-1) Verify tree cleanliness.** Tree-wide conflict-marker scan (`<<<<<<<`, `=======`, `>>>>>>>`) → **must be empty**. Print command and output. Also run `git diff --check`.
- **(W-2) Stage deliberately.** Stage product source, tests, governance docs, Build Orders, delivery reports and ITRGA determinations. **Exclude** evidence artifacts per P-1. Show `git status --short` before commit.
- **(W-3) Baseline commit.** One commit on the existing branch, on top of `22c735a`. Message must state the platform of record:
  ```
  AXIOM v0.62.0 — governance baseline
  Alembic head 20260717_0037 · backend 414 · frontend 61f/276t
  Waves 0–7 CLOSED · UI-001…UI-007 COMPLETE · Gate CLOSED · Production NOT CERTIFIED
  Establishes the first anchored baseline (TD-AXIOM-GIT-PROVENANCE).
  ```
- **(W-4) Annotated tag** `AXIOM_v0.62.0_BASELINE` on that commit. Verify with `git rev-parse --verify AXIOM_v0.62.0_BASELINE` and `git tag -n99`.
- **(W-5) Retrospective workstream tags — honest form only.** Because per-phase history does not exist, **do not fabricate it.** Point completion tags at the single baseline commit and say so in each annotation, e.g.:
  ```
  git tag -a UI-007_COMPLETE -m "UI-007 complete at v0.62.0. NOTE: retrospective marker —
  no per-phase commit history existed prior to the baseline; this tag points at the
  v0.62.0 baseline commit, not at the historical completion point."
  ```
  Apply for `UI-001_COMPLETE` … `UI-007_COMPLETE`. **The annotation disclaimer is mandatory** — a tag implying history that never existed is a falsified record.
- **(W-6) Recurrence guard.** Add a pre-commit hook (or documented CI step) that fails on conflict markers **and** on the P-2 credential pattern. Demonstrate it: attempt a commit containing a marker, show the rejection, then show a clean commit succeeding.
- **(W-7) Forward protocol.** Document in `docs/governance/` that **every future ITRGA-approved phase is committed and tagged at approval**, so phase-isolating diffs become possible from here forward. This is what actually retires the debt.
- **(W-8) Registers.** Update `TECHNICAL_DEBT_REGISTER` (TD-AXIOM-GIT-PROVENANCE → Closed, with the baseline SHA), `GOVERNANCE_AMENDMENTS` (new GA entry recording the baseline and forward protocol), `PROJECT_STATE`, `CHANGELOG`.

---

## 5. Mandatory evidence checklist (Level-I, operator-run on target)

Use the **v2.0.0 runner pattern** — per-gate exit-code sentinels, terminal summary, guarded blocks. Emit **UTF-8 no-BOM** (OBS-P06-4) and fix the row-counter defect (OBS-P06-3).

- **(a) Build identity** — pack is OF this unit. *(Verify before sending: `Select-String -Path OPERATOR_RESULTS.md -Pattern 'TD_AXIOM_GIT_PROVENANCE'` returns hits.)*
- **(b) 🔴 P-1 `.gitignore` diff displayed.**
- **(c) 🔴🔴 P-2 `STAGED_SECRET_MARKER_COUNT: 0`** — command + output. **Non-zero halts the unit.**
- **(d) 🔴 P-3 redaction list** (or an evidenced statement that no tracked file required redaction).
- **(e) 🔴 W-1 conflict-marker scan empty** + `git diff --check` clean.
- **(f) W-2 `git status --short`** before commit.
- **(g) 🔴 W-3/W-4** — `git log --oneline -3`, new commit SHA printed, `git rev-parse --verify AXIOM_v0.62.0_BASELINE` succeeds, `git tag -n99` shows annotations.
- **(h) 🔴 W-5** — all seven `UI-00n_COMPLETE` tags listed **with the retrospective disclaimer visible** in the annotation output.
- **(i) 🔴 Phase-isolating diff now WORKS** — the capability this unit exists to restore:
  ```
  git diff --stat AXIOM_v0.62.0_BASELINE..HEAD
  ```
  must **succeed** (no `fatal:`) and return empty at baseline. Guard on `$LASTEXITCODE` so a git error **fails loudly** — the UI-002-P05 false-clean lesson.
- **(j) 🔴 W-6 hook demonstration** — rejection shown, then clean commit shown.
- **(k) 🔴 NO PRODUCT CHANGE** — `git show --stat <baseline SHA>` limited to expected paths; **`alembic current` = `20260717_0037`**; manifests unchanged; **no source file modified by this unit** (the commit records existing state, it does not alter it).
- **(l) Regression unchanged** — frontend **≥61f/276t** gated exit 0; backend **≥414**; `LOCAL_CI_EXIT_CODE: 0` or a named tracked flake after gates green.
- **(m) W-7/W-8** — forward-protocol doc + four register diffs displayed.
- **(n) Gate posture** — Gate CLOSED and Production NOT CERTIFIED unchanged; no governance-mutation control introduced.

**No browser evidence required** — this unit has no UI surface.

---

## 6. Determination rule

**Any staged secret (`STAGED_SECRET_MARKER_COUNT > 0`)**, any conflict marker committed, any fabricated or undisclosed retrospective tag, any product-source change, a failing or false-clean phase-diff verification, a history rewrite/force-push, any Gate or certification posture change, a report-only or halted transcript, or any unmet mandatory item ⇒ **Corrective Actions Required / Rejected**.

Only **Approved** or **Approved with Observations** closes `TD-AXIOM-GIT-PROVENANCE` and authorizes **`BUILD_ORDER_UI-007-P07-AUDIT-REACHABILITY`**.

---

## 7. What closure means — and does not

**Closes:** the absence of an anchored baseline; the inability to run phase-isolating diffs; the risk of conflict residue re-entering; the exposure of months of work to a single loss.

**Does not close:** the *historical* gap. Waves 0–7 and UI-001…UI-006 will never have real per-phase commits, and the retrospective tags must say so. **This unit makes provenance correct from v0.62.0 forward; it cannot manufacture a past that was not recorded.** ITRGA will state that limitation plainly in the closure determination, and Doc 11 certification will assess the platform on that honest footing.

**DA does not self-approve. Governance Gate remains CLOSED. Production remains NOT CERTIFIED.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
