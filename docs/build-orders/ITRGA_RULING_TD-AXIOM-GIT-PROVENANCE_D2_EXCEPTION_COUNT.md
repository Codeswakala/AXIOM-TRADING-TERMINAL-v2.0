# ITRGA RULING — D-2 Exception Count Disposition (TD-AXIOM-GIT-PROVENANCE)

**In response to:** `ITRGA_REQUEST_TD-AXIOM-GIT-PROVENANCE_D2_EXCEPTION_COUNT.md` (DA)

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Unit | `TD-AXIOM-GIT-PROVENANCE-REMEDIATION` |
| **DISPOSITION** | ✅ **OPTION A — formal exception manifest with SEPARATE counters** (as specified below) · plus **one ITRGA self-correction** removing the third occurrence |
| Build Order status | **AMENDMENT 2** — supersedes the P-2 counting rule; §2 scanner pattern unchanged |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Ruling in brief

1. **Option A is selected** — with a strict counting rule: exceptions are **reported separately, never subtracted silently**.
2. **The third occurrence is my error, not an exception.** My D-5 hook-demonstration literal self-matches Class A. I am **withdrawing that literal** and replacing it with a non-self-matching form. **Three occurrences become two.**
3. Option B is declined (§5). Option C is declined (§6).

---

## 2. The counting rule — this is the operative determination

The question the DA asked is the right one: *may a permitted exception be subtracted from a blocking count?* My answer:

> **`STAGED_SECRET_MARKER_COUNT` counts UNREVIEWED value matches only. It is not a filtered total — it is a residual after every match has been individually adjudicated in the open.**

Three counters are required, all printed:

```
STAGED_SECRET_MARKER_COUNT:        0     ← must be 0. Unreviewed/unlisted matches.
D2_PERMITTED_EXCEPTION_COUNT:      2     ← must equal the manifest length exactly.
D5_SYNTHETIC_DEMO_EXCEPTION_COUNT: 0     ← now 0, per §3.
TOTAL_CLASS_MATCH_COUNT:           2     ← raw scanner output, unfiltered.
```

**Binding arithmetic:** `TOTAL_CLASS_MATCH_COUNT` **must equal** `STAGED_SECRET_MARKER_COUNT + D2_PERMITTED_EXCEPTION_COUNT + D5_SYNTHETIC_DEMO_EXCEPTION_COUNT`. If the sum does not reconcile, **the unit halts** — that mismatch is the signature of a hidden filter.

**Why this form and not an allowlist:** an allowlist makes matches disappear from the output. A separate counter keeps every match **visible, named, and attributable**, and forces the raw total to be published alongside. This is the **W3-U08 precedent** applied directly: *"a wave-wide grep will have residual hits — demand they be DISCLOSED and each shown benign, never filtered into silence."* There, 3 residual hits were shown with command, output and individual justification. Same discipline here.

**The DA's framing was exactly right:** *"We do not convert a known exception into a hidden exception."* That is the distinction this ruling encodes.

---

## 3. 🔴 ITRGA self-correction — the D-5 demonstration literal is withdrawn

I specified a hook demonstration using a **Class-A-shaped assignment literal**. **I tested it: that illustrative form matches Class A.** My own illustrative example became a permanent Class-A occurrence in the authority record — a defect I introduced.

**Corrected D-5 demonstration protocol:**

- The hook demo value is **generated at runtime and never written into any governance document**:
  ```powershell
  $demo = 'PASS' + 'WORD = "' + [guid]::NewGuid().ToString('N').Substring(0,12) + '"'
  ```
- Write it to a scratch file, attempt the commit, capture the rejection (filename/line/class only), then **delete the scratch file**. Prove deletion.
- In the ruling record and any documentation, the demonstration is described as *"a Class-A shaped assignment generated at demo time"* — **no literal is transcribed.**

**Effect:** `D5_SYNTHETIC_DEMO_EXCEPTION_COUNT: 0`. The exception manifest carries **two** entries, not three. **Recorded as ITRGA-ERR-4 under R19** — fourth correction in this programme, again surfaced by a DA that halted rather than guessed.

---

## 4. Required manifest specification (Option A)

**File:** `docs/governance/TD-AXIOM-GIT-PROVENANCE_D2_EXCEPTION_MANIFEST.md` — tracked, permanent, referenced by the closure determination.

**Required fields per entry:**

| Field | Rule |
|---|---|
| `path` | Repository-relative file path |
| `line` | Line number at time of manifest |
| `class` | `A`, `B`, or `C` |
| `identifier` | The matched **key** only (e.g. `PGPASSWORD`) — **never the value** |
| `value_sha256_first12` | First 12 hex chars of the SHA-256 of the matched value |
| `justification` | One line: why this is a permitted D-2 dev/test constant |
| `disposition` | `TD-AXIOM-DEV-CREDENTIAL-LITERALS` |

**On hashing — yes, and here is why:** a truncated SHA-256 gives a stable fingerprint that lets me verify at re-review that *the same* value is still there, without the plaintext ever entering a governance document. If a hash changes, the value changed and the exception must be re-adjudicated. **Full values are never printed anywhere** — not in the manifest, not in the scanner output, not in the transcript.

**Hook behaviour when a known-exception line changes (D-5 follow-on):** the guard matches on `path + identifier + value_sha256_first12`. If any element differs — new path, new key, changed value — **the exception does not apply and the commit is rejected.** An exception is granted to a specific reviewed occurrence, not to a file or a line number in perpetuity. This prevents an approved exception becoming a permanent hole through which a real secret later passes.

---

## 5. Why Option B is declined

Remediating the two literals now would require editing source/configuration inside a unit whose §2 forbids exactly that. It would convert a metadata-only change into a source change with its own test and regression obligations — scope creep (R16) on a governance-integrity unit, and precisely the trap D-2 was written to avoid.

They are already correctly dispositioned: **`TD-AXIOM-DEV-CREDENTIAL-LITERALS`** (MEDIUM, pre-certification for Doc 11 §2), with `admin/admin123` additionally proven **rejected under production framing** at W7-U07. They are known, tracked, fingerprinted, and gated before certification. That is the governed treatment.

---

## 6. Why Option C is declined

Because the count is not evidence of a security problem. Two adjudicated dev-fixture literals in a 1105-file corpus, each fingerprinted and tracked to a named pre-certification residual, is a **managed** condition. Halting indefinitely would block a governance-integrity fix — one that protects months of unversioned work — over a condition already under governance.

The security objective is unchanged: **no unreviewed credential value enters permanent history.** Two reviewed, hashed, manifested, certification-gated fixtures satisfy that.

---

## 7. Required evidence (amends §5 of the Build Order)

- **(c-i)** All four counters printed, with the reconciliation arithmetic shown.
- **(c-ii)** The exception manifest displayed in full — 2 entries, hashed values, **no plaintext**.
- **(c-iii)** Raw scanner output for all matches: **filename · line · class · identifier only.**
- **(c-iv)** D-5 demonstration per §3: runtime-generated value, rejection captured, scratch file deleted and deletion proven. `D5_SYNTHETIC_DEMO_EXCEPTION_COUNT: 0`.
- **(c-v)** P-3 redaction manifest as already prepared — **37 files / 71 Class-A / 1 Class-B / 0 Class-C**, filename-only. *(Noted and accepted as prepared; the Class-B connection URL redaction is particularly correct.)*
- **(c-vi)** Confirmation that no source, test, or configuration **value** was edited by this unit.

All other items in the Build Order and Amendment 1 stand.

---

## 8. Findings

| ID | Severity | Status |
|---|---|---|
| **ITRGA-ERR-4** | RECORDED (R19) | D-5 demonstration literal self-matched Class A, creating a permanent occurrence in the authority record. **Withdrawn; runtime-generated form substituted** |
| **TD-AXIOM-DEV-CREDENTIAL-LITERALS** | MEDIUM | Open — pre-certification. Now carries a **hashed, manifested** inventory of the two occurrences |
| **TD-AXIOM-GIT-PROVENANCE** | HIGH | Open — this unit closes it |
| — | **COMMENDATION** | The DA reported **3 matches** when 2 were permitted and 1 was mine, declined to create an allowlist, declined to subtract a count, declined to label the outcome zero, and reproduced **no matched value** in the request itself. The P-3 preparation (37/71/1/0) is thorough. **Three consecutive halts, three genuine defects in my instruments** — this is what an independent authority is supposed to be told |

---

## 9. Disposition

**Amendment 2 issued. Option A selected. The unit is unblocked.**

The DA asked whether a permitted exception may be subtracted from a blocking count. It may not — but it may be **counted separately, in the open, with the raw total published beside it.** That keeps the gate honest while letting correct work proceed, and it is the same discipline this project applied at W3-U08.

One of the three occurrences was mine. It is withdrawn and the record says so.

**Proceed:** apply the corrected D-5 protocol, produce the manifest, run the scanner to a **reconciling** result, then execute the §4 safe path from Amendment 1 — index removal, staging, anchored commit, baseline tag, honest retrospective tags, hook demonstration, forward protocol, registers.

On approval, `TD-AXIOM-GIT-PROVENANCE` closes and `BUILD_ORDER_UI-007-P07-AUDIT-REACHABILITY` is authorized.

Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**.

---

## 10. Evidence Confidence Statement

- **Evidence reviewed:** the DA request in full; direct validation that the withdrawn Class-A-shaped demonstration form matches while `$`-indirection and placeholder forms do not; the W3-U08 disclosed-benign-residue precedent; the W7-U07 `admin/admin123` disposition.
- **Confidence:** **HIGH** that the third occurrence is my own artifact and removable. **HIGH** that separate counting with a reconciliation identity preserves the security objective — it publishes the raw total, so a hidden filter cannot survive review.
- **Remaining unknowns:** none blocking; the two D-2 entries will be identified by path/line/hash in the manifest.
- **Additional evidence required:** §7 (c-i)–(c-vi).

---

*An exception you can see, count, and fingerprint is governance. An exception you subtract is a hole. The DA refused to dig one.*

**We don't guess. We prove.**

*— AXIOM ITRGA*
