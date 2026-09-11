# ITRGA DETERMINATION — BO-F-01
## Assistant Input Surface (the ask path)

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_F-01.txt` |
| Build Order | `BO-F-01` (Operator-authorized 2026-08-21) |
| Predecessors | B-06 (backend ask path) · F-00 (design foundation) · BO-B-AUDIT CLOSED · custody decision recorded |
| Date | 2026-08-21 |
| Evidence standard | Level I (direct) / Level II (executed) / Level III (documentary) |

---

## 1. What I verified (Level I/II — reproduced in my custody)

| Check | Result |
|-------|--------|
| **CA-TRANSMIT-1** | **HONORED** — all 10 declared artifacts present, all 10 hashes match |
| Patch `f01.patch.txt` sha256 | `a9623927…` — **matches** |
| `git apply --check` + apply | **Clean** (exit 0) — register-in-patch applied onto my drifted register |
| Patch composition | 5 files (4 frontend + register), **zero backend** — correct |
| Ask client | `askAssistant(prompt, groundingSourceIds)` → POST `assistant-respond` (Bearer), + `useAskAssistant` hook — genuine |
| Composer | Accessible labelled input, grounding picker (8 families, ≤10 cap), grounded/refusal rendering, honest empty/401/error states |
| Boundary | "Strictly zero order/trade execution controls" — no-actuation scan **zero violations** |
| New F-01 tests | **17/17 passed** |
| **Full frontend suite** | **930 passed / 183 files, 0 failures** (environment-count difference vs DA's 906/176 — see OBS) |
| Capture log | Real B-06 round-trip: grounded `r=0.7321` + source id + audit-correlation; Enter-key submit; classed refusal; a11y labelled |

## 2. Acceptance criteria vs. Build Order — line-by-line

| BO §8 requirement | Status |
|-------------------|--------|
| `askAssistant` POSTs to correct endpoint with Bearer; GET unchanged | ✓ |
| Input + submit + grounding selector accessible | ✓ (label, in-form, keyboard Enter proven in capture) |
| Grounded ask renders summary + source ids + disclaimer + audit correlation | ✓ (capture + test) |
| Each refusal class renders distinctly and honestly | ✓ (`Refused: ORDER_INSTRUCTION_REFUSED` + disclaimer) |
| Empty-grounding and 401 handled (no fabricated response) | ✓ |
| No actuation controls in the surface | ✓ (zero-violation scan) |
| Register rows in the patch | ✓ (pure-addition, applied onto drifted register) |
| Full suite + typecheck green | ✓ |

**All acceptance criteria met.**

## 3. The pivotal property — the assistant is now genuinely usable

The frontend half of FIND-3 is closed. The assistant is no longer a row of cosmetic prompt chips: it is a **real ask surface** that round-trips to the B-06 backend. The capture proves a genuine grounded answer (`Correlation BTCUSDT/ETHUSDT r=0.7321 n=17520` with source id + audit correlation), a classed refusal, and Enter-key submission — with a zero-violation no-actuation scan.

The boundary held throughout: grounded (operator-selected artifacts), deterministic-local, no external LLM, no execution controls, honest empty/401 states. This is the assistant the Vision & Principles described — an evidence-grounded research companion, not a generative actor.

## 4. Observations (non-blocking)

- **OBS-F01-1 (Info):** my full-suite count is 930/183 vs the DA's 906/176 — the same test-file-count environment difference observed in F-00 (my clone carries additional test files from earlier units; the 17 F-01 tests are identical; 0 failures in both). No discrepancy in the work.
- **OBS-F01-2 (Info, carried):** dataset snapshots are absent from the grounding picker (no client-side GET exists). Correctly disclosed (D3) and honest — the picker's note states the empty case. A future client GET for snapshots would complete the family coverage; not a defect.
- **Carried:** OBS-B-AUDIT residual (file-sqlite business-write serialization — future backend unit); the two react-router MODERATE advisories (pending RR7 migration order).

## 5. Determination

| Field | Value |
|-------|-------|
| Determination | **APPROVED WITH OBSERVATIONS** |
| Basis | All acceptance criteria met; 17/17 new + full suite green; real B-06 round-trip verified; zero-actuation scan clean; register-in-patch honored |
| Observations | OBS-F01-1, OBS-F01-2 (non-blocking) |
| Next authorization state | **F-01 CLOSED** — F-02 (signal presentation) may be issued |
| What this is not | Not production certification; not gate-opening; not authorization beyond BO-F-01 |

## 6. Record

- Patch: `a9623927701474eadb3c308cb87a096e21f28f60d8e247abc29898dba7e7a9bb`
- 17/17 new tests · full suite 930/183 green · register-in-patch verified
- Ask path verified end-to-end: grounded answer + refusal + empty/401 + no-actuation

> **We don't guess. We prove.** The assistant is now a real, grounded, non-actuating ask surface — an operator can actually ask it a question and get an evidence-backed answer or an honest refusal. The frontend is no longer cosmetic. Approved.

**End of ITRGA Determination BO-F-01**
