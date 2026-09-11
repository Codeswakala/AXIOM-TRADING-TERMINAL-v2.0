/**
 * LineageEvidencePanel — BO-F-05 (2026-08-22)
 *
 * The read-only lineage/evidence view for domain-derived analytical values,
 * reusing `ArtifactLineageTree` with PERSISTED-ONLY nodes. It answers the
 * Reconciliation §17 / §37 question — "where did this come from, what
 * supports it, what are its limitations" — by rendering the fields the
 * records actually carry:
 *
 *   - the artifact node: id, real `report_hash` (only when persisted),
 *     created_at, research status;
 *   - one `source_artifact` node per persisted `source_artifact_ids` entry;
 *   - the audit correlation id and created_by as evidence rows;
 *   - honest "provenance not recorded" wherever a lineage field is absent.
 *
 * It NEVER renders `buildDefaultLineageChain`'s illustrative default chain
 * (market → features → model → report) for real artifacts — that chain
 * would fabricate relationships the record does not assert. No mutation, no
 * actuation, no invented relationships.
 */

import {
  ArtifactLineageTree,
  type LineageNode,
} from "../../workstation/ai/ArtifactLineageTree";

export interface LineageEvidencePanelProps {
  artifactId: string;
  artifactType: string;
  reportHash?: string | null;
  createdAt?: string | null;
  researchStatus?: string | null;
  sourceArtifactIds?: string[] | null;
  auditCorrelationId?: string | null;
  createdBy?: string | null;
  /** For signal artifacts: the inference input hash (persisted field). */
  inputHash?: string | null;
}

/** BO-F-05: the number of persisted source nodes rendered per panel — real
    reports can carry per-bar lineage ids (hundreds); the cap keeps the tree
    legible and is disclosed honestly below the list (platform list-cap
    discipline). */
export const LINEAGE_SOURCE_RENDER_CAP = 12;

export function buildPersistedLineageNodes(
  props: Omit<LineageEvidencePanelProps, "artifactId"> & { artifactId: string },
): LineageNode[] {
  const nodes: LineageNode[] = [
    {
      id: props.artifactId,
      label: props.artifactType.replace(/_/g, " ").toUpperCase(),
      type: "report",
      hash: props.reportHash ?? undefined,
      timestamp: props.createdAt ?? undefined,
      status: props.researchStatus ?? undefined,
    },
  ];
  for (const sourceId of (props.sourceArtifactIds ?? []).slice(0, LINEAGE_SOURCE_RENDER_CAP)) {
    nodes.push({
      id: sourceId,
      label: "Source artifact",
      type: "source_artifact",
    });
  }
  return nodes;
}

const formatUtc = (iso: string): string => {
  const parsed = new Date(iso);
  if (Number.isNaN(parsed.getTime())) return iso;
  return `${parsed.toISOString().slice(0, 16).replace("T", " ")} UTC`;
};

export function LineageEvidencePanel({
  artifactId,
  artifactType,
  reportHash,
  createdAt,
  researchStatus,
  sourceArtifactIds,
  auditCorrelationId,
  createdBy,
  inputHash,
}: LineageEvidencePanelProps) {
  const nodes = buildPersistedLineageNodes({
    artifactId,
    artifactType,
    reportHash,
    createdAt,
    researchStatus,
    sourceArtifactIds,
  });

  const hasAnyEvidence =
    Boolean(reportHash) ||
    Boolean(auditCorrelationId) ||
    Boolean(createdBy) ||
    Boolean(createdAt) ||
    Boolean(inputHash);

  const totalSources = (sourceArtifactIds ?? []).length;
  const cappedSources = totalSources > LINEAGE_SOURCE_RENDER_CAP;

  return (
    <div
      className="lineage-evidence-panel"
      data-testid="lineage-evidence-panel"
      role="region"
      aria-label={`Lineage evidence for ${artifactId}`}
    >
      <ArtifactLineageTree
        rootArtifactId={artifactId}
        rootArtifactType={artifactType}
        customNodes={nodes}
        inputHash={inputHash ?? undefined}
      />
      {cappedSources ? (
        <p className="muted" data-testid="lineage-source-cap-note">
          {totalSources} source artifacts recorded; showing the first{" "}
          {LINEAGE_SOURCE_RENDER_CAP} (render cap).
        </p>
      ) : null}

      <div className="lineage-evidence-block" data-testid="lineage-evidence-block">
        <span className="expanded-heading">Evidence record</span>
        <dl className="kv-grid mono">
          <dt>Report hash:</dt>
          <dd data-testid="lineage-report-hash">
            {reportHash ? `${reportHash.slice(0, 16)}…` : "provenance not recorded"}
          </dd>
          <dt>Audit correlation:</dt>
          <dd data-testid="lineage-audit-correlation">
            {auditCorrelationId ?? "provenance not recorded"}
          </dd>
          {inputHash !== undefined && inputHash !== null ? (
            <>
              <dt>Input hash:</dt>
              <dd data-testid="lineage-input-hash">
                {inputHash ? `${inputHash.slice(0, 16)}…` : "provenance not recorded"}
              </dd>
            </>
          ) : null}
          <dt>Created:</dt>
          <dd>{createdAt ? formatUtc(createdAt) : "provenance not recorded"}</dd>
          <dt>Created by:</dt>
          <dd>{createdBy ?? "provenance not recorded"}</dd>
        </dl>
        {!hasAnyEvidence ? (
          <p className="muted" data-testid="lineage-not-recorded">
            Provenance not recorded for this artifact.
          </p>
        ) : null}
      </div>
    </div>
  );
}
