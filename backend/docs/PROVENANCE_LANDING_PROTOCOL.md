# AXIOM — Provenance & Landing Protocol
## Binding for every subsequent unit (BO-B-00 §B-00.4)

| Item | Value |
|---|---|
| Instrument | `BO-B-00` §B-00.4 |
| Status | **BINDING** — applied to every subsequent unit (B-01 → B-07, F-units, X-01) |
| Scope | DA deliveries on the AXIOM programme |

## R1 — A unit is landed only when its SHAs are cited

A Delivery Report may claim a unit landed only if it cites, for every shipped artifact:

1. the **patch artifact sha256** (the delta against the verified chain, per the
   baseline stated in the report);
2. the **per-file content SHA-256** of every changed source/test file;
3. the **evidence artifact SHA-256** of every capture, transcript, and log the
   report relies on (Level-I raw output, Level-II executed test output,
   Level-III document content);
4. the **chain position** the patch occupies and the baseline it applies onto,
   with a `git apply --check` exit-0 transcript from a pristine clone.

No SHA, no landing claim. A declaration of completion is not evidence of
completion.

## R2 — Delivery Reports reference the canonical registers

Every Delivery Report must name, and update where the unit changes them:

1. `docs/governance/TECHNICAL_DEBT_REGISTER.md` — findings, debt rows, carried
   observations;
2. the verified patch chain (the artifact of record) — new element sha256 and
   position;
3. `docs/evidence/` — the evidence directory where this unit's transcripts
   live, with hashes.

## R3 — Declared-but-untransmitted is a delivery-process defect

Per the standing rule `OBS-DELIVERY-PROCESS`: before any transmission, verify
mechanically that every hash declared in the report resolves to an actual
artifact on disk, and state which artifacts are newly transmitted versus
already received. No "ATTACHED" claim for an artifact that has not been sent.

## R4 — Evidence classes

| Class | Definition | Example |
|---|---|---|
| Level I | Raw, directly observable output | command transcripts, runtime probes, soak output, live API responses |
| Level II | Executed test output | pytest/vitest run transcripts with counts |
| Level III | Document content | protocols, reports, register entries |

## R5 — Custody model

The repository is Operator-controlled storage. The DA works in its own
workspace; publication, commits, pushes, and pulls are Operator actions, not DA
actions. The verified patch artifact is the record of record between the DA and
ITRGA.

## R6 — No self-approval

The DA evidences; ITRGA verifies. A unit closes only on ITRGA's independent
determination. Production certification remains a separate Operator/ITRGA
decision, and nothing in this protocol alters the posture
GATE CLOSED · NOT CERTIFIED · RESEARCH-ONLY · NON-ACTUATING.

---

**End of Provenance & Landing Protocol (BO-B-00 §B-00.4)**
