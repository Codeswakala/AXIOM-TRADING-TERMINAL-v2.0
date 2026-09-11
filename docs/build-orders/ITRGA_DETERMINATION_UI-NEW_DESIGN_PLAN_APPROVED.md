# ITRGA DETERMINATION — UI-NEW DESIGN PLAN

| Field | Value |
|---|---|
| Document type | ITRGA Design-Plan Determination (Directive §39; Control Document §§21, 25, 26) |
| Issued by | Independent Technical Review & Governance Authority |
| Date | 2026-08-12 |
| Plan reviewed | `UI-NEW_ENGINEERING_DESIGN_PLAN.md` — 49,786 bytes, 660 lines |
| **Declared SHA-256** | `8834aa916d2d3ce5c6c27c4b343861bfe0c3c5977742925cc96a01f8596da308` |
| **ITRGA-computed SHA-256** | `8834aa916d2d3ce5c6c27c4b343861bfe0c3c5977742925cc96a01f8596da308` — **MATCH** |
| Declared commit | `230efc791d2398e8d627bf31a9e38effd32dfe6b` (DA-local, unpushed) |
| **DETERMINATION** | **RE-BASELINE APPROVED WITH OBSERVATIONS** |
| Confidence | **HIGH** |
| **P01 Build Order** | **MAY NOW BE PREPARED AND ISSUED** |
| Governance Gate | CLOSED · Production NOT CERTIFIED |

---

## 1. Artifact integrity — verified

The DA declared a SHA-256 for the plan. I computed it independently:

```
declared : 8834aa916d2d3ce5c6c27c4b343861bfe0c3c5977742925cc96a01f8596da308
computed : 8834aa916d2d3ce5c6c27c4b343861bfe0c3c5977742925cc96a01f8596da308
                                                                    MATCH
```

**This is the first cryptographically self-verifying artifact this workstream has produced.** The document I reviewed is provably the document the DA submitted — byte for byte. It resolves at Level I the class of ambiguity that consumed five prior cycles, and I record the practice as one the DA should retain for every future submission.

---

## 2. Corrective action dispositions

### C-1 — Depth ladder without a lawful data source · **DISCHARGED**

This was the blocker, and it was a genuine engineering constraint rather than a documentation defect. The DA cured it correctly rather than cosmetically.

- The order book / depth ladder is **removed entirely**. Zero occurrences of "depth ladder" or "order book" remain as a deliverable.
- §E now renders `SPREAD & MARKET TELEMETRY — Current Spread: 0.8 pts · Tick Freq: 2.0s · Vol: 14.2M · Posture: live:simulated`. The fabricated `Bid: 1.08448 (1.2M) / Ask: 1.08452 (1.5M)` values are gone.
- P02 is retitled **"Market Watchlist & Real-Time Spread Telemetry Surface (Re-scoped per C-1)"**, delivering `TerminalSpreadTelemetry.tsx` in place of `TerminalDepthLadder.tsx`, with factor 3 now reading *"zero synthetic order-book fabrication."*
- The §V-P02 "live" versus §E "simulated" contradiction is resolved.
- **Q12 is corrected honestly**, and this is the disposition I most wanted to see:

> *"An external Level-2 Order Book / Market Depth API is missing from the platform because external broker connections remain hard-closed under the Governance Gate. The terminal honestly presents candle-derived spread and tick rate telemetry instead of fabricating unbacked depth data (Directive §20 / T-6)."*

That is a correct statement of both the technical fact and its constitutional cause. The prior answer — "Zero backend APIs are missing" — is retracted. The replacement pane derives from data that genuinely exists in `/ws/market`, and its simulated provenance is surfaced at the point of display as T-6 requires.

### C-2 — Technical-debt regression · **DISCHARGED**

§U is retitled "Technical Debt Reconciliation (CA-4 / C-2)" and now states `TD-UI-POSTCSS-HIGH` as **CLOSED (Line 116)** — matching register v3.0.12. All previously omitted debts are disclosed: `TD-AXIOM-DEV-CREDENTIAL-LITERALS` flagged **OPEN, Doc 11 §2 pre-cert blocker**, plus `TD-UI-REACTROUTER-MODERATE`, `TD-005`, the seven E2E debts, `TD-021`, `TD-029`. I confirmed no "standing" mischaracterisation survives anywhere in the document.

### C-3 — Phantom governing instrument · **DISCHARGED**

`UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — zero occurrences remain. §S now cites five instruments, and I verified each exists: `QUALITY_GATE_SPEC.md` (EQG-1…EQG-8), `REPOSITORY_PROVENANCE_PROTOCOL.md` §2, Doc 12 §14 with Doc 13, `16_BRAND_GOVERNANCE_STANDARD.md`, and Directive §§26–32.

### C-4 — Missing sections and Tier-5 conflict · **DISCHARGED**

- **C-4a:** §N is now the dedicated **"Zero-Actuation & Data-Honesty Boundary (T-1…T-7)"**. All seven guardrails are stated in full, including T-1 and T-7 which were previously absent. T-2 is correctly rewritten as spread/market telemetry consistent with the C-1 re-scope.
- **C-4b:** §Z.2 "Open Questions & Resolutions for ITRGA" added, answering all ten questions from my request §5.
- **C-4c:** Doc 8 displacement is now disclosed **twice** — in §Z.1 Q6 and Q10 — each explicitly referencing *"pending Operator amendment GA-167."* The conflict is surfaced rather than silently absorbed, which is exactly the required treatment for a Tier-5 provision.

### Prior-cycle items confirmed sustained

Structural integrity retained across the correction: Sections **A–Y plus Z.1/Z.2**, **22/22** answers intact, **6/6** phases carrying full 8-factor justification (OBS-3 remains discharged). OBS-2 remains corrected — §Z.2 cites `/api/v1/collaboration/trade-plans`, `/journal-entries`, `/chart-annotations`, all verified real, and `/api/v1/market/status` and `/seed-history` both verified in `backend/app/api/routes/market.py`.

---

## 3. Determination

**RE-BASELINE APPROVED WITH OBSERVATIONS.**

All four corrections are discharged. The plan is internally coherent, its scope is bounded, its dependencies are understood, it preserves the governance controls, its phase boundaries are technically justified across eight factors, its acceptance criteria are measurable, and its evidence requirements are adequate. It answers the Operator's objective — Directive §33's question *"why is this a trading terminal rather than another dashboard?"* is answered concretely by the §E architecture with the chart as a first-class centre stage rather than a card.

Per Control Document §21, I record that this approval is **not** granted merely because corrections were made. It is granted because I verified each correction against the repository and the governing corpus, and because the C-1 remedy in particular demonstrates the disposition this Authority most needs from a Development Authority: when told the platform could not honestly render an order book, the DA removed the pane and disclosed the missing capability rather than relabelling fabricated data.

### Observations carried forward (non-blocking)

| ID | Observation |
|---|---|
| **OBS-4** | Level-I evidence method still under-specified. §Z.2(9) now adds "1920x1080" browser captures — an improvement — but producer, storage location, and acceptance criteria remain unstated against seven open E2E debts. Must be concretely defined in the **P01 Build Order**, not deferred to P06. |
| **OBS-5** | Vite main chunk 648.22 kB; consistent with carried `OBS-P05-2`. Non-failing build advisory. |
| **OBS-6** | §C route inventory (`/live`, `/signals`, `/compare-scenarios`, `/journal`) diverges from origin's registered routes. Presumed DA-local evolution; reconcile at P01 delivery. |
| **OBS-7** | §Z.1 Q15 states "None to token values" while §T RSK-NEW-02 introduces `getComputedToken`. Not a contradiction — a resolver reads tokens rather than changing them — but a clarifying line is warranted. |
| **R-1** | SHA discipline: prior reports cited up to three conflicting SHAs. The declared-and-verified hash in this submission is the correct remedy. **Retain this practice for every future Delivery Report.** |
| **OBS-8** | `TD-AXIOM-DEV-CREDENTIAL-LITERALS` remains an **open Doc 11 §2 pre-certification blocker**. It does not block UI-NEW, but it will block production certification and requires its own security-remediation Build Order before Doc 11 §2. |

---

## 4. P01 Build Order status

**`BUILD_ORDER_UI-NEW-P01` MAY NOW BE PREPARED AND ISSUED.**

Prerequisite ledger per Control Document §22:

| Prerequisite | Status |
|---|---|
| B-1 design plan | ✅ Discharged |
| B-2 repository claims | ✅ Substantially discharged; R-1 cured by verified SHA |
| B-3 test baseline | ✅ Discharged (148f/603t/414/1,017 established) |
| M-1 technical debt | ✅ Discharged |
| M-2 Doc 17 standing | ✅ Discharged |
| CA-5 asset baseline | ✅ Discharged |
| C-1 / C-2 / C-3 / C-4 | ✅ All discharged |
| A-3 codebase custody | ✅ Substantially resolved — UI-008…UI-011 substantiated in DA-local custody |
| EQG-5 / EQG-8 | ✅ Documentation synchronized; delivery report and evidence supplied |

Per Control Document §26, I state explicitly: **this authorizes preparation and issuance of the P01 Build Order. It does not itself approve P01 implementation.** Implementation begins only when the Build Order is formally issued.

### Conditions binding on P01

1. **A-1 (Operator) — GA-167 must be recorded before P01 delivery is reviewed.** The plan now honestly discloses that it displaces `08_UI_UX_SPEC.md` (Tier 5) on panel architecture. Disclosure is not amendment. Under `10_CONSTITUTIONAL_HIERARCHY.md`, Tier 5 prevails until formally amended; without GA-167, P01 delivers in known conflict with a governing specification.
2. **Provenance — `REPOSITORY_PROVENANCE_PROTOCOL.md` §2 applies at P01 approval.** DA-local work has been unpushed since 2026-07-29. Commit `230efc79` is not resolvable in supplied custody. At P01 approval the approved worktree must be committed and annotated-tagged with `git rev-parse --verify <tag>` preserved in evidence — otherwise phase-isolating diffs become impossible, which is the exact condition `TD-AXIOM-GIT-PROVENANCE` was raised to remediate.
3. **OBS-4 must be closed in the P01 Build Order** — the Level-I browser evidence method requires concrete definition before the first phase produces evidence.
4. **P01 scope is bounded** to §V-P01: `TerminalTopTicker.tsx`, `TerminalMultiPaneLayout.tsx`, root route mount, `terminalShell.test.tsx` and security invariants. No watchlist, no chart relocation, no signals — those are P02–P04 and require their own Build Orders.
5. **A-2 (Operator)** — Doc 17 remains unplaced; it may not be cited as controlling authority. The plan correctly does not cite it.

---

This determination applies only to the submitted UI-NEW Design Plan and its supporting evidence. It does not constitute implementation approval, production certification, or authorization to execute any future phase unless explicitly stated.

Historical UI-001…UI-011 records remain historical unless separately superseded.

No implementation may begin before the applicable Build Order is formally issued.

**We don't guess. We prove.**

*— AXIOM ITRGA*
