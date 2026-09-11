# BUILD ORDER — UI-NEW-P01

**Terminal Foundation & Multi-Pane Shell Architecture · Persistent Global Ticker · Root Route Mount · Zero-Actuation Scaffolding**

| Field | Value |
|---|---|
| Issuing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional Trading Terminal Transformation |
| Workstream | UI-NEW — Institutional Trading Terminal Rebuild |
| Phase | **UI-NEW-P01** |
| Design-plan determination | `ITRGA_DETERMINATION_UI-NEW_DESIGN_PLAN_APPROVED.md` — ✅ **RE-BASELINE APPROVED WITH OBSERVATIONS** |
| Approved plan artifact | `UI-NEW_ENGINEERING_DESIGN_PLAN.md` · SHA-256 `8834aa916d2d3ce5c6c27c4b343861bfe0c3c5977742925cc96a01f8596da308` (ITRGA-verified) |
| Governing docs | Operator Directive §§18–20, 25–32; Plan §N (T-1…T-7), §V-P01, §W, §X; `17_INSTITUTIONAL_SECURITY_STANDARD.md` (Operator-designated governing); Doc 16 Part XIV; `QUALITY_GATE_SPEC.md` EQG-1…EQG-8; `REPOSITORY_PROVENANCE_PROTOCOL.md` §2 |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend **414** · frontend **148f / 603t** · platform **1,017** |
| Governance Gate | CLOSED (must remain closed) |
| Production | NOT CERTIFIED (unchanged) |

**Motto: "We don't guess. We prove."**

---

## 1. Operator determinations recorded

Two Operator determinations are recorded as governing context for this phase:

**A-2 — DISCHARGED BY OPERATOR.** `17_INSTITUTIONAL_SECURITY_STANDARD.md` is designated a **governing document**. It is therefore binding on UI-NEW-P01 and all successor phases. Applied to this phase, its operative provisions are §4 SAL classification, §10 Secure Software Engineering, §12 Application Security, §17 Security Implementation Governance & Build Order Control (§17.4 Build Order content; §17.8 four validation gates; §17.11 no security regression), and §19 threat modelling.

Two residual matters remain and are recorded, not resolved: the document is **absent from `docs/governance/`**, and Part VI is duplicated with **no Part VII**. Neither prevents its application here. Both should be cured before Doc 11 certification so the standard is verifiable by a future reviewer. Per Master Role Init Part 2, I do not assign its tier; I assess it operates as a Tier-5 domain constitution, supreme within security and subordinate to Tiers 1–4, and defer the formal placement to Operator amendment.

**Level-I evidence method — RESOLVED BY OPERATOR (closes OBS-4).** The Operator will start the server, capture browser screenshots on target, and supply them. This satisfies the Directive §30 Level-I requirement for this phase and is consistent with the operator-relayed evidence model used throughout UI-001…UI-007.

---

## 2. Purpose & scope

Establish the **terminal shell** — the full-bleed multi-pane grid, the persistent global ticker header, and the root-route mount — and lay down the **T-1…T-7 zero-actuation and data-honesty boundary** BEFORE any market, chart, signal, or risk surface is built. This phase is **presentation scaffolding only**. It renders no market analytics and computes nothing.

**IN scope (Plan §V-P01, verbatim):**

1. **`TerminalMultiPaneLayout.tsx`** — full-bleed multi-pane grid container with docked panel slots (left / centre / right / bottom). Slots may render empty or placeholder-labelled states; they are populated in P02–P05.
2. **`TerminalTopTicker.tsx`** — persistent global ticker header: symbol, price, 24h change, high/low, session clock, WebSocket connection status, and governance badge.
3. **`TerminalGovernanceBadge.tsx`** — compact `RESEARCH-ONLY · NON-ACTUATING` + `GATE: CLOSED` indicator (Plan §J).
4. **Root route (`/`) mount** of the unified terminal workstation, replacing `DashboardPage.tsx` (Plan §D: REPLACE).
5. **Terminal layout tokens** — additions to `tokens.css` if required, strictly `--ix-*` prefixed.
6. **`terminalShell.test.tsx`** + security-invariant tests.

**OUT of scope — do NOT build:**

- **P02** watchlist dock, spread telemetry (`TerminalWatchlistDock.tsx`, `TerminalSpreadTelemetry.tsx`); **P03** chart stage and timeframe toolbar; **P04** signal stream; **P05** bottom-dock tabbed analytics content; **P06** whole-surface audit.
- Any **order book / depth ladder / bid / ask / size** rendering. **Permanently excluded from the programme by C-1** — no lawful data source exists; `/ws/market` carries OHLC only and `BrokerQuote` raises `BrokerDisabledError` behind the closed Gate.
- Any actuation: buy/sell control, order ticket, order submission, broker connection or mutation, account mutation, execution trigger, automated trading trigger, execution shortcut, hidden execution API (T-1).
- Any external AI/LLM dependency or call (T-4). Dependency set remains exactly `lightweight-charts`, `react`, `react-dom`, `react-router-dom`.
- Any new backend endpoint, service, table, migration, or dependency. Alembic head **locked at `20260717_0037`** (Plan §M).
- Any fabricated price, spread, volume, or telemetry value. Unavailable data renders as an explicit state, never as a plausible number (T-6, Directive §20).
- Removal or regression of existing routes. `/charts`, `/intelligence`, `/governance`, `/investigate` and the remaining registered routes remain reachable as focus views (Plan §Z.2 Q4).

---

## 3. Binding conditions carried from the determination

- **B-P01-1 — A-1 dependency.** The plan discloses that it displaces `08_UI_UX_SPEC.md` (**Tier 5**) on panel architecture, deferring multi-window popout detachment. Disclosure is not amendment. **`GA-167` must be recorded in `GOVERNANCE_AMENDMENTS.md` before this phase's delivery is reviewed.** Absent it, P01 delivers in known conflict with a governing specification and I cannot approve it without a Tier-5 finding. Owner: **Operator**.
- **B-P01-2 — Provenance (`REPOSITORY_PROVENANCE_PROTOCOL.md` §2).** DA-local work has been unpushed since 2026-07-29; commit `230efc79` is not resolvable in supplied custody. At P01 delivery the DA shall commit the approved worktree, create an annotated tag, and preserve `git rev-parse --verify <tag>` output in evidence. Owner: **DA**.
- **B-P01-3 — Single Active Phase.** P02–P06 remain unauthorized. Implementing beyond §V-P01 scope is a scope violation regardless of technical merit (Directive §27).
- **B-P01-4 — Doc 17 §17.11 no security regression.** The redesign shall not weaken any existing boundary. Current verified state to be preserved: `dangerouslySetInnerHTML` = 0, `eval(` = 0, authenticated access, RBAC, ticket-authenticated WebSocket.
- **B-P01-5 — SAL classification (Doc 17 §4.5).** The DA shall state the Security Assurance Level of each new component. ITRGA assesses the terminal shell and ticker as **SAL-2 (Internal)** presentation surfaces carrying no SAL-3+ payload; the DA shall confirm or justify otherwise.

---

## 4. Mandatory named tests

To be **DISPLAYED passing by name** under a verbose reporter:

1. `test_uinew_p01_terminal_shell_mounts_multipane_layout_without_dom_collisions`
2. `test_uinew_p01_global_ticker_renders_symbol_price_change_clock_and_ws_status`
3. `test_uinew_p01_terminal_contains_no_execution_or_order_or_broker_or_account_control`
4. `test_uinew_p01_terminal_renders_no_fabricated_market_values_and_labels_unavailable_states`
5. `test_uinew_p01_root_route_mounts_terminal_workstation_and_preserves_existing_routes`
6. `test_uinew_p01_governance_badge_renders_gate_closed_research_only_inert`

Test #3 is the T-1 spine. Test #4 is the T-6 spine and must prove that a disconnected or empty feed renders `Loading` / `Empty` / `Stale` / `Disconnected` / `Unauthorized` / `Degraded` — **not** a plausible placeholder number.

---

## 5. Mandatory evidence checklist (Level-I operator-run on target)

- **(a) Build identity** — delivery report and transcript header proving the pack is OF UI-NEW-P01, at the declared commit SHA.
- **(b) Six named tests DISPLAYED passing** by name, verbose reporter.
- **(c) 🔴 T-1 zero-actuation grep CLEAN** — `buy|sell|place_order|submit_order|order_ticket|execute|go-live|connect-broker|broker|account_id|position|balance|margin|capital|real_pnl|open_gate|allow_execution` → no functional match in `frontend/src`.
- **(d) 🔴 T-4 external-LLM grep CLEAN** — `openai|anthropic|langchain|gpt|claude|external_llm|llm_summary|ai_summary|api\.openai|remote_prompt` → no match. Plus `package.json` diff proving the four-package dependency set unchanged.
- **(e) 🔴 T-6 data-honesty proof** — named test #4 plus a served-browser capture showing the ticker in a **disconnected or pre-feed state**, rendering an explicit status rather than a fabricated price. This is the single most important evidence item in this phase.
- **(f) 🔴 C-1 permanence grep** — `depth.?ladder|order.?book|orderbook|\bbid\b|\bask\b` → no order-book rendering in `frontend/src/components/terminal/`.
- **(g) Sandbox safety** — `dangerouslySetInnerHTML` = 0; `eval(` / `new Function` = 0 (Doc 17 §12.6, §17.11).
- **(h) Token purity** — no ad-hoc hex literal outside `tokens.css`; all new styling via `var(--ix-*)` (Plan §K; Doc 16).
- **(i) Secrets scan** — 0 credentials in new source (Doc 17 §21.9).
- **(j) No-drift substitute** — `alembic current` = `20260717_0037`; no new backend endpoint; no new table; `package.json` / `package-lock.json` unchanged.
- **(k) Regression** — frontend Vitest **≥148f / 603t**, no test lost, full total printed with sentinel; backend `pytest -q` **≥414 passed**; `tsc -b` exit 0; `vite build` exit 0 with bundle delta disclosed against the 648.22 kB baseline (OBS-5).
- **(l) 🔴 Browser served-session screenshots (Operator-supplied, 1920×1080)** — (i) logged-in `/` showing the multi-pane terminal shell with persistent ticker header, `GATE: CLOSED`, `RESEARCH-ONLY · NON-ACTUATING` badge, and **no execution control anywhere in the frame**; (ii) the disconnected/pre-feed honest state from (e); (iii) logged-out `/` correctly blocked to `/login`.
- **(m) Doc 16 brand B-1…B-7** — palette conformance, `--ix-font-mono` with `tabular-nums` on all numerics, no hardcoded colour in production TSX, institutional-not-retail wording, never colour alone.
- **(n) Doc 17 §17.8 validation gates** — Gate 1 requirement compliance · Gate 2 technical validation · Gate 3 regression assessment · Gate 4 governance approval, each explicitly addressed.
- **(o) SAL declaration** per B-P01-5.
- **(p) Provenance** per B-P01-2 — commit, annotated tag, `git rev-parse --verify <tag>` output.
- **(q) Local CI** — `LOCAL_CI_EXIT_CODE: 0` + sentinel; or a disclosed `TD-090` environment-flake waiver after substantive gates are green. Any other nonzero cause is a finding.

---

## 6. Acceptance criteria (Plan §W, P01 row)

> *"Global ticker header renders persistent price, 24h change, clock, WS status; multi-pane grid mounts without DOM collisions."*

Plus, as binding additions from this Build Order: no execution affordance present (T-1); unavailable data rendered honestly (T-6); existing routes preserved; regression baseline held at ≥148f/603t and ≥414.

---

## 7. Delivery Report requirement

Per Directive §32, the DA shall produce `DELIVERY_REPORT_UI-NEW-P01.md` containing all 21 required elements, and shall:

- declare the **SHA-256 of every submitted artifact** — this practice resolved five cycles of custody ambiguity and is now a standing requirement (R-1);
- cite **one** commit SHA consistently throughout;
- state the technical-debt position against register **v3.0.12**, and disclose `TD-AXIOM-DEV-CREDENTIAL-LITERALS` as an open Doc 11 §2 pre-certification blocker (OBS-8);
- reconcile the §C route inventory against the delivered state (OBS-6);
- **not** state that the phase is approved. Only the ITRGA issues that determination.

---

## 8. Authorization

**`BUILD_ORDER_UI-NEW-P01` IS HEREBY ISSUED.** The DA is authorized to implement §2 IN-scope items only.

The DA shall not commence P02. The DA shall not self-approve. On delivery, ITRGA will perform a four-pass review — Custody → Claim reconciliation → Engineering review → Governance determination — and issue a single consolidated determination.

**Governance Gate remains CLOSED. Production remains NOT CERTIFIED. No live execution affordance may be introduced by this or any successor phase absent a separate governing instrument.**

**We don't guess. We prove.**

*— AXIOM ITRGA*
