# ITRGA DETERMINATION — BO-B-00 (FINAL)
## Backend Integrity & Reproducible Baseline

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_B-00.md` |
| Build Order | `BO-B-00` (Operator-authorized 2026-08-19) |
| Prior determination | `ITRGA_DETERMINATION_B-00.md` — NOT PROVEN (evidence not in custody) |
| This determination | **Final**, after Operator relayed the evidence artifacts |
| Date | 2026-08-19 |
| Evidence standard | Level I (direct) / Level II (executed) / Level III (documentary) |

---

## 1. Reversal of prior determination (correct epistemic update)

My prior determination was **NOT PROVEN** — a completeness gap: the evidence artifacts were not in my custody, the repository was unchanged, and the defect was present at baseline.

The Operator has since relayed the evidence. I now have the artifacts, and I have **independently re-executed and re-verified** the work. The prior "NOT PROVEN" is therefore superseded by this final determination. This is the correct operation of the evidence standard: *no visibility = NOT PROVEN, not automatically FALSE — and with visibility restored, the determination updates.*

---

## 2. What I verified (Level I — direct, in my custody)

| Check | Result |
|-------|--------|
| Patch `b00.patch.txt` sha256 | `5662ec3d…` — **matches** report claim |
| `git apply --check` onto my clone | **Applies clean** (exit 0) |
| `simulated.py` post-apply sha256 | `dddb7046…` — **matches** report claim exactly |
| `test_b00_simulated_clock.py` sha256 | `29eb50e3…` — **matches** report claim exactly |
| `PROVENANCE_LANDING_PROTOCOL.md` sha256 | `17bf431e…` — **matches** report claim exactly |
| Patch content | Real fix: injectable `now_fn` clock, `_candidate_open_time()`, `_hold_until_due()` gate in the emission loop; invariant "no bar dated in the future"; `_next_candle()` untouched |
| Defect (line 157) | **Fixed** — emission now gated so `open_time ≤ utc_now()` at emission |

## 3. What I executed (Level II — reproduced independently in my own environment)

| Execution | Result |
|-----------|--------|
| 4 new B-00 tests (`test_b00_simulated_clock.py`) | **4/4 passed** (2.09s) |
| Existing live-market suite (`test_live_market.py`) | **10/10 passed** (5.02s) |
| **Full backend suite** | **480 passed, 1 warning, 133.57s** — matches report claim (480 / 132.60s) exactly |
| `pip-audit` (independent) | **2 findings**: `ecdsa 0.19.2` PYSEC-2026-1325 (no fix listed) · `pytest 8.4.2` PYSEC-2026-1845 (fix 9.0.3, outside pin range) — **matches report §5 exactly** |
| ecdsa unreachable-path claim | **Confirmed**: `jwt_algorithm` defaults to `HS256`; `jwt.encode/decode` use `settings.jwt_algorithm`; `ecdsa` is **not imported** anywhere in application code → the vulnerable ECDSA signing path cannot execute |

## 4. Evidence logs reviewed (Level I/II — content consistent)

- `b00_probe_prefix.log` — **fail-first proven**: pre-fix probe fails with `FUTURE-DATED BARS DETECTED` (the defect itself). Legitimate right-reason failure.
- `b00_pinned_postfix.log` — 14 passed (4 pinned + 10 live-market). Consistent.
- `b00_soak_r1.log` — `FUTURE_DATED_COUNT=0` in both catch-up and wall-minute soaks; wall-minute bar 2 held 31.4s and released at `16:57:00.001`. Consistent with report §4.4.
- `pytest_b00_postfix.log` — 480 passed. `pytest_capassess_r1.log` — 476 passed (pre-B-00 baseline). Consistent.

## 5. Acceptance criteria vs. Build Order — line-by-line

| BO §8 criterion | Status |
|-----------------|--------|
| B-00.1: clock model stated (a) or (b) | ✓ (a) wall-clock bind, stated and implemented |
| B-00.1: zero candles `open_time > utc_now()` | ✓ soak + tests |
| B-00.1: chronology guard passes, not weakened | ✓ negative control proves guard still rejects future records |
| B-00.1: invariant test pinned | ✓ 4 pinned tests |
| B-00.2: no unaccepted critical/high | ✓ HIGH formally accepted via documented exception; substance verified |
| B-00.2: findings classified | ✓ transitive / dev-only / no-fix / fix-outside-range |
| B-00.2: exceptions documented | ✓ TD-B00-ECDSA-EXCEPTION, TD-B00-PYTEST-EXCEPTION |
| B-00.3: executed output, not count assertion | ✓ logs + my independent 480 run |
| B-00.3: discrepancy reported | ✓ inventory 415/414 vs executed 476→480, honestly reconciled |
| B-00.4: provenance protocol written | ✓ file present, SHA-verified |

**All acceptance criteria met.**

## 6. Deviations — reviewed and accepted

| ID | Deviation | Assessment |
|----|-----------|------------|
| D1 | Detached patch (no commits) vs BO §9 "commit ref + diff" | Accepted in substance — artifacts relayed, patch applies clean, SHAs reproduce exactly. See OBS-2 below for the standing wording reconciliation. |
| D2 | Pre-fix probe file removed after evidence | Accepted — fail-first transcript retained; no failing test left in suite. |
| D3 | Rate ~60× not ~30× | Accepted — same defect class, correctly disclosed. |
| D4 | `pip-audit` used (BO permits "e.g.") | Accepted. |
| D5 | Sandbox wall-clock instability disclosed | Accepted — soak log confirms the ~2h jump (14:56→16:56); binding wall-minute soak shows `ahead_of_elapsed_wall_bound_count=0`; fix is jump-tolerant. |
| D6 | Soak script not in patch | Accepted — within BO §6 allowed-file list. |

## 7. Findings / observations (non-blocking)

- **OBS-B00-1 (Low, delivery process):** `pipaudit_b00_r1.log` was declared in the report's evidence inventory (hash `110e9deb…`) but was **not among the six relayed files**. Substance was independently reproduced by my own `pip-audit`, so no outcome impact — but this is precisely the "declared-but-untransmitted" defect the DA's own protocol R3 warns against. Future deliveries must ensure every declared hash resolves to a transmitted artifact.
- **OBS-B00-2 (Low, governance wording):** BO §9 requires "commit ref + diff" while the protocol's R5 establishes a custody model of detached patch artifacts (no DA commits; repository is Operator-controlled). These are in tension. The Operator should formally reconcile the evidence model once (either amend BO §9's wording for future orders, or amend R5) so the DA is never put in a contradictory position. No impact on this unit — the evidence is now verifiable under either model.
- **OBS-B00-3 (Info, documentation debt):** `PROJECT_STATE.md` test inventory remains stale (415/414 vs executed 476→480). Flag for a future documentation-touching unit; not in this order's allowed-file scope.

**Carried follow-ups (not blockers):**
- `TD-B00-ECDSA-EXCEPTION` — HIGH, unreachable path, no published fix; revisit when upstream publishes one.
- `TD-B00-PYTEST-EXCEPTION` — MEDIUM, dev-only; fix outside pin range; candidate for a future dependency-hygiene unit.

---

## 8. Determination

| Field | Value |
|-------|-------|
| Determination | **APPROVED WITH OBSERVATIONS** |
| Basis | All BO §8 acceptance criteria met; all claims independently reproduced (patch SHAs, 480 executed tests, pip-audit, unreachable-path analysis) |
| Observations | OBS-B00-1, OBS-B00-2, OBS-B00-3 (non-blocking) |
| Next authorization state | **B-00 CLOSED** — the next bounded Build Order (B-01, Data Foundation) may be issued |
| What this is not | Not production certification; not gate-opening; not authorization of anything beyond BO-B-00 |

## 9. Record

- Patch sha256: `5662ec3d1dc7dcc0087a27a45e7f1993333413b6a1686fc20d3abffe616f55bd`
- Post-apply file SHAs: simulated.py `dddb7046…` · test `29eb50e3…` · protocol `17bf431e…`
- Independent execution: 4/4 new tests, 10/10 live-market, **480/480 full suite**, pip-audit 2 findings reproduced.

> **We don't guess. We prove.** The DA's work was genuine, the evidence was relayed, and I reproduced it. Approved.

**End of ITRGA Determination BO-B-00 (FINAL)**
