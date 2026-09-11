# ADR-066 — Research Management Collections and Tags

| Field | Value |
|---|---|
| Status | Implemented by DA; pending operator evidence / ITRGA review |
| Date | 2026-07-18 |
| Unit | W7-U03 — Research Management Collections & Tags |
| Platform candidate | v0.57.0 |
| Alembic head | `20260717_0037` |

## Context

W7-U03 authorizes a metadata organization layer for existing governed research artifacts. Operators need collections and tags, but the constitutional boundary is strict: organizing an artifact must never mutate the organized artifact, its content, or its own audit trail.

The unit also carries W7-U02 OBS-1: mutation endpoints must authorize ownership before validating request bodies so cross-operator mutation attempts return deterministic `403` rather than body-validation `422`.

## Decision

AXIOM adds three operator-scoped tables:

- `research_collections` (`20260717_0035`)
- `research_collection_members` (`20260717_0036`)
- `research_tags` (`20260717_0037`)

Members and tags store only `(artifact_type, artifact_id)` reference metadata. There is no source-artifact FK, no cascading source relationship, and no source-content copy column.

The API is added under `/api/v1/institutional-platform`:

- `GET/POST /research-collections`
- `GET/DELETE /research-collections/{collection_id}`
- `GET/POST /research-collections/{collection_id}/members`
- `DELETE /research-collections/{collection_id}/members/{member_id}`
- `GET/POST /research-tags`
- `GET/DELETE /research-tags/{tag_id}`
- `GET /research-management`

All routes require current-operator authentication and apply operator scoping. Cross-operator collection/tag reads and mutation attempts return `403`. Member addition checks collection ownership before parsing the request body.

The frontend adds `/research-management`, a protected research-management page displaying collections, member references, tags, and read-only scenario report targets.

## Consequences

- Operators can organize governed artifacts without changing source artifact rows.
- Persistence capture is available for all three W7-U03 tables.
- Audit events are appended for collection/member/tag create and delete operations.
- No execution/order/broker/account/Gate path is introduced.
- No dependency is added.
- W7-U04 remains unauthorized until ITRGA approves W7-U03.

## Required proof

Operator evidence must prove:

- raw rows exist in all three tables;
- no orphan audit and no orphan operator rows for all three tables;
- forbidden/source-content columns are absent;
- source artifact before/after identity is unchanged across collection/tag operations;
- source artifact audit trail gains no mutation event;
- two real operators with valid tokens have zero cross-operator leakage;
- cross-operator mutation with an empty body returns `403`;
- no secret/PII markers are stored;
- browser `/research-management` proof shows no actuation controls;
- Gate remains CLOSED and broker suite remains green.

---

**End of ADR-066**
