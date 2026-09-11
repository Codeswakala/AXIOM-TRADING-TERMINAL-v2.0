import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useTerminal } from "./TerminalContext";
import {
  fetchAdvisorySignals,
  fetchInstitutionalIntelligenceBundle,
  fetchSignalValidationReports,
  type AdvisorySignal,
  type InstitutionalIntelligenceBundle,
  type SignalValidationReport,
} from "../../api/client";
import { CalibratedConfidenceBadge } from "./StatisticalValueRenderer";
import { StructuralSignalStream } from "./StructuralSignalStream";
import {
  EMPTY_INTELLIGENCE,
  REPORT_GROUPS,
  reportSummary,
  reportTitle,
  SignalInvestigationFrame,
} from "./signals/SignalInvestigationRecords";
import "./TerminalMultiPane.css";

export interface TerminalSignalStreamProps {
  className?: string;
  onSignalSelect?: (signal: AdvisorySignal) => void;
}

/**
 * TerminalSignalStream
 *
 * Quantitative Advisory Signal Stream docked in the terminal right dock (P04 / CONV-P02).
 * Consumes GET /api/v1/signals/history and binds confidence to uncertainty intervals via
 * the single canonical CalibratedConfidenceBadge (B-CONV2-1).
 *
 * BO-F-02 (2026-08-21): the stream is now the TWO-FAMILY signal center per
 * CA-RECON-2 / §13 — Structural (deterministic, indicator-derived) and
 * Predictive (ML, gated). The families are visually separated by an explicit
 * family tab bar and family labels; they are never merged, and neither
 * fabricates entries (structural events come only from server-computed
 * indicator series; predictive entries only from persisted advisory signals).
 * The predictive track's deferral is stated honestly in its empty state.
 *
 * Adheres strictly to:
 * - B-CONV2-1: Exactly one shared statistical rendering code path
 * - B-CONV2-2: Rich signal detail drill-down (rationale, guardrails, lineage, explainability)
 * - B-P04-2: Zero client-side computation of statistics (ECE, Brier, Wilson intervals)
 * - B-P04-3: Advisory research notes only, never trade instructions (T-1)
 * - B-P04-4: Stale and expired signals explicitly tagged with absolute UTC time
 * - B-P04-5: Full model provenance and explainability feature attribution per signal
 * - T-4 / T-5: Zero external LLMs; assistant subordinate
 * - SAL-2 (Internal) presentation surface
 */
export function TerminalSignalStream({
  className = "",
  onSignalSelect,
}: TerminalSignalStreamProps) {
  const { selectedSymbol } = useTerminal();
  const [signals, setSignals] = useState<AdvisorySignal[]>([]);
  const [validationReports, setValidationReports] = useState<SignalValidationReport[]>([]);
  const [intelligence, setIntelligence] = useState<InstitutionalIntelligenceBundle | null>(null);
  const [stateFilter, setStateFilter] = useState<string>("ALL");
  const [expandedSignalId, setExpandedSignalId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [fetchError, setFetchError] = useState<string | null>(null);
  // BO-F-02.1: two-family framing — default is the predictive family (the
  // pre-F-02 behavior; existing surface pins expect its state filters).
  const [family, setFamily] = useState<"predictive" | "structural">("predictive");

  // Normalized active symbol key
  const symbolKey = useMemo(() => {
    return selectedSymbol.replace(/[^a-zA-Z0-9]/g, "").toUpperCase();
  }, [selectedSymbol]);

  // Load signals, validation reports, and the intelligence bundle (item 6:
  // linked intelligence reports — independent fetch, absence renders as
  // "No reports returned." never fabricated).
  useEffect(() => {
    let cancelled = false;
    async function loadData() {
      setIsLoading(true);
      setFetchError(null);
      try {
        const [sigData, valData, intelData] = await Promise.all([
          fetchAdvisorySignals({ symbol: symbolKey, limit: 30 }),
          fetchSignalValidationReports(20).catch(() => []),
          fetchInstitutionalIntelligenceBundle(5).catch(() => null),
        ]);
        if (!cancelled) {
          setSignals(sigData || []);
          setValidationReports(valData || []);
          setIntelligence(intelData);
        }
      } catch (err) {
        if (!cancelled) {
          setFetchError(err instanceof Error ? err.message : "Failed to load signals");
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }
    void loadData();
    return () => {
      cancelled = true;
    };
  }, [symbolKey]);

  // Filter signals by symbol and state
  const filteredSignals = useMemo(() => {
    return signals.filter((sig) => {
      const sigSym = sig.symbol.replace(/[^a-zA-Z0-9]/g, "").toUpperCase();
      const symbolMatch = sigSym.includes(symbolKey) || symbolKey.includes(sigSym) || symbolKey === "ALL";
      if (!symbolMatch) return false;

      if (stateFilter === "ALL") return true;
      return sig.signal_state.toUpperCase() === stateFilter;
    });
  }, [signals, symbolKey, stateFilter]);

  // Map validation reports by model artifact id
  const validationMap = useMemo(() => {
    const map = new Map<string, SignalValidationReport>();
    for (const val of validationReports) {
      if (val.id) {
        map.set(val.id, val);
      }
    }
    return map;
  }, [validationReports]);

  const toggleExpand = (sigId: string, sig: AdvisorySignal) => {
    setExpandedSignalId((prev) => (prev === sigId ? null : sigId));
    if (onSignalSelect) {
      onSignalSelect(sig);
    }
  };

  return (
    <div
      className={`terminal-signal-stream ${className}`}
      data-testid="terminal-signal-stream"
      role="region"
      aria-label="Quantitative Advisory Signal Stream"
    >
      {/* Stream Header */}
      <div className="stream-header">
        <div className="stream-title-row">
          <span className="stream-title">ADVISORY SIGNALS</span>
          <span
            className="signal-family-label mono"
            data-testid="predictive-family-label"
            data-family="predictive"
          >
            PREDICTIVE (ML)
          </span>
          <span className="stream-count-badge mono" data-testid="signal-count-badge">
            {filteredSignals.length} SIGNALS
          </span>
        </div>
        <div className="stream-disclaimer-chip">
          <span>RESEARCH-ONLY · NON-ACTUATING</span>
        </div>
      </div>

      {/* BO-F-02.1: two-family framing — explicit family separation (CA-RECON-2 §13) */}
      <div className="signal-family-tabs" role="tablist" aria-label="Signal Family">
        <button
          type="button"
          role="tab"
          aria-selected={family === "structural"}
          className={`signal-family-tab mono ${family === "structural" ? "active" : ""}`}
          onClick={() => setFamily("structural")}
          data-testid="signal-family-structural"
          data-family="structural"
        >
          STRUCTURAL
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={family === "predictive"}
          className={`signal-family-tab mono ${family === "predictive" ? "active" : ""}`}
          onClick={() => setFamily("predictive")}
          data-testid="signal-family-predictive"
          data-family="predictive"
        >
          PREDICTIVE (ML)
        </button>
      </div>

      {family === "structural" ? (
        <StructuralSignalStream />
      ) : (
      <>
      {/* State Filter Tabs */}
      <div className="stream-filter-bar" role="tablist" aria-label="Signal State Filter">
        {(["ALL", "EMITTED", "WITHHELD", "EXPIRED", "SUPERSEDED"] as const).map((st) => (
          <button
            key={st}
            type="button"
            role="tab"
            aria-selected={stateFilter === st}
            className={`stream-filter-btn mono ${stateFilter === st ? "active" : ""}`}
            onClick={() => setStateFilter(st)}
            data-testid={`signal-filter-${st.toLowerCase()}`}
          >
            {st}
          </button>
        ))}
      </div>

      {/* Signals List Container */}
      <div className="signals-cards-list" role="list" aria-label="Advisory Signal Cards">
        {isLoading ? (
          <div className="signal-empty-msg loading" data-testid="signal-loading-state">
            <span>Loading quantitative signal stream…</span>
          </div>
        ) : fetchError ? (
          <div className="signal-empty-msg error" data-testid="signal-error-state">
            <span>Signal stream unavailable: {fetchError}</span>
          </div>
        ) : filteredSignals.length === 0 ? (
          <div
            className="signal-empty-msg empty"
            data-testid="signal-empty-state"
            data-deferred="true"
          >
            <span data-testid="signal-deferred-empty-state">
              No predictive signals — the predictive track is deferred (no eligible
              model). Deterministic structural signals remain available in the
              Structural family.
            </span>
            <small>Filters active: {stateFilter}</small>
          </div>
        ) : (
          filteredSignals.map((sig) => {
            const isExpanded = expandedSignalId === sig.signal_id;
            // OBS-CONV2-3: Render signal_state VERBATIM. State display must never be derived
            // from freshness_status — a withheld signal whose TTL has lapsed must still
            // render as WITHHELD, with freshness carried separately by the freshness tag.
            const stateLower = sig.signal_state.toLowerCase();

            // Bind uncertainty interval from linked validation report (B-P04-1)
            const linkedVal = sig.calibration_report_id ? validationMap.get(sig.calibration_report_id) : null;
            const wilsonBounds = linkedVal?.uncertainty;

            // Direction formatting without imperative instruction (B-P04-3)
            const dir = sig.signal_direction.toUpperCase();
            const isLong = dir.includes("LONG") || dir.includes("BUY") || dir.includes("POSITIVE");
            const isShort = dir.includes("SHORT") || dir.includes("SELL") || dir.includes("NEGATIVE");
            const dirLabel = isLong ? "POSITIVE BIAS" : isShort ? "NEGATIVE BIAS" : "NEUTRAL BIAS";

            // UTC Time formatting (B-P04-4)
            const asOfDate = new Date(sig.as_of_time);
            const formattedUtc = asOfDate.toTimeString().slice(0, 8) + " UTC";

            return (
              <div
                key={sig.signal_id}
                role="listitem"
                className={`signal-card ${stateLower} ${isExpanded ? "expanded" : ""}`}
                onClick={() => toggleExpand(sig.signal_id, sig)}
                data-testid={`signal-card-${sig.signal_id}`}
              >
                {/* Card Header: Symbol, Timeframe, State, Direction */}
                <div className="signal-card-header">
                  <div className="signal-header-left">
                    <span className="signal-symbol-badge mono">{sig.symbol}</span>
                    <span className="signal-tf-badge mono">{sig.timeframe}</span>
                    <span
                      className={`signal-state-badge ${stateLower} mono`}
                      data-testid={`signal-state-${sig.signal_id}`}
                    >
                      {sig.signal_state.toUpperCase()}
                    </span>
                  </div>

                  <div className="signal-header-right">
                    <span
                      className={`signal-direction-badge ${isLong ? "positive" : isShort ? "negative" : "neutral"} mono`}
                      data-testid={`signal-direction-${sig.signal_id}`}
                    >
                      {dirLabel}
                    </span>
                  </div>
                </div>

                {/* Card Primary Metric: Single Canonical Calibrated Confidence Component (B-CONV2-1: isBracketed validated, renders [Uncertainty: Unavailable] on uncalibrated) */}
                <div className="signal-metric-row">
                  <span className="metric-label">Calibrated Confidence:</span>
                  <CalibratedConfidenceBadge
                    confidence={sig.calibrated_confidence}
                    uncertainty={wilsonBounds}
                    testId={`signal-confidence-${sig.signal_id}`}
                  />
                </div>

                {/* Freshness, Staleness & As-Of UTC Timestamp (B-P04-4) */}
                <div className="signal-meta-row">
                  <span className="signal-as-of mono" data-testid={`signal-asof-${sig.signal_id}`}>
                    As of: {formattedUtc}
                  </span>
                  <span className="signal-freshness-tag mono" data-testid={`signal-freshness-${sig.signal_id}`}>
                    {sig.freshness_status?.toUpperCase() ?? "CURRENT"}
                  </span>
                </div>

                {/* State Reason (Why Withheld / Expired) */}
                {sig.state_reason ? (
                  <div className="signal-reason-banner" data-testid={`signal-reason-${sig.signal_id}`}>
                    <span className="reason-lbl">State Rationale:</span> {sig.state_reason}
                  </div>
                ) : null}

                {/* Model Provenance Header (B-P04-5) */}
                <div className="signal-provenance-block" data-testid={`signal-provenance-${sig.signal_id}`}>
                  <div className="provenance-id-row mono">
                    <span>Model: {sig.model_artifact_id} v{sig.model_version}</span>
                    <span>Feat: {sig.feature_set_version}</span>
                  </div>
                  <div
                    className="provenance-hash mono"
                    title={`Full input hash: ${sig.inference_input_hash}`}
                    data-testid={`signal-hash-${sig.signal_id}`}
                  >
                    Hash: {sig.inference_input_hash ? sig.inference_input_hash.slice(0, 16) + "…" : "N/A"}
                  </div>
                </div>

                {/* Expanded Signal Detail Drill-Down (B-CONV2-2, extended UI-CONV-P03 item 6) */}
                {isExpanded ? (
                  <div
                    className="signal-expanded-body"
                    data-testid={`signal-expanded-${sig.signal_id}`}
                    aria-label="Signal investigation detail"
                  >
                    {/* Item 6 group 1: the re-homed investigation workspace frame */}
                    <SignalInvestigationFrame />

                    {/* Section 1: Verbatim Rationale */}
                    <div className="expanded-section" data-testid={`signal-detail-rationale-${sig.signal_id}`}>
                      <span className="expanded-heading">Research Rationale (Verbatim):</span>
                      <p className="verbatim-text">{sig.rationale || "No narrative rationale supplied."}</p>
                    </div>

                    {/* Section 2: Guardrails & State Verification */}
                    <div className="expanded-section" data-testid={`signal-detail-guardrails-${sig.signal_id}`}>
                      <span className="expanded-heading">Guardrails & State Criteria:</span>
                      <dl className="kv-grid mono">
                        <dt>Operating Domain:</dt>
                        <dd>{sig.operating_domain_status || "in_domain"}</dd>
                        <dt>Economic Verdict:</dt>
                        <dd>{sig.economic_verdict || "cost_favorable"}</dd>
                        <dt>Calibration Status:</dt>
                        <dd>{sig.calibration_status || "calibrated"}</dd>
                        <dt>Validity Window:</dt>
                        <dd>{sig.signal_validity_seconds ? `${sig.signal_validity_seconds}s` : "60s"} (TTL)</dd>
                        <dt>Expires At:</dt>
                        <dd>{sig.expires_at ? new Date(sig.expires_at).toTimeString().slice(0, 8) + " UTC" : "N/A"}</dd>
                        <dt>Eligibility Reasons:</dt>
                        <dd>{sig.eligibility_reasons.length ? sig.eligibility_reasons.join(", ") : "—"}</dd>
                      </dl>
                    </div>

                    {/* Section 3: Lineage & Model Identification */}
                    <div className="expanded-section" data-testid={`signal-detail-lineage-${sig.signal_id}`}>
                      <span className="expanded-heading">Model Lineage & Audit:</span>
                      <dl className="kv-grid mono">
                        <dt>Signal id:</dt>
                        <dd>{sig.signal_id}</dd>
                        <dt>Artifact ID:</dt>
                        <dd>{sig.model_artifact_id}</dd>
                        <dt>Model version:</dt>
                        <dd>{sig.model_version}</dd>
                        <dt>Experiment ID:</dt>
                        {/* BO-F-05 honesty: the pre-F-05 "exp-001" fallback was a
                            fabricated value; absence is stated, never invented. */}
                        <dd>{sig.experiment_id || "not recorded"}</dd>
                        <dt>Feature Set:</dt>
                        <dd>{sig.feature_set_version}</dd>
                        <dt>Input hash:</dt>
                        <dd>{sig.inference_input_hash || "not recorded"}</dd>
                        <dt>Statistical Report:</dt>
                        <dd data-testid={`signal-lineage-stat-${sig.signal_id}`}>
                          {sig.statistical_report_id || "not recorded"}
                        </dd>
                        <dt>Calibration Report:</dt>
                        <dd>{sig.calibration_report_id || "not recorded"}</dd>
                        <dt>Economic Report:</dt>
                        <dd data-testid={`signal-lineage-econ-${sig.signal_id}`}>
                          {sig.economic_report_id || "not recorded"}
                        </dd>
                        <dt>Generalization Report:</dt>
                        <dd data-testid={`signal-lineage-gen-${sig.signal_id}`}>
                          {sig.generalization_report_id || "not recorded"}
                        </dd>
                        <dt>Audit Correlation:</dt>
                        <dd data-testid={`signal-lineage-audit-${sig.signal_id}`}>
                          {sig.audit_correlation_id
                            ? sig.audit_correlation_id.slice(0, 16) + "…"
                            : "not recorded"}
                        </dd>
                      </dl>
                    </div>

                    {/* Section 4: Risk Notes */}
                    {sig.risk_notes ? (
                      <div className="expanded-section" data-testid={`signal-detail-risk-${sig.signal_id}`}>
                        <span className="expanded-heading">Risk Disclosures:</span>
                        <p className="verbatim-text risk">{sig.risk_notes}</p>
                      </div>
                    ) : null}

                    {/* Section 5: Explainability Feature Attribution */}
                    {sig.explainability_summary && Object.keys(sig.explainability_summary).length > 0 ? (
                      <div className="expanded-section" data-testid={`signal-detail-explainability-${sig.signal_id}`}>
                        <span className="expanded-heading">Explainability Feature Attribution:</span>
                        <div className="attribution-grid mono">
                          {Object.entries(sig.explainability_summary).map(([feat, score]) => (
                            <div key={feat} className="attribution-item">
                              <span className="feat-name">{feat}:</span>
                              <span className="feat-val">{typeof score === "number" ? score.toFixed(4) : String(score)}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : null}

                    {/* Item 6 group 8: Linked validation and report ids (M2: verbatim ?? "—") */}
                    <div className="expanded-section" data-testid={`signal-detail-report-ids-${sig.signal_id}`}>
                      <span className="expanded-heading">Linked validation and report ids:</span>
                      <div className="linked-report-id-grid mono">
                        <span>
                          Statistical: <code>{sig.statistical_report_id ?? "—"}</code>
                        </span>
                        <span>
                          Calibration: <code>{sig.calibration_report_id ?? "—"}</code>
                        </span>
                        <span>
                          Economic: <code>{sig.economic_report_id ?? "—"}</code>
                        </span>
                        <span>
                          Generalization: <code>{sig.generalization_report_id ?? "—"}</code>
                        </span>
                      </div>
                    </div>

                    {/* Item 6 group 9: Related evidence links (M5 / OBS-CONV3-10 —
                        in-app navigation to post-absorption destinations; no raw anchors) */}
                    <div
                      className="expanded-section"
                      aria-label="Related investigation evidence links"
                      data-testid={`signal-detail-evidence-links-${sig.signal_id}`}
                    >
                      <span className="expanded-heading">Related evidence links:</span>
                      <p className="muted">
                        Navigation only. Links open existing research workspaces that disclose stored
                        reports, signal context, and chart context without changing this investigation.
                      </p>
                      <div className="investigation-evidence-link-list">
                        <Link className="btn" to="/?dock=intelligence">
                          Open intelligence report viewer
                        </Link>
                        <Link className="btn" to="/?dock=signals">
                          Open advisory signal record
                        </Link>
                        <Link className="btn" to="/?view=chart">
                          Open chart context
                        </Link>
                      </div>
                    </div>

                    {/* Item 6 group 10: Linked intelligence reports (M2: "No reports returned.") */}
                    <div className="expanded-section" data-testid={`signal-detail-intelligence-${sig.signal_id}`}>
                      <span className="expanded-heading">Linked intelligence reports:</span>
                      <div className="investigation-report-grid">
                        {REPORT_GROUPS.map(([key, label]) => {
                          const group = (intelligence ?? EMPTY_INTELLIGENCE)[key];
                          return (
                            <div key={key} className="investigation-report-group">
                              <strong>{label}</strong>
                              {group.length === 0 ? (
                                <span className="muted">No reports returned.</span>
                              ) : null}
                              {group.slice(0, 2).map((report) => (
                                <article key={`${key}-${report.id}`} className="investigation-report-card">
                                  <span>{reportTitle(report)}</span>
                                  <small>{reportSummary(report)}</small>
                                </article>
                              ))}
                            </div>
                          );
                        })}
                      </div>
                    </div>

                    <div className="expanded-footer-disclaimer">
                      <span>Statistical model advisory note. Zero transaction execution affordance.</span>
                    </div>
                  </div>
                ) : null}
              </div>
            );
          })
        )}
      </div>
      </>
      )}
    </div>
  );
}
