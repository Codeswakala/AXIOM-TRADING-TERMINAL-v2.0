# DELIVERY REPORT — BO-B-00
## Backend Integrity & Reproducible Baseline

| Item | Value |
|---|---|
| Build Order | `BO-B-00` (Operator directive of 2026-08-19: "first build order authorized") |
| Implementer | AXIOM Development Authority (DA) |
| Reviewer | Independent Technical Review & Governance Authority (ITRGA) — determination pending |
| Date | 2026-08-19 |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 1. Claimed scope vs. this Build Order

| BO requirement | Delivered | Where |
|---|---|---|
| B-00.1 clock model fixed, stated as (a) or (b) | **(a) wall-clock bind** — stated §3 | `backend/app/market/adapters/simulated.py` |
| B-00.1 soak: zero candles `open_time > utc_now()` | **0 future-dated** across both soaks (Level-I output) | `docs/evidence/uiconv/b00_soak_r1.log` |
| B-00.1 chronology guard passes against corrected feed | **Passed, 0 FUTURE_OPEN_TIME quarantines** (+ negative control proving the guard not weakened) | `tests/test_b00_simulated_clock.py` |
| B-00.1 invariant test pinned (Level II executed output) | **4 pinned tests**, fail-first proven | `b00_probe_prefix.log`, `b00_pinned_postfix.log` |
| B-00.2 dependency audit + classification | `pip-audit 2.10.1` run; 2 findings, both classified + formally noted | §5, `pipaudit_b00_r1.log` |
| B-00.2 no unaccepted critical/high | **0 unaccepted** — the one HIGH is a formally accepted, documented exception (no fix published, unreachable path) | §5 |
| B-00.3 executed test baseline + reconciliation | **480 executed** (71 files), reconciled against PROJECT_STATE.md with the discrepancy explicitly reported | §6, `pytest_b00_postfix.log` |
| B-00.4 Provenance & Landing Protocol | Written, binding for all subsequent units | `backend/docs/PROVENANCE_LANDING_PROTOCOL.md` |
| §3 exclusions honored | No new features, no frontend changes, no real data source, no gate/actuation, no ML work, no governance-document changes, no repository publication | — |

## 2. What changed (files + SHAs)

Patch artifact: **`b00.patch.txt`** — sha256 `5662ec3d1dc7dcc0087a27a45e7f1993333413b6a1686fc20d3abffe616f55bd`
- Applies clean (**`git apply --check` exit 0**) onto the verified 18-element chain over baseline `34f4c62`, in a pristine clone, as the **19th chain element**; post-apply, all three files byte-identical to the DA workspace (cmp-verified).

| File | Content SHA-256 |
|---|---|
| `backend/app/market/adapters/simulated.py` | `dddb7046469d9a038244873d6317611e800a41dd040f2c8e080822d11be7fac4` |
| `backend/tests/test_b00_simulated_clock.py` (new) | `29eb50e31ed724be101bdecb038ed6e99add37535c84910418cfa859e80809ea` |
| `backend/docs/PROVENANCE_LANDING_PROTOCOL.md` (new) | `17bf431e000dd0ea1bf77bc2dde0803c6c7137b1d642757825fcc39d7bbcee0f` |

Per R5 of the new protocol: no commits, pushes, or pulls — the patch artifact is the record (custody model; Operator standing instruction).

## 3. Chosen clock model: (a) wall-clock bind — and rationale

**The adapter now emits bar `N` only when the wall clock has reached `start_time + N minutes`; while the simulated clock is behind the wall clock (fresh start, restart, catch-up), emission proceeds at the configured accelerated tick cadence. The invariant: no emitted bar is ever dated in the future (`open_time ≤ utc_now()` at emission).**

Mechanism (all inside the authorized file): an injectable wall clock (`now_fn`, default UTC — the only new constructor parameter), a `_candidate_open_time()` computation, and a `_hold_until_due()` gate in the emission loop that waits in ≤`interval` slices so `stop()` stays responsive. `_next_candle()` is unchanged — the bar content logic (CA-DATA1-1/CA-DATA1-2 corrections) is untouched.

**Why (a) over (b):** the BO's binding invariant, soak criterion, and guard criterion are all written for the no-future-bars model; option (b) (accelerated-clock label) requires a new data state propagated consistently through persistence and the UI ("never presented or persisted as live", "a partial label is a defect"), which the BO's own exclusions put out of reach — §3 excludes frontend changes and §11 excludes schema migrations. (a) is fully contained in the authorized file, strengthens the as-of discipline (FIND-5's actual complaint), and is robust to wall-clock jumps in either direction (documented sandbox instability): a forward jump accelerates catch-up; a backward jump re-holds the feed — no future bars either way.

## 4. Test evidence (executed, not asserted)

**4.1 Fail-first probe (right-reason failure pinned pre-fix).** `b00_probe_prefix.log` — probe failed against the pre-fix adapter with the defect itself:
```
AssertionError: FUTURE-DATED BARS DETECTED: emitted within 0.40s of wall time,
dated ['2026-08-19T16:54:00+00:00', '2026-08-19T16:55:00+00:00']
(wall bound 2026-08-19T16:53:05.400593+00:00)
```
(First probe attempt taught the evidence, not the code: the sandbox wall clock can jump forward minutes within a sub-second sleep — the probe was rebuilt against a monotonic elapsed-time bound, immune to wall-clock jumps, and then failed for the right reason.)

**4.2 Post-fix behavior change.** The same probe post-fix fails inversely (the feed no longer emits 3 accelerated bars from a wall-clock-started feed; it emits 1 and holds) — transcript in `b00_probe_prefix.log`. The probe was then removed: it was this unit's pre-fix evidence tooling, never part of the 476-test baseline, and its premise is the old defective contract (see §7, D2).

**4.3 Pinned invariant suite — 4/4 passed** (`b00_pinned_postfix.log`, `tests/test_b00_simulated_clock.py`):
1. catch-up emission accelerated + never future-dated + strictly one-minute-stepped (fake clock);
2. feed holds at the wall clock and resumes exactly when the clock advances (fake clock);
3. corrected feed passes `ChronologyGuard` with zero `FUTURE_OPEN_TIME` quarantines + negative control (the guard still rejects a genuinely future record — invoked, not weakened, per BO §6);
4. real-clock catch-up smoke (jump-tolerant: wall-clock comparison applies only if the wall clock did not move backwards mid-test).

**4.4 Soak evidence (Level I).** `b00_soak_r1.log`. Wall-minute soak at production defaults (interval 1.0s): bar 1 (`16:56:00`) emitted at start (`16:56:28.59`); bar 2 (`16:57:00`) emitted at **`16:57:00.001`** — held 31.4s and released precisely when the wall clock reached the bar's minute. Both soaks: `FUTURE_DATED_COUNT=0`, strictly stepped, no duplicates. (Catch-up soak: 120 catch-up bars emitted, zero future-dated; the sandbox wall clock jumped forward ~2h mid-run — the wall-minute soak's stable window is the binding proof.)

**4.5 Existing live-market suite unaffected — 10/10 passed** (same log): both direct adapter tests use past `start_time` (catch-up cadence unchanged); API-driven tests require ≥1 message (bar 1 emits immediately at start).

**4.6 Full backend suite — `480 passed, 1 warning in 132.60s`** (`pytest_b00_postfix.log`): 476 baseline + 4 new pinned; **0 failed, 0 skipped**. The test floor was extended, never reduced, and no failing test was deleted to force green.

**4.7 Clone-side proof.** The applied patch's content was re-executed in the pristine+chain clone (workspace venv for deps, clone code under test): 4/4 passed, ruff clean.

## 5. Dependency findings and classification (B-00.2)

`pip-audit 2.10.1` against the fresh venv — raw output `pipaudit_b00_r1.log`:

| Package | Version | Advisory | CVSS | Fix | Classification |
|---|---|---|---|---|---|
| ecdsa (transitive of python-jose[cryptography]) | 0.19.2 | PYSEC-2026-1325 — Minerva timing attack on P-256 (`SigningKey.sign_digest()`, ECDH, keygen) | **7.4 HIGH** (AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N) | **none published** (PYSEC lists no fixed version; 0.19.2 is current) | **Transitive · no-fix · unreachable path → formally accepted exception.** AXIOM's JWT flow is HS256 (`settings.jwt_algorithm` default `"HS256"`; `security.py` encodes/decodes with the configured secret — no ES* path exists), and `ecdsa` is never imported by application code. The vulnerable signing path cannot execute in this application. Exception noted below and in the register; revisit when upstream publishes a fix. |
| pytest (dev/test dependency) | 8.4.2 | PYSEC-2026-1845 — `/tmp/pytest-of-{user}` tmpdir pattern allows local DoS/privilege | **6.5 MEDIUM** (AV:L/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L) | 9.0.3 — **outside the pin range** `pytest>=8.3.0,<9.0.0` | **Dev-only · local-attacker vector · fix outside pin range → formally accepted exception.** BO §7 requires respecting the pin-range policy unless an advisory forces a targeted bump; a medium, local-only, dev-tool advisory does not force a major-version range change mid-unit. Candidate for a future dependency-hygiene unit (adopting 9.x requires the full suite re-run). |

Acceptance read-out: **0 unaccepted critical/high findings** (the HIGH is formally accepted via the exception above, recorded in the register as TD-B00-ECDSA-EXCEPTION); all findings classified (transitive / dev-only / no-fix / fix-outside-range); exceptions documented and formally noted — not silently waived; **no lockfile/pin changes applicable** (no fix exists for ecdsa; the pytest fix violates the pin-range policy). No backend dependency changed by this order.

## 6. Reconciliation against PROJECT_STATE.md (B-00.3)

| Source | Figure |
|---|---|
| PROJECT_STATE.md (UI-CONV-P02 baseline, 2026-08-15) | "162 suites / 736 tests · **415 backend**" |
| PROJECT_STATE.md (UI-007-P05/P06 final baseline, v0.62.0) | "**backend 414**" |
| **Executed, pre-B-00** (2026-08-19, recorded) | **476 passed / 0 failed / 0 skipped** — `pytest_capassess_r1.log` |
| **Executed, this delivery** (post-B-00) | **480 passed / 0 failed / 0 skipped**, 71 backend test files, 132.60s — `pytest_b00_postfix.log` |

**Discrepancy — explicitly reported, per the BO's instruction.** The executed suite exceeds the PROJECT_STATE.md inventory by 62–66 tests. The inventory figures are frozen at the v0.62.0 baseline; the eight approved convergence phases added backend tests after that inventory was last written — visibly: DATA-P01 generator-determinism tests, DATA-P02 aggregation suites (`test_data_p02_aggregation.py`), CHART-P01/P02/P03 indicator + market-structure suites (`test_chart_p01_indicators.py`, `test_chart_p02_indicators.py`, `test_chart_p03_market_structure.py`), POLISH-P01 drift tests (`test_polish_p01_drift.py`), plus the earlier chart/annotation files — 7 phase-tagged files among the 71 executed. **Inventory ≠ executed result; the document is stale, nothing was fabricated, and the executed transcript is the record of record.** Recommendation: update PROJECT_STATE.md's test inventory at the next unit that touches documentation (not done here — outside BO §6 allowed files).

## 7. Deviations register

- **D1 — Evidence form for "commit ref + diff" (BO §9).** The Operator's standing custody instruction forbids commits/pushes; the repository is Operator-controlled storage. The DA delivered the equivalent under the established transport: diff-as-patch artifact with sha256 + per-file SHAs + `git apply --check` exit-0 transcript in a pristine clone. No commit refs exist anywhere in the chain (18 prior elements identically).
- **D2 — Pre-fix probe file removed after evidence.** `tests/test_b00_clock_probe_pre.py` was created this unit as fail-first evidence tooling (never part of the 476 baseline). Its premise is the pre-fix defective contract; post-fix it fails by design (proven in `b00_probe_prefix.log`). It was removed so no failing test remains in the suite; both transcripts are retained on the record. The pinned suite (`test_b00_simulated_clock.py`) carries the invariant permanently.
- **D3 — Rate measurement.** The BO problem statement cites "~2 s tick (~30×)"; the adapter default is `interval_seconds=1.0` → **~60×** (the roadmap's figure). Same defect class; the fix is identical under either number.
- **D4 — Audit tool.** `pip-audit` used, as the BO permits ("e.g. pip-audit"); installed at runtime in the local venv only (not added to requirements — tooling, not a dependency).
- **D5 — Sandbox wall-clock instability, disclosed.** The sandbox wall clock jumped forward ~2h during the catch-up soak and minutes within sub-second sleeps elsewhere. All evidence instruments were made jump-tolerant (monotonic bounds); the binding soak (wall-minute) ran in a stable window. The fix itself is robust to both jump directions.
- **D6 — Soak script not in the patch.** `backend/scripts/b00_soak.py` is DA evidence tooling (untracked, like the phase capture scripts); the patch ships code+tests+protocol only, per BO §6's allowed-file list. The script's output log is hashed evidence.

## 8. Known limitations / remaining risk

1. **Live cadence consequence of (a):** once caught up, the feed emits one M1 bar per real minute — the honest cadence of M1 bars. Watchlist/telemetry update ~1/min while caught up; the chart keeps six days of seeded history plus the live tail. Any presentation-level cadence concern is frontend territory (F-00+), out of scope here.
2. **ecdsa HIGH remains until upstream publishes a fix** — mitigated by the unreachable-path analysis; formally accepted as an exception (register TD-B00-ECDSA-EXCEPTION).
3. **Chronology discipline is adapter-local.** The fix covers the simulated adapter per scope; any future real-provider adapter needs its own chronology discipline, with the W2-U01 ChronologyGuard at ingestion as the backstop.
4. **PROJECT_STATE.md inventory remains stale** (§6) — flagged for a future documentation unit.

## 9. Technical-debt entries

`docs/governance/TECHNICAL_DEBT_REGISTER.md` updated (workspace record, disclosed):
- **TD-UI-CAPASSESS-SIMCLOCK** → status: *Implemented by BO-B-00 (option (a), wall-clock bind); patch `b00.patch.txt` `5662ec3d…`; fail-first proven; soak 0 future bars; awaiting ITRGA determination.*
- **TD-B00-ECDSA-EXCEPTION** (new) — HIGH, formally accepted exception; no fix published; unreachable path (HS256-only); revisit on upstream fix.
- **TD-B00-PYTEST-EXCEPTION** (new) — MEDIUM, dev-only; fix outside pin range; future hygiene-unit candidate.
- **TD-B00-UNIT** (new) — unit row: executed counts, patch sha, chain position, status awaiting ITRGA.

## Evidence inventory (all hashes verified on disk this session)

| Artifact | sha256 |
|---|---|
| `b00.patch.txt` (patch artifact, chain position 19) | `5662ec3d1dc7dcc0087a27a45e7f1993333413b6a1686fc20d3abffe616f55bd` |
| `docs/evidence/uiconv/b00_probe_prefix.log` (fail-first + post-fix inverse) | `adabe8492f0f759731fe56c2a5307f4296570883ec3a8273b093802fd8f353ff` |
| `docs/evidence/uiconv/b00_pinned_postfix.log` (4 pinned + 10 live-market) | `ab43a69eea54ed41c323a5014500f7dfa36a4eb9f2e00efb2dd08c2904a3d747` |
| `docs/evidence/uiconv/b00_soak_r1.log` (Level-I soak, 0 future-dated) | `5b8af1c35f9c4e5c031a905bb0a8d208ec9aa93bf152a019bb33e8c77ba251b0` |
| `docs/evidence/uiconv/pytest_b00_postfix.log` (480 passed) | `1c4fa5284eae21c43501dc8c101294d234fc52307491b9e617bf7d40e5f34d99` |
| `docs/evidence/uiconv/pipaudit_b00_r1.log` (audit raw output) | `110e9deb70c28aa7c9608766d8309b2543497239deaf0fb5ed07987ea0f2754b` |
| `docs/evidence/uiconv/pytest_capassess_r1.log` (pre-B-00 executed baseline, 476) | `f214e11ac7eeed9f1828e3684b8ceb3b332967c73a16e6553f7e844db1d18527` |

---

Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
