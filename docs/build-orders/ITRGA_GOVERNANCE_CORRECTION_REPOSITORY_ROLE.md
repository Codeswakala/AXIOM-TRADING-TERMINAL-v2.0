# ITRGA GOVERNANCE CORRECTION — REPOSITORY ROLE & EVIDENCE STANDARD

**Issuing authority:** Independent Technical Review & Governance Authority
**Date:** 2026-08-16
**Trigger:** Operator clarification, 2026-08-16
**Status:** Binding. Supersedes the landing condition asserted in `ITRGA_DETERMINATION_UI-CONV-P03_PHASE.md` §6 and every prior determination that made origin state a precondition of phase closure.

---

## 1. THE OPERATOR'S CLARIFICATION — RECORDED VERBATIM IN SUBSTANCE

1. The repository is **storage and migration infrastructure**, not the build surface. Its purpose is to hold project files and folders, and to carry both authorities into a new chat session when migration is required.
2. **Neither the DA nor ITRGA has authority to commit, push, or pull.** That role belongs to the Operator alone.
3. This separation is **deliberate and defensive**: it prevents corrupted files reaching the repository. The Operator has already experienced that failure, and it caused the CR1–CR4 corrective build phase.
4. **No commits, pushes, or pulls are to follow a Build Order.** Repository activity is Operator-timed.
5. **No governing document assigns GitHub activity to ITRGA or the DA.**

---

## 2. ITRGA ERROR — ACKNOWLEDGED

Point 5 is dispositive and I did not verify it before acting on the opposite assumption.

**What I did wrong:**

| Error | Correction |
|---|---|
| Treated origin state as a **precondition of phase closure** — "APPROVED IN SUBSTANCE — NOT LANDED" | No governing document makes repository state an acceptance criterion. **Withdrawn.** |
| Raised `OBS-CONV3-8` as a **finding** against work existing outside the repository | The condition it describes is the **designed operating model**, not a defect. **Withdrawn — see §4.** |
| Recorded `OBS-CERT-2` and `CA-CONV2-3` as obligations dischargeable by the DA | The DA never held push authority — not merely lacking a credential, but **barred by role**. `OBS-CERT-2` was already re-attributed; `CA-CONV2-3` is now corrected on the same basis. |
| **Recommended issuing the DA a repo-scoped PAT**, repeatedly and with emphasis, across seven cycles | This recommended granting the DA an authority the governance model **withholds by design**, for a reason the Operator had already learned the hard way. **Withdrawn in full.** |
| Wrote `OPERATOR_DIRECTIVE_TRANSPORT_RESOLUTION.md` prescribing PAT creation, branch-push permissions and branch protection | **Superseded in full by this document.** Do not action it. |

The PAT recommendation is the substantive error. I invented a requirement — precisely what §14 of my own role prohibits — and pressed it as the "highest-leverage open decision" when the correct finding was that **transport must work without repository access**, which the inline-patch protocol already achieves.

I also framed a workspace inconvenience as a programme risk. `/tmp` being cleared mid-review was **my** environment problem, solved by holding the patches durably. It was never a governance defect.

---

## 3. CORRECTED EVIDENCE STANDARD

**The artifact of record is the verified patch, not the commit.**

What ITRGA certifies, and how:

| Certifiable | Method |
|---|---|
| The patch is authentic and unaltered | sha256 reconciliation against the DA's declared hash |
| The patch applies to a stated base | `git apply --check` exit 0 on a pristine clone |
| The resulting source satisfies the Build Order | String-level verification of the applied tree |
| The suites pass | Raw console transcripts, corroborated by build-hash reproducibility |
| The UI behaves as claimed | Level-I captures with reconciled hashes; interaction traces for click-dependent surfaces |

**Not certifiable by ITRGA, and no longer asserted as a gap:** whether the Operator has committed the work. That is Operator-timed activity outside both authorities' remit, and reviewing it was outside mine.

This standard is not weaker. Every item of UI-CONV-P03 was verified by applying the patch to a pristine clone and reading the resulting source — **not** by trusting a commit. A commit would have proven the bytes arrived; it would not have proven a single acceptance criterion.

---

## 4. FINDINGS AMENDED

| ID | Prior state | Corrected state |
|---|---|---|
| `OBS-CONV3-8` | Open — "verified work outside the repository", binding on phase closure | **WITHDRAWN.** Describes the designed operating model. Not a defect. |
| `CA-CONV2-3` | Open — structural transport blocker; PAT recommended | **AMENDED and CLOSED as a governance finding.** The DA holds no repository authority by design. The residual concern — transmission — is resolved: the inline-patch protocol produced four consecutive hash-reconciled deliveries. Retained only as the **standing transport protocol** in §6. |
| `OBS-CERT-2` | Re-attributed to ITRGA as misassigned | **Confirmed withdrawn.** Correctly diagnosed earlier; now correctly grounded — role, not credential. |
| `OBS-PROV-2` | Open — `docs/evidence/` absent at origin | **AMENDED.** Evidence delivery to ITRGA is discharged by inline transmission. Whether evidence is archived in the repository is an **Operator storage decision**, not a DA obligation. Reclassified from finding to Operator note. |

**Unaffected and still open:** `OBS-5` (bundle, POLISH-P01) · `OBS-CONV2-5` (seeded evidence fixtures → deviation register) · `F-BRAND-1` (GA-173, Operator).

---

## 5. UI-CONV-P03 — CORRECTED PHASE DETERMINATION

The withheld condition was invalid. Applying the corrected standard to evidence already verified:

# UI-CONV-P03 — APPROVED WITH OBSERVATIONS

All six items verified against `34f4c62` + the four-patch chain:

| Item | Surface | State |
|---|---|---|
| 1 | Portfolio Research → PORTFOLIO dock | APPROVED WITH OBSERVATIONS |
| 2 | Scenario Comparison → SCENARIOS dock | APPROVED WITH OBSERVATIONS |
| 3 | Workspace Customization → settings overlay | APPROVED WITH OBSERVATIONS |
| 5 | Governance Evidence → governance overlay | APPROVED WITH OBSERVATIONS |
| 6 | Signal Investigation → drill-down extension | APPROVED WITH OBSERVATIONS |
| 4 | Research Management → `?view=research` stage | APPROVED WITH OBSERVATIONS |

**Verified end state:** 1,190 tests green (775 frontend / 415 backend) · `tsc -b` exit 0 · production build succeeds · 16/16 RBAC wrappers · all four P02 closures intact · six absorbed pages deleted, exactly one implementation each · every legacy route redirects, none 404 · interactivity hit-tested in real Chromium.

# CONV PROGRAMME — COMPLETE

| Phase | State |
|---|---|
| UI-CONV-P01 unified shell | APPROVED WITH OBSERVATIONS |
| UI-CONV-P02 absorb duplicates | APPROVED WITH OBSERVATIONS |
| UI-CONV-P03 re-home the remainder | **APPROVED WITH OBSERVATIONS** |

Sixteen routes converge into one terminal: five bottom-dock tabs, three right-dock views, two overlays, two stage views, one signal drill-down. **The turn-56 reframe held throughout — no capability was removed or re-scoped.**

Observations carried forward are `OBS-5`, `OBS-CONV2-5`, `F-BRAND-1`. None blocks programme closure.

---

## 6. STANDING TRANSPORT PROTOCOL

Retained as the working method, now grounded correctly — not as a workaround for missing credentials, but as the **correct mechanism given that neither authority touches the repository**.

**DA → ITRGA:**
- Patch **inline in the message body**. `git diff <base>` is the accepted form; `format-patch` requires commits, which the DA does not make.
- **State the base explicitly**, including any prior patches in the chain.
- LF endings, terminating newline, `git apply --check` exit code reported, sha256 declared.
- Raw console transcripts — not summary tables.
- Captures as a single self-contained HTML with base64-embedded PNGs, no external `src`.
- Interaction traces for any click-dependent surface. jsdom cannot hit-test.

**ITRGA:** verify by applying to a pristine clone. Never approve on assertion.

**Operator:** commits, pushes, pulls and repository timing — sole authority, no ITRGA precondition attached.

**Artifacts of record for UI-CONV-P03**, held in `/home/user/uploads/`, chain re-verified clean against `34f4c62` on 2026-08-16:

```
item3.patch.txt        b7b4c4f74f3016cb   1,609 lines
item5.patch.txt        4c03910c76fdcbf2   1,689 lines
item6.patch.txt        f65da5c3ce8433ec   2,019 lines
item4.patch (1).txt    a516c2c144c1f2f6   1,915 lines   (Rev B)
```

Apply order: item3 → item5 → item6 → item4. Patches carry CRLF; normalise with `sed 's/\r$//' in > out && printf '\n' >> out`.

---

## 7. WHAT DOES NOT CHANGE

Independent verification of every repository claim · executed-test evidence distinguished from static inventory · **a summary line is not a transcript** · empty-state captures for any surface rendering statistics · correction ≠ approval · no DA self-approval · verdict vocabulary · anti-recursion · **"This is required." distinguished from "This is recommended."**

Constitutional constraints unchanged: no automated execution · no external LLMs · no dynamic plugins · **no live trading**.

The rigour that found `OBS-CONV3-4` (research stage inert) and `OBS-CONV3-10` (raw anchors forcing full page reloads) by inspection is unaffected. **What changed is the boundary of my remit, not the standard applied inside it.**

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
Handover **WITHHELD**.
This correction closes the CONV programme. It is **not** authorization for SURF, DATA, CHART or POLISH — those require a Build Order.

**We don't guess. We prove.**
