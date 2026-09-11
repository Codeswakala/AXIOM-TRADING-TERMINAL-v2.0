import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import {
  ArtifactLineageTree,
  buildDefaultLineageChain,
} from "./ArtifactLineageTree";

describe("UI-008-P04 ArtifactLineageTree Component (T-2, T-7, U-2)", () => {
  it("renders visual lineage tree with all sequential chain nodes (T-2, U-2)", () => {
    render(
      <ArtifactLineageTree
        rootArtifactId="rep-regime-001"
        rootArtifactType="regime_report"
        sourceArtifactIds={["sig-101"]}
        inputHash="abcdef1234567890abcdef1234567890"
      />,
    );

    const tree = screen.getByTestId("artifact-lineage-tree");
    expect(tree).toBeInTheDocument();
    expect(screen.getByText(/Root: rep-regime-001/i)).toBeInTheDocument();

    expect(screen.getByText("Market Data Series")).toBeInTheDocument();
    expect(screen.getByText("Feature Set Engine")).toBeInTheDocument();
    expect(screen.getByText("Grounded Model Registry")).toBeInTheDocument();
    expect(screen.getByText("REGIME REPORT")).toBeInTheDocument();
    expect(screen.getByText("Source: sig-101")).toBeInTheDocument();
    expect(screen.getByText("Assistant Research Explanation")).toBeInTheDocument();
  });

  it("handles node click selection (T-7 Lineage Integrity)", () => {
    const handleSelect = vi.fn();

    render(
      <ArtifactLineageTree
        rootArtifactId="rep-corr-002"
        rootArtifactType="correlation_report"
        onSelectNode={handleSelect}
      />,
    );

    const node = screen.getByTestId("lineage-node-rep-corr-002");
    expect(node).toBeInTheDocument();

    fireEvent.click(node.querySelector(".ix-node-card")!);
    expect(handleSelect).toHaveBeenCalledWith("rep-corr-002");
  });

  it("buildDefaultLineageChain produces valid node graph", () => {
    const nodes = buildDefaultLineageChain("rep-test-99", "scenario_report", ["src-a", "src-b"]);
    expect(nodes.length).toBe(7);
    expect(nodes[0].type).toBe("market_input");
    expect(nodes[nodes.length - 1].type).toBe("assistant_explanation");
  });
});
