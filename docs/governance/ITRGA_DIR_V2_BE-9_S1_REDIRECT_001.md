# ITRGA DIRECTION — BE-9 Provider Redirect (O-1 resolved) + S1 Re-cut Scope for Design v1.1.0
# ITRGA-DIR-V2-BE-9-S1-REDIRECT-001 · v1.0.0 · 2026-09-05

- **From:** ITRGA · **To:** Replacement Development Authority (DA) · **Via:** Operator
- **Supersedes nothing; amends:** S1.1–S1.3 of `AXIOM-V2-BE-9-DESIGN-001` v1.0.0 only.
  The review `ITRGA-REV-V2-BE-9-DESIGN-001` stands in full; its own condition
  applies verbatim: a non-OANDA selection re-reviews S1.1–S1.3, and "the S1.4
  contract binds regardless".

## §1 — O-1 decision (Operator, 2026-09-05, on record)

- OANDA v20 is **unavailable in the operator's country**; the operator holds an
  **Exness** relationship. **Provider selection: Exness**, substrate = a locally
  installed **MetaTrader 5 terminal** on the operator console, credentials =
  a dedicated **demo account with the investor (read-only) password** set.
- This is a strict improvement on one axis: the investor password is a
  **provider-side structural read-only arm of N1** — the vaulted credential
  cannot submit, amend, or cancel anything AT THE BROKER, not merely at our
  type level (evidence-cited in ITRGA field note: Exness Personal Area
  "Set Read-Only Access"; MT4/MT5 investor-password standard flow).
- The operator's demo provisioning intent is AFFIRMATIVE ("so we can use it in
  BE-9"); final confirmation is carried to BO as before (ASSUMPTION A-1
  successor: provision demo account + set read-only access at BO prep).
  PROVISION PIN (operator guidance 2026-09-05): DEMO account, MetaTrader 5,
  "Standard" type (USD plumbing, no commission field; Standard Cent refused —
  cent-denominated balances pollute the money/reconciliation law; Pro/Raw/Zero
  tiers refused — needless commission/spread complexity; NO live account of
  any tier in this band). Vault credential = investor (read-only) password;
  sealed binding = exact server hostname + account number + environment string.
  STATUS 2026-09-05: DEMO ACCOUNT CREATED (operator, on record); MT5 desktop
  connectivity probe on plain wifi = SUCCESSFUL (operator, on record) —
  baseline provider reachability proven outside the governed act.
  STATUS 2026-09-05 (b): READ-ONLY ACCESS (investor password) SET on the demo
  (operator, on record; terminal-side set per MT5 law — the PA carries no
  toggle). N1 provider-side arm (a) HOLDS: the vault credential at BO is the
  investor password. Provider provisioning for v1.1.0 is hereby COMPLETE;
  ASSUMPTION A-1 successor discharged except the BO-time binding pins
  (server hostname + account number + environment string, operator-held). a
  pre-BO sanity probe (MT5 desktop login with the investor credential on
  plain wifi) is optional, operator-side housekeeping, no governed act.

## §2 — Environmental law (operator-reported; binding on the design)

**E-ENV-1 (MT5/proxy unavailability):** the operator reports MT5 connectivity
fails behind their proxy regime even after MT5 proxy-setting tuning; plain
wifi connectivity works and is the current posture. The design must therefore:
1. Treat **"MT5 terminal unavailable / not connected"** as a FIRST-CLASS typed
   class in the S1.3 taxonomy (e.g. `broker.terminal.unavailable`, distinct
   from `broker.unavailable` = remote/server-side failure) — pure fact,
   never an error improvisation.
2. Sync/reconcile attempts under that regime fail typed, land nothing, and
   record the fact into health (S7) — the design's existing all-or-nothing
   law already covers the landing law.
3. `reachable_stale`-style honesty extends to terminal state: health must
   separately show terminal process state (installed/running/logged-in) vs
   broker reachability vs data freshness — three independent facts, GREEN
   requires all three.
4. E1 sandbox evidence acts and sync runs are documented as executed under
   compatible connectivity (plain wifi); a BO-time runbook note records the
   operator's proxy windows as a sync-unavailable regime BY DESIGN.
5. The design must NOT promise proxy traversal; E-ENV-1 is recorded as
   environmental law, not a bug.

## §3 — Required S1 re-cut content (v1.1.0, in addition to C-1…C-3 of the review)

1. **S1.1 candidate rationale** re-cut for Exness/MT5 with the residency fact
   (OANDA unavailable; Exness held; FXCM eliminated on contradictory residency
   + demo expiry; MT5 cloud relays eliminated on N4 — third-party credential
   custody, investor password notwithstanding; cTrader/IBKR alternatives
   recorded as runner-ups with reasons).
2. **S1.3 adapter ↔ contract mapping:** the six closed read verbs map onto the
   official `MetaTrader5` Python integration (Windows-native — A-2 posture):
   account(s) → `account_info` (single-account connection; the "list" verb is
   a documented singleton with the account-number pin); balances →
   `account_info` money fields; positions → `positions_get`; orders →
   `orders_get`; fills/transactions → `history_deals_get`/`history_orders_get`
   over DECLARED time windows (paging = time-window law; window size +
   overlap policy stated; anchors for the fill idempotency law unchanged:
   broker-assigned ticket/position ids); instruments → `symbols_get` +
   `symbol_info` trade-mode/visibility facts. Every page's provenance blob
   pins: provider id, **server hostname**, account number, environment
   string, fetch basis (server-time vs local-time law stated), window.
3. **Q9 successor (binding, replaces the registry-literal rule):** the
   environment binding = code-pinned server hostname + account number +
   environment string in the sealed registry; re-asserted at every vault
   unlock AND at every sync start (mismatch = typed refusal + audit); pinned
   into every row's provenance. A config error cannot repoint reads because
   the binding is hash-pinned code, not config.
4. **Rate/time posture:** local-terminal envelope — no provider REST headers;
   state the fetch-budget law (C-1/C-2 review observation) as per-window
   limits; token-bucket rule replaced by a documented terminal-courtesy law
   (sequential calls, no parallel fan-out in v1).
5. **Health (S7 delta):** terminal state probe added per §2.3; `broker.
   terminal.unavailable` outcome counts; vault lock state as before.
6. **N1 arms restated:** (a) provider-side investor password (NEW, strongest);
   (b) type-level closed vocabulary (existing); (c) route census + scans
   (existing). Verbatim provider payloads in order/instrument tables remain
   subject to the payload-echo canary class (review non-blocking note — keep).

## §4 — Unchanged (do not re-open)

S1.4 contract shape; S2 vault (AES-256-GCM + Argon2id + DPAPI second layer —
the stored secret is now the investor password + account/server tuple; the
same blindness law applies to the tuple); S3 projections/data_class
'practice'-CHECK ('simulated' pin — demo money); S4 all-or-nothing sync;
S5/S6 reconciliation + discrepancy; S8–S12; migration recounts as amended by
C-2's resolution; E1–E5 mapping; honesty/assumptions registers (append the
A-1 successor + E-ENV-1).

## §5 — Deliverable

Design **v1.1.0** (byte-count + sha256 declared in the delivery note): C-1…C-3
landed + this direction's §3. ITRGA full-depth review of v1.1.0 follows on
receipt; answers from the Operator on O-2 (vault TTL) are welcome at any time
and can land at BO. Chain: REQ → DESIGN v1.0.0 → REVIEW (PASS w/ corrections)
→ REDIRECT (this document) → **DESIGN v1.1.0 → acceptance → BO (zero-code).**

— ITRGA-DIR-V2-BE-9-S1-REDIRECT-001 · v1.0.0 · 2026-09-05
