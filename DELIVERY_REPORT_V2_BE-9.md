# DELIVERY REPORT — AXIOM V2 BE-9: Broker/Exchange Connectivity and Account Visibility

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-9-DR-001 |
| Version | 1.0.0 |
| Build Order | BO-V2-BE-9-001 |
| Governing design | AXIOM-V2-BE-9-DESIGN-001 v1.2.1 (ACCEPTED) + DIR redirect final edition (Exness/MT5/investor-password; provision pin) |
| Date | 2026-09-05 |
| Author | Development Authority (DA) |
| Status | **SUBMITTED FOR ITRGA INT INTAKE + DEEP REVIEW** |
| Baseline in | SEALED head `20260904_0048` (`1d4005fa…dd3e`) · 1,026 tests · triggers 58 · permissions 57 · compver 10 |
| Baseline out | migration `20260905_0049` (**DA test chains only**) · **1,076 tests** (1,026 + 50) · triggers **76** · permissions **64** · compver **11** — all T-17 pins hit exactly |

**Standing discipline: we don't guess. We prove.**

---

## 1. Executive summary

Band BE-9 implemented in full per the accepted v1.2.1 design: a
**read-only-at-type-level** six-verb `BrokerReadContract` (V1 `BrokerPort`
NOT reused — no mutation shape enters the graph); the Exness/MT5 provider
leg with **`broker.terminal.unavailable` first-class** (E-ENV-1) and the
Q9-successor code-pinned binding (fail-closed until the Operator pinning
act); the **sole-resolution encrypted vault** (AES-256-GCM + Argon2id,
passphrase never stored, repr-blind, import-boundary-tested); nine
`v2_broker_*` tables under the zero-UPDATE regime with provenance pins
NOT NULL and `data_class` CHECK `'simulated'`; **all-or-nothing sync**
(a half-fetched page cannot half-land — proven live); the **S4.1 digest
canon verbatim** with its three pinned tests; **reconciliation-first**
(clean runs evidenced in `v2_broker_reconcile_run` with both-side digests
under the ONE canon); the 7-class discrepancy machine with the full
lifecycle + reason-mandatory dismissal (iff-CHECKed at schema);
three-facts health. **1,076/1,076 passed.** Zero network in the suite
(socket guard on every test; the fixture provider carries recorded
practice-shaped payloads); the E1 practice contact remains the
separately-authorized act.

## 2. Terminal contracts T-1…T-20 (evidence map)

| T | Evidence (executed) |
|---|---|
| T-1 | DECISION-1 second literal prefix `v2.broker.` in the guard (comment cites the boundary law); arms: `test_decision1_broker_prefix_exempt` / `_markers_still_die_elsewhere` (`v2.research.broker.*` dies) / `_boundary_brokerage_dies` (`v2.brokerage.*` dies) |
| T-2 | `read_only_login_asserted` reads the terminal trade-permission FLAG only (no mutation attempt); the fixture pins `read_only_login: true` end-to-end into the account row and the health surface; master-login refusal class `broker.auth.misprovisioned` in the taxonomy (the live-leg arm executes at the E1 act) |
| T-3 | `test_t3_contract_verb_census_exact` (exactly six members); `test_t3_no_v1_brokerport_import_anywhere` (no `external_integration`/`broker.port` import) |
| T-4 | `test_t4_api_surface_census_exact`: 4 POST + 8 GET = 12 routes, zero PUT/PATCH/DELETE; `test_t4_no_mutation_vocabulary_in_domain_code` (order_send/OrderIntent/TRADE_ACTION absent, docstring-stripped scan) |
| T-5 | `test_n2_no_provider_hostname_in_frontend` + `test_n2_hostname_only_in_binding`; provider hostname exists only in `contract.py` (binding) + the leg's provenance echo |
| T-6 | Both-sides wall: `test_n3_paper_wall_from_broker_side` + `test_n3_paper_wall_from_paper_side` + no-cross-FK scan; provenance pins NOT NULL asserted via PRAGMA; `data_class` non-'simulated' INSERTs schema-refused ×3; `environment` non-'practice' refused |
| T-7 | Vault: roundtrip; wrong-passphrase ⇒ ABSENT; tamper ⇒ ABSENT; repr/str blindness (canary never renders); TTL 8h constant (O-2 default); sole-resolution import boundary (no argon2/AESGCM/cryptography outside vault.py); vault path env read only in vault.py; no `operator-vault/` under the repo |
| T-8 | **Payload-echo canary executed**: a provider-smuggled token lands ONLY in the lawful projection row — absent from the sync response, health output, and every audit row (`test_t8_payload_echo_canary`); vault acts record intent only, no material crosses the API |
| T-9 | 18 guard triggers; **all 18 messages byte-exact vs independent literals** (`test_0049_guard_messages_verbatim`, 9 tables probed UPDATE+DELETE) |
| T-10 | Fill anchor uq probed at schema; **×3 replay: three syncs → equal digests, ONE fill row, three lineage rows, `broker.fill.reused` audited** (`test_t10_replay_x3_equal_digests_and_fill_dedupe`) |
| T-11 | S4.1 canon in `sync.py::canonical_digest` (allow-list per model; fixed model order; natural-key sort; JSON canonical); three pinned tests: shuffle-invariance / single-value sensitivity / volatile-invariance (unknown fields excluded by construction) |
| T-12 | Every reconciliation lands exactly one `v2_broker_reconcile_run` row; clean run: `outcome='clean'`, count 0, both-side 64-char digests recorded (`test_t12_clean_run_evidenced`); outcome↔count consistency = application invariant, test-armed (the mechanism election per T-12's "pinned at INT") |
| T-13 | 7 closed classes (schema CHECK + detection tests: amount_mismatch + missing_in_axiom seeded and found); lifecycle detected→triaged→owned→dismissed_with_reason executed; illegal jump refused; reason-mandatory dismissal refused typed AND iff-CHECKed at schema; every transition audited |
| T-14 | Three-facts law: `classify()` closed vocabulary; `terminal_down` / `terminal_up_unreachable` / `reachable_no_data` / `reachable_stale` / `green`; E-ENV-1 arm live (`test_e_env1_terminal_unavailable_typed`: health shows terminal=not_running, refusal class surfaced); read-only-login state surfaced; unowned count derived |
| T-15 | Operator-initiated POST only (no scheduler); **partial page ⇒ zero rows landed, `partial_refused` lineage, typed refusal — proven live**; terminal-down ⇒ `failed` + zero rows; windows per A-8 (24h/1h, `test_t20_n4_origin_rule_pinned` checks the arithmetic); fetch-budget refusal in the leg (`broker.fetch_budget.exceeded`) |
| T-16 | Decimal exact-compare (`_dec_eq`; no tolerance); currency explicit — **cent-environment test**: a USC/100× fixture surfaces `currency_mismatch`, never silent (`test_t16_cent_environment_refused_at_binding`); binding admits `'practice'` only |
| T-17 | Censuses at 0049 head: **76 / 64 / 11** exact (live apply witnessed + `test_0049_seeds_and_totals`); `broker_read_engine=bre-1.0.0` over `{providers/exness_mt5,sync,reconcile}.py`, recipe identical to 0047/0048; RPE/RJE/PXS/PRG rows all asserted present with 64-char hashes (append-only law) |
| T-18 | `test_drift_gate_0049[both revs]`: nonzero exit, zero BE-9 tokens both heads, inherited witness |
| T-19 | No-touch (non-broker rows byte-identical; trigger delta exactly the 18 names); downgrade cycle content-based (compver delete-guard restored, count-asserted); **full suite 1,076/0** (machine note §7.1) |
| T-20 | N-1 n/a (this DR's change-note law); **N-2**: page/window vocabulary declared canonically at the head of `contract.py` (page = fetch unit; window = TIME SPAN), test-asserted; **N-3**: zero REST-era vocabulary (`token bucket`/`rate_limited`/`retry-after` scanned absent — terminal-courtesy law only); **N-4**: ORIGIN rule pinned — `ORIGIN_FLOOR_ISO = 2026-09-01T00:00:00+00:00` (rationale: the demo account was created 2026-09-05; no meaningful history precedes the band's era; the floor bounds the first sync deterministically); origin fact recorded on every sync-run row (`origin_basis`) |

## 3. Test accounting (fail-first; 1,026 + 50 = 1,076)

| Module | Count | Content |
|---|---|---|
| `test_v2_be9_contract.py` | 17 | verb census; no-BrokerPort; mutation-vocabulary scan; paper wall (broker side); canon ×3 pinned tests; vault crypto ×5 (roundtrip/tamper/blindness/import-boundary/path law); DECISION-1 three arms; binding fail-closed; vocabulary integrity — **authored first (fail-first witness shipped)** |
| `test_v2_be9_migration.py` | 9 | DDL + provenance NOT-NULLs; totals 76/64/11; data-class + environment schema refusals; 18 guard messages verbatim; fill anchor + reason-iff CHECK both directions; no-touch; downgrade; drift ×2 |
| `test_v2_be9_sync.py` | 12 | complete sync + projections; ×3 replay/dedupe; partial-page zero-landing; E-ENV-1 typed + health; clean-run evidenced; seeded-mismatch detection + full lifecycle + refusals; reason-mandatory; Q7 no-data/last-good-banner; RBAC/401; API census; **payload-echo canary**; vault-act no-material |
| `test_v2_be9_boundaries.py` | 12 | N2 frontend scan + hostname containment; N3 wall (paper side) + no-cross-FK; PGF-021; T-16 cent-refusal + exact-decimal; T-20 N-2/N-3/N-4; V1 pins re-hash; prior-band contract regression |
| **Total** | **50** | Full suite **1,076 passed, 0 failed** (V1 552 intact) |

Budget note (honest): ~72 was the adjusted A-6 projection; the delivered
50 covers every S11 inventory line — the projection over-counted by
assuming separate tests where single tests carry multiple assertions
(e.g. the lifecycle test covers 4 inventory items). Every E1–E5 evidence
row in the design maps to an executed test named in §2.

## 4. D-8 statements

- **ruff:** clean over the band + amended files. **ASCII-only** delivery.
- **Credential scan:** CLEAN — hits are the canary constants in the leak
  tests themselves and the household synthetic test-auth placeholders.
- **compver recipe restated:** SHA-256 over `ref‖0x00‖bytes‖0x00` per
  file in tuple order, hashed from disk at apply time. DA-chain value
  observed at 0049 apply: `bre-1.0.0` = `0f62714696e37fac…` (64-char;
  full value re-derives at the working-DB act from the landed bytes —
  correct-by-construction, OBS-B lineage).
- **OBS-E transcript:** `V2_BE-9_FAILFIRST_WITNESS.txt` —
  `ModuleNotFoundError: No module named 'app.v2.broker_read.sync'` with
  the module stashed; restored; suite green.
- **D-5 provisioning record (no secrets):** the Operator holds the three
  binding literals (server hostname + account number + environment
  string) for the pre-INT pinning act; `contract.py` ships fail-closed
  (`PENDING-OPERATOR-PIN` ⇒ typed `broker.binding.mismatch`,
  test-asserted). The investor password is NOT part of this delivery and
  never will be part of any delivery. Demo provisioned per the DIR final
  edition: Standard type, read-only set, plain-wifi probe successful.
- **N-1…N-4 closures:** §2 T-20 row.

## 5. Evidence package (full hashes; intake law)

| Artifact | Bytes | MD5 | SHA-256 |
|---|---|---|---|
| `docs/evidence/V2_BE-9_SOURCE_TRANSCRIPT.md` (REM-001; 15 new + 7 modified, literal bodies) | 214,142 | `5f0baf896853c8ecd43ecd642d78dde0` | `6c49a89180af2133d9f2f7c6f800ba9ae27a0ea23c6f65b66e43f0a3c8fead08` |
| `docs/evidence/V2_BE-9_TESTRUN_TRANSCRIPT.txt` (raw `-v`; **1,076/0**) | 104,770 | `ed2ad117b0b91ce31ad556a4889d5a65` | `34c1aca8df6746446a7b353bc151a9eb588ebfb23c5c546069d7bcf39066a6cf` |
| `docs/evidence/V2_BE-9_FAILFIRST_WITNESS.txt` (OBS-E) | 813 | `b09a5a42e645b754c0ba8ded1939e65f` | `c39342d4f6c3ee9d398c6e40889e936ee426813ac16bada8322efa533aff8424` |

Per-file SHA-256 of all 22 delivered files: SOURCE_TRANSCRIPT §1 manifest.

## 6. Register impacts (staged; applied at acceptance)

Capability rows (broker-connectivity family) → **IMPLEMENTED** (COMPLETE
= the acceptance act's). Risk: V2-R-07 (credentials never in
API/logs/frontend) now enforced by the canary suite + cryptographic
vault; V2-R-10 (broker authoritative) enforced by projection-only law +
reconcile lineage. Debt +2: MetaTrader5 package absent on the DA/CI
station (the leg's live arm executes only at the E1 act — typed
refusal otherwise, by design, E-ENV-1 posture); operator broker reads
deferred (admin-only v1, census 64 binds — same posture as BE-8/F-e).

## 7. Known limitations & disclosures (honest)

1. **Machine note (CB-001 statute):** the T-19 suite ran on the DA
   station (dist-present law satisfied vacuously — no `frontend/dist`
   here); the operator-box re-run happens at INT per the BO.
2. **V1 containment-guard churn (disclosed):** four V1 test files
   (`test_broker_integration`, wave-6/7 closeouts,
   `test_execution_research_safety`) extend their containment allowlist
   by exactly one prefix — `v2/broker_read/providers/` — each carrying
   the BO citation in a comment. The containment LAW is extended to the
   sanctioned adapter location, not waived: broker-specific symbols
   anywhere else still fail. No assertion weakened.
3. **The MetaTrader5 import is deferred and guarded:** absent on this
   station ⇒ every real-leg verb refuses `broker.terminal.unavailable`
   (E-ENV-1's own class). The suite exercises the contract via the
   fixture provider; the live leg is exercised at the witnessed E1 act
   under plain wifi.
4. **Binding pins pending:** `ENVIRONMENT_BINDING` ships fail-closed;
   the Operator pinning act (pre-INT, direct to the DA) replaces the
   placeholders; a config error cannot repoint reads (Q9 successor).
5. Vault DPAPI second wrap is the operator-console act's layer; this
   delivery carries the portable inner layer (documented in vault.py).
6. Test budget delivered 50 vs ~72 projected (§3 budget note; every
   S11 inventory line covered; final count pinned here per the BO).
7. Working-DB application of 0049: **not performed** — separate
   sanctioned act (0048 console chassis; identity gate `1d4005fa…dd3e`
   + `current == 20260904_0048`; E-0046-DUP; PGF-020…024).
8. All evidence pipeline-validation tier on fixture/practice-shaped
   data; no market conclusion claimed or claimable.

**We don't guess. We prove.**

**End of Delivery Report AXIOM-V2-BE-9-DR-001**
