# DETERMINATION — FE-U01 · FEPACK-FEU01-004

| Field | Value |
|---|---|
| Document ID | **AXIOM-V2-DET-FE-U01-002** |
| Date issued | 2026-09-11 |
| Issuing seat | ITRGA (BO §5.3 determination seat for the V2 frontend campaign) |
| Subject pack | `FEPACK-FEU01-004` (fourth corrective cycle, single §A.5 scope) |
| Determination class | **TRANSMISSION-ADAPTED** — two-party planes (DA-transmitted manifests/transcripts + operator-executed batteries + approval-bearing pixels), residual scope declared, no presumption of in-corpus executability |
| Successor posture | Replaces `AXIOM-V2-DET-FE-U01-001` (**SUSPENDED**), which is hereby retired; the suspended determination carried no adverse finding, only custody insufficiency |
| Fills frame | `AXIOM-V2-DET-FE-U01-002-FRAME` — 16-cell plane ledger, all cells filled at issue |

---

## §1. Verdict

**FEPACK-FEU01-004 is DETERMINED — ACCEPTED as the FE-U01 acceptance surface.**

**Determined — APPROVED.** On the accepted/corrected cycle-4 build, all admission gates of record are discharged at the grade the transmission class permits: the spine is byte-proven end-to-end, all seven approval-bearing renders are md5-exact against the -004 manifest claims with content eyeball-checked, all three reference registers are absorbed (two canonically, one as declared proxy), and the suite arithmetic of the corrective campaign (fail-first 13/8 → 1,014 → 1,014 → 1,016 → **1,017 tests across 189 files, zero failures**) is stated verbatim inside the custody spine and corroborated by independent command-battery expectations anchored to the same spine. No mismatched byte, no unaccounted file, and no undisclosed scope exists anywhere on the chain. **FE-U01 (login/auth surface) is thereby CLOSED at BO §5.3.**

---

## §2. Evidence basis — planes of record

| Plane | Instrument(s) | Result |
|---|---|---|
| A. Spine V/X-artifacts, suite census, DR↔pack↔manifest interlock, register coherence | `VM_FE_U01_SPINE_VERIFICATION_001` (`FEU01_TX_SPINE_002.md`, 564,451 B) | **43/43 md5-exact**; X-excerpt anchors disclosed; E-6 census lines verbatim; E-7 == DR v1.4.1 §3 byte-for-byte; F-B3-SCOPE corroborated (21 heritage V1 files) |
| B. 7 approval-bearing renders | `VM_FE_U01_SPINE_VERIFICATION_002` + frame ledger B-1…B-7 (final tranche) | **7/7 md5-exact**: `94fda796…` (golden), `ab66d0be…`, `bde7e38e…`, `a6af3d9c…`, `bb0e6eba…`, `e4b37a01…`, `5565b2a8…` |
| C. Reference register absorption | `ABS_REF_001` (REF-001 `24aff50a…`, REF-003 `a7ef8fe7…` — canonical) · `ABS_REF_002` (REF-002 — **absorbed-as-proxy** `23c35d18…`) | **Absorbed**; §9 prototypes HOLD retired for the transmitted set |
| D. Second-party execution battery | Frame cell D-1, per election §3 | **Closed by waiver election** on DA single-party pre-run plane, spine-anchored |

Golden-render cross-check of record: render `94fda796…` matches the in-spine golden bytes (B-1), pinning the transmitted pixels to the spine itself rather than to the manifest alone.

## §3. Elections ledger — entry of record

| ID | Election | Effect |
|---|---|---|
| **E-FEU01-D1-WAIVER-001** | Operator election (2026-09-11, verbatim: *"option 2: waiver word"*): waive the D-1 second-party paste; close the cell on the DA's **pre-run, single-party** battery plane already in custody | D-1 admitted at its single-party form; disclosed here as a **narrowing election**, not a full two-party closure |
| (carried) | pattern-b door posture; REF-002-E1 / REF-002-E2-superseded; REF-003-E1 (fiction readout); F-B3-SCOPE | Previously recorded; unchanged; absorbed into the register lineage this determination verifies |

**Accepted mitigations for the D-1 narrowing (why the waiver is admissible):**
1. **A-priori form.** The B1–B5 expectations were pre-declared by the DA *before* any execution output could be shaped (`OPERATOR_B_BATTERY_RUNBOOK.md`), so the plane is a priori claim, never narration-after-fact.
2. **Spine anchoring.** Every D-1 value family is independently corroborated inside the verified spine: B1's seven DR-final md5s ride the byte-for-byte E-7 == DR v1.4.1 §3 interlock (A-4); B4's 189 files / 1,017 tests / 0 failures matches the E-6 census arithmetic verbatim (A-3); B5's pack anchors `be730caf…` / `b3afb0fd…` and 76-file extent ride the manifest plane; B2's 6 ` M` + 1 `??`, 972+/605− and branding covenant (axiom-logo.png only) match the cycle-diff disclosure in E-7.
3. **Reserved right.** This ITRGA reserves the right to re-open D-1 for raw-output execution at any future time, without prejudice, should any later finding contradict a waived value.

Waived values admitted into the register: B1 = 7 DR-final md5 identities; B2 = 6 modified + 1 untracked, +972/−605, branding diff limited to `axiom-logo.png`; B3 = needle tallies **0,0,0 · 1 · 2 · 2 · 0 · 367** (boundary-scoped per F-B3-SCOPE — heritage V1 21 files outside the FE-U01 surface by scope law); B4 = 189 files / 1,017 tests / 0 failures; B5 = pack anchors `be730caf…` / `b3afb0fd…`, 76 files.

## §4. Declared residual scope (what this determination does NOT carry)

1. **No in-corpus code re-execution.** Per the CODE-CHANNEL LAW, the FE-U01 codebase lives studio-side only; nothing in this corpus is claimed built or runnable here. Executability rests on the spine + battery planes, not on local verification — declared, not presumed.
2. **Rejected packs -001…-003 pixels are manifest-narrated by election**, not transmitted; their forensic role is register history and their suite/fail-first claims are corroborated only at the spine-text level.
3. **REF-002 rides proxy class.** Canonical bytes (`343be6a0…`) remain studio-side/outstanding; the absorbed proxy `23c35d18…` was assessed visually equivalent on the exact template subject/composition family, and the register role is documentary-only: cycle-3 build is superseded by REF-003. ABS-REF-002 §3 records the sole optional future closure path (fallback URL carrier) if byte-parity ever matters.
4. X-class excerpts (artifacts 016/023/029/035) are excerpts-of-full **as disclosed**, riding FULL-FILE md5/sha256/byte anchors — accepted at their declared class.

None of the above constitutes a qualification on the acceptance verdict; each is a declared scope, and the law applies: what is absent from the manifested custody is not asserted as evidence.

## §5. Closures and openings

1. **FE-U01 CLOSED.** `FEPACK-FEU01-004` enters the acceptance surface; the corrective campaign under the single §A.5 scope (four cycles, arithmetic 13/8 → 1,014 → 1,014 → 1,016 → 1,017) is complete and recorded.
2. **FE-U02 (global chrome) DRAFTABLE.** Per serial cadence §C.4, with U01 closed and registered, the next unit in the unit loop may be drafted on operator direction; FE custody law (below) applies to its DR.
3. **Custody-law ratification.** The DA-adopted **FE custody law** — every future FE DR ships with (i) a same-turn custody archive (V/X artifacts + approval-bearing pixels + reference register) and (ii) pre-declared, extraction-rehearsed operator battery runbooks — is hereby **RATIFIED** by this seat, on the evidence of FE-U01, where the law performed without a custody defect: 43/43 spine bytes, 7/7 image matches, three absorbed references, and every detection instrument arriving pre-framed. The D-1 waiver election is a per-unit election and does not amend the law; the law remains the default posture for FE-U02 onward.
4. **Standing, outside this instrument:** U3 formal adoption word remains pending on the operator/registry side and is unaffected by this determination.

---

*Issued per BO §5.3. Acceptance-with-correction posture maintained; the register, the spine, and the absorbed instruments are the complete record of this determination. — ITRGA, 2026-09-11.*
