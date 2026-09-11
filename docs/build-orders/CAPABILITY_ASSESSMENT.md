# AXIOM — Capability Implementation Assessment (ITRGA)

| Item | Value |
|------|-------|
| Review identity | ITRGA capability-implementation verification |
| Date | 2026-08-19 |
| Subject | `AXIOM_COMPLETE_PLATFORM_CAPABILITIES.md` (49-section capability catalogue) |
| Platform version | backend v0.62.0 · frontend Vite 8 + React 18.3 |
| Method | Static code inspection (backend services/routes, frontend components) **+** live runtime probes (OpenAPI schema, authenticated API calls, browser navigation) |
| Evidence class | Level I (direct runtime output, file contents, live API responses) unless labeled |

---

## 0. Executive summary

AXIOM is a **genuinely working institutional trading *terminal shell*** with real, end-to-end-operable: authentication/RBAC, unified workspace UI, simulated real-time market data over WebSocket, a server-computed technical-analysis engine (~30 indicators incl. SMC/ICT concepts), interactive charting, and working CRUD for research notes, collections, tags, journal entries, and chart annotations — plus pervasive governance framing and read-only audit/governance display.

However, a **large fraction of the catalogue's "intelligence" and "AI" capabilities are implemented only as persistence + read-only APIs + computation *services* with no generation wiring and no trained models.** In the running application these surfaces are **operable but empty** — signals, intelligence reports, alerts, scenarios, portfolio-risk, ML, and the assistant all show zero data and cannot be produced by an operator. The assistant has **no request path at all** (read-only history only). The ML platform is declared `stub` at the package root.

This is precisely the catalogue's own **DESIGNED ≠ IMPLEMENTED ≠ VERIFIED ≠ APPROVED ≠ PRODUCTION CERTIFIED** distinction (§45) and its §47 caveat ("a capability can be correct but not landed in the repository; implementation-vs-repository distinctions exist"). I found no fabricated data; empty states are honest. The gap is **absence of generation/execution wiring**, not broken code.

---

## 1. Capability matrix

Legend:
- 🟢 **OPERABLE** — implemented and works end-to-end in the running app (verified).
- 🟡 **SCAFFOLD** — code + API exist, read/display works, but **no generation path / no data**; not operable end-to-end.
- 🔴 **NOT IMPLEMENTED** — stub, absent, or no request path.

| # | Capability | State | Evidence |
|---|-----------|-------|----------|
| 1–2 | Product identity / operating model | 🟢 | Branding, disclaimers, "GATE CLOSED · RESEARCH-ONLY · NON-ACTUATING" pervasive |
| 3.1 | Unified terminal shell | 🟢 | Five-region shell, nav dock, command bar — navigated all 26 states |
| 3.2 | Market navigator / watchlists | 🟢 | 11 pairs, ALL/FX/CRYPTO grouping, live price/change/range/provenance |
| 3.3 | Instrument workspace | 🟢 | Instrument header (symbol/price/change/spread/session); persists across surfaces |
| 4 | Market data | 🟢 | WS-simulated live feed streams; ingestion; data-state labels; `SEED:SYNTHETIC` / `LIVE:SIMULATED` provenance |
| 5 | Interactive charting | 🟢 | Lightweight Charts canvas renders (784×452); timeframes 1M–1D; series types; drawing tools |
| 6 | Technical analysis | 🟢 | **~30 server-computed indicators** (SMA, EMA, RSI, MACD, Bollinger, ATR, HMA, Supertrend, Ichimoku, Stoch, CCI, ROC, ADX, Keltner, Donchian, Pivots, Camarilla, Prev H/L, Session Lvls, BOS/CHOCH/FVG/OrderBlock/Swings/Structure, ZScore, PctRank, RegChan) — live-verified via `/persistence/indicator-series` |
| 7 | Signals | 🟡 | Read API + guardrails + `produce()` exist; **inference adapter not wired**; `signals/history` → `[]`; no UI path to generate |
| 8 | Market intelligence | 🟡 | 5 read-only report APIs + computation services; **no generation endpoint/wiring**; all → `[]` |
| 9 | Research management | 🟡 | Collections/tags CRUD works; but **zero governed artifacts** to organize |
| 10 | Artifact explorer | 🟡 | UI reads 10 sources; **all 0 rows** |
| 11 | Investigation | 🟡 | Read-only surface; depends on empty signals/intelligence |
| 12 | Scenario analysis | 🟡 | Read-only list → `[]`; no generation |
| 13 | Portfolio analytics | 🟡 | Dashboard returns **"hypothetical research descriptors, not live venue records"** — no account/positions/broker linkage (by governance design) |
| 14 | Risk management | 🟡 | Simulated/hypothetical risk reports only; 0 data |
| 15 | Alerts & monitoring | 🟡 | Read-only + `ack`; generation service exists, **not wired to auto-trigger**; → `[]` |
| 16 | Journal | 🟢 | CRUD works (verified), inert research notes |
| 17 | Artifact lineage & evidence | 🟡 | Lineage tree + hash relationships in code; **0 artifacts** to trace |
| 18 | Governance & audit | 🟢 | Governance/certification status surfaces + `/persistence/audit-events` (works) |
| 19 | Security & access | 🟢 | JWT auth, RBAC gate, 401 handling, secret-marker redaction — verified |
| 20 | Governed AI assistant | 🔴 | **No "ask" endpoint**; read-only response history (`[]`); deterministic keyword refusal + grounded-summary engine exist but are **unreachable from UI/API** |
| 21 | AI refusal system | 🟡 | 6 refusal classes implemented (keyword policy); **not reachable** — no request path |
| 22 | AI disclosure | 🟢 | Disclaimers present on all AI/intelligence surfaces |
| 23 | AI auditability | 🟡 | Read-only response/refusal records; **empty** |
| 24 | AI API seams | 🟢 | `GET /collaboration/assistant-responses` (+`/{id}`) exist (read-only) |
| 25 | AI boundaries | 🟢 | No external LLM, no actuation, no state mutation — enforced in code |
| 26 | Non-actuation | 🟢 | No order/execution/broker/gate endpoints anywhere |
| 27 | Command palette & productivity | 🟢 | `Ctrl+K` opens; workspace switcher, search |
| 28–29 | Workspace/layout & docking | 🟢 | Docks, overlays, stage views, panel persistence (theme persists per-operator) |
| 30 | Global/terminal status | 🟢 | Gate, research-only, WS state, UTC clock, environment |
| 31 | Data-state handling | 🟢 | Explicit empty/loading/stale/disconnected states; "renders absence, not an improvised series" |
| 32 | Accessibility | 🟢 | Skip link, landmarks, ~15:1 contrast, keyboard command palette (one gap: no `<h1>` on `/`) |
| 33 | Performance | 🔴 | **Not measured** — no evidence supplied; NOT PROVEN |
| 34 | Design system | 🟢 | `--ix-*` token system (colors, type, spacing, elevation) verified in `:root` |
| 35–37 | Market↔Research↔Intelligence convergence | 🟡 | Terminal unifies surfaces; but research/intelligence layers are empty |
| 38 | Operator workflow | 🟡 | Market→chart→analysis operable; signal/intelligence/assistant stages empty |
| 39 | Governance protections | 🟢 | Non-actuation, RBAC, honest empty states enforced |
| 40 | Engineering/ops infrastructure | 🟢 | FastAPI, Alembic (37 migrations), Vite/React, typecheck passes (`tsc -b` exit 0) |
| 41 | Research-only posture | 🟢 | `GATE CLOSED · NOT CERTIFIED · RESEARCH-ONLY · NON-ACTUATING` — accurately reflected |
| 42–49 | Vision/capability map | — | Aspirational; assessed per-row above |

---

## 2. Key findings (evidence-grounded)

### FIND-1 — Signals are not operable end-to-end (🟡, Medium)
The `LiveMarketInferenceAdapter` and `AdvisorySignalService.produce()` exist with full guardrails (as-of/no-look-ahead, calibration, economic, staleness), but the adapter is **only imported, never instantiated or invoked** (`grep` shows no caller outside `__init__.py`/its own module). `GET /signals/history` returns `[]`. No model is eligible (see FIND-4), so the inference gate can never open. **Consequence:** §7 "signal discovery/drill-down/investigation" and §43 "inspect signals" are non-functional in the running terminal.

### FIND-2 — Institutional intelligence has no generation path (🟡, Medium)
Correlation, regime, scenario, portfolio-risk, and signal-validation **computation services are real** (e.g. `RegimeReportService.create_report`, Fisher-interval correlation), but the routes expose only `list`/`get` (read-only), and there is **no endpoint or startup hook that calls `create_report`**. All five families return `[]`. **Consequence:** §8, §12, §14 are read-only empty surfaces.

### FIND-3 — The "governed AI assistant" cannot be asked anything (🔴, High)
- Backend `RuleBasedGroundedAssistant` is deterministic, local, no-LLM, and correctly refuses (`ORDER_INSTRUCTION_REFUSED`, etc.) — but its `respond()` is **not exposed over HTTP** (collaboration router has only `GET` on `assistant-responses`).
- Frontend `ContextualAssistantPanel` renders context chips + static prompt-suggestion chips + disclaimer, and reads response history; `DocumentationLookupSurface` is "100% static, client-side, sandboxed"; `ResearchReportSummarizer` is client-side rendering.
- **There is no input that submits a question, and no endpoint that would answer one.**
- **Consequence:** §20 "grounded research responses / ask grounded research questions" (§43) is **not implemented** as an operable capability. The assistant is an audited refusal/response *record* viewer, not an assistant.

### FIND-4 — ML platform is a stub at the package root (🔴, High)
`app/ml/__init__.py`: `ML_PLATFORM_STATUS = "stub"`, docstring "no ML pipelines or models are implemented … reserves the architectural boundary." Despite ~3,500 lines of W2 sub-package code (dataset, features, validation, calibration, economic, generalization, experiments, model harness), there are **0 model_artifacts, 0 experiments, 0 feature_records**, **no `/ml` API surface**, and **no live inference** (the engine requires an `advisory_approved` model with validation/calibration/economic/generalization reports — none exist). **Consequence:** all "machine learning" capability claims are framework-only; nothing has been trained, and the "Intelligence Layer" has no models to run.

### FIND-5 — Future-dated simulated bars (Medium) *(carried from prior UI review OBS-3)*
Seeded/live candles carry `open_time` up to ~17:57Z while wall-clock is ~15:05Z (`simulated.py` advances one M1 bar per ~2s tick ⇒ ~30× real-time). Indicators still compute over these bars, but the timestamps violate the project's own as-of discipline and could mislead. A `SIMULATED` label mitigates but does not remove it.

### FIND-6 — Supply-chain advisories remain (Medium) *(carried SEC-1)*
`react-router-dom` (direct) + `postcss` (transitive) high-severity advisories, fixes available, lockfile pins affected versions.

---

## 3. Honest limitations

1. I verified **operability** (endpoints fire, UI renders, code is wired) and **data presence** (empty vs populated). I did **not** run the full test suites, nor re-verify the "162 suites / 736 tests" claim in `PROJECT_STATE.md`.
2. `DESIGNED`-level claims (e.g. "future FIX/cTrader/IBKR brokers", "voice interaction", "federated learning") are correctly out-of-scope per the roadmap and were not counted against implementation.
3. This assessment concerns **implementation**, not **approval status**. The project's own records already mark much of this as "inert / research-only / Gate CLOSED / NOT CERTIFIED" — which my runtime evidence confirms is accurate.

---

## 4. Determination

**CAPABILITIES: PARTIALLY IMPLEMENTED (in the running repository).**

- **Operable now:** terminal shell, watchlists, simulated live market data, interactive charting, ~30 server-computed indicators, research-note/collection/tag/journal/annotation CRUD, security/RBAC, governance/audit display, command palette, design system, accessibility.
- **Not operable (scaffold-only):** signals, institutional intelligence, alerts, scenarios, portfolio-risk, artifact lineage (all empty, no generation), and — most materially — **the AI assistant (no request path) and the ML platform (stub, no models)**.

The platform faithfully enforces its own governance boundaries (non-actuation, honest empty states, no fabricated data), but the catalogue's §43 "intended full capability" is **not currently reachable** in the running application. No production-certification implication should be drawn from any of the above; the posture `GATE CLOSED · NOT CERTIFIED` remains correct.
