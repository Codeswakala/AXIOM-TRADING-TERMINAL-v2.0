# ITRGA DETERMINATION — BO-B-06
## Governed Assistant Ask Path

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_B-06.txt` |
| Build Order | `BO-B-06` (Operator-authorized 2026-08-20) |
| Predecessors | B-00 → B-05 (all APPROVED WITH OBSERVATIONS) · Reconciliation Determination · predictive deferral |
| Date | 2026-08-20 |
| Evidence standard | Level I (direct) / Level II (executed) / Level III (documentary) |

---

## 1. What I verified (Level I/II — reproduced independently)

| Check | Result |
|-------|--------|
| **CA-TRANSMIT-1** | **HONORED (third consecutive)** — all 6 declared artifacts present, all 5 hashes match |
| Patch `b06.patch.txt` sha256 | `ce0fedff…` — **matches** |
| `git apply --check` + apply | **Clean** (exit 0) |
| 4 post-apply file SHAs | **All 4 match** |
| Endpoint delegation | **Correct** — `assemble_grounding` → `RuleBasedGroundedAssistant.respond(AssistantRequest(…))`, `CurrentOperatorDep`-authenticated, no new reasoning logic |
| Grounding module | Resolves 9 families from **persisted** summaries (r/n, regime label/confidence, scenario/dataset/annotation/journal/trade-plan notes) — never fabricates |
| No external network surface | **Confirmed** (no urllib/socket/httpx/requests/http.client anywhere in router/grounding/responder) |
| New B-06 tests (7) | **7/7 passed** (incl. grounded-over-real-artifact, empty-grounding-refused, refusal-classes, mutation-boundary, no-external-surface) |
| **Full backend suite** | **537 passed** — matches report (537 / 155.01s) |
| Ask log | Grounded answer over real correlation artifact (`r=0.7321 n=17520`), all 4 refusal classes, empty/unknown → `GROUNDING_REQUIRED`, 401 unauth |

## 2. Acceptance criteria vs. Build Order — line-by-line

| BO requirement | Status |
|-----------------|--------|
| `POST /assistant-respond` exists, authenticated | ✓ |
| Valid grounding → grounded summary with source ids, disclaimer, audit correlation | ✓ |
| Empty/invalid grounding → `GROUNDING_REQUIRED` (not fabricated) | ✓ |
| Each refusal class fires (order/gate/secret/tool) | ✓ all four verified |
| Responses + refusals persisted; read back via GET | ✓ 7 records read back |
| No external network calls (test-pinned) | ✓ |
| Full suite green | ✓ 537 passed |

**All acceptance criteria met.**

## 3. The pivotal properties — verified

1. **The assistant is now askable — and it is grounded, not generative.** A real question over the real B-04 correlation artifact produced `grounding_summary = "Correlation BTCUSDT/ETHUSDT r=0.7321 n=17520"` with source ids and an audit correlation. The answer came from AXIOM's own persisted research, not from free-form generation.

2. **The constitutional boundary held.** All four refusal classes fired and persisted (`ORDER_INSTRUCTION_REFUSED`, `GATE_OPEN_INSTRUCTION_REFUSED`, `SECRET_EXFILTRATION_REFUSED`, `UNBOUNDED_TOOL_REQUEST_REFUSED`); empty/unknown grounding returned `GROUNDING_REQUIRED` rather than invented content; unauthenticated access returned 401; and there is **zero** external network surface. The assistant remains deterministic, local, non-actuating — exactly the onboarding §20/§25/§34 boundary.

3. **FIND-3 is closed.** The last "scaffold with no request path" capability is now an operable, governed, auditable ask surface. The fail-first probe (7/7 pre-fix failures) proves the gap was real and is gone.

## 4. The provenance milestone (noted for the record)

The delivery included a **consolidated 27-element patch-chain transcript** (`chain_verification_r2_transcript.txt`) listing every patch from the pre-B-00 era through B-06 with hashes, ending at the correct `b06.patch.txt` hash. This is the first time the *entire* provenance chain has been made visible in one artifact, and it directly addresses the project's historical "approved-in-substance-but-not-landed" concern. It is a genuine institutional-integrity improvement, independent of this unit's functionality.

## 5. Deviations — reviewed and accepted

| ID | Deviation | Assessment |
|----|-----------|------------|
| D1 | 9 grounding families (5 B-04 + snapshots + 3 collaboration artifacts) | Accepted — all persisted-summary reads, all within §6 domain |
| D2 | No workspace auto-context (BO's operator-selected contract implemented verbatim) | Accepted — smaller surface, correct |
| D3 | Returns persisted record, not transient object | Accepted — correct persistence discipline, no duplicate write |
| D4 | No migration, no dependency, no responder/policy change | Accepted |

## 6. Observations (non-blocking)

- **OBS-B06-1 (Info):** the responder is deterministic rule-based; richer per-family summarization and any external-LLM path are future, separately-governed work (correctly out of scope).
- **F-01 (assistant input surface) is now unblocked** — the backend seam exists with the documented contract.
- **Carried:** PROJECT_STATE.md inventory staleness; W3-U03 semantic-narrowing record; fingerprint-determinism hardening.

## 7. Determination

| Field | Value |
|-------|-------|
| Determination | **APPROVED WITH OBSERVATIONS** |
| Basis | All acceptance criteria met; CA-TRANSMIT-1 honored (3rd consecutive); 4/4 SHAs; 7/7 new + 537/537 full suite; grounding/refusal/no-external/non-actuation invariants proven |
| Observations | OBS-B06-1 (non-blocking) |
| Next authorization state | **B-06 CLOSED** — B-07 (Cross-Cutting Hardening) may be issued; F-01 (assistant input surface) is unblocked |
| What this is not | Not production certification; not gate-opening; not authorization beyond BO-B-06 |

## 8. Record

- Patch: `ce0fedff1c19e360e932b1f5d261da18a24b936cc822c2d3928a2656adeea7a7`
- Post-apply: 4/4 file SHAs · 7/7 new · 537/537 full suite
- Ask path verified: grounded answer + 4 refusal classes + GROUNDING_REQUIRED + 401 + no external surface

> **We don't guess. We prove.** The assistant now answers — grounded in AXIOM's own research, refusing when it must, audited and non-actuating — and the full provenance chain is finally visible in one artifact. The backend's last scaffold is now a working, governed capability. Approved.

**End of ITRGA Determination BO-B-06**
