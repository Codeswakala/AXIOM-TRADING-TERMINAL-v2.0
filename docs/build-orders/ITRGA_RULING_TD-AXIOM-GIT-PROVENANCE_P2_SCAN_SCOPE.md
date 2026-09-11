# ITRGA RULING — P-2 Credential-Scan Scope (TD-AXIOM-GIT-PROVENANCE)

**In response to:** `ITRGA_REQUEST_TD-AXIOM-GIT-PROVENANCE-P2_SCAN_SCOPE_CLARIFICATION.md` (DA)

| Field | Value |
|---|---|
| Authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Unit | `TD-AXIOM-GIT-PROVENANCE-REMEDIATION` |
| **DISPOSITION** | ✅ **P-2 AMENDED — value-oriented scanner authorized** · all five decision points determined · DA's proposed safe path **APPROVED as amended** |
| Build Order status | **AMENDMENT 1** — supersedes §3 P-2/P-3 and §4 W-6 of the issued order |
| Governance Gate | CLOSED (unchanged) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. The DA is right, and the defect is mine

The P-2 expression I issued was **value-blind**: it matched the *identifier* `access_token` rather than an exposed *secret value*. In a platform whose auth contract legitimately returns `tokens.access_token` and `refresh_token`, that pattern makes `STAGED_SECRET_MARKER_COUNT: 0` **structurally unreachable** without either editing source the same order forbids, or excluding baseline content the order requires.

I verified the contradiction independently rather than accepting it: `access_token` appears throughout the corpus as a genuine API response field (`$login.tokens.access_token`), and my own Build Order text contains the marker expression, so the order would have failed its own scan.

**461 occurrences across 148 files is not a security finding — it is a broken control.** A gate that cannot be passed by correct work is not rigour; it is an obstacle wearing rigour's uniform. **This is ITRGA-ERR-3**, recorded under R19 — the third such correction in this programme, and, like the first two, surfaced by a DA that halted instead of guessing.

**The DA's conduct is exactly right:** it ran the control as written, hit an impossibility, changed nothing, and asked for the governed form. *"We do not guess a security control. We ask for its exact governed form."* That sentence belongs in the record.

---

## 2. AMENDED P-2 — the authorized value-oriented scanner

**Replace the §3 P-2 expression with the following three-class scan.** It targets exposed **values**, not identifiers.

**Class A — credential assignment with a literal value:**
```
(PGPASSWORD|POSTGRES_PASSWORD|DB_PASSWORD|SECRET_KEY|JWT_SECRET|JWT_SECRET_KEY|
 BOOTSTRAP_ADMIN_PASSWORD|ADMIN_PASSWORD|PASSWORD|PASSWD|API_KEY|APIKEY|
 PRIVATE_KEY|CLIENT_SECRET|ACCESS_KEY)\s*[:=]\s*["'][^"'$<>{}\s]{4,}["']
```

**Class B — credentials embedded in a connection URL:**
```
[a-z0-9+]+://[^/\s:@]+:[^/\s:@]+@
```

**Class C — a literal bearer/JWT value:**
```
Bearer\s+[A-Za-z0-9._-]{20,}   |   eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.
```

**Deliberately NOT matched** (safe by construction):
- Bare identifiers — `access_token`, `refresh_token`, `token`, `password` as a field/param/column name.
- Variable indirection — `$env:PGPASSWORD = $SecurePw`, `Bearer $token`, `${DB_PASSWORD}`.
- Placeholders — `<REDACTED_DEV_PASSWORD>`, `***`, `changeme`, `your-password-here`.

**I validated this pattern before authorizing it** against nine cases drawn from the real corpus — the three known credential literals, a real connection URL, and five safe identifiers/indirections. **9/9 correct: every real secret caught, every safe identifier passed.**

**Output discipline (binding):** the scan prints **filename · line number · marker class only — never the matched value.** A scanner that echoes the secret it found has leaked it into the transcript.

**Required result:** `STAGED_SECRET_MARKER_COUNT: 0`. Non-zero still halts the unit.

---

## 3. The five decision points — determined

### D-1 · P-2 matching semantics — **APPROVED as amended**
Yes. The scanner distinguishes secret **values** from safe identifiers, per §2. Filename/line/class output only.

### D-2 · Bootstrap and test literals — **MAY REMAIN; separate Build Order required**
Existing dev/test constants (`admin/admin123`, the local JWT string, `axiom_dev_password`) **stay where they are.** Rationale:

- This is a **metadata-only** unit. Editing source or tests here is prohibited by its own §2 and would be scope creep (R16).
- These are **known, tracked, dispositioned** items. `admin/admin123` was proven **rejected under production framing** at W7-U07 (`ADMIN_DEFAULT_CREDENTIAL_REJECTED_WITH_INSECURE_DEV_OFF: True`); the JWT-secret warning and dev defaults are long-standing register entries.
- They are **development fixtures**, not production credentials.

**But they must not be silently normalised by being committed into a permanent baseline.** I am therefore opening:

> **`TD-AXIOM-DEV-CREDENTIAL-LITERALS`** — MEDIUM, non-blocking, **pre-certification**. Development credential literals reside in tracked source, tests, configuration and governance records. **To close:** migrate to environment/fixture injection with no literal defaults, under a dedicated security-remediation Build Order. **Must be dispositioned before Doc 11 §2 (Secret & Credential Management) certification.**

Disclose it on the governance surface alongside the other residuals.

### D-3 · Tracked evidence and database backup — **INDEX-ONLY REMOVAL AUTHORIZED**
`git rm --cached` **is authorized** for the 570 tracked `docs/evidence/**` files and the tracked `*.db` backup — **index removal only, local files preserved.**

- Evidence artifacts are **review inputs, not source of record**. The authoritative record is the ITRGA determination that cites them; I hold the transcripts independently.
- A committed database backup is both a bloat and a data-exposure hazard.
- **No historical artifact need remain in the new tree.** Governance documents, Build Orders, delivery reports and ITRGA determinations **do** remain tracked — those are the record.

**Evidence required:** the `git rm --cached` command, a count of de-indexed paths, and confirmation the local review corpus is intact (`Test-Path` on a sample).

### D-4 · P-3 canonical redaction — **NARROWED**
Redaction is required **only** where a credential **value** is exposed per the §2 classes, and only in these families: `docs/governance/**`, `docs/build-orders/**`, root-level delivery reports and ITRGA determinations.

- Canonical replacements: `<REDACTED_DEV_PASSWORD>` · `<REDACTED_JWT_SECRET>` · `<REDACTED_DB_URL>`.
- **Source, tests and configuration are NOT redacted** under this unit (per D-2).
- **The Build Order's own pattern text is retained verbatim.** A security control must be legible in the authority record. The §2 patterns are written to not self-match (they require a quoted literal value, which the pattern text does not contain) — so no exclusion is needed. If the scanner nonetheless trips on a governance document that contains only *pattern text and no value*, that is a **documented exception**: list it by filename with the marker class and a one-line justification. **Exceptions are disclosed, never silently filtered** — the W3-U08 residual-grep precedent.
- Deliverable: a **filename-only redaction manifest** (no values).

### D-5 · W-6 recurrence guard — **APPROVED, same scanner**
The pre-commit hook uses the **identical §2 three-class pattern** plus the conflict-marker check. Using the same definition in the gate and the guard is deliberate: a guard stricter than the gate blocks legitimate future commits; a looser one lets secrets through. Demonstrate both: a rejection on a **Class-A-shaped assignment generated at demo time** and a clean commit succeeding. The originally transcribed literal is withdrawn by `ITRGA_RULING_TD-AXIOM-GIT-PROVENANCE_D2_EXCEPTION_COUNT.md` §3.

---

## 4. DA's proposed safe path — **APPROVED as amended**

All six steps are authorized, with these bindings:

| Step | Disposition |
|---|---|
| 1. Preserve immutable `22c735a` | ✅ Required — no rewrite, no force-push |
| 2. Index-only removal of evidence/backup | ✅ Authorized (D-3) — local files preserved |
| 3. Redact ITRGA-specified literals; filename-only manifest | ✅ Authorized (D-4) — governance families only |
| 4. Stage full approved v0.62.0 source/tests/governance corpus | ✅ Required — baseline must be complete |
| 5. Run the approved semantic scanner to a **real** zero | ✅ Required — §2 pattern, real zero, no filtering to green |
| 6. Anchored commit · baseline tag · honest retrospective tags · hook demo · forward protocol · Level-I evidence | ✅ Required — unchanged from the issued order |

**"A real zero result" is the operative phrase, and it is the DA's own.** A zero produced by narrowing the pattern until nothing matches is a false-clean (UI-002-P05 precedent). The §2 pattern is fixed by this ruling and is not to be further narrowed.

---

## 5. Everything else in the Build Order stands unchanged

W-1 conflict scan · W-3 baseline commit · W-4 annotated tag · **W-5 retrospective tags with the mandatory disclaimer** · W-7 forward protocol · W-8 registers · §5 evidence checklist (a)–(n) · §6 determination rule · §7 closure meaning.

**The §6 determination rule is amended in one respect only:** "any staged secret" now means a **Class A/B/C value match**, not an identifier occurrence.

---

## 6. Findings

| ID | Severity | Status |
|---|---|---|
| **ITRGA-ERR-3** | RECORDED (R19) | P-2 issued value-blind, matching identifiers not values; made a mandatory gate unpassable. **Amended per §2. ITRGA error, not DA** |
| **TD-AXIOM-DEV-CREDENTIAL-LITERALS** | MEDIUM (new) | Dev credential literals in tracked source/tests/config/governance. Non-blocking; **pre-certification for Doc 11 §2**. Own Build Order |
| **TD-AXIOM-GIT-PROVENANCE** | HIGH | Open — this unit closes it |
| — | **COMMENDATION** | The DA quantified the contradiction (1105 scoped / 148 matched / 461 occurrences), identified the precise cause, refused both unilateral interpretations, changed nothing, and requested the governed form. **Halting on an impossible control is harder than quietly satisfying it** — narrowing the pattern or excluding files would have produced a green result I might not have caught for several turns |

---

## 7. Disposition

**Amendment 1 issued. The unit is unblocked and may proceed on the §4 safe path.**

The control I wrote could not be satisfied by correct work. That is a defect in the control, not in the platform and not in the DA — and the honest way to handle it is to fix the instrument and record why, which is what this ruling does.

The security objective is unchanged and undiluted: **no credential value enters permanent git history.** The amended scanner is *more* precise about that, not less — it catches the three real literals and the connection-URL form while ceasing to flag an API field name as a leak.

**Proceed to execution.** On approval, `TD-AXIOM-GIT-PROVENANCE` closes and `BUILD_ORDER_UI-007-P07-AUDIT-REACHABILITY` is authorized, per the operator sequence.

Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**.

---

## 8. Evidence Confidence Statement

- **Evidence reviewed:** the DA request in full; corpus verification that `access_token`/`refresh_token` are legitimate contract fields; the W7-U01/W7-U04/W7-U07 secret-marker precedents; direct validation of the amended pattern against nine real-corpus cases (9/9 correct).
- **Confidence:** **HIGH** that the original P-2 was structurally unpassable, and **HIGH** that the amended pattern preserves the security objective — validated, not asserted.
- **Remaining unknowns:** the count of governance files needing value-redaction under the narrowed rule; determinable by the first scan.
- **Additional evidence required:** per the amended §5 checklist.

---

*A control that cannot be passed teaches nothing except to work around it. The DA declined to work around it. Fixed, and recorded.*

**We don't guess. We prove.**

*— AXIOM ITRGA*
