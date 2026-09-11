# ITRGA INTAKE — QUARANTINE RETURN (AXIOM-V2-BE-8-DA-QRET-001) — RULING §2.3 OBLIGATIONS CLOSED

- **Record:** ITRGA-INTAKE-V2-BE8-QRET-001 · v1.0.0 · 2026-09-05
- **Intake object:** `V2_BE-8_0048_QUARANTINE_RETURN.md` (DA-QRET-001)
- **Executes/acknowledges:** ITRGA-RULE-V2-BE8-HALT-0048-001 §2.3 (debris disposition) + §2.4 (standing rule)

## 1 — Verification of the return

| Ruling requirement | Return content | ITRGA check | Result |
|---|---|---|---|
| Post-rename sha256 == `b64b8400…cdc0` (byte preservation) | Identical hash + 1,699,840 B, pre- and post-rename both printed | Cross-checked vs DB_PINS chain (pre == backup == post-halt == tombstone) | **PASS** |
| Working filename absent on DA station | `ls axiom_dev.db` -> No such file or directory | Asserted; hazard closed (debris no longer squats the working name anywhere reachable by a future DA-side fallback) | **PASS** |
| Anchor `.bak` retained, untouched | 1,699,840 B, `b64b8400…` byte-identical | Consistent | **PASS** |
| No deletion | Explicit, standing until a future explicit order | Doctrine-conformant | **PASS** |
| §2.4 standing rule in force | Encoded as first env line of every DA generator; ahead of PGF registration | Acknowledged into record | **PASS** |
| §2.5 observation untouched | Confirmed excluded from any act; no code movement | Consistent with the ruling's exclusion | **PASS** |

## 2 — §3 relic disclosure: independently corroborated via the ITRGA clone

`backend/axiom_dev.db.backup`: the DA measured **155,648 B, sha256 `561b2758…c5e4a98`**, claimed git-tracked V1-era repo relic (alembic `20260710_0003`, 9 tables/6 rows), Operator git custody, untouched.

**ITRGA measurement on its own clone (fd8d649):** byte count 155,648 **exact**; sha256 `561b275800ab2b677d7c643e65fe2de2b18cee2e9b4840036a2fc2aebc5e4a98` **exact**; `git ls-files --error-unmatch` confirms versioned custody. Disclosure corroborated byte-for-byte.

**Rulling note (non-blocking):** no action this cycle — the relic is git-custody heritage, not on the working filename, not E-0046-DUP-relevant to the console apply path. Disposition (if any) is a future housekeeping matter for the Operator; the relic stays **untouched**.

## 3 — Chain state

Quarantine obligations **CLOSED**. Working lineage untouched at `27bda311…c776f` (Operator console); corpus frozen/act-ready (20/20, twice attested); act VOID (first attempt) with re-target ruled; **ITRGA is authoring the STAGE/APPLY/VERIFY console-pack family (`ITRGA-ISS-V2-0048-PACKS-001`)** under the 0047 pack law: refuse-if-completed, pure-read-until-mutation, identity gate (`sha256 == 27bda311…` AND `current == 20260903_0047`), 20-file corpus staging with byte pins, PGF-022-validated summary gates (real-output shape proofs, the 972-lesson), compver PXS/PRG exact-match, consensus 57/58/10, drift zero-BE-8-token law (both heads), suite 1,026/0 bare/decorated, byte/MD5 identities of record.

On issuance: Operator hash-gates by MD5, runs the packs, returns transcripts -> ITRGA act review -> CLO/SEAL -> DA register sync (staged line + F-e verbatim).

**We don't guess. We prove.**
