# BO-V2-BE-10-001 — BUILD ORDER — BE-10: SIGNAL-AGAINST-ACCOUNT INTELLIGENCE
`STATUS: FOR OPERATOR COMMISSION — 2026-09-06 — DR accepted; survey evidence frozen;`
`BO-prelude COMPLETE (3 evidence cycles: inventory, suffix census, full 36-row map + sources)`

## B-0 — Evidence rulings carried in (sealed)
- **D-4 RULED (revised from DR fallback):** mapping layer = `v2_md_source` + `v2_md_symbol_map`
  extended with a FOURTH source. Broker namespace `exness_mt5_demo` absent from both
  (36 rows = 12 canonical × 3 non-broker sources) ⇒ migration seeds
  `exness_mt5_demo` source row + exactly 12 map rows (`EURUSDm→forex.eurusd`, …
  incl. 8 forex / 3 crypto / 1 metal canonical set). **Zero new tables confirmed.**
- **Census baseline (pre-band, witnessed):** compver 11 · permissions 64 · triggers 76 ·
  22-pin corpus · brokers tops carrying first real rows (2/2/1/319×2/2) · signals empty
  (0 — `flat_no_signal`/fixture-verified until signals appear).
- **Read shapes pinned:** positions/orders/fills columns (witnesses),
  `v2_signal_record` columns (incl. `instrument_id`, `state`, `expires_at`) — join keys named.

## B-1 — Body set (files to be authored; corpus pins freeze at acceptance)
1. `app/v2/account_context/__init__.py` — band package (N1/N4 declarations).
2. `app/v2/account_context/contract.py` — typed envelope + **closed verdict enum**
   (`aligned|opposed|unsignalled_holding|signal_without_holding|flat_no_signal|indeterminate|unmapped`)
   + refusal taxonomy (`account_context.no_basis`, `account_context.mapping_artifact_absent`)
   + wording-law declaration (state nouns only).
3. `app/v2/account_context/engine.py` — the join: basis law (newest complete sync),
   instrument map resolution (explicit seeded rows ONLY; miss → `unmapped` + census),
   signal join (`v2_signal_record` by canonical `instrument_id`, state/expiry aware),
   verdict computation, digest over `(sync_run_id, map rowset, signal pins, ace version)`.
4. `app/v2/account_context/api.py` — TWO GETs:
   `GET …/account-context/alignment` (the matrix), `GET …/account-context/summary` (census).
5. `alembic/versions/20260908_0050_v2_be10_account_context.py` — seed-only migration:
   (a) compver row `account_context_engine | ace-1.0.0 | <sha-of-engine-body at acceptance>`;
   (b) permission `v2.account_context.read` (+ role rows per BE-9 ROLE-ROW convention);
   (c) `v2_md_source` row `exness_mt5_demo`; (d) 12 `v2_md_symbol_map` rows (suffixed forms).
   INSERT-only; zero UPDATE/DELETE; `downgrade` reverses exactly those inserts.
6. Tests (~budget 30): `tests/test_v2_be10_contract.py` (enum closed, wording scan,
   refusal shapes), `tests/test_v2_be10_boundaries.py` (banned-import set
   {providers.exness_mt5, vault, MetaTrader5, socket, network} absent; zero-mutation
   verb census on module), `tests/test_v2_be10_engine.py` (table-driven verdict matrix,
   determinism ×3 on fixtures, basis law, staleness banner, `unmapped` census law),
   `tests/test_v2_be10_api.py` (both GETs: envelope, RBAC 404/403 paths, banner carriage),
   `tests/test_v2_be10_migration.py` (census 76/65/12, seed idempotency, no-writes guard).

## B-2 — Laws under construction (every one a test)
L1 GET-only; L2 zero broker_* writes; L3 banned imports; L4 basis fail-closed;
L5 closed enum + state-nouns-only vocabulary; L6 unmapped visible (never filtered);
L7 digest determinism (×3); L8 banner end-to-end; L9 RBAC new-permission gates both routes;
L10 seed-only migration, reversible exact.

## B-3 — Census expectation at band acceptance (tattoo)
triggers **76** · compver **12** · permissions **65** (+role rows per convention) ·
suite **1,077 + band tests** · corpus pins = 22 + BE-10 body SHAs.
File fingerprint changes only via the 0050 seed act; drift law (enumeration) applies.

## B-4 — Protocol (inherited from BE-9, zero improvisation)
BUILD (DA authors bodies, corpus SHAs frozen) → INT (sandbox: apply 0050 on clone,
verify census, suite band + full) → E1-style evidence (sandbox live calculus:
fixture basis + fixture signals → matrix, ×3 digest reproduction) → acceptance doc
(census tattoo + pins) → operator-signed apply act on the working DB (P-1…P-5 pattern)
→ first-read witness → closeout. No step self-promotes.

## Commission request
Operator commissions BUILD with this order (same signing formula as BE-9's BO).
Deferred decisions bound in law, not discretion: the 12 map-row literal pairs are
sealed HERE (below) — build may not invent others:
EURUSDm,GBPUSDm,USDJPYm,AUDUSDm,USDCADm,USDCHFm,NZDUSDm,EURGBPm,
BTCUSDm,ETHUSDm,SOLUSDm,XAUUSDm → their canonical twins listed in survey §S.
