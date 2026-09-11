# ITRGA INT REVIEW — BE-9 DELIVERY (full-depth, byte-level)
# ITRGA-REV-V2-BE-9-INT-001 · v1.0.0 · 2026-09-05

- **Objects:** `AXIOM-V2-BE-9-DR-001` v1.0.0 (13,717 B, `d0925343…5f2d`) +
  evidence artifacts: SOURCE_TRANSCRIPT (214,142 B, `6c49a891…`), TESTRUN
  (104,770 B, `34c1aca8…`), FAILFIRST (813 B, `c39342d4…`) — all intake
  identities byte+sha256 EXACT per DR §5.
- **Law:** BO-V2-BE-9-001 (D-1…D-8, T-1…T-20); design v1.2.1 ACCEPTED;
  intake memo ITRGA-INTAKE-V2-BE-9-INT-001.

## VERDICT: BUILD PASS with ONE correction (F-C1) + one observation (N-O1).

Twenty-two files were read at the byte level; every foreshadowed finding
adjudicated on evidence; one compver declaration does NOT reproduce
(correction directed at the DA ACK, not the corpus); the corpus itself
stands pin-ready.

## §1 — Verified on bytes (the proof table)

1. **Manifest self-proof (REM-001):** all 22 literal bodies re-hash EXACTLY
   to the transcript's per-file SHA-256+bytes. The corpus is self-proving;
   there is nothing between the bytes and the claims.
2. **F-1 (V1 test-file edits) — ADMITTED.** Four diffs vs the sealed V1
   originals are purely additive, single-clause allowlist extensions
   (`v2/broker_read/providers/`) with BO citations; `test_execution_
   research_safety` reflows a condition without weakening any token law.
   Zero deletions anywhere. Process note (non-blocking): a BO amendment
   naming the files was the cleaner path; recorded.
3. **Band-spanning amendments:** `permissions.py` / `router.py` /
   `models/__init__.py` diffs are ADDITIONS-ONLY hunks; the BE-9 blocks
   are BO-cited; DECISION-1 second literal prefix `v2.broker.` present
   with boundary companions; 7 permission literals = exactly the closed
   design set.
4. **Model/migration census:** 9 `CREATE TABLE` ≡ 9 tablenames (the six
   projections + sync_run + reconcile_run + discrepancy); **18 trigger
   tuples** with 18 distinct messages covering 9 tables × (UPDATE +
   DELETE) completely; the migration test holds an INDEPENDENT message
   map (line 23+) matching verbatim and never imports the migration;
   `data_class CHECK ('simulated')`, `environment IN ('practice')`;
   `down_revision = 20260904_0048`; compver inserts ONLY `bre-1.0.0`
   (RPE/RJE/PXS/PRG untouched — append-only law respected); PL/pgSQL
   fallback guards present for non-SQLite dialects.
5. **T-3/T-4 arms:** contract members = EXACTLY the six read verbs;
   docstring-stripped scans for `order_send` / `OrderIntent` /
   `TRADE_ACTION` / `BrokerPort` / scheduler / `requests` / `httpx` /
   `socket` / `urllib` across the whole domain: ZERO. `MetaTrader5`
   outside the provider leg occurs ONLY inside V1 forbidden-token lists
   (the containment law's own needles) and one fixture docstring — lawful.
6. **Q9 successor binding:** sealed registry `exness_mt5_demo`;
   `PENDING-OPERATOR-PIN` fail-closed literal verified; single-site
   `ORIGIN_FLOOR_ISO` (N-3 closure) verified; vocabulary-declaration
   header (page vs window) verified (N-2 closure).
7. **Canon = S4.1 faithful:** allow-list tables match the design
   field-for-field; record sort by natural external keys (lambda-keyed,
   hence phrase-level grep misses); fixed model order; JSON canonical
   (`sort_keys`, tight separators, `default=str` exact-string law);
   unknown/volatile fields excluded by construction.
8. **T-12:** single `V2BrokerReconcileRun(` construction site (writer
   chokepoint); outcome is count-derived inside that site; negative
   laws test-armed per DR. MECHANISM RECORDED: application invariant at
   the single writer (design's "pinned at INT" clause hereby consumed).
9. **API census:** EXACTLY 4 POST (`/sync`, `/reconcile`,
   `/discrepancies/transition`, `/vault`) + 8 GET; zero PUT/PATCH/DELETE
   decorators.
10. **N-3 closure:** zero REST-era tokens (`token bucket`,
    `rate_limited`, `retry-after`, `429`) across band code.
11. **Test accounting re-derived from the raw transcript:** per-module
    items 17/9/12/12 = 50 = BO-pinned-law final count; full suite
    transcript contains EXACTLY 1,076 PASSED items and the banner
    `1076 passed, 2 warnings in 468.25s`; OBS-E witness is authentic
    (module-stashed ImportError chain).
12. **Vault/scope posture:** TTL 8h constant, sole-resolution import
    boundary, repr blindness, payload-echo canary law — claimed tests
    present in bodies and counted above; full code-level re-read found
    no credential-material egress paths.

## §2 — F-C1 (correction; OBS-B class): compver pre-declaration is NOT reproducible

DR §4 declares DA-chain `bre-1.0.0` = `0f62714696e37fac…`. ITRGA
recomputation from the manifest-verified corpus under the recipe as
WRITTEN in the migration (rel + NUL + bytes + NUL over
`{providers/exness_mt5, sync, reconcile}.py`):

- **`924df1ab13fa4a9e59910b71a7d0c4cbe2217c93764515a0c8584d8685a42958`**
  (LF canonical bytes, forward-slash rels — the corpus/landing canon).

Nine additional recipe/encoding variants (CRLF, backslash rels, absolute
paths incl. the DA station path, chain-of-hex) — none reproduce the
declared prefix. Conclusion: the declared value cannot derive from the
delivered bytes under the recipe; most likely station-side content drift
at declare time (or a transcription error of another row's prefix).
**Adjudication:** the corpus is unaffected (self-proven); the true gate
remains the act's live recompute-and-compare at the working-DB station
where the chassis lands corpus bytes as base64 literals = LF canonical.
**Correction (DA ACK, mandatory):** state the root cause explicitly and
CONFIRM the ITRGA-pinned expectation above as the sole compver
expectation for the 0049 act (it will be carried into the act pins; the
♦0049 VERIFY will recompute it from landed bytes).

## §3 — N-O1 (non-blocking observation)

Orders canon includes the whole verbatim `payload` rather than only the
substantive provider-named fields the design listed (type/units/price/
time-in-force). As shipped this is MORE inclusive, sorted-key-stable,
and passes the shipped volatile-invariance test; the residual risk is a
provider payload containing a retrieval-volatile field that would flip
run digests between identical states. DA must answer at ACK: confirm no
volatile-class field can reside in `payload` (or pin the substantive
projection now, one-line canon change with test). Not acceptance-
blocking given the fixture law + E1 act re-evidence.

## §4 — Findings ledger closed

F-1 admitted (§1.2) · F-2 consumed (§1.8) · F-3 closed §1.6 · F-4 drift
laws verified at the bodies ×2 parametrize (nine inherited V1 tokens
law stands; zero BE-9 tokens asserted with the [both revs] parametrization
present in the corpus) · F-5 consumed by F-C1's pin (tuple spelling
authoritative: `providers/exness_mt5.py`, `sync.py`, `reconcile.py`).

## §5 — Next lawful actions

1. **DA:** the F-C1 ACK memo (cause + confirmation of the ITRGA pin) +
   N-O1 answer. No code changes admitted under this review unless the
   N-O1 answer elects the canon refinement (then: amended bytes +
   re-hashed transcript + re-run; scoped supplement).
2. **Operator:** (a) run the suite on the operator box per T-19/CB-001
   (expected 1,076/0) after the DA's ack lands; (b) the binding-pin act
   (D-5: hand the three literals to the DA; receive the registry-only
   amendment + new byte identities); (c) confirm O-2 (8h).
3. **ITRGA:** INT acceptance record on (1)+(2) → DA ACK → Operator INT
   ACCEPTED declaration → E1 practice-contact act (witnessed, plain-wifi)
   → band acceptance → the 0049 working-DB act (0048 chassis lineage;
   identity gate `1d4005fa…`, `current == 20260904_0048`).

— ITRGA-REV-V2-BE-9-INT-001 · v1.0.0 · 2026-09-05
