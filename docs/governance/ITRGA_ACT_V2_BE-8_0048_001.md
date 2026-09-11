# ITRGA-ACT-V2-BE-8-0048-001 — APPLICATION ORDER: WORKING-DB UPGRADE TO HEAD 20260904_0048

- **Record:** v1.0.0 · 2026-09-05 · AXIOM V2 / BE-8 · BLOCKING
- **Authorization on file:** Operator, 2026-09-05 — *"0048 application order authorized"*
- **Chain:** …→ ITRGA-REV-V2-BE-8-INT-001 (PASS) → DA-INT-ACK-001 → ITRGA-INTAKE-V2-BE-8-ACK-001 → ITRGA-ACC-V2-BE-8-INT-001 (ACCEPTED + DRIFT GATE) → **THIS ORDER**
- **Directed at:** the Development Authority (DA). Scope: apply **one** alembic step on the working DB, on the **0047 chassis** (`20260903_0047 -> 20260904_0048`), honor the PGF-020…024 statutes as applied at the 0047 act, and return the act evidence set defined in §6. Nothing else is authorized by this order.

## 1 — Scope gate (what this act is, and is not)

- IS: backup -> pre-flight census -> pre-upgrade drift print -> `alembic upgrade head` -> post-flight pins print -> suite re-print -> evidence return.
- IS NOT: any code edit (bytes are frozen vs §2), any Git operation, any register write (register sync lands AFTER ITRGA act review — §7), any second/duplicate database artifact on the apply path (**E-0046-DUP startup law**), any grant of operator `v2.paper.*.read` (F-e remains an open Operator option — excluded from this act), any UI/scheduler/worker surface.

## 2 — Frozen corpus (sha256; must match the station BEFORE upgrade; transcript-body convention)

```
d0a090fe31cad5e36012b939987b9f3ae627f5d363ff34a3ee76d8f0b48c9911  app/v2/paper_trading/__init__.py                 (312)
c90e6e5828811a4699dabbb538183a55534306604020a11e96771cd79589b502  app/v2/paper_trading/contracts.py                (4,924)
0e54f4c2c38d66a4d386d34574fc9625f9cc4d045fc92f814a1167e3a40b40ef  app/v2/paper_trading/accounts.py                (7,811)
af1ad32afc6953116a4b06289f3886dfd69442d6b2cbcd8f583b1bbdcfe87582  app/v2/paper_trading/orders.py                 (12,257)
ea4abf270da2cea46cc66a3bbff32ce1bdae70b9a4b4ddbb25e73bb082375717  app/v2/paper_trading/risk.py                    (3,456)
4fb0d5586232f73ccbdff29c2a18d35b8d5670d8a4c9d5d4b9cc48c44162a804  app/v2/paper_trading/simulator.py               (5,069)
7a901f8145b40aaaa80d3ef9c6c466be24ab55c7d290ede8887956dc86677138  app/v2/paper_trading/ledger.py                  (5,507)
74d7e70f89be1822d6ea2dce91920f471c7a0b5a43ea4b7c5d9524f48c044deb  app/v2/paper_trading/reconciliation.py          (4,121)
1e4064e367cfd7340038388503dd90710c70a32cf386b568d0504097cc96b3be  app/v2/paper_trading/api.py                    (30,095)
61ccb99966106cdf85485dfdfc9fed276512501553af59c9a4e6ddb02d73b56c  app/db/models/v2_paper_trading.py              (14,163)
2cb83b3d102598523834b867aa780bb659df3366a8775c65cc0750740dc398c2  alembic/versions/20260904_0048_v2_be8_paper_trading.py (20,583)
129c3d32f05945da5e55c33b6f020c3d4bebb8227d8baca07de3c47da2ae7f61  tests/test_v2_be8_simulator.py                  (8,783)
bd3227587bd913d5bead7c8958ff3fb6bd18b077ca1b5975f0ae806e0ab019b1  tests/test_v2_be8_migration.py                 (22,484)
46c9cee65ca01033849f4b4176b3ae270673a25e9fa6151850533264920f1b01  tests/test_v2_be8_orders.py                    (23,910)
a42a19f803385fe6829e9623e97878935fbe89add3670f20a37282364e72a99e  tests/test_v2_be8_boundaries.py                (10,262)
3346e0eee27d6f13a2d6d02e2df06089879c563789a113cf0bf014223c040b59  app/v2/mode/contract.py  (1,682, amended)
064019ca495328e2f1c00e9735f6c97f3e786cadcccb52b673a353bed5c5a99b  app/v2/rbac/permissions.py (10,069, amended)
530f91ec709b1d66c5c5cb7e339af5714d581f57169cb5b4566d0c9c45aafecd  app/v2/api/router.py (2,336, amended)
0b188cbf69fb984bb076648eba17c2408d42a5fb29462b6d4ff1ff853f1c6e68  app/db/models/__init__.py (5,981, amended)
19020e26a80ee7453abd34d88273d7e586c81b4bb075a9729a5016326e687ec4  tests/test_v2_mode.py   (2,214, amended)
```

Any mismatch = the act aborts before it starts; the bytes are restored from the pinned transcript corpus; nothing is corrected in place.

## 3 — Execution contract (ordered; every step's output lands in the evidence set)

1. **Backup.** Content-addressed copy of the working DB; print byte count + sha256 of BOTH the pre-upgrade DB and the backup (lawful rollback surface; E-0046-DUP: backup lives outside the apply path, and the apply path sees exactly one target DB).
2. **Pre-flight station census.** hash-all-20 print == §2 (20/20).
3. **Pre-upgrade state print.** `alembic current` == `20260903_0047`; `alembic check` output captured: nonzero drift expected; **zero** BE-8 tokens; inherited 9-token V1 drift class with `audit_write_failure_records` representative.
4. **Apply.** `alembic upgrade head` (single step). Console captured verbatim.
5. **Post-upgrade state print.** `alembic current` == `20260904_0048`; `database_changelog` tail shows the 0048 row; `alembic check` captured with the same zero-BE-8-token law, 9-token inherited class only.
6. **Census prints (exact pins; not ranges).**
   - permissions: **57** rows (49 baseline + exactly the 8 `v2.paper.*` rows; table printed)
   - triggers: **58** (42 baseline + 16 `v2_paper_*` guards; names listed)
   - computation versions: **10** rows; the two new rows rolled at apply time from live disk must equal:
     - pxs-1.0.0 = `c58a06a5402f30a3828012f91b4aeb564008a9bfa34685cc57558e1003d106c0`
     - prg-1.0.0 = `ed6434fa5ff00b937b71e1d76a8fef32bc019f134e56831ac9f74af525376b1b`
     - RPE/RJE rows byte-identical to 0047 (carried, never rewritten)
   - tables: the 8 `v2_paper_*` tables present, each with its `_guard_update/_guard_delete` trigger pair; compver delete-guard re-created (existence count == 1)
7. **Suite re-print at head.** Full pytest transcript tail: **1,026 passed / 0 failed**. Any other byte = abort doctrine (§5), never a patch.
8. **Workspace freeze statement.** No Git op; no register write; delivered bytes still bit-identical to §2 post-apply (20-file hash re-print).

## 4 — Expected-value pins (summary of hard numbers this act must produce)

| Quantity | Pinned value |
|---|---|
| head string | `20260904_0048` |
| migration chain | single step from `20260903_0047` |
| permissions | 57 (49 + 8 paper) |
| triggers | 58 (42 + 16) |
| compver | 10 (8 + PXS + PRG; values per §3.6) |
| paper tables | 8, all guarded |
| suite | 1,026 passed / 0 failed |
| BE-8 drift tokens (pre and post) | 0 |
| inherited V1 drift tokens | exactly the 9-token class |

## 5 — Failure doctrine

Halt at the first deviation. The act is void at that point: restore the §3.1 backup, print the restore hash, report the anomaly as a typed refusal-class record. **No in-place corrections, no re-run without a fresh ITRGA note.**

## 6 — Evidence return contract (files the DA returns)

1. `V2_BE-8_0048_ACT_TRANSCRIPT.md` — console-as-transcript of §3.1–§3.7 in order, unparsed tail included.
2. `V2_BE-8_0048_CENSUS.txt` — the §3.2 AND §3.8 20-file hash prints (pre and post), machine-clean.
3. `V2_BE-8_0048_DB_PINS.txt` — pre-upgrade DB sha256/bytes, backup sha256/bytes, post-upgrade DB sha256/bytes, changelog tail.
4. Five-artifact hash manifest of the evidence set itself (md5 + bytes, DR-style).

## 7 — Post-act ladder (unchanged)

Act evidence returns -> **ITRGA act review** (full depth, pins vs §4) -> **CLO/SEAL** by ITRGA -> only then **DA register sync** with the staged line (incl. the F-e operator-option sentence verbatim). Run-phase maturity remains PENDING until the CLO seals.

**We don't guess. We prove.**
