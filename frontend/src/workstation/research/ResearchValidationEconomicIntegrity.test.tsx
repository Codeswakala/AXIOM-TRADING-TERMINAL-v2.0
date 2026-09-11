import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ValidationEconomicIntegrityPanel } from "../../pages/InstitutionalIntelligencePage";
import type {
  AdvisoryAnalyticsResponse,
  AdvisorySignal,
  InstitutionalIntelligenceBundle,
  InstitutionalReport,
} from "../../api/client";

function report(overrides: Partial<InstitutionalReport> = {}): InstitutionalReport {
  return {
    id: "validation-report-1",
    artifact_type: "signal_validation_report",
    method_version: "validation.v1",
    sample_count: 9,
    research_status: "research_only",
    report_hash: "hash-validation-1",
    limitations: ["research_only", "low_sample_count"],
    uncertainty: {
      method: "wilson_score_interval",
      lower: 0.12,
      upper: 0.64,
      confidence_level: 0.95,
      sample_count: 9,
    },
    economic_usefulness: { verdict: "not_assessed" },
    outcome_data_status: { status: "not_available" },
    source_artifact_ids: ["sig-warning", "report-source"],
    market_scope: { symbol: "EURUSD", timeframe: "M1", sample_count: 9 },
    results: { stored_validation_rate: 0.33 },
    ...overrides,
  };
}

function signal(overrides: Partial<AdvisorySignal> = {}): AdvisorySignal {
  return {
    signal_id: "sig-warning",
    created_at: "2026-07-24T08:00:00Z",
    as_of_time: "2026-07-24T07:59:00Z",
    market_class: "forex",
    provider: "internal",
    symbol: "EURUSD",
    timeframe: "M1",
    model_artifact_id: "model-1",
    model_version: "model.v1",
    feature_set_version: "features.v1",
    experiment_id: "exp-1",
    statistical_report_id: "stat-1",
    calibration_report_id: "cal-1",
    economic_report_id: "econ-1",
    generalization_report_id: "gen-1",
    inference_input_hash: "hash-1",
    raw_score: 0.99,
    calibrated_confidence: 0.41,
    input_staleness_seconds: 60,
    signal_validity_seconds: 300,
    expires_at: "2026-07-24T08:05:00Z",
    freshness_status: "fresh",
    signal_direction: "positive_bias",
    signal_state: "warning",
    state_reason: "POORLY_CALIBRATED",
    eligibility_reasons: [],
    operating_domain_status: "valid",
    calibration_status: "warning:POORLY_CALIBRATED",
    economic_verdict: "not_assessed",
    risk_notes: null,
    rationale: "Stored warning signal.",
    explainability_summary: {},
    state_transition_history: ["candidate", "warning"],
    audit_correlation_id: "corr-1",
    ...overrides,
  };
}

const bundle: InstitutionalIntelligenceBundle = {
  relation: [],
  context: [],
  hypothetical: [],
  risk: [],
  validation: [report()],
};

const analytics = {
  generated_from: "existing-read-api",
  disclaimer: "Research analytics only.",
  metrics: [
    {
      key: "clean_rate",
      label: "Clean rate",
      value: 0.5,
      unit: "ratio",
      sample_count: 9,
      uncertainty: {
        method: "wilson_score_interval",
        lower: 0.12,
        upper: 0.64,
        confidence_level: 0.95,
        sample_count: 9,
      },
      interpretation: "Stored analytics field.",
    },
  ],
  confidence_bands: [],
  notes: [],
  included_scope: { symbol: "EURUSD", timeframe: "M1", sample_count: 9 },
} as AdvisoryAnalyticsResponse & { included_scope: Record<string, unknown> };

async function readProductionSource(pathSuffix: string): Promise<string> {
  const modules = import.meta.glob("../../**/*.{ts,tsx}", {
    query: "?raw",
    import: "default",
  });
  const fileName = pathSuffix.split("/").pop() ?? pathSuffix;
  const entry = Object.entries(modules).find(
    ([path]) => path.endsWith(pathSuffix) || path.endsWith(fileName),
  );
  if (!entry) throw new Error(`Raw source not found: ${pathSuffix}`);
  return (entry[1] as () => Promise<string>)();
}

describe("UI-004-P04 validation and economic-usefulness integrity panels", () => {
  it("test_ui004_validation_statuses_are_rendered_verbatim_from_existing_artifacts", () => {
    render(<ValidationEconomicIntegrityPanel bundle={bundle} signals={[signal()]} analytics={analytics} />);

    const validation = screen.getByLabelText("Stored validation statuses");
    expect(validation).toHaveTextContent("research_only");
    expect(validation).toHaveTextContent("not_available");
    expect(validation).toHaveTextContent("POORLY_CALIBRATED");
    expect(validation).toHaveTextContent("warning:POORLY_CALIBRATED");
    expect(validation).toHaveTextContent("valid");
    expect(validation).toHaveTextContent("fresh");
  });

  it("test_ui004_economic_usefulness_verdicts_are_not_rederived_or_upgraded", () => {
    render(<ValidationEconomicIntegrityPanel bundle={bundle} signals={[signal()]} analytics={analytics} />);

    const economic = screen.getByLabelText("Stored economic-usefulness verdicts");
    expect(economic).toHaveTextContent("not_assessed");
    expect(economic).toHaveTextContent("research_only");
    expect(economic).not.toHaveTextContent(/economically usable/i);
    expect(economic).not.toHaveTextContent(/tradable/i);
    expect(economic).not.toHaveTextContent(/approved/i);
    expect(economic).not.toHaveTextContent(/reliable/i);
  });

  it("test_ui004_no_cherry_picking_sample_counts_scope_and_limitations_visible", () => {
    render(<ValidationEconomicIntegrityPanel bundle={bundle} signals={[signal()]} analytics={analytics} />);

    const scope = screen.getByLabelText("Validation scope sample counts and limitations");
    expect(scope).toHaveTextContent("9");
    expect(scope).toHaveTextContent("12.00% to 64.00%");
    expect(scope).toHaveTextContent("sig-warning, report-source");
    expect(scope).toHaveTextContent("EURUSD");
    expect(scope).toHaveTextContent("M1");
    expect(scope).toHaveTextContent("research_only");
    expect(scope).toHaveTextContent("low_sample_count");
  });

  it("test_ui004_validation_economic_panels_contain_no_client_side_analytics_engine", async () => {
    const sourceText = await readProductionSource("pages/InstitutionalIntelligencePage.tsx");
    const forbidden = [
      "recompute",
      "recalculat",
      "reclassif",
      "deriveConfidence",
      "upgradeVerdict",
      "normalizeVerdict",
      "normalizeStatus",
      "new AnalyticsEngine",
      "new IntelligenceEngine",
      "/api/v1/orders",
    ];
    for (const marker of forbidden) {
      expect(sourceText).not.toContain(marker);
    }
    expect(sourceText).toContain("ValidationEconomicIntegrityPanel");
    expect(sourceText).toContain("Verbatim verdicts");
  });

  it("test_ui004_validation_economic_panels_preserve_research_only_disclaimers", () => {
    render(<ValidationEconomicIntegrityPanel bundle={bundle} signals={[signal()]} analytics={analytics} />);

    const panel = screen.getByLabelText("Validation and economic-usefulness integrity panels");
    expect(panel).toHaveTextContent("Research-only interpretation boundary");
    expect(panel).toHaveTextContent("not trading instructions");
    expect(panel).toHaveTextContent("not financial advice");
    expect(panel).toHaveTextContent("not execution criteria");
    expect(panel).toHaveTextContent("operator decides independently");
    expect(within(panel).getByLabelText("Verbatim verdict guardrail")).toHaveTextContent("Stored status");
  });
});
