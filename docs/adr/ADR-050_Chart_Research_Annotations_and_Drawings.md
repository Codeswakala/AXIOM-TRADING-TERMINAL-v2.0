# ADR-050 — Chart Research Annotations and Drawing Tools

| Field | Value |
|---|---|
| Status | Accepted for W5-U03 implementation by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-17 |
| Unit | W5-U03 — Human-AI Collaboration: Chart Research Annotations & Drawing Tools |
| Platform version | 0.41.0 |
| Builds on | W0-U07 chart foundation, W5-U01 safety foundation, W5-U02 audited assistant response persistence |

---

## Context

W5-U03 is the first Wave-5 operator-facing UI unit. The Build Order authorizes inert, presentation-only chart research annotations/drawing tools linked to source artifacts. Because the unit has UI, browser evidence is mandatory. The unit must not create order tickets, signals, execution instructions, account/broker/position linkage, raw-score display, guaranteed/predicted outcomes, external LLM behavior, or client-side authoritative recomputation.

---

## Decision

Add a single inert table, `chart_research_annotations`, for both research note annotations and drawing-tool markups. Drawing variants are represented through the inert `artifact_type` and `content.drawing_kind` fields rather than a separate table.

Each annotation stores:

- `id`
- UTC `created_at`
- `operator_id`
- `artifact_type`
- `chart_context` JSON: market/symbol/timeframe/anchor context only
- `content` JSON: research text and presentation geometry only
- `source_artifact_ids`
- `provenance`
- `uncertainty`
- `disclaimer`
- `research_status`
- `audit_correlation_id`

Creation is confined to `ChartResearchAnnotationRepository.create_annotation()`, which validates inertness, writes the annotation, and appends `audit_events.action = 'chart_research_annotation.created'` in the same transaction. If audit append fails, the repository raises so the outer transaction rolls back rather than leaving an orphan annotation.

Expose API:

- `GET /api/v1/collaboration/chart-annotations`
- `GET /api/v1/collaboration/chart-annotations/{annotation_id}`
- `POST /api/v1/collaboration/chart-annotations`

The POST endpoint is an authenticated operator-authored write to the annotation store only. It does not invoke assistant behavior, emit a signal, place an order, size a position, modify an account, or open the Gate.

Add a presentation-only annotation layer to the existing chart workspace. The UI renders persisted annotations on the chart with source ids and a research/not-instruction disclaimer. No AI-assisted annotation generation is implemented in W5-U03.

---

## Inertness controls

The annotation contract rejects forbidden keys recursively, including order/sizing/account/execution/position fields and signal/raw-score/guarantee fields. It also rejects raw-score and guaranteed-outcome text markers.

The schema itself has no columns named:

- `order_payload`
- `order_intent`
- `side`
- `quantity`
- `lot_size`
- `order_size`
- `position_size`
- `entry_price_order`
- `stop_loss`
- `take_profit`
- `broker_account_id`
- `account_id`
- `position_id`
- `execution_status`
- `live_position`
- signal-emission payload columns
- raw-score or predicted/guaranteed-outcome columns

---

## Consequences

### Positive

- Operators can create and view research annotations on charts while preserving advisory-only governance.
- Annotation persistence is auditable and no-orphan by construction.
- Browser-visible UI evidence can prove annotation rendering, disclaimer, and no execution controls.
- Future W5 units can link to the annotation store without creating execution semantics.

### Deliberately not included

- No external LLM/API.
- No AI-assisted annotation generation.
- No assistant action tool.
- No execution/order/sizing/broker/account/position path.
- No signal investigation workspace.
- No scenario comparison workspace.
- No trade plan or journal persistence.
- No client-side authoritative inference/analytics/signal recomputation.
- No raw-score rendering or guaranteed/predicted outcome framing.
- No Gate opening.

---

## Validation expectations

- Backend W5-U03 named tests pass: inert schema, forbidden-field rejection, triggers-nothing, persistence/no-orphan audit, API auth/read/create behavior.
- Frontend W5-U03 tests pass: annotations render on chart layer with sources/status, no raw score/guarantee display, no execution controls, no recompute language in annotation layer.
- Alembic head advances to `20260717_0025`.
- Operator evidence includes raw PostgreSQL SELECT, no-orphan audit JOIN, and real browser screenshots.

---

**End of ADR-050**
