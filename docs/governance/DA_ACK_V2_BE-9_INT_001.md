# DA ACK MEMO — BE-9 INT REVIEW (F-C1 ROOT CAUSE + N-O1 ELECTION + BINDING-PIN ACT)
# AXIOM-V2-BE-9-DA-INT-ACK-001 · v1.0.0 · 2026-09-05 · AXIOM Trading Terminal v2.0
# Acknowledges: ITRGA-REV-V2-BE-9-INT-001 (BUILD PASS, one correction F-C1,
#               one observation N-O1)
# Author: Replacement Development Authority (DA)
# Contents: §1 F-C1 root cause + pin confirmation · §2 N-O1 answer (canon
# refinement ELECTED; scoped supplement shipped) · §3 the Operator
# binding-pin act landed · §4 supplement identities · §5 posture.

---

## §1 — F-C1: root cause stated explicitly, ITRGA pin confirmed

**Root cause (measured, not guessed):** the DR §4 value `0f62714696e37fac…`
was captured from the DA-chain 0049 apply that ran **before** the
reconcile.py repair landed during the same build session (the
instrument-permissions comparison side was completed after the first
chain apply; `reconcile.py` is a member of the `_BRE_FILES` tuple, so the
early apply hashed pre-repair bytes). Exactly the review's "station-side
content drift at declare time" hypothesis. The declared value derived
from bytes that were never delivered; the delivered corpus is the
authority.

**Confirmation:** the DA re-executed the recipe as WRITTEN in the
migration over the manifest-verified corpus and reproduces the ITRGA pin
**exactly**:

> `bre-1.0.0` = `924df1ab13fa4a9e59910b71a7d0c4cbe2217c93764515a0c8584d8685a42958`
> (LF canonical bytes, forward-slash rels — the corpus/landing canon)

The DA **confirms this as the compver expectation for the reviewed
corpus** and adopts the review's adjudication in full: the true gate is
the act's live recompute-and-compare from landed bytes.

**Supersession disclosure (lawful, §5.1-sanctioned):** the N-O1 canon
refinement elected below amends `sync.py`, which is a `_BRE_FILES`
member — the ACK-cycle corpus therefore carries a NEW expectation,
computed from the supplement bytes under the same recipe:

> `bre-1.0.0` (post-ACK-cycle) =
> `b0008cb900b6e129a89239fab6f0d5c62fb2e994f7810366a08651d7a5e833a2`

Chain of record: `0f627146…` (declare-time drift — VOID) → `924df1ab…`
(ITRGA pin, reviewed corpus — CONFIRMED for those bytes) →
**`b0008cb9…` (ACK-cycle corpus — the 0049-act expectation, subject to
ITRGA re-verification from the §4 supplement bytes).** The VERIFY act
recomputes from landed bytes either way — correct-by-construction.

## §2 — N-O1: the canon refinement is ELECTED (the stronger position)

The DA does not merely assert that no volatile-class field can reside in
`payload` — a provider owns that blob, and an assertion about another
party's future bytes is not proof. **Elected instead (one-line canon
change + test, per the review's own option):**

- The orders canon now hashes `payload_substantive` — the design S1.2
  provider-named substantive fields only (`type`, `volume`/`units`,
  `price`, `time_in_force`, `symbol`) projected out of the payload blob.
  A provider-smuggled retrieval-volatile field **cannot flip run digests
  between identical states** — excluded by construction, the allow-list
  law now applied inside the blob too.
- The verbatim payload still lands in the projection row (the lawful
  storage site, payload-echo canary law unchanged).
- **New test** `test_canon_order_payload_volatile_invariance`: a volatile
  field injected into the payload leaves the digest unmoved; a
  substantive change (price) still moves it. Both arms executed.

## §3 — The Operator binding-pin act LANDED (review §5.2b; D-5 record)

Operator literals delivered 2026-09-05, direct to the DA:

| Pin | Value |
|---|---|
| `server_hostname` | `ExnessKE-MT5Trial9` |
| `account_number` | `476910140` |
| `environment` (governed class) | `practice` — the schema CHECK law; the Operator's account label ("AXIOM") is recorded here as the environment-string fact of the pinning record |
| Investor password | **NOT delivered, never will be** — vault-only at the operator console |

Landed as the registry-only amendment in `contract.py::ENVIRONMENT_BINDING`
(pinned facts, not credentials). Consequential test updates, disclosed:
the pre-pin fail-closed arm is superseded by the pinned-state both-arms
test (exact match passes; wrong server refused; wrong account refused);
the boundary containment scan now also asserts the REAL hostname and
account literals appear nowhere outside `contract.py`/the provider leg.

**Environment-string note for the ITRGA (honest):** the binding's
`environment` field carries the governed class `'practice'` (the S3/T-6
schema CHECK vocabulary). The Operator-supplied label "AXIOM" is the
account's display label at the broker, recorded in this act's record; if
ITRGA rules the label belongs in the binding tuple instead of (or beside)
the class, that is a one-literal amendment at the next scoped cycle.

## §4 — Scoped supplement identities (amended bytes + re-hashed + re-run)

| Artifact | Bytes | MD5 | SHA-256 |
|---|---|---|---|
| `docs/evidence/V2_BE-9_ACK1_SOURCE_SUPPLEMENT.md` (REM-001 scoped; 4 changed files, literal bodies) | 40,567 | see below | see below |
| `docs/evidence/V2_BE-9_ACK1_TESTRUN_TRANSCRIPT.txt` (full raw `-v` re-run: **1,077 passed / 0 failed** = 1,076 + the N-O1 test) | — | see below | see below |

(Full hashes in the delivery-note block appended at transmission — the
supplement was hashed after this memo's final byte to avoid the
self-reference loop; the two artifacts' identities ride in the relay
message per the §7.1 law.)

Changed files (4; nothing else moved): `contract.py` (binding pins),
`sync.py` (N-O1 canon), `test_v2_be9_contract.py` (pinned-binding +
N-O1 tests), `test_v2_be9_boundaries.py` (real-literal containment).
Suite: **1,077/0**. Ruff clean. Credential scan CLEAN (the account
number and server hostname are pinned facts by ITRGA/BO definition, not
credentials).

## §5 — Posture

- O-2: the 8h TTL default stands in code; Operator confirmation rides to
  INT acceptance per the review.
- Operator-box T-19 re-run (expected **1,077/0** after this cycle — the
  supplement moves the floor by one) awaits the Operator per §5.2a.
- No further code changes under this review; the corpus is frozen at the
  supplement identities pending the ITRGA INT acceptance record.
- Working DB untouched at sealed `20260904_0048`; the 0049 act remains
  separately sanctioned; expected compver at that act: **`b0008cb9…` (§1
  chain), RPE/RJE/PXS/PRG unchanged.**

**We don't guess. We prove.**

— AXIOM-V2-BE-9-DA-INT-ACK-001 · v1.0.0 · 2026-09-05
