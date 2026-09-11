# DELIVERY REPORT — AXIOM V2 BE-3 P2: Bounded Provider Contract Evaluation (Non-Network Delivery)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-3-P2-DR-003 (supersedes DR-002) |
| Build Order | BO-V2-BE-3-P2-001 (authority: ITRGA-DET-V2-BE-3-P2-PLAN-001 + ITRGA-DET-V2-BE-3-P2-ENT-001) |
| Governing plan | AXIOM-V2-BE-3-P2-DA-PLAN-001 v3.0.0 |
| Date | 2026-08-25 |
| Author | Development Authority (DA) |
| Status | **CORRECTED AND RESUBMITTED** (CAR-001 for DEL-001…004 [accepted]; CAR-002 for DEL-005) — mandatory pre-network gate (BO §4) |
| Parent baseline | BE-3 P1 approved head `20260824_0040` |
| P2 Alembic head | `20260825_0041` |
| Provider state after migration | `twelvedata · architecture_candidate · verified(entitlement) · persistence_permitted=false` |

---

## 1. Executive Summary

The P2 contract-test capability is implemented exactly as ordered — and
verified **entirely without a credential or network call**: the outbound
socket guard is active across the whole P2 suite, the transport was mocked
for the full-run test, and no provider payload can persist anywhere.

DA verification after DEL-001…005 corrections: **733 tests executed, 733
passed, 0 failed** (552 V1 + 78 BE-1 + 45 BE-2 + 33 BE-3 P1 + 25 P2). V2
lint scope clean. Key correction: audit events are now COMMITTED per event
(durable pre-call gate), every transport failure receives a durable
completion, the construction-token test is path-exact, and the historical
0038 seed is revision-local — the P2 permission provably absent before
`20260825_0041`.

Per BO §§4–5, this delivery must be ITRGA-reviewed **before** any Operator
network-run instruction is issued. A successful review does not itself
authorize the run; a successful run does not authorize promotion (§7).

## 2. Scope Delivered (BO §3, complete)

| BO item | Delivered |
|---|---|
| §3.1 Credential boundary | `providers/credentials.py` — sole resolver module; env (`AXIOM_TD_API_KEY`) + file (`AXIOM_TD_API_KEY_FILE`) backends; placeholder/empty → explicit ABSENT; value excluded from repr/str/globals; import-boundary test proves no other module references the variable; P1 `FixtureCredentialResolver` remains default everywhere else |
| §3.2 Network boundary | `providers/transport.py` — sole network module; fixed host `api.twelvedata.com`; HTTPS + certificate verification only (no insecure switch exists); fixed 5s/15s timeouts; no redirects; no WS; **construction token-gated to the authenticated endpoint chain**; httpx imported lazily inside execute; P1 socket guard retained for all non-P2 tests |
| §3.3 Authenticated invocation | `POST /api/v1/v2/marketdata/providers/twelvedata/contract-test` — admin-only `v2.marketdata.provider.contract_test` (SAL-4), JWT auth, server correlation, generic denial; **no CLI or alternate path exists** |
| §3.4 Preconditions | All five gates implemented + default-deny matrix tests (all-absent and each-independently-blocking); failures → honest refusal + durable BE-1 refusal audit; zero attempts |
| §3.5 Durable audit sequence | start → durable `call_started` before every attempt (no durable start = no attempt — proven by transport-invocation counter) → `call_completed` → `complete`; completion failure → hard stop + independent incident marker (SECURITY log + marker file, not the failed DB path) + `indeterminate-after-start`; E.5-only evidence fields |
| §3.6 Budget | `AttemptBudget(35)`; debit before every attempt incl. AUTH probes and retries; BO's fixed allocation verified to total exactly 35 (2+12+18+2+1); retry-storm test bounds worst case at 35; post-exhaustion refusal without transport construction |
| §3.7 Request planner | 16 calls: AUTH×2 (valid + deliberately-absent-key), BARS-DEEP×3, SYMBOL-SWEEP×9 (all 12 canonical instruments covered), QUOTE×1, SYMBOLS-NEG×1; unknown shapes → delta findings, never silently normalized; bodies transient (sole reference dropped after hash/validation) |
| §3.8 Entitlement migration | `20260825_0041` — records ONLY the ITRGA-reviewed entitlement (Basic; 8/min; 8 WS; 800/day; evidence ref ITRGA-DET-V2-BE-3-P2-ENT-001); `source_status` unchanged; `persistence_permitted` false; dialect-aware guard drop/update/recreate (PG trigger+function; SQLite dual triggers); `_verify_guard_present` fails the migration loudly if the guard did not return; interruption-detection test proves it; downgrade restores P1 state fully |

### BO §2 absolute-restriction compliance

No credential received/held/logged in any form; no network request of any
kind executed (socket guard proof); no payload retained; no status change,
history append, authority activation, or transition writer; the displayed
entitlement allowance does **not** amend the 35-attempt cap (recorded in the
migration note itself).

## 3. Implementation Inventory

**New (6):** `providers/credentials.py`, `providers/transport.py`,
`providers/contract_test.py`, `api/contract_test.py`, migration
`20260825_0041`, `tests/test_v2_p2_contract_test.py` (23 tests).
**Modified (5):** RBAC permissions (contract_test, admin/SAL-4), marketdata
router mount, and three bounded generational test scopings (BE-2/P1
lifecycle revision-scoping; P1 static scan excluding the sole authorized
transport module) — all documented in the transcript.

Full SHA-256 manifest + literal contents:
`docs/evidence/V2_BE-3_P2_SOURCE_TRANSCRIPT.md`.

## 4. Verification

| Check | Result |
|---|---|
| Full suite | **731 passed, 0 failed** (3:25) |
| P2 suite | **23 passed** (socket guard active throughout) |
| V2 lint | All checks passed |
| SQLite migration lifecycle | upgrade → verified entitlement/unchanged status/guard restored + refusals → zero P2 drift → downgrade (full P1 restoration incl. permission removal + guard refusal) → re-upgrade |
| Interruption recovery | Manually-removed guard detected: `_verify_guard_present` raises "NOT restored" |

## 5. Known Limitations / Open Items

1. **Operator PostgreSQL verification outstanding** (BO §6) — pre-redacted
   pack in evidence annex §4.
2. **Operator network run** is separately gated (BO §5): only after ITRGA
   accepts this delivery; single bounded run; pre-redacted transcript only.
3. Live provider behavior remains NOT PROVEN until that run; all schema
   expectations are fixture-derived.
4. Inherited V1 lint/drift debt unchanged.

## 6. Handover

| Item | State |
|---|---|
| Evidence | `docs/evidence/V2_BE-3_P2_SOURCE_TRANSCRIPT.md` + `docs/evidence/V2_BE-3_P2_EVIDENCE.md` + **`V2_BE-3_P2_CA_RESPONSE_DELIVERY-001.md`** (DEL-001…004, accepted) + **`V2_BE-3_P2_CA_RESPONSE_DELIVERY-002.md`** (DEL-005 fail-closed final audit) |
| State docs | `V2_CURRENT_STATE.md` v13.0.0; registers updated |
| Git | No DA Git operation; custody remains Operator-only |
| Next | (1) ITRGA reviews this non-network delivery; (2) Operator PostgreSQL pack; (3) if accepted — Operator receives the credential-safe execution checklist for ONE bounded run; (4) promotion remains outside P2 entirely (BO §7) |

**We don't guess. We prove.**

**End of Delivery Report AXIOM-V2-BE-3-P2-DR-001**
