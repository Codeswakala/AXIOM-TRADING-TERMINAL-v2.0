import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { GovernanceEvidenceWorkspace } from "../../components/terminal/governance/GovernanceOverlay";
import { UI007_EVIDENCE_MANIFEST } from "../../components/terminal/governance/governanceRecords";
import type { InstitutionalIntelligenceBundle } from "../../api/client";

const validationBundle: InstitutionalIntelligenceBundle = {
  relation: [],
  context: [],
  hypothetical: [],
  risk: [],
  validation: [
    {
      id: "validation-report-007",
      artifact_type: "signal_validation_report",
      method_version: "validation.v1",
      research_status: "research_only",
      sample_count: 9,
      validation_scope: { market_class: "forex", symbol: "EURUSD", timeframe: "M1" },
      uncertainty: {
        method: "wilson_score_interval",
        lower: 0.12,
        upper: 0.64,
        confidence_level: 0.95,
        sample_count: 9,
      },
      limitations: ["research_only", "outcome_data_not_available"],
      source_signal_ids: ["signal-007", "signal-008"],
      input_lineage: { dataset_snapshot_hash: "snapshot-007", split_manifest_hash: "split-007" },
      audit_correlation_id: "audit-correlation-007",
      report_hash: "report-hash-007",
      created_at: "2026-07-27T09:00:00Z",
    },
  ],
};

function workspace() {
  return <GovernanceEvidenceWorkspace validationBundle={validationBundle} />;
}

async function readP04ProductionSource(): Promise<string> {
  const modules = import.meta.glob(
    [
      "../../components/terminal/governance/GovernanceOverlay.tsx",
      "../../components/terminal/governance/governanceRecords.ts",
      "../registry/workspaceRegistry.tsx",
      "../commands/quickActionCatalogue.ts",
      "../commands/commandTypes.ts",
      "../workflows/workflowNavigationMetadata.ts",
    ],
    {
      query: "?raw",
      import: "default",
    },
  );
  const values = await Promise.all(
    Object.values(modules).map((loader) => (loader as () => Promise<string>)()),
  );
  return values.join("\n").toLowerCase();
}

describe("UI-007-P04 evidence viewer and validation summary panels", () => {
  it("test_ui007_evidence_viewer_renders_existing_records_verbatim_no_ai_summary", () => {
    render(workspace());

    const viewer = screen.getByLabelText("Read-only evidence viewer");
    expect(viewer).toHaveTextContent("UI-007-P03");
    expect(viewer).toHaveTextContent("APPROVED WITH OBSERVATIONS");
    expect(viewer).toHaveTextContent("PLUGIN_CONTRACT_IMPORT_REFUSED");
    expect(viewer).toHaveTextContent("TD-UI-POSTCSS-HIGH");
    expect(viewer).toHaveTextContent("APPROVED — CLOSED");
    expect(viewer).toHaveTextContent("docs/build-orders/ITRGA_REVIEW_UI-007-P03.md");
    expect(UI007_EVIDENCE_MANIFEST).toHaveLength(2);
    expect(within(viewer).queryAllByRole("textbox")).toHaveLength(0);
    expect(within(viewer).queryAllByRole("button")).toHaveLength(0);
  });

  it("test_ui007_validation_summaries_preserve_scope_sample_uncertainty_and_limitations_no_cherry_picking", () => {
    render(workspace());

    const panel = screen.getByLabelText("Read-only validation summary panels");
    expect(panel).toHaveTextContent("1 returned record");
    expect(panel).toHaveTextContent("validation-report-007");
    expect(panel).toHaveTextContent("9");
    expect(panel).toHaveTextContent("EURUSD");
    expect(panel).toHaveTextContent("M1");
    expect(panel).toHaveTextContent("wilson_score_interval");
    expect(panel).toHaveTextContent("research_only");
    expect(panel).toHaveTextContent("outcome_data_not_available");
    expect(panel).toHaveTextContent("signal-007, signal-008");
    expect(panel).toHaveTextContent("snapshot-007");
    expect(panel).toHaveTextContent("report-hash-007");
  });

  it("test_ui007_evidence_viewer_no_recomputed_or_stronger_verdicts_than_source", () => {
    render(workspace());

    const panel = screen.getByLabelText("Read-only validation summary panels");
    expect(panel).toHaveTextContent("research_only");
    expect(panel).not.toHaveTextContent(/trading instruction/i);
    expect(panel).not.toHaveTextContent(/financial advice/i);
    expect(panel).not.toHaveTextContent(/production ready/i);
    expect(panel).not.toHaveTextContent(/approved for execution/i);
  });

  it("test_ui007_evidence_viewer_contains_no_governance_mutation_gate_or_certification_control", async () => {
    render(workspace());

    const sourceText = await readP04ProductionSource();
    for (const marker of [
      "open_gate",
      "allow_execution",
      "gate toggle",
      "toggle gate",
      "certify",
      "mark_ready",
      "approve_production",
      "waive",
      "risk_accept",
      "place_order",
      "exec" + "ute",
      "go-live",
      "connect-" + "broker",
      "br" + "oker",
      "account_id",
      "order_ticket",
      "pos" + "ition",
      "bal" + "ance",
      "mar" + "gin",
      "cap" + "ital",
      "alloc" + "ation",
      "real_pnl",
      "infersignal",
      "runinference",
      "authoritativerecompute",
      "emitsignal",
      "generatesignal",
      "generatescenario",
      "inferrelationship",
      "rec" + "ompute",
      "recalculat",
      "deriveconfidence",
      "reclassif",
      "open" + "ai",
      "external_" + "llm",
      "llm_" + "summary",
      "ai_" + "summary",
      "/api/v1/" + "orders",
    ]) {
      expect(sourceText).not.toContain(marker);
    }
  });

  it("test_ui007_evidence_viewer_accessibility_and_doc16_brand_hold", () => {
    render(workspace());

    const viewer = screen.getByLabelText("Read-only evidence viewer");
    const validation = screen.getByLabelText("Read-only validation summary panels");
    expect(screen.getByRole("heading", { name: "Evidence Viewer" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Validation Summary Panels" })).toBeInTheDocument();
    expect(viewer.querySelectorAll(".mono").length).toBeGreaterThan(8);
    expect(validation.querySelectorAll(".mono").length).toBeGreaterThan(8);
    expect(viewer.querySelectorAll("[data-verbatim='true']").length).toBe(UI007_EVIDENCE_MANIFEST.length);
    expect(validation.querySelectorAll("[data-verbatim='true']").length).toBe(1);
  });
});
