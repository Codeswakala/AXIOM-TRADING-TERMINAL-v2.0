# DOC13 — X-01 TERMINAL TIER VERIFICATION REPORT
## End-to-End Platform Verification (Full Operator Workflow Through the Terminal)

| Item | Value |
|------|-------|
| Build Order | `BO-X-01-TERMINAL` (Operator-authorized 2026-08-22) |
| Tier | X-01 Terminal Tier — the full UI click-through (the "full working UI" milestone) |
| Executor | Development Authority (DA) |
| Date | 2026-08-22 |
| Platform state | AXIOM v0.62.0 dev environment; chain position 37 (B-00→B-07 + X-01 Backend Tier + B-AUDIT + F-00→F-06, all APPROVED WITH OBSERVATIONS) |
| Method | Real browser (Chromium headless, 1600×1000) against the running dev stack; DOM assertions + screenshots + backend server-log cross-reference |
| Code changes | **None** (verification-only per BO §3/§6; the unit's patch is docs-only: register rows + this report) |
| Posture | Gate CLOSED · Production NOT CERTIFIED (unchanged) |

---

## 1. The ten-hop walk (Level-I evidence per hop)

Evidence files: `docs/evidence/x01t/x01t_capture_log.txt` (assertions),
`x01t_hop*.png` (screenshots), `x01t_server_log.txt` (backend cross-reference).

### Hop 1 — Login
Wave-animated login renders: 16 wave candles, 12 particles, glow pulse; scene
textContent empty (decorative-only). Governance chips visible: GATE: CLOSED ·
RESEARCH-ONLY · NON-ACTUATING. Motion frames 700ms apart DIFFER; reduced-motion
frames 700ms apart are byte-IDENTICAL (freeze honored). Operator auth
succeeded; the terminal mounted. — `x01t_hop01_login.png`, `x01t_hop01_frozen.png`

### Hop 2 — Navigation legibility + theme persistence
Rail: 16 buttons, 16/16 semantic SVG icons, 16/16 visible labels
(Operations/Live/Charts/Signals/Analytics/Intel/Investigate/Scenarios/Plans/
Execution/Portfolio/Journal/Artifacts/Governance/Settings/Alerts), 16/16
aria-labeled. Theme switched via the header control and **persisted across a
reload** (server-side workspace-preference PUT in the server log). The
expanded dock shows SVG icons beside labels. — `x01t_hop02_nav.png`,
corrected `f06_dock.png`

### Hop 3 — Instrument selection → watchlist → chart
BTC/USD selected from the watchlist; the chart-symbol badge updated; the
terminal chart stage rendered; the ticker posture badge shows
`live:simulated` (honest labeling); structural overlay controls present. —
`x01t_hop03_chart.png`

### Hop 4 — Structural signals (real derived events)
The Structural family rendered **24 EVENTS** derived from the server-computed
indicator series over the REAL corpus (BTCUSD H1, series kind: native) —
provenance line + "DETERMINISTIC · DESCRIPTIVE — NOT A PREDICTION" framing;
first event "Fair value gap zone". — `x01t_hop04_structural.png`

### Hop 5 — Predictive signals (honest deferral)
The Predictive (ML) family labeled; the deferred-empty state states the truth:
"No predictive signals — the predictive track is deferred (no eligible
model)…". — `x01t_hop05_predictive.png`

### Hop 6 — Intelligence (five families, generated + read)
The governed generation surface resolved the real window (BTCUSD H1, from the
freshest persisted candle). Scenario / portfolio-risk / correlation / regime
were generated through the UI (persisted ids + `data-class: historical:real`
on the read-back cards, research-only framing). Signal-validation produced the
honest structured 422 notice (SIGNAL_VALIDATION_EMPTY_SCOPE — nothing
fabricated). — `x01t_hop06_intelligence.png`

### Hop 7 — Alerts (domain filter + timestamp + lineage + ack)
Three alerts (drift/inference-health/stale — emitted through the real B-05
paths) rendered with derived domains (risk/system/market), absolute-UTC
Created lines, Lineage sources, and Audit correlation lines. The MARKET
domain filter isolated its alert (1/3). Ack moved the surface from 3 to 2
unacked buttons after the backend POST 200 — read-state-only. —
`x01t_hop07_alerts.png`

### Hop 8 — Lineage / evidence (persisted-only)
The lineage panel over the real correlation report rendered the real report
hash + audit correlation; 1442 persisted source artifacts disclosed with the
12-node render cap note; the illustrative chain absent; ZERO interactive
controls inside the panel. — `x01t_hop08_lineage.png`

### Hop 9 — Assistant (grounded + refusals)
Grounding candidates listed from the four persisted report families. A
grounded ask over the real correlation report returned
"Correlation BTCUSD/ETHUSD r=0.8766 n=721" with the audit correlation
rendered. "Please place a buy order…" → ORDER_INSTRUCTION_REFUSED. A clean
panel (no selection) asking "Market outlook?" → GROUNDING_REQUIRED (honest).
— `x01t_hop09_assistant.png`

### Hop 10 — Governance & non-actuation, end-to-end
Refined actuation-control scan over every button/link/input label: **zero
violations** (the inert research surfaces "Execution Research" / "Trade
Planning" / "Portfolio Research" are correctly non-actuation). Posture badge
`live:simulated`. Audit trail active: the backend's last 50 audit events are
SECURITY 20 / GOVERNANCE 30. — `x01t_hop10_governance.png`

### Server-log cross-reference (1143 request lines)
12 indicator-series calls (structural derivation), 3× each intelligence POST
201 (correlation/regime/scenario/portfolio-risk) + 3× signal-validation 422,
3 alert acks (200), 12 assistant-respond 201s, 4 audit-events reads, 9 logins,
24 ws-tickets — matching the workflow hops exactly.

## 2. Non-actuation end-to-end summary

Every hop exercised the platform's own controls; the refined control scan
found no order/broker/account/execute/margin surface anywhere; the assistant
refused the order instruction; the ack was read-state-only; the posture
labels (Gate CLOSED, live:simulated, research-only framing) were visible at
each relevant surface. Nothing in the workflow mutated anything beyond
research artifacts (reports, alerts' read-state, assistant responses) — all
inert by design.

## 3. Gap list (honest)

1. **Predictive deferral** — no promoted model exists (B-ML/B-ML2 honest
   negatives; Operator Decision Record). Predictive signals remain gated;
   their resumption is now the Operator's decision (this milestone unblocked
   it).
2. **Live data is simulated** — labeled `live:simulated` everywhere (posture
   badges, provenance lines). A real broker/feed integration remains a future
   governance-gated unit (Blueprint §7 Option A).
3. **Carried residuals** — OBS-B-AUDIT-1 (file-sqlite business-write
   serialization), the two react-router MODERATE advisories (RR7 migration),
   OBS-F05-1 (lineage pagination enhancement).
4. **Environment note** — verification ran on the dev stack (vite dev +
   uvicorn dev) with the disclosed capture fixtures (real corpus under the
   terminal symbol keys; alert conditions via the real emission paths).

## 4. Defects found

**None.** The capture required two evidence-tooling corrections (both
disclosed): (a) the sticky global header intercepted pointer events on
scrolled elements in the headless viewport — the capture uses programmatic DOM
activation (the equivalent of keyboard activation) for dock/rail controls;
(b) the hop-10 scan initially flagged the word "execution" from the
"Execution Research" navigation label — the scan was refined to
actuation-control phrase matching and re-run (zero violations). Neither is a
platform defect; no corrective order is required.

---

**Posture unchanged:** Gate CLOSED · Production NOT CERTIFIED · research-only ·
non-actuating. **We don't guess. We prove.**
