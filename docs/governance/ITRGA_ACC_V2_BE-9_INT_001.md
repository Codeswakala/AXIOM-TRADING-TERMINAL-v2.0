# ITRGA INT ACCEPTANCE — BE-9 (ACK-cycle corpus frozen)
# ITRGA-ACC-V2-BE-9-INT-001 · v1.0.0 · 2026-09-05

- **Builds on:** ITRGA-REV-V2-BE-9-INT-001 (BUILD PASS; F-C1 correction,
  N-O1 observation) · DA-ACK memo `AXIOM-V2-BE-9-DA-INT-ACK-001`
  (6,576 B, sha256 `f46ccb679c79…9346d6d`) · evidence:
  `V2_BE-9_ACK1_SOURCE_SUPPLEMENT.md` (**40,600 B**, sha256
  `c2ff0f1e6719…0244aec1`) + `V2_BE-9_ACK1_TESTRUN_TRANSCRIPT.txt`
  (**104,866 B**, sha256 `f65475937726…029bcd0`).
- **VERDICT: INT ACCEPTED.** The sampled-and-then-exhaustively-verified
  ACK-cycle corpus is law-compliant, byte-consistent, and FROZEN at the
  identities below. INT acceptance authorizes the remaining stations.
  The working DB stands untouched at sealed `20260904_0048`.

## §1 — F-C1 CLOSED (correction satisfied)

Root cause accepted as stated and measured (declare-time chain-apply ran
on pre-repair `reconcile.py` bytes, itself a `_BRE_FILES` member). Chain
of record closed and both sides reproduce each link:

| Stage | Value | Status |
|---|---|---|
| DR §4 declare | `0f62714696e37fac…` | **VOID** — bytes never delivered |
| Reviewed corpus | `924df1ab13fa4a9e59910b71a7d0c4cbe2217c93764515a0c8584d8685a42958` | CONFIRMED (ITRGA pin; DA re-reproduced exactly) |
| **ACK-cycle corpus** | `b0008cb900b6e129a89239fab6f0d5c62fb2e994f7810366a08651d7a5e833a2` | **ITRGA RE-REPRODUCED EXACTLY** from supplement bytes + unchanged leg/reconcile; adopted as the 0049-act compver expectation |

## §2 — N-O1 CLOSED (election verified at bytes)

`sync.py` diff is EXACTLY the elected refinement: orders canon swaps the
verbatim `payload` for `payload_substantive` (`type/volume/units/price/
time_in_force/symbol`, the design S1.2 provider-named set), projected by
a named helper; the verbatim payload still lands in the projection row
(storage site untouched). Nothing else in the file moved. The two-arm
test `test_canon_order_payload_volatile_invariance` (volatile smuggle
→ digest unmoved; substantive price → digest moves) is present and
PASSED in the raw transcript. The allow-list law now runs inside the
blob; a provider cannot flip run digests by byte smuggling.

## §3 — Binding-pin act (D-5) VERIFIED AT BYTES

- **Registry-only amendment:** `contract.py` diff contains ONLY the
  comment-block rewrite and the two literal swaps:
  `server_hostname = "ExnessKE-MT5Trial9"`,
  `account_number = "476910140"`; `environment = "practice"` (governed
  class — ITRGA ruling stands; the broker-side label "AXIOM" is
  pinning-record material only unless the Operator elects an alias
  literal at a future scoped cycle).
- **No credential material anywhere:** the only `password`-family
  occurrences in all four amended bodies are (a) a comment affirming the
  password never enters code and (b) test-side identifier/canary
  references to the literal `canary-investor-pw-3f9d1c` — manufactured
  test content, not a secret. The arrangement matches the standing law:
  the investor password remains operator-side, vault-only at E1.
- **Fail-closed posture preserved in the pinned state:** the pre-pin arm
  is lawfully superseded by `test_binding_pinned_and_mismatch_refuses`
  (exact match passes; wrong server `Exness-LIVE1` → typed refusal;
  wrong account → typed refusal; `broker.binding.mismatch` cannot
  silently repoint reads).
- **Containment extended:** the boundary scan now asserts the real
  hostname and account appear nowhere in scanned sources outside the
  binding site (2 additive lines; nothing removed).

## §4 — Suite re-verification (raw transcript)

Exactly **1,077 PASSED / 0 FAILED / 0 ERROR**, banner
`1077 passed, 2 warnings in 513.37s`; band items **51**
(contract 18 = 17 − 1 superseded + 1 pinned both-arms + 1 N-O1 ·
migration 9 · sync 12 · boundaries 12). Floor moved +1 exactly as
disclosed; no other movement anywhere in the 1,077-item ledger.

## §5 — N-O2 (minor declaration defect, recorded, immaterial)

The ACK memo §4's byte column listed the source supplement at 40,567 B;
received = 40,600 B. Identities of record are ITRGA-COMPUTED (above) and
the four inline per-body SHA-256s all re-verify EXACTLY — the premature
column was a provisional fill, superseded by this record's pins. Same
defect family as F-C1; noted so the naming-of-numbers discipline is
restored at the next delivery.

## §6 — Corpus of record (FROZEN — 0049-act input set)

Eighteen original manifest bodies UNCHANGED (sha256s per
`V2_BE-9_SOURCE_TRANSCRIPT.md`, verified 22/22 earlier this cycle) ∪
four superseding bodies:

| Body | sha256 |
|---|---|
| `app/v2/broker_read/contract.py` | `f2862af9a7ad28e9b468b2d5b84c47e3a363227778cc3d449db785894f785176` |
| `app/v2/broker_read/sync.py` | `d1e5d4b56c881db4547dcea88ea2e4f34e8642509916907c0a228f47714dfa09` |
| `tests/test_v2_be9_contract.py` | `12733c46f5fe495513fe2f44b66eadee5845abb35b03ca0b97bdc23131610d5e` |
| `tests/test_v2_be9_boundaries.py` | `9ba9fd8290d5861911582a5286752c7ed5aee71c06e56acb9f4ac4337355f91f` |

**Deriving laws for the 0049 act:** suite expectation **1,077/0**;
quantity census **triggers 76 / permissions 64 / compver rows 11**;
compver expectation `broker_read_engine = bre-1.0.0` =
`b0008cb9…` (recomputed live from landed bytes; chassis landing writes
LF-canonical bytes) with RPE/RJE/PXS/PRG values unchanged; routes
2 (4 POST + 8 GET under one mount); head-in `20260904_0048`
(sha `1d4005fa…61dd3e`), down_revision exactly that; zero BE-9 drift
tokens.

## §7 — Remaining stations (in order; none optional)

1. **Operator:** box suite run on this corpus → expect **1,077/0**
   (T-19/CB-001 at INT acceptance).
2. **Operator:** confirm **O-2** — 8h vault TTL default (code carries it;
   one word suffices).
3. **Operator:** declare **INT ACCEPTED**.
4. **Operator:** the **E1 practice-contact act** — separate
   authorization; plain-wifi; investor password typed once, locally, by
   the Operator's own hand into the vault provisioning flow; witnessed.
5. **ITRGA:** band acceptance review → CR pack (FD byte pins carried
   from §6) → the **`20260905_0049` working-DB apply act** on the 0048
   console chassis (identity gate: sealed sha `1d4005fa…61dd3e` +
   `current == 20260904_0048`; E-0046-DUP; PGF-020…024; execution-card
   law; ISS-004/005/006 lessons).

— ITRGA-ACC-V2-BE-9-INT-001 · v1.0.0 · 2026-09-05
