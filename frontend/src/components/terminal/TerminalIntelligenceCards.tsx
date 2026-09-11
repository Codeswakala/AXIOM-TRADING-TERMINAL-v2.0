import { useEffect, useState } from "react";
import { useTerminal } from "./TerminalContext";
import {
  fetchCandles,
  fetchCorrelationReports,
  fetchPortfolioRiskReports,
  fetchRegimeReports,
  fetchScenarioReports,
  fetchSignalValidationReports,
  createCorrelationReport,
  createPortfolioRiskReport,
  createRegimeReport,
  createScenarioReport,
  createSignalValidationReport,
  IntelligenceGenerationError,
  type CorrelationReport,
  type PortfolioRiskReport,
  type RegimeReport,
  type ScenarioReport,
  type SignalValidationReport,
} from "../../api/client";
import { MetricWithInterval } from "./StatisticalValueRenderer";
import { LineageEvidencePanel } from "./LineageEvidencePanel";
import "./TerminalMultiPane.css";

export type IntelligenceTab =
  | "CALIBRATION"
  | "CORRELATION"
  | "REGIME"
  | "SCENARIO"
  | "PORTFOLIO-RISK";

export interface TerminalIntelligenceCardsProps {
  className?: string;
  initialTab?: IntelligenceTab;
}

/**
 * TerminalIntelligenceCards
 *
 * Docked quantitative intelligence surface exposing:
 * - Signal Validation & Reliability metrics (Calibrated Coverage, Clean Advisory Rate, Guardrail Rate, Wilson bounds)
 * - Cross-Asset Correlation Matrix & Significance (Pearson r, Fisher Z confidence intervals)
 * - Market Regime Detection (HMM/Classifier labels and posterior uncertainty bounds)
 *
 * BO-F-03 (2026-08-21): the surface now presents ALL FIVE B-04 intelligence
 * families (correlation, regime, scenario, portfolio-risk, signal-validation)
 * — each card carries uncertainty, sample counts, limitations, the data-class
 * label (server-appended `notes`), lineage (report hash prefix / source ids),
 * and the research-only framing — plus a GOVERNED GENERATION surface that
 * calls the B-04 POSTs (research-artifact creation ONLY; on-request; never
 * actuation, never a signal).
 *
 * Adheres strictly to:
 * - B-P04-2: Zero client-side computation of statistics (renders server figures verbatim)
 * - B-P04-1: All metrics bound to their uncertainty intervals
 * - BO-F-03.4: no actuation controls; no fabricated reports; server-values-only
 * - SAL-2 (Internal) presentation surface
 */

const CRYPTO_SYMBOL_KEYS = new Set(["BTCUSD", "ETHUSD", "SOLUSD"]);

/** The generation window is a 30-day span ending at the freshest persisted
 * candle of the active series (real data only — no fabricated windows). */
const GENERATION_WINDOW_DAYS = 30;

/** Deterministic correlation partner for the active symbol (disclosed D2). */
function correlationPartner(activeSymbolKey: string): string {
  if (activeSymbolKey === "ETHUSD" || activeSymbolKey === "SOLUSD") return "BTCUSD";
  if (activeSymbolKey === "BTCUSD") return "ETHUSD";
  if (activeSymbolKey === "EURUSD") return "GBPUSD";
  return "EURUSD";
}

function marketClassOf(symbolKey: string): string {
  return CRYPTO_SYMBOL_KEYS.has(symbolKey) ? "crypto" : "forex";
}

const RESEARCH_ONLY_FRAMING =
  "Research artifact only — not a signal, not causation, not a prediction, not financial advice.";

/** Server-value-only: the outcome-data status is rendered verbatim. */
function formatOutcomeStatus(report: SignalValidationReport): string {
  const status = (report as Record<string, unknown>).outcome_data_status;
  if (status === null || status === undefined) return "n/a";
  if (typeof status === "string") return status;
  return JSON.stringify(status);
}

type GenerationStatus =
  | { phase: "idle" }
  | { phase: "generating" }
  | { phase: "done"; reportId: string }
  | { phase: "insufficient"; errorCode: string }
  | { phase: "error"; message: string };

interface GenerationWindow {
  asOfStart: string;
  asOfEnd: string;
}

/** Window builder shared by the generation triggers. */
async function resolveGenerationWindow(
  symbolKey: string,
  timeframe: string,
): Promise<GenerationWindow | null> {
  try {
    const series = await fetchCandles({
      symbol: symbolKey,
      timeframe,
      limit: 1,
      order: "desc",
    });
    if (series.kind === "unavailable" || series.bars.length === 0) return null;
    const latest = series.bars[0].open_time;
    const endMs = new Date(latest).getTime();
    if (Number.isNaN(endMs)) return null;
    return {
      asOfEnd: latest,
      asOfStart: new Date(endMs - GENERATION_WINDOW_DAYS * 24 * 3600 * 1000).toISOString(),
    };
  } catch {
    return null;
  }
}

/** BO-F-03.3 — the governed generation surface (research-artifact creation). */
function IntelligenceGenerationPanel({ onGenerated }: { onGenerated: () => void }) {
  const { selectedSymbol } = useTerminal();
  const symbolKey = selectedSymbol.replace(/[^a-zA-Z0-9]/g, "").toUpperCase();
  const timeframe = "H1"; // the corpus timeframe (disclosed D2)
  const [window, setWindow] = useState<GenerationWindow | null | "loading">("loading");
  const [statuses, setStatuses] = useState<Record<string, GenerationStatus>>({});

  useEffect(() => {
    let cancelled = false;
    setWindow("loading");
    setStatuses({});
    void resolveGenerationWindow(symbolKey, timeframe).then((resolved) => {
      if (!cancelled) setWindow(resolved);
    });
    return () => {
      cancelled = true;
    };
  }, [symbolKey]);

  async function runGeneration(family: string) {
    if (window === "loading" || window === null) return;
    setStatuses((current) => ({ ...current, [family]: { phase: "generating" } }));
    try {
      let reportId: string;
      if (family === "correlation") {
        const report = await createCorrelationReport({
          left: { market_class: marketClassOf(symbolKey), symbol: symbolKey, timeframe },
          right: {
            market_class: marketClassOf(correlationPartner(symbolKey)),
            symbol: correlationPartner(symbolKey),
            timeframe,
          },
          as_of_start: window.asOfStart,
          as_of_end: window.asOfEnd,
        });
        reportId = report.id;
      } else if (family === "regime") {
        const report = await createRegimeReport({
          series: { market_class: marketClassOf(symbolKey), symbol: symbolKey, timeframe },
          as_of_start: window.asOfStart,
          as_of_end: window.asOfEnd,
        });
        reportId = report.id;
      } else if (family === "scenario") {
        const report = await createScenarioReport({
          series: { market_class: marketClassOf(symbolKey), symbol: symbolKey, timeframe },
          assumptions: {
            scenario_name: `${symbolKey} adverse-shock research scenario`,
            shock_return: -0.15,
            horizon_bars: 24,
            volatility_multiplier: 1.5,
          },
          as_of_start: window.asOfStart,
          as_of_end: window.asOfEnd,
        });
        reportId = report.id;
      } else if (family === "portfolio-risk") {
        const report = await createPortfolioRiskReport({
          series: { market_class: marketClassOf(symbolKey), symbol: symbolKey, timeframe },
          assumptions: {
            report_name: `${symbolKey} research portfolio-risk`,
            stress_multiplier: 2,
            tail_quantile: 0.05,
          },
          as_of_start: window.asOfStart,
          as_of_end: window.asOfEnd,
        });
        reportId = report.id;
      } else {
        const report = await createSignalValidationReport({
          scope_start: window.asOfStart,
          scope_end: window.asOfEnd,
          market_class: marketClassOf(symbolKey),
          symbol: symbolKey,
          timeframe,
          include_states: ["emitted", "withheld", "warning"],
        });
        reportId = report.id;
      }
      setStatuses((current) => ({
        ...current,
        [family]: { phase: "done", reportId },
      }));
      onGenerated();
    } catch (err) {
      if (err instanceof IntelligenceGenerationError && err.insufficientData) {
        setStatuses((current) => ({
          ...current,
          [family]: { phase: "insufficient", errorCode: err.errorCode ?? "INSUFFICIENT_DATA" },
        }));
      } else if (err instanceof Error) {
        setStatuses((current) => ({ ...current, [family]: { phase: "error", message: err.message } }));
      } else {
        setStatuses((current) => ({
          ...current,
          [family]: { phase: "error", message: "Generation failed" },
        }));
      }
    }
  }

  const families = [
    { id: "correlation", label: "CORRELATION" },
    { id: "regime", label: "REGIME" },
    { id: "scenario", label: "SCENARIO" },
    { id: "portfolio-risk", label: "PORTFOLIO-RISK" },
    { id: "signal-validation", label: "SIGNAL-VALIDATION" },
  ] as const;

  return (
    <div className="intel-generation-panel" data-testid="generation-panel">
      <div className="intel-generation-header">
        <span className="panel-heading">Governed Generation</span>
        <span className="provenance-badge mono">B-04 · RESEARCH-ARTIFACT CREATION ONLY</span>
      </div>
      <p className="intel-generation-framing" data-testid="generation-framing">
        {RESEARCH_ONLY_FRAMING}
      </p>

      {window === "loading" ? (
        <p className="intel-generation-note" data-testid="generation-window-note">
          Resolving the data window for {symbolKey} {timeframe}…
        </p>
      ) : window === null ? (
        <p className="intel-generation-note" data-testid="generation-no-series-notice">
          No candle series for {symbolKey} {timeframe} — generation requires an existing series;
          no window is fabricated.
        </p>
      ) : (
        <p className="intel-generation-note mono" data-testid="generation-window-note">
          Window: {window.asOfStart} → {window.asOfEnd} · series {symbolKey} {timeframe} · on-request only
        </p>
      )}

      <div className="intel-generation-actions">
        {families.map((family) => {
          const status = statuses[family.id] ?? { phase: "idle" as const };
          const busy = status.phase === "generating";
          return (
            <div key={family.id} className="intel-generation-row">
              <button
                type="button"
                className="ix-shell-button intel-generate-btn mono"
                disabled={window === "loading" || window === null || busy}
                onClick={() => void runGeneration(family.id)}
                data-testid={`gen-btn-${family.id}`}
              >
                {busy ? "Generating…" : `Generate ${family.label}`}
              </button>
              {status.phase === "done" && (
                <span className="intel-gen-status ok mono" data-testid={`gen-status-${family.id}`}>
                  persisted: {status.reportId.slice(0, 16)}…
                </span>
              )}
              {status.phase === "insufficient" && (
                <span
                  className="intel-gen-status insufficient mono"
                  data-testid={`gen-insufficient-${family.id}`}
                >
                  Insufficient data: {status.errorCode} — nothing fabricated.
                </span>
              )}
              {status.phase === "error" && (
                <span className="intel-gen-status error mono" data-testid={`gen-error-${family.id}`}>
                  {status.message}
                </span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export function TerminalIntelligenceCards({
  className = "",
  initialTab = "CALIBRATION",
}: TerminalIntelligenceCardsProps) {
  const { selectedSymbol } = useTerminal();
  const [activeTab, setActiveTab] = useState<IntelligenceTab>(initialTab);
  const [validationReports, setValidationReports] = useState<SignalValidationReport[]>([]);
  const [correlationReports, setCorrelationReports] = useState<CorrelationReport[]>([]);
  const [regimeReports, setRegimeReports] = useState<RegimeReport[]>([]);
  const [scenarioReports, setScenarioReports] = useState<ScenarioReport[]>([]);
  const [portfolioRiskReports, setPortfolioRiskReports] = useState<PortfolioRiskReport[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [refreshTick, setRefreshTick] = useState(0);
  // BO-F-05.2: one read-only lineage panel open at a time (per report id).
  const [lineageOpenId, setLineageOpenId] = useState<string | null>(null);

  useEffect(() => {
    let isCancelled = false;
    async function loadIntelligence() {
      setIsLoading(true);
      try {
        const [valData, corrData, regimeData, scenData, riskData] = await Promise.all([
          fetchSignalValidationReports(10).catch(() => []),
          fetchCorrelationReports(10).catch(() => []),
          fetchRegimeReports(10).catch(() => []),
          fetchScenarioReports(10).catch(() => []),
          fetchPortfolioRiskReports(10).catch(() => []),
        ]);
        if (!isCancelled) {
          setValidationReports(valData);
          setCorrelationReports(corrData);
          setRegimeReports(regimeData);
          setScenarioReports(scenData);
          setPortfolioRiskReports(riskData);
        }
      } finally {
        if (!isCancelled) setIsLoading(false);
      }
    }
    void loadIntelligence();
    return () => {
      isCancelled = true;
    };
  }, [refreshTick]);

  const latestValReport = validationReports[0] ?? null;
  const latestRegime =
    regimeReports.find((r) => r.symbol.includes(selectedSymbol.replace("/", ""))) ??
    regimeReports[0] ??
    null;
  const latestScenario = scenarioReports[0] ?? null;
  const latestPortfolioRisk = portfolioRiskReports[0] ?? null;

  // Helper to extract rate and wilson interval safely
  const getRateData = (metricKey: string) => {
    if (!latestValReport?.metrics) return null;
    const raw = (latestValReport.metrics as Record<string, any>)[metricKey];
    if (!raw) return null;
    if (typeof raw === "number") {
      return { value: raw, lower: null, upper: null };
    }
    if (typeof raw === "object" && raw !== null) {
      const val = typeof raw.value === "number" ? raw.value : null;
      const unc = raw.uncertainty;
      const low = unc && typeof unc.lower === "number" ? unc.lower : null;
      const up = unc && typeof unc.upper === "number" ? unc.upper : null;
      return { value: val, lower: low, upper: up };
    }
    return null;
  };

  const calibCoverage = getRateData("calibrated_confidence_coverage");
  const cleanAdvisory = getRateData("clean_advisory_rate");
  const guardrailRate = getRateData("guardrail_intervention_rate");

  const hasAnyData =
    Boolean(latestValReport) ||
    Boolean(latestRegime) ||
    correlationReports.length > 0 ||
    Boolean(latestScenario) ||
    Boolean(latestPortfolioRisk);

  const dataClassOf = (notes: string | null | undefined): string => {
    if (!notes) return "data-class: none";
    const marker = notes.split(";").find((part) => part.trim().startsWith("data-class:"));
    return marker ? marker.trim() : "data-class: none";
  };

  const hashPrefix = (hash: string | undefined): string =>
    hash ? hash.slice(0, 12) : "none";

  const toggleLineage = (artifactId: string) => {
    setLineageOpenId((current) => (current === artifactId ? null : artifactId));
  };

  /** BO-F-05.2 — the read-only lineage/evidence affordance per report. */
  const renderLineage = (report: {
    id: string;
    artifact_type: string;
    report_hash?: string;
    created_at?: string;
    research_status?: string;
    audit_correlation_id?: string;
    created_by?: string;
    source_artifact_ids?: string[];
  }) => {
    const isOpen = lineageOpenId === report.id;
    return (
      <div className="intel-lineage-block">
        <button
          type="button"
          className="ix-shell-button intel-lineage-toggle mono"
          aria-expanded={isOpen}
          onClick={() => toggleLineage(report.id)}
          data-testid={`lineage-toggle-${report.id}`}
        >
          {isOpen ? "Close lineage" : "Lineage"}
        </button>
        {isOpen ? (
          <LineageEvidencePanel
            artifactId={report.id}
            artifactType={report.artifact_type}
            reportHash={report.report_hash ?? null}
            createdAt={report.created_at ?? null}
            researchStatus={report.research_status ?? null}
            sourceArtifactIds={report.source_artifact_ids ?? null}
            auditCorrelationId={report.audit_correlation_id ?? null}
            createdBy={report.created_by ?? null}
          />
        ) : null}
      </div>
    );
  };

  return (
    <div
      className={`terminal-intelligence-cards ${className}`}
      data-testid="terminal-intelligence-cards"
      role="region"
      aria-label="Institutional Quantitative Intelligence"
    >
      {/* Tab Switcher */}
      <div className="intelligence-tabs-header">
        <span className="intel-title">INTELLIGENCE</span>
        <div className="intel-tab-group" role="tablist">
          {(
            ["CALIBRATION", "CORRELATION", "REGIME", "SCENARIO", "PORTFOLIO-RISK"] as const
          ).map((tab) => (
            <button
              key={tab}
              type="button"
              role="tab"
              aria-selected={activeTab === tab}
              className={`intel-tab-btn ${activeTab === tab ? "active" : ""}`}
              onClick={() => setActiveTab(tab)}
              data-testid={`intel-tab-${tab.toLowerCase()}`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      <div className="intelligence-card-body">
        {isLoading && !hasAnyData ? (
          <div className="intel-loading-msg" data-testid="intel-loading">
            <span>Loading quantitative intelligence metrics…</span>
          </div>
        ) : activeTab === "CALIBRATION" ? (
          /* Card 1: Signal Validation & Reliability */
          <div className="intel-panel" data-testid="intel-calibration-panel">
            <div className="intel-panel-header">
              <span className="panel-heading">Signal Validation & Reliability</span>
              <span className="provenance-badge mono">Validated Server-Side</span>
            </div>

            {latestValReport ? (
              <div className="intel-metrics-grid">
                <MetricWithInterval
                  label="Calibrated Coverage"
                  value={calibCoverage?.value != null ? calibCoverage.value : null}
                  uncertainty={
                    calibCoverage?.lower != null && calibCoverage?.upper != null
                      ? { lower: calibCoverage.lower, upper: calibCoverage.upper, method: "wilson_score_interval" }
                      : null
                  }
                  isPercentage
                  precision={1}
                  testId="val-calibrated-coverage"
                />
                <MetricWithInterval
                  label="Clean Advisory Rate"
                  value={cleanAdvisory?.value != null ? cleanAdvisory.value : null}
                  uncertainty={
                    cleanAdvisory?.lower != null && cleanAdvisory?.upper != null
                      ? { lower: cleanAdvisory.lower, upper: cleanAdvisory.upper, method: "wilson_score_interval" }
                      : null
                  }
                  isPercentage
                  precision={1}
                  testId="val-clean-advisory"
                />
                <MetricWithInterval
                  label="Guardrail Intervention Rate"
                  value={guardrailRate?.value != null ? guardrailRate.value : null}
                  uncertainty={
                    guardrailRate?.lower != null && guardrailRate?.upper != null
                      ? { lower: guardrailRate.lower, upper: guardrailRate.upper, method: "wilson_score_interval" }
                      : null
                  }
                  isPercentage
                  precision={1}
                  testId="val-guardrail-rate"
                />
                <div className="intel-metric-box">
                  <span className="box-lbl">Aggregate Wilson Interval (95% CI)</span>
                  <span className="box-val mono" data-testid="val-wilson">
                    {latestValReport.uncertainty?.lower != null && latestValReport.uncertainty?.upper != null
                      ? `[${(Number(latestValReport.uncertainty.lower) * 100).toFixed(1)}% – ${(Number(latestValReport.uncertainty.upper) * 100).toFixed(1)}%]`
                      : "[Uncertainty: Unavailable]"}
                  </span>
                  <span className="box-sub mono">Sample N = {latestValReport.sample_count}</span>
                </div>

                {/* BO-F-03: outcome-data status (server value, verbatim) */}
                <div className="intel-metric-footer mono">
                  <span>Report ID: {latestValReport.id.slice(0, 16)}…</span>
                  <span>Method: {latestValReport.method_version}</span>
                </div>
                <div className="intel-framing-line mono" data-testid="val-outcome-status">
                  outcome-data: {formatOutcomeStatus(latestValReport)}
                </div>
                <div className="intel-framing-line" data-testid="val-framing">
                  {RESEARCH_ONLY_FRAMING}
                </div>
                {/* BO-F-05.1/.2 — per-report lineage (read-only) */}
                {renderLineage(latestValReport)}
              </div>
            ) : (
              <div className="intel-empty-note">
                <span>No validation report generated yet. Evaluated server-side.</span>
              </div>
            )}
          </div>
        ) : activeTab === "CORRELATION" ? (
          /* Card 2: Cross-Asset Correlation Matrix */
          <div className="intel-panel" data-testid="intel-correlation-panel">
            <div className="intel-panel-header">
              <span className="panel-heading">Cross-Asset Correlation</span>
              <span className="provenance-badge mono">Pearson r · Fisher Z</span>
            </div>

            <div className="correlation-list">
              {correlationReports.length === 0 ? (
                <div className="intel-empty-note">
                  <span>No correlation reports available.</span>
                </div>
              ) : (
                correlationReports.map((corr) => {
                  const r = corr.correlation_value;
                  const isNeg = r < 0;
                  const unc = corr.uncertainty;
                  const hasBounds = unc?.lower != null && unc?.upper != null;
                  return (
                    <div key={corr.id} className="correlation-row" data-testid={`corr-row-${corr.id}`}>
                      <div className="corr-pair-block">
                        <span className="corr-pair mono">
                          {corr.left_symbol} ⇄ {corr.right_symbol}
                        </span>
                        <span className="corr-tf mono">{corr.timeframe}</span>
                      </div>

                      <div className="corr-val-block">
                        <span className={`corr-r mono font-bold ${isNeg ? "negative" : "positive"}`}>
                          r = {r.toFixed(3)}
                        </span>
                        <span className="corr-unc mono">
                          {hasBounds
                            ? `CI: [${Number(unc.lower).toFixed(2)}, ${Number(unc.upper).toFixed(2)}]`
                            : "CI: [Uncertainty: Unavailable]"}
                        </span>
                      </div>

                      {/* BO-F-03: sample count, data-class, lineage, framing */}
                      <div className="intel-metric-footer mono">
                        <span>N = {corr.sample_count}</span>
                        <span data-testid={`corr-data-class-${corr.id}`}>
                          {dataClassOf(corr.notes)}
                        </span>
                        <span>hash {hashPrefix(corr.report_hash)}</span>
                      </div>
                      <div className="intel-framing-line" data-testid={`corr-framing-${corr.id}`}>
                        {RESEARCH_ONLY_FRAMING}
                      </div>
                      {/* BO-F-05.1/.2 — per-report lineage (read-only) */}
                      {renderLineage(corr)}
                    </div>
                  );
                })
              )}
            </div>
          </div>
        ) : activeTab === "REGIME" ? (
          /* Card 3: Market Regime Detection */
          <div className="intel-panel" data-testid="intel-regime-panel">
            <div className="intel-panel-header">
              <span className="panel-heading">Market Regime Classification</span>
              <span className="provenance-badge mono">HMM / Classifier</span>
            </div>

            {latestRegime ? (
              <div className="regime-content">
                <div className="regime-header-row">
                  <span className="regime-tag mono font-bold" data-testid="regime-label">
                    {latestRegime.regime_label.toUpperCase()}
                  </span>
                  <span className="regime-conf mono">
                    Confidence: {(latestRegime.confidence * 100).toFixed(1)}%
                    {latestRegime.uncertainty?.lower != null && latestRegime.uncertainty?.upper != null
                      ? ` [${(Number(latestRegime.uncertainty.lower) * 100).toFixed(1)}% – ${(Number(latestRegime.uncertainty.upper) * 100).toFixed(1)}%]`
                      : " [Uncertainty: Unavailable]"}
                  </span>
                </div>

                <div className="regime-meta-row mono">
                  <span>Symbol: {latestRegime.symbol}</span>
                  <span>Timeframe: {latestRegime.timeframe}</span>
                  <span>N = {latestRegime.sample_count}</span>
                </div>

                {/* BO-F-03: data-class + lineage + framing */}
                <div className="intel-metric-footer mono">
                  <span data-testid="regime-data-class">{dataClassOf(latestRegime.notes)}</span>
                  <span>hash {hashPrefix(latestRegime.report_hash)}</span>
                </div>
                <div className="intel-framing-line" data-testid="regime-framing">
                  {RESEARCH_ONLY_FRAMING}
                </div>
                {/* BO-F-05.1/.2 — per-report lineage (read-only) */}
                {renderLineage(latestRegime)}
              </div>
            ) : (
              <div className="intel-empty-note">
                <span>No active market regime report for this symbol.</span>
              </div>
            )}
          </div>
        ) : activeTab === "SCENARIO" ? (
          /* Card 4: Hypothetical Scenario (BO-F-03) */
          <div className="intel-panel" data-testid="intel-scenario-panel">
            <div className="intel-panel-header">
              <span className="panel-heading">Hypothetical Scenario</span>
              <span className="provenance-badge mono">HYPOTHETICAL · RESEARCH ONLY</span>
            </div>

            {latestScenario ? (
              <div className="scenario-content">
                <div className="scenario-header-row">
                  <span className="scenario-name mono font-bold" data-testid="scenario-name">
                    {latestScenario.scenario_name}
                  </span>
                  <span className="scenario-return mono" data-testid="scenario-return">
                    Hypothetical return: {(latestScenario.hypothetical_return * 100).toFixed(2)}%
                  </span>
                </div>
                <div className="scenario-meta-row mono">
                  <span>{latestScenario.symbol} {latestScenario.timeframe}</span>
                  <span>N = {latestScenario.sample_count}</span>
                  <span data-testid="scenario-assumptions">
                    assumptions: {JSON.stringify(latestScenario.assumptions)}
                  </span>
                </div>
                {latestScenario.limitations && latestScenario.limitations.length > 0 && (
                  <div className="scenario-limitations mono" data-testid="scenario-limitations">
                    limitations: {latestScenario.limitations.join("; ")}
                  </div>
                )}
                <div className="intel-metric-footer mono">
                  <span data-testid="scenario-data-class">{dataClassOf(latestScenario.notes)}</span>
                  <span>hash {hashPrefix(latestScenario.report_hash)}</span>
                </div>
                <div className="intel-framing-line" data-testid="scenario-framing">
                  {RESEARCH_ONLY_FRAMING}
                </div>
                {/* BO-F-05.1/.2 — per-report lineage (read-only) */}
                {renderLineage(latestScenario)}
              </div>
            ) : (
              <div className="intel-empty-note">
                <span>No scenario report generated yet.</span>
              </div>
            )}
          </div>
        ) : (
          /* Card 5: Portfolio-Risk (BO-F-03) */
          <div className="intel-panel" data-testid="intel-portfolio-risk-panel">
            <div className="intel-panel-header">
              <span className="panel-heading">Portfolio-Risk Research</span>
              <span className="provenance-badge mono">HYPOTHETICAL · RESEARCH ONLY</span>
            </div>

            {latestPortfolioRisk ? (
              <div className="portrisk-content">
                <div className="portrisk-metrics-grid">
                  <div className="intel-metric-box">
                    <span className="box-lbl">Max Drawdown</span>
                    <span className="box-val mono" data-testid="portrisk-drawdown">
                      {(latestPortfolioRisk.max_drawdown * 100).toFixed(2)}%
                    </span>
                  </div>
                  <div className="intel-metric-box">
                    <span className="box-lbl">Realized Volatility</span>
                    <span className="box-val mono" data-testid="portrisk-vol">
                      {(latestPortfolioRisk.realized_volatility * 100).toFixed(2)}%
                    </span>
                  </div>
                  <div className="intel-metric-box">
                    <span className="box-lbl">Stress Loss</span>
                    <span className="box-val mono" data-testid="portrisk-stress">
                      {(latestPortfolioRisk.stress_loss * 100).toFixed(2)}%
                    </span>
                  </div>
                </div>
                <div className="scenario-meta-row mono">
                  <span>{latestPortfolioRisk.symbol} {latestPortfolioRisk.timeframe}</span>
                  <span>N = {latestPortfolioRisk.sample_count}</span>
                </div>
                {latestPortfolioRisk.limitations && latestPortfolioRisk.limitations.length > 0 && (
                  <div className="scenario-limitations mono" data-testid="portrisk-limitations">
                    limitations: {latestPortfolioRisk.limitations.join("; ")}
                  </div>
                )}
                <div className="intel-metric-footer mono">
                  <span data-testid="portrisk-data-class">{dataClassOf(latestPortfolioRisk.notes)}</span>
                  <span>hash {hashPrefix(latestPortfolioRisk.report_hash)}</span>
                </div>
                <div className="intel-framing-line" data-testid="portrisk-framing">
                  {RESEARCH_ONLY_FRAMING}
                </div>
                {/* BO-F-05.1/.2 — per-report lineage (read-only) */}
                {renderLineage(latestPortfolioRisk)}
              </div>
            ) : (
              <div className="intel-empty-note">
                <span>No portfolio-risk report generated yet.</span>
              </div>
            )}
          </div>
        )}
      </div>

      {/* BO-F-03.3 — the governed generation surface (all five families) */}
      <IntelligenceGenerationPanel onGenerated={() => setRefreshTick((tick) => tick + 1)} />
    </div>
  );
}
