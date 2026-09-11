# ITRGA-REV-V2-BE-8-INT-001 — Integration Build Review, BLOCKING

## BLOCKING REVIEW FINDING: **INT ACCEPTANCE RECOMMENDED — BUILD PASS** (act NOT authorized by this document)

- **Delivery under review:** AXIOM-V2-BE-8-DR-001 (v1.0.0), received 2026-09-04 against **BO-V2-BE-8-001** v1.0.0 (five evidence artifacts, intake-sha/md5 verified == the delivery report's manifest).
- **Review class:** pre-declared full-depth (post-implementation, pre-act). Method: intake identity → witness verification → independent ANNEX-P re-computation → transcript-level consent/permission/routing verification → literal source extraction → per-file hash binding → diff-anchored amendment review → mechanism-level code review of every new plane.
- **Files reviewed literally (20/20):** 15 created (`app/v2/paper_trading/` ×9 incl. `__init__`, `contracts`, `accounts`, `orders`, `risk`, `simulator`, `ledger`, `reconciliation`, `api`; `app/db/models/v2_paper_trading.py`; `alembic/versions/20260904_0048_v2_be8_paper_trading.py`; four `test_v2_be8_*` modules) + 5 amended (`app/v2/mode/contract.py`, `app/v2/rbac/permissions.py`, `app/v2/api/router.py`, `app/db/models/__init__.py`, `tests/test_v2_mode.py`). Every body was re-hashed from the source transcript (REM-001 line-ending convention) and **20/20 match their declared per-file SHA-256; the 20 manifest rows match the block-level declarations 1:1**.
- **Amendment anchoring (the decisive check):** baseline pre-amendment versions of the 3 prior-pinned files were extracted from V2_BE-7_SOURCE_TRANSCRIPT.md and re-hashed == the 0047-act pins exactly (`router.py` ad4afdd4…, `permissions.py` a3dff082…, `models/__init__.py` 32b0f770… — all match); `mode/contract.py` and `tests/test_v2_mode.py` were diffed against my repo reference. **All five diffs are exactly the sanctioned amendments — additive-only, no silent edits:**

    1. `router.py`: +1 import, +1 mount line (whitelist position).
    2. `permissions.py`: +8 constants, +8 permission-row inserts, +8 SAL entries, and the D-1 exemption implemented as **a single literal `startswith("v2.paper.")` prefix test** (comment documents the boundary: `v2.paperwork.*` is NOT exempt — the trailing dot is part of the prefix). Binding-condition wording honored.
    3. `models/__init__.py`: +1 import block (8 models) + 8 `__all__` entries — PG-002 law (models in the same unit as the module).
    4. `mode/contract.py`: `VALID_MODES` += `PAPER`; `DEFERRED_MODES` == `("LIVE",)`; refusal text updated to LIVE-only deferral; D-2 ruling cited in docstring.
    5. `tests/test_v2_mode.py`: the three BE-1-era pins superseded to the D-2 vocabulary, each docstring citing `ITRGA-REV-V2-BE-8-DESIGN-001 §6 / BO T-2`. Disclosed churn — executed exactly as disclosed (D-2 §e).

## DELIVERABLES (D-1 … D-8)

| D | Verdict | Evidence |
|---|---------|----------|
| D-1 module | PASS | 9 files; N1/N2 declaration in `__init__.py`; import-order legality proven by fail-first witness (ModuleNotFoundError accounts→orders, artifact cmp-checked verbatim into the transcript) then green |
| D-2 models + registration | PASS | 8 closed tables; BE-1 columns appended on every table; PG-002 same-unit registration; a-priori pins NOT touched (X-2 mutation-scan green in suite) |
| D-3 forecourt | PASS | mode + permission vocabulary + integration + RBAC seams as diffed above |
| D-4 migration 0048 | PASS | single-revision op (47→48); `_check_schema_version` scan-fail-first; X-9 checkout contract; 16/16 guard triggers census-asserted with RuntimeError+recovery text; compver delete-guard dance preserved; symmetric content-based downgrade with all-a-clear |
| D-5 routers | PASS | exactly 2 markdown files; no format drift; enforcement pin + no-whitelisting claim verified |
| D-6 tests | PASS | 54 new collected tests (15+10+16+13); totals 972+54 = **1,026/0** at head, x2 full runs |
| D-7 evidence | PASS | five artifacts, consistent cross-references; hashes pinned |
| D-8 statements | PASS | pre-declared compver inputs; obs-E honored; 8 honest disclosures incl. compver-hash caveat with recompute rule |

## TERMINAL CONTRACTS (T-1 … T-18) — mechanism-verified, not transcript-verified alone

| T | Verdict | What I verified |
|---|---------|-----------------|
| T-1 | PASS | D-1 exemption scoped exactly to the literal prefix; guard still kills markers elsewhere; boundary test dies on `v2.paperwork` |
| T-2 | PASS | PAPER accepted only in `VALID_MODES`; LIVE refusal intact; writers enforce `mode == "PAPER"` (typed refusal otherwise — T-2 test reads real mode contract) |
| T-3 | PASS | every writer + reader requires PAPER mode; research-mode client refusal tested (`T-2` file + order-writer test) |
| T-4 | PASS | `EXECUTION_BACKENDS` = frozen MappingProxy single entry `paper`; no adapter ABC/injection anywhere in the domain (negative test asserts absence) |
| T-5 | PASS | CR2 routing raster respected: no borrowed writers; simulator typed seam `PaperOrderIntent` only (untyped = typed refusal) |
| T-6 | PASS | replay engines untouched; drift scan at both pre-upgrade and head empties BE-8 tokens; audit-write drift is the inherited 9-token class only |
| T-7 | PASS | `run` is the only execution path; seam typed; snapshot content hash reverified pre-run (G-5; witness: content-mismatch → quarantined_unknown + typed refusal class, hash pair recorded) |
| T-8 | PASS | default-deny: `may_execute` returns typed (False, reasons) when decision row absent; evaluated_limits measured {observed, threshold, verdict} per limit |
| T-9 | PASS | exactly-once evaluation as a schema fact (`uq(intent_id)`); 7-limit vocabulary settled; single decision authority (gateway decides; margin engine computes only) |
| T-10 | PASS | deterministic single-pass; replay contract x3 byte-identical test passes; ANNEX-P hand-computed values asserted verbatim (9609.40 / 10009.40 / 9.40 / 0 / 200 / 9809.40 / position 4) — I independently recomputed the full annex and agree digit-for-digit |
| T-11 | PASS | cost units restricted to CR-V2-BE-7-001 vocabulary (`price`/`fraction`); unknown unit = typed refusal; cost influence on effective price only |
| T-12 | PASS | genesis-recompute over append-only fills; content comparison; discrepant = typed alarm, never auto-corrected; position/balance/reconciliation writes cohere |
| T-13 | PASS | T-13 schema census asserted in code: **57 permissions (49+8), 58 triggers (42+16), 10 compver** rows constitutional-pinned with names printed; 8-table shape + iff-CHECK literal + single-key uq + `fill_class` single-value CHECK; deep equality refused |
| T-14 | PASS | single-revision op with symmetric content downgrade; alembic check at both heads in both file-format forms; zero BE-8 drift tokens; 16/16 trigger census with fail-loud recovery text |
| T-15 | PASS | no external code paths; no scheduler/worker/UI surface; repo-reference mode invariant included in suite |
| T-16 | PASS | operator-visible refusal classes enumerated and tested: RBAC denied, unauthenticated, mode-wrong, hold-refusals ×4, transition-refusal, cancel-refusals, drift refusal — all typed, audited, non-enumerating |
| T-17 | PASS | consent surfaces closed: register-copy drift impossible (no interpolations anywhere in /paper); audit classes closed-set asserted |
| T-18 | PASS | four new files ≤3 independent modules each; four-file split matches delivery accounting; the test matrix (54) tied to D-6 deliverables |

## VERDICT ON BINDING DESIGN POINTS (structural, code-level)

1. **C-1a iff-CHECK** — rewritten exactly as mandated (`(decision = 'hold') = (confirmation_ref IS NOT NULL)`), identical literal in model + migration DDL; immutable (no UPDATE regime).
2. **C-1a may_execute** — implemented once in `orders.py` with the exact three-case semantics (pass → true; block → typed terminal refusal; hold → requires `hold.confirmed` citing the decision's exact `confirmation_ref` AND no `hold.cancelled`), consuming confirmation as a **derived ledger fact** (no consumable repository column).
3. **C-1b** — `confirm_hold` implements the four typed refusal classes in the mandated order, with durable audit + commit **before** returning each refusal (C-1 commit-before-return law). Confirm mints `risk_hold→risk_passed` + `paper.order.hold_confirmed`; cancel mints `risk_hold→cancelled` + `paper.order.hold_cancelled`; cancel can never confirm, confirm can never cancel.
4. **C-1c** — event/audit classes all present and mapped to the audited actions verbatim (API transcript: 12 audit classes incl. refusal audits observed live).
5. **C-1d** — block terminality structural: `LEGAL_TRANSITIONS` contains **no outgoing edge from `risk_blocked`**; a confirm-targeted-at-block dies typed `not_confirmable` (test asserts block is unreachable by confirmation).
6. **S2.6 single-writer law** — `append_event` is the only state-advancing writer; absent-from-table transitions are typed refusals with from-state observation.
7. **S5 money law** — Decimal-only across the money pipeline (transcript shows 28-digit Decimal concentration strings); snapshot layers are derivations by construction (recompute==outcome), rounding only at the presentation boundary — full precision on the plane.
8. **G-5 lineage** — content-hash re-verification immediately pre-run; tamper witness (E1-style tampering → content mismatch → `quarantined_unknown` not silent inclusion) verified.
9. **Idempotency** — both writers key-protected; replay-safe (`E2` rerun converges, no second fill-set).
10. **Cancel semantics** — cancel is pre-risk/pre-execution only; terminal/executing/filled/partial/risk_passed cancel = typed refusals; hold cancel goes through the C-1 mechanism exclusively (single-mechanism law honored).

## FLAGS — triaged and closed

| # | Flag | Resolution |
|---|------|-----------|
| F-a | "inherited V1 drift ops: 18" vs the 9-token vocabulary | **Closed — arithmetic, not discrepancy.** The drift gate is parametrized ×2 heads × 2 file-format forms → 18 printed ops = 9 tokens × 2 heads; the drift test pins zero BE-8 tokens at both heads and `audit_write_failure_records` as the inherited representative. Law stands. |
| F-b | JSON envelope `correlation_id: null` on /paper happy paths | Closed — consistent with the V2 envelope law (key presence asserted; value optional); baseline behaves identically. |
| F-c | `ORDER_SIDES`/`ORDER_TYPES` renamed to `INTENT_*` | Verified in code (disclosure §7.1): V1 broker-guard tests byte-unchanged, paper-native `INTENT_SIDES`/`INTENT_TYPES` = ('buy','sell')/('market','limit') — values identical, names domain-scoped. |
| F-d | 3 `test_v2_mode.py` pins superseded | Verified — disclosed D-2 churn executed exactly; docstrings cite the ruling per the D-2 condition. |
| F-e | Operator paper-read grants deferred (admin-only v1 surface) | Accepted as a conservative tightening, disclosed (BO scope, permissions note in-file). The design S7.1 roles column had admin+operator reads; the delivery ships the least-privilege narrower set with the 57-census intact. **Recommendation (non-binding):** at the 0048-act register entry, note that granting operator `v2.paper.*.read` remains an open Operator option for a later governed act. |

## PINS — source of truth for the 0048-act file census (20 files, sha256, transcript-body convention)

```
d0a090fe31cad5e36012b939987b9f3ae627f5d363ff34a3ee76d8f0b48c9911  app/v2/paper_trading/__init__.py                 (312 B)
c90e6e5828811a4699dabbb538183a55534306604020a11e96771cd79589b502  app/v2/paper_trading/contracts.py                (4,924 B)
0e54f4c2c38d66a4d386d34574fc9625f9cc4d045fc92f814a1167e3a40b40ef  app/v2/paper_trading/accounts.py                (7,811 B)
af1ad32afc6953116a4b06289f3886dfd69442d6b2cbcd8f583b1bbdcfe87582  app/v2/paper_trading/orders.py                 (12,257 B)
ea4abf270da2cea46cc66a3bbff32ce1bdae70b9a4b4ddbb25e73bb082375717  app/v2/paper_trading/risk.py                    (3,456 B)
4fb0d5586232f73ccbdff29c2a18d35b8d5670d8a4c9d5d4b9cc48c44162a804  app/v2/paper_trading/simulator.py               (5,069 B)
7a901f8145b40aaaa80d3ef9c6c466be24ab55c7d290ede8887956dc86677138  app/v2/paper_trading/ledger.py                  (5,507 B)
74d7e70f89be1822d6ea2dce91920f471c7a0b5a43ea4b7c5d9524f48c044deb  app/v2/paper_trading/reconciliation.py          (4,121 B)
1e4064e367cfd7340038388503dd90710c70a32cf386b568d0504097cc96b3be  app/v2/paper_trading/api.py                    (30,095 B)
61ccb99966106cdf85485dfdfc9fed276512501553af59c9a4e6ddb02d73b56c  app/db/models/v2_paper_trading.py              (14,163 B)
2cb83b3d102598523834b867aa780bb659df3366a8775c65cc0750740dc398c2  alembic/versions/20260904_0048_v2_be8_paper_trading.py (20,583 B)
129c3d32f05945da5e55c33b6f020c3d4bebb8227d8baca07de3c47da2ae7f61  tests/test_v2_be8_simulator.py                  (8,783 B)
bd3227587bd913d5bead7c8958ff3fb6bd18b077ca1b5975f0ae806e0ab019b1  tests/test_v2_be8_migration.py                 (22,484 B)
46c9cee65ca01033849f4b4176b3ae270673a25e9fa6151850533264920f1b01  tests/test_v2_be8_orders.py                    (23,910 B)
a42a19f803385fe6829e9623e97878935fbe89add3670f20a37282364e72a99e  tests/test_v2_be8_boundaries.py                (10,262 B)
3346e0eee27d6f13a2d6d02e2df06089879c563789a113cf0bf014223c040b59  app/v2/mode/contract.py  (1,682 B, amended)
064019ca495328e2f1c00e9735f6c97f3e786cadcccb52b673a353bed5c5a99b  app/v2/rbac/permissions.py (10,069 B, amended)
530f91ec709b1d66c5c5cb7e339af5714d581f57169cb5b4566d0c9c45aafecd  app/v2/api/router.py (2,336 B, amended)
0b188cbf69fb984bb076648eba17c2408d42a5fb29462b6d4ff1ff853f1c6e68  app/db/models/__init__.py (5,981 B, amended)
19020e26a80ee7453abd34d88273d7e586c81b4bb075a9729a5016326e687ec4  tests/test_v2_mode.py   (2,214 B, amended)
```

## REGISTER NOTE (for DA after act)

After the 0048 act, DA updates the register: mark **BE-8 built (evidence accepted) / 0048 applied**, with the register-copy line: *"BE-8: paper trading — 8 tables zero-UPDATE, sealed simulator routing, hold/confirmation seam (C-1), 57 permissions / 58 triggers / 10 compver; design v1.1.0 (76e718c4…ccc073) + BO-V2-BE-8-001 T-1…T-18 satisfied; 1,026/0 suite at head 20260904_0048."* Optionally record the open Operator option to grant `v2.paper.*.read` to the operator role in a later act.

## NEXT LAWFUL ACTIONS

1. **Operator:** independently confirm (per your rule) — a spot hash of any delivered file vs the pin table above — then declare acceptance ("INT ACCEPTED" or corrections).
2. On your acceptance I issue the **INT acceptance + drift gate** (audit-write checklist + alembic-check evidence at 0047 and 0048 apkg forms, zero-BE-8-token pins, 1,026/0 re-print, 20-file station census) — auto-checked into the act evidence set.
3. On your explicit act authorization I issue the **0048 application order** (B-plane pins carried from §PINS; working-DB upgrade to 20260904_0048 + database_changelog + PGF-020…024 statutes; *not authorized yet*).
