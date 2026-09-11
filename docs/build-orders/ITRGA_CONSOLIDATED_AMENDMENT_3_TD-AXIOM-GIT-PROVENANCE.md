# ITRGA CONSOLIDATED AMENDMENT 3 — TD-AXIOM-GIT-PROVENANCE-REMEDIATION

**Self-audit, defect correction, and single consolidated execution order**

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Unit | `TD-AXIOM-GIT-PROVENANCE-REMEDIATION` |
| Supersedes | Build Order §3/§4/§5 · Amendment 1 · Amendment 2 — **consolidated here; this is now the single execution reference** |
| Trigger | Operator quality directive + ITRGA self-audit performed in response |
| **Status** | **EXECUTE — no further clarification expected** |
| Governance Gate | CLOSED · Production NOT CERTIFIED |

**Motto: "We don't guess. We prove."**

---

## 1. Accountability

The operator is right. Four instrument defects in one unit is too many:

| # | Defect | Cost |
|---|---|---|
| ITRGA-ERR-1 | C-2 baseline-diff demanded against a ref that could not exist | 1 cycle |
| ITRGA-ERR-2 | `category=SECURITY&limit=200` authorized without checking partition size | 1 cycle |
| ITRGA-ERR-3 | P-2 pattern matched identifiers, not values — unpassable gate | 1 cycle |
| ITRGA-ERR-4 | D-5 demo literal self-matched Class A | 1 cycle |

**The common root cause: I specified controls without executing them against the actual corpus first.** Each was individually defensible; together they are a pattern, and the pattern is mine.

**Standing correction to my own method, effective now:** *no control ships until I have run it against real project data and shown the result.* I applied that to the Amendment 1 scanner (9/9 validated before authorizing) and it held — that ruling has produced no further defect. I am now applying it retroactively to the whole order.

---

## 2. Self-audit findings — two further defects, found before the DA hit them

I stress-tested my own outstanding order rather than waiting for a fifth halt.

### 🔴 ITRGA-ERR-5 — §5(k) is self-contradictory

§5(k) requires *"no source file modified by this unit (the commit records existing state, it does not alter it)."*

But the same order mandates: `.gitignore` edits (P-1), redaction of ~37 documents (P-3), a new pre-commit hook (W-6), a forward-protocol doc (W-7), four register updates (W-8), and an exception manifest (Amd 2). **The commit demonstrably alters files.** As written, §5(k) is unsatisfiable — a fifth halt waiting to happen.

**Corrected — §5(k) is replaced by an explicit permitted-change allowlist:**

| Permitted to change | Forbidden to change |
|---|---|
| `.gitignore` | Any `backend/app/**` or `frontend/src/**` **product source** |
| Governance/Build-Order/report **redactions** (value→placeholder only) | Any test file |
| `.githooks/**` or `scripts/hooks/**` (new) | Any dependency manifest (`package.json`, `pyproject.toml`, lockfiles) |
| `docs/governance/**` (registers, forward protocol, exception manifest) | Any migration, schema, or route |
| `PROJECT_STATE.md`, `CHANGELOG.md` | Any Gate/certification/execution posture |

**Verification:** `git show --stat <baseline SHA>` must show **zero** files from the forbidden column. That is the real, checkable control.

### 🟠 ITRGA-ERR-6 — P-3 and D-3 overlap

D-3 de-indexes 570 `docs/evidence/**` files. The DA prepared redaction across 37 files. **Any of those 37 inside `docs/evidence/**` will leave the index entirely — redacting them is wasted work.**

**Corrected — strict ordering:** perform **D-3 index removal FIRST**, then re-scan, then redact only what remains tracked. Report both numbers (`REDACTION_CANDIDATES_BEFORE_DEINDEX` / `_AFTER_DEINDEX`) so the reduction is visible.

### 🟡 W-5 simplified — seven retrospective tags reduced to one

Seven tags all pointing at the same commit, each needing a disclaimer that it points at the wrong place, is low value and seven more chances to err.

**Corrected:** create **one** annotated tag `AXIOM_v0.62.0_BASELINE` whose annotation records the completed workstreams:

```
AXIOM v0.62.0 — first anchored governance baseline.
Alembic 20260717_0037 · backend 414 · frontend 61f/276t
Waves 0-7 CLOSED · UI-001…UI-007 COMPLETE · Gate CLOSED · Production NOT CERTIFIED
NOTE: no per-phase commit history existed before this baseline. This tag marks the
state at UI-007 completion, not the historical completion point of any earlier phase.
Per-phase tagging begins with the next ITRGA-approved unit.
```

Same honesty, one artifact, six fewer failure points.

---

## 3. THE CONSOLIDATED EXECUTION ORDER — do exactly this, in this order

Everything supersedes prior text. Use the v2.0.0 runner: per-gate sentinels, terminal summary, **UTF-8 no-BOM**, fixed row counter.

| Step | Action | Sentinel |
|---|---|---|
| **1** | `.gitignore` — add `docs/evidence/**`, `**/OPERATOR_RESULTS*.md`, `**/*_RAW_*.json`, `*.db` | show diff |
| **2** | **D-3 first:** `git rm --cached` the 570 evidence files + tracked `*.db`. Local files preserved (prove with `Test-Path` on a sample) | `DEINDEXED_PATH_COUNT: <n>` |
| **3** | Conflict-marker scan tree-wide + `git diff --check` | must be empty |
| **4** | Re-scan for redaction candidates **after** de-index | `REDACTION_CANDIDATES_BEFORE_DEINDEX` / `_AFTER_DEINDEX` |
| **5** | Redact remaining tracked governance/BO/report **values** → `<REDACTED_DEV_PASSWORD>` etc. Filename-only manifest | `REDACTED_FILE_COUNT: <n>` |
| **6** | Write `docs/governance/TD-AXIOM-GIT-PROVENANCE_D2_EXCEPTION_MANIFEST.md` — path·line·class·identifier·`value_sha256_first12`·justification·disposition. **No plaintext values** | manifest displayed |
| **7** | Stage per the §2 allowlist. `git status --short` | displayed |
| **8** | Run the Amendment-1 three-class scanner. Print **all four counters** and the reconciliation | `STAGED_SECRET_MARKER_COUNT: 0` · `D2_PERMITTED_EXCEPTION_COUNT: 2` · `D5_SYNTHETIC_DEMO_EXCEPTION_COUNT: 0` · `TOTAL_CLASS_MATCH_COUNT: 2` · sum must reconcile |
| **9** | Baseline commit on top of `22c735a`. No rewrite, no force-push | new SHA printed |
| **10** | **One** annotated tag `AXIOM_v0.62.0_BASELINE` per §2 | `git rev-parse --verify` + `git tag -n99` |
| **11** | Install hook (conflict markers + three-class scanner + `path+identifier+hash` exception match). Demo with a **runtime-generated** value; delete scratch; prove deletion | rejection shown, then clean commit |
| **12** | `git diff --stat AXIOM_v0.62.0_BASELINE..HEAD` — **must succeed**, guard on `$LASTEXITCODE` so a git error fails loudly | empty result at baseline |
| **13** | Forward protocol doc + 4 registers (TD register: `TD-AXIOM-GIT-PROVENANCE` → **Closed**, with baseline SHA) | diffs displayed |
| **14** | `git show --stat <SHA>` — **zero** forbidden-column files | verified |
| **15** | Regression: frontend ≥61f/276t exit 0 · backend ≥414 · `alembic current 20260717_0037` · CI | sentinels |

**No browser evidence required.** No product source change. Gate and certification posture untouched.

---

## 4. Determination rule (final)

**Halt/Corrective on:** `STAGED_SECRET_MARKER_COUNT > 0` · counters that do not reconcile · any forbidden-column file in the commit · a conflict marker committed · a history rewrite or force-push · a plaintext value printed anywhere · a false-clean (sentinel printed off a failed command) · any unmet step above.

**Approved / Approved with Observations** closes `TD-AXIOM-GIT-PROVENANCE` and authorizes `BUILD_ORDER_UI-007-P07-AUDIT-REACHABILITY`.

---

## 5. On the deadline — a direct answer

The operator is right that errors cost cycles. But I want to be precise about the trade, because the wrong lesson here would be expensive.

**What actually cost time:** four defective instruments of mine — all now corrected, with a method change to prevent recurrence, and two more caught by self-audit in this document before they cost anything.

**What did not cost time:** rigour. Every DA halt was correct and cheap — a request, a ruling, no rework. Compare the alternative: had the DA guessed at P-2, it would have narrowed the pattern until it hit zero, and **development credentials would now be in permanent, immutable git history.** That is not a cycle lost; that is a Doc 11 §2 certification failure discovered at the certification gate, with no clean remedy because git history cannot be selectively unwritten.

The same logic covers the UI-007 phases: five submissions produced a workspace that provably cannot mutate governance — and surfaced that **every constitutional refusal in the system is invisible to operators**. Approving quickly would have shipped that defect into a "complete" workstream.

**Where I can genuinely accelerate, and will:**
- Validating controls against real data before issuing them (already in force since Amendment 1).
- Consolidating amendments into one execution reference — as done here — rather than layering rulings.
- Auditing my own orders for contradictions proactively, as in §2.
- Batching decisions: this document answers questions the DA has not yet had to ask.

**Where I will not accelerate:** the evidence bar itself. A deadline met with an uncertified platform, credentials in history, or an invisible audit trail is not a deadline met.

**Remaining to UI-008:** this unit, then UI-007-P07 (audit reachability), then the UI-008 design plan. Both governance items are small and now fully specified.

---

## 6. Findings

| ID | Severity | Status |
|---|---|---|
| **ITRGA-ERR-5** | RECORDED (R19) | §5(k) self-contradictory — corrected to an explicit permitted-change allowlist |
| **ITRGA-ERR-6** | RECORDED (R19) | P-3/D-3 overlap — corrected to strict ordering |
| ITRGA-ERR-1…4 | RECORDED | Previously corrected |
| **METHOD CHANGE** | STANDING | No ITRGA control ships without prior validation against real project data |
| TD-AXIOM-DEV-CREDENTIAL-LITERALS | MEDIUM | Open — pre-certification |
| TD-AXIOM-GIT-PROVENANCE | HIGH | Open — this unit closes it |

---

## 7. Disposition

**Amendment 3 issued as the single consolidated execution order. Execute §3 steps 1–15.**

Six ITRGA errors are recorded against this programme — four found by the DA, two by my own audit. All are corrected, and the method that produced them is changed. The DA has not made a substantive error in this unit; it has halted correctly four times and each halt prevented a worse outcome than the delay it caused.

Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**.

---

*An authority that cannot audit itself has no standing to audit anyone else. Six errors found, six corrected, two of them before they cost a cycle.*

**We don't guess. We prove.**

*— AXIOM ITRGA*
