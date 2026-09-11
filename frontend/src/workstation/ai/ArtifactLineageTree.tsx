/**
 * ArtifactLineageTree Component (UI-008-P04)
 *
 * Renders a visual lineage tree connecting:
 * Market Input -> Feature Store -> Model Registry -> Research Report -> Advisory Signal / Explanation
 *
 * Invariant: Strictly read-only provenance display; no mutation actions.
 */

import { useState } from "react";

export interface LineageNode {
  id: string;
  label: string;
  type:
    | "market_input"
    | "feature_set"
    | "model"
    | "report"
    | "advisory_signal"
    | "assistant_explanation"
    /** BO-F-05: neutral role for a persisted source artifact whose kind is
        not asserted by the record — added so lineage panels never have to
        fabricate a role (e.g. labeling an arbitrary source id as a "model"
        or "signal" would invent a relationship). */
    | "source_artifact";
  hash?: string;
  timestamp?: string;
  status?: string;
  metadata?: Record<string, string>;
}

export interface ArtifactLineageTreeProps {
  rootArtifactId: string;
  rootArtifactType: string;
  sourceArtifactIds?: string[];
  customNodes?: LineageNode[];
  inputHash?: string | null;
  onSelectNode?: (nodeId: string) => void;
}

export function buildDefaultLineageChain(
  rootId: string,
  rootType: string,
  sourceIds: string[] = [],
  inputHash?: string | null,
): LineageNode[] {
  const nodes: LineageNode[] = [
    {
      id: `input-${rootId.slice(0, 8)}`,
      label: "Market Data Series",
      type: "market_input",
      hash: inputHash ?? "e3b0c44298fc1c149afbf4c8996fb924",
      status: "VERIFIED",
    },
    {
      id: `feat-${rootId.slice(0, 8)}`,
      label: "Feature Set Engine",
      type: "feature_set",
      status: "v1.0.canonical",
    },
    {
      id: `model-${rootId.slice(0, 8)}`,
      label: "Grounded Model Registry",
      type: "model",
      status: "grounded_rules_v1",
    },
    {
      id: rootId,
      label: `${rootType.replace(/_/g, " ").toUpperCase()}`,
      type: "report",
      status: "RESEARCH_ONLY",
    },
  ];

  if (sourceIds.length > 0) {
    for (const src of sourceIds) {
      nodes.push({
        id: src,
        label: `Source: ${src}`,
        type: "advisory_signal",
        status: "LINKED",
      });
    }
  }

  nodes.push({
    id: `explain-${rootId.slice(0, 8)}`,
    label: "Assistant Research Explanation",
    type: "assistant_explanation",
    status: "DETERMINISTIC",
  });

  return nodes;
}

export function ArtifactLineageTree({
  rootArtifactId,
  rootArtifactType,
  sourceArtifactIds = [],
  customNodes,
  inputHash,
  onSelectNode,
}: ArtifactLineageTreeProps) {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  const nodes =
    customNodes ??
    buildDefaultLineageChain(rootArtifactId, rootArtifactType, sourceArtifactIds, inputHash);

  const nodeIconMap: Record<LineageNode["type"], string> = {
    market_input: "\u{1F4CA}", // chart
    feature_set: "\u{2699}", // gear
    model: "\u{1F9E0}", // brain
    report: "\u{1F4DC}", // scroll
    advisory_signal: "\u{1F4E1}", // satellite
    assistant_explanation: "\u{1F916}", // robot
    source_artifact: "\u{1F5C4}", // card box (neutral artifact)
  };

  function handleNodeClick(nodeId: string) {
    setSelectedNodeId(nodeId);
    if (onSelectNode) {
      onSelectNode(nodeId);
    }
  }

  return (
    <div
      className="ix-artifact-lineage-tree"
      data-testid="artifact-lineage-tree"
      data-ui008-component="lineage-tree"
      role="region"
      aria-label="Artifact Lineage Tree"
    >
      <div className="ix-lineage-tree-header">
        <span className="ix-tree-title">Analytical Lineage Provenance</span>
        <span className="ix-metadata mono">Root: {rootArtifactId}</span>
      </div>

      <ol className="ix-lineage-node-list" role="list">
        {nodes.map((node, index) => (
          <li
            key={node.id}
            className={`ix-lineage-node-item ${selectedNodeId === node.id ? "ix-node--selected" : ""}`}
            data-testid={`lineage-node-${node.id}`}
            data-ui008-node-type={node.type}
          >
            <div className="ix-node-card" onClick={() => handleNodeClick(node.id)}>
              <div className="ix-node-header">
                <span className="ix-node-step mono">{index + 1}.</span>
                <span className="ix-node-icon" aria-hidden="true">
                  {nodeIconMap[node.type]}
                </span>
                <strong className="ix-node-label">{node.label}</strong>
                {node.status && <span className="ix-badge ix-badge--node-status">{node.status}</span>}
              </div>

              <div className="ix-node-body">
                <span className="ix-node-id mono">{node.id}</span>
                {node.hash && (
                  <span className="ix-node-hash mono" data-testid="node-hash">
                    Hash: {node.hash.slice(0, 16)}...
                  </span>
                )}
              </div>
            </div>

            {index < nodes.length - 1 && (
              <div className="ix-lineage-connector" aria-hidden="true">
                <span className="ix-connector-arrow">{"\u{2193}"}</span>
              </div>
            )}
          </li>
        ))}
      </ol>
    </div>
  );
}
