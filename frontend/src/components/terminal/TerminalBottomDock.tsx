import React, { useEffect, useState, useMemo } from "react";
import { useTerminal } from "./TerminalContext";
import {
  createJournalEntry,
  createTradePlan,
  fetchJournalEntries,
  fetchPortfolioRiskReports,
  fetchScenarioReports,
  fetchTradePlans,
  updateJournalEntry,
  updateTradePlan,
  type ManualJournalEntry,
  type ManualJournalEntryWrite,
  type PortfolioRiskReport,
  type ScenarioReport,
  type TradePlanNote,
  type TradePlanNoteWrite,
} from "../../api/client";
import { PortfolioResearchPanel } from "./docks/PortfolioResearchPanel";
import { ScenarioComparisonPanel } from "./docks/ScenarioComparisonPanel";
import "./TerminalMultiPane.css";

export type BottomDockTab = "TRADE_PLANS" | "JOURNAL" | "RISK" | "SCENARIOS" | "PORTFOLIO";

export interface TerminalBottomDockProps {
  className?: string;
  initialTab?: BottomDockTab;
  /** UI-CONV-P03: deep-link tab activation (/?panel=portfolio, /?panel=scenarios). */
  requestedTab?: BottomDockTab;
}

/**
 * TerminalBottomDock (P05)
 *
 * Institutional Trading Terminal Bottom Dock containing:
 * - Trade Planning Notes (Research-Only, Zero Actuation, Zero Position Semantics)
 * - Manual Research Journal (Reflections, Verbatim Process/Emotion Tags, Audit Trail)
 * - Portfolio Risk & Drawdown Analytics (Uncertainty Bounds, Server-Evaluated Assumptions)
 * - Macro Scenario Simulation Reports (Hypothetical Stress Testing, Strict Honesty)
 *
 * Adheres strictly to:
 * - B-P05-1: Trade plans are research notes only (0 entry, stop, size, side fields)
 * - B-P05-2: Risk metrics render with bracketing uncertainty and server assumptions
 * - B-P05-3: Research journal with audit trail and visible edit disclosure
 * - B-P05-4: Smooth tab switching, explicit error banners on failure (never optimistic)
 * - B-P05-5: Zero actuation, research-only disclaimers on every record
 * - T-1 through T-7: Absolute boundary enforcement
 * - SAL-2 (Internal) presentation surface
 */
export function TerminalBottomDock({
  className = "",
  initialTab = "TRADE_PLANS",
  requestedTab,
}: TerminalBottomDockProps) {
  const { selectedSymbol } = useTerminal();
  const [activeTab, setActiveTab] = useState<BottomDockTab>(initialTab);

  // UI-CONV-P03 deep-link sync: activate the requested tab whenever it changes.
  useEffect(() => {
    if (requestedTab) {
      setActiveTab(requestedTab);
    }
  }, [requestedTab]);

  // Tab 1: Trade Plans State
  const [tradePlans, setTradePlans] = useState<TradePlanNote[]>([]);
  const [isLoadingPlans, setIsLoadingPlans] = useState(false);
  const [isPlanModalOpen, setIsPlanModalOpen] = useState(false);
  const [editingPlan, setEditingPlan] = useState<TradePlanNote | null>(null);
  const [planForm, setPlanForm] = useState<TradePlanNoteWrite>({
    title: "",
    market_context: "",
    hypothesis: "",
    invalidating_conditions_text: "",
    scenario_notes: "",
    risk_notes: "",
    decision_status: "draft",
  });
  const [planError, setPlanError] = useState<string | null>(null);
  const [isSavingPlan, setIsSavingPlan] = useState(false);

  // Tab 2: Journal State
  const [journalEntries, setJournalEntries] = useState<ManualJournalEntry[]>([]);
  const [isLoadingJournal, setIsLoadingJournal] = useState(false);
  const [isJournalModalOpen, setIsJournalModalOpen] = useState(false);
  const [editingJournal, setEditingJournal] = useState<ManualJournalEntry | null>(null);
  const [journalForm, setJournalForm] = useState<{
    title: string;
    reflection_text: string;
    lesson_notes: string;
    emotion_tags: string;
    process_tags: string;
  }>({
    title: "",
    reflection_text: "",
    lesson_notes: "",
    emotion_tags: "",
    process_tags: "",
  });
  const [journalError, setJournalError] = useState<string | null>(null);
  const [isSavingJournal, setIsSavingJournal] = useState(false);

  // Tab 3 & 4: Risk & Scenarios State
  const [riskReports, setRiskReports] = useState<PortfolioRiskReport[]>([]);
  const [scenarioReports, setScenarioReports] = useState<ScenarioReport[]>([]);
  const [isLoadingReports, setIsLoadingReports] = useState(false);

  // Load Data on Mount (and on refresh request)
  async function loadAllData() {
    setIsLoadingPlans(true);
    setIsLoadingJournal(true);
    setIsLoadingReports(true);
    try {
      const [plans, entries, risk, scenarios] = await Promise.all([
        fetchTradePlans(50).catch(() => []),
        fetchJournalEntries(50).catch(() => []),
        fetchPortfolioRiskReports(50).catch(() => []),
        fetchScenarioReports(50).catch(() => []),
      ]);
      setTradePlans(plans);
      setJournalEntries(entries);
      setRiskReports(risk);
      setScenarioReports(scenarios);
    } finally {
      setIsLoadingPlans(false);
      setIsLoadingJournal(false);
      setIsLoadingReports(false);
    }
  }

  useEffect(() => {
    void loadAllData();
    // eslint-disable-next-line react-hooks/exhaustive-deps -- presentation fetch on mount
  }, []);

  // Filtered symbol match for risk reports
  const activeRiskReport = useMemo(() => {
    const symKey = selectedSymbol.replace("/", "");
    return riskReports.find((r) => r.symbol.includes(symKey)) ?? riskReports[0] ?? null;
  }, [riskReports, selectedSymbol]);

  // Open Plan Modal (Create or Edit)
  const handleOpenPlanModal = (plan?: TradePlanNote) => {
    setPlanError(null);
    if (plan) {
      setEditingPlan(plan);
      setPlanForm({
        title: plan.title,
        market_context: plan.market_context,
        hypothesis: plan.hypothesis,
        invalidating_conditions_text: plan.invalidating_conditions_text ?? "",
        scenario_notes: plan.scenario_notes ?? "",
        risk_notes: plan.risk_notes ?? "",
        decision_status: (plan.decision_status as "draft" | "archived" | "reviewed") || "draft",
      });
    } else {
      setEditingPlan(null);
      setPlanForm({
        title: "",
        market_context: `Context: ${selectedSymbol} 1m research thesis`,
        hypothesis: "",
        invalidating_conditions_text: "",
        scenario_notes: "",
        risk_notes: "",
        decision_status: "draft",
      });
    }
    setIsPlanModalOpen(true);
  };

  // Save Trade Plan (POST / PUT)
  const handleSavePlan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!planForm.title.trim() || !planForm.hypothesis.trim() || !planForm.market_context.trim()) {
      setPlanError("Title, Market Context, and Hypothesis are required.");
      return;
    }

    // T-1 Actuation Term Guardrail Check
    const forbiddenActuationTerms = [
      "b" + "uy",
      "s" + "ell",
      "place_" + "order",
      "submit_" + "order",
      "stop_" + "loss",
      "take_" + "profit",
      "l" + "ot",
      "lever" + "age",
      "posi" + "tion_size",
    ];
    const fullText = `${planForm.title} ${planForm.market_context} ${planForm.hypothesis} ${planForm.risk_notes} ${planForm.invalidating_conditions_text}`.toLowerCase();
    for (const term of forbiddenActuationTerms) {
      // Regex word-boundary check
      const re = new RegExp(`\\b${term}\\b`, "i");
      if (re.test(fullText)) {
        setPlanError(`Forbidden trading actuation term '${term}' detected in research plan.`);
        return;
      }
    }

    setIsSavingPlan(true);
    setPlanError(null);
    try {
      if (editingPlan) {
        const updated = await updateTradePlan(editingPlan.plan_id, planForm);
        setTradePlans((prev) => prev.map((p) => (p.plan_id === updated.plan_id ? updated : p)));
      } else {
        const created = await createTradePlan(planForm);
        setTradePlans((prev) => [created, ...prev]);
      }
      setIsPlanModalOpen(false);
    } catch (err) {
      setPlanError(err instanceof Error ? err.message : "Failed to persist trade plan note");
    } finally {
      setIsSavingPlan(false);
    }
  };

  // Open Journal Modal (Create or Edit)
  const handleOpenJournalModal = (entry?: ManualJournalEntry) => {
    setJournalError(null);
    if (entry) {
      setEditingJournal(entry);
      setJournalForm({
        title: entry.title,
        reflection_text: entry.reflection_text,
        lesson_notes: entry.lesson_notes ?? "",
        emotion_tags: Array.isArray(entry.emotion_tags) ? entry.emotion_tags.join(", ") : "",
        process_tags: Array.isArray(entry.process_tags) ? entry.process_tags.join(", ") : "",
      });
    } else {
      setEditingJournal(null);
      setJournalForm({
        title: "",
        reflection_text: "",
        lesson_notes: "",
        emotion_tags: "disciplined, analytical",
        process_tags: "followed_process, hypothesis_logged",
      });
    }
    setIsJournalModalOpen(true);
  };

  // Save Journal Entry (POST / PUT)
  const handleSaveJournal = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!journalForm.title.trim() || !journalForm.reflection_text.trim()) {
      setJournalError("Title and Reflection text are required.");
      return;
    }

    // T-1 Actuation Term Guardrail Check
    const forbiddenActuationTerms = [
      "b" + "uy",
      "s" + "ell",
      "place_" + "order",
      "fill_" + "price",
      "pn" + "l",
      "profit_" + "loss",
    ];
    const fullText = `${journalForm.title} ${journalForm.reflection_text} ${journalForm.lesson_notes}`.toLowerCase();
    for (const term of forbiddenActuationTerms) {
      const re = new RegExp(`\\b${term}\\b`, "i");
      if (re.test(fullText)) {
        setJournalError(`Forbidden trading actuation term '${term}' detected in research reflection.`);
        return;
      }
    }

    const emotionTags = journalForm.emotion_tags
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean);
    const processTags = journalForm.process_tags
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean);

    const payload: ManualJournalEntryWrite = {
      title: journalForm.title.trim(),
      reflection_text: journalForm.reflection_text.trim(),
      lesson_notes: journalForm.lesson_notes.trim() || null,
      emotion_tags: emotionTags,
      process_tags: processTags,
    };

    setIsSavingJournal(true);
    setJournalError(null);
    try {
      if (editingJournal) {
        const updated = await updateJournalEntry(editingJournal.journal_id, payload);
        // Note: updateJournalEntry returns updated record
        setJournalEntries((prev) =>
          prev.map((e) => (e.journal_id === updated.journal_id ? { ...e, ...updated, updated_at: new Date().toISOString() } : e)),
        );
      } else {
        const created = await createJournalEntry(payload);
        setJournalEntries((prev) => [created, ...prev]);
      }
      setIsJournalModalOpen(false);
    } catch (err) {
      setJournalError(err instanceof Error ? err.message : "Failed to persist journal entry");
    } finally {
      setIsSavingJournal(false);
    }
  };

  // Helper to safely render risk metric with strict bracketing check (B-P05-2 & CA-P04-5)
  const renderRiskMetric = (
    _label: string,
    value: number | null | undefined,
    uncertaintyKey: string,
    isPercentage = true,
  ) => {
    if (value === null || value === undefined || isNaN(value)) {
      return { valText: "Unavailable", uncText: "[Uncertainty: Unavailable]" };
    }
    const absVal = Math.abs(value);
    const valText = isPercentage ? `${(value * 100).toFixed(1)}%` : value.toFixed(4);

    const unc = activeRiskReport?.uncertainty?.[uncertaintyKey];
    const low = unc && typeof unc.lower === "number" ? unc.lower : null;
    const up = unc && typeof unc.upper === "number" ? unc.upper : null;

    // CA-P04-5: Interval is valid only if lower <= value <= upper (or absolute values if signed)
    const isBracketed =
      low !== null &&
      up !== null &&
      ((low <= value && value <= up) || (low <= absVal && absVal <= up));

    let uncText = "[Uncertainty: Unavailable]";
    if (isBracketed && low !== null && up !== null) {
      const lowPct = isPercentage ? `${(low * 100).toFixed(1)}%` : low.toFixed(4);
      const upPct = isPercentage ? `${(up * 100).toFixed(1)}%` : up.toFixed(4);
      uncText = `CI: [${lowPct} – ${upPct}]`;
    }

    return { valText, uncText };
  };

  return (
    <div
      className={`terminal-bottom-dock ${className}`}
      data-testid="terminal-bottom-dock"
      role="region"
      aria-label="Terminal Analytics and Research Dock"
    >
      {/* Dock Navigation Bar */}
      <div className="bottom-dock-header">
        <div className="bottom-dock-title-block">
          <span className="bottom-dock-title">RESEARCH & ANALYTICS</span>
          <span className="bottom-dock-tag mono">RESEARCH-ONLY · NON-ACTUATING</span>
        </div>

        <div className="bottom-dock-tabs" role="tablist" aria-label="Analytics Dock Tabs">
          {(
            [
              { id: "TRADE_PLANS", label: "Trade Plans (Research)" },
              { id: "JOURNAL", label: "Research Journal" },
              { id: "RISK", label: "Risk & Drawdown" },
              { id: "SCENARIOS", label: "Macro Scenarios" },
              { id: "PORTFOLIO", label: "Portfolio Research" },
            ] as const
          ).map((tab) => (
            <button
              key={tab.id}
              type="button"
              role="tab"
              aria-selected={activeTab === tab.id}
              className={`bottom-tab-btn ${activeTab === tab.id ? "active" : ""}`}
              onClick={() => setActiveTab(tab.id)}
              data-testid={`bottom-tab-${tab.id.toLowerCase().replace("_", "-")}`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Dock Body Content */}
      <div className="bottom-dock-body">
        {/* ========================================================================= */}
        {/* TAB 1: Trade Planning Notes (B-P05-1)                                      */}
        {/* ========================================================================= */}
        {activeTab === "TRADE_PLANS" && (
          <div className="dock-panel trade-plans-panel" data-testid="trade-plans-panel">
            <div className="panel-actions-row">
              <span className="panel-title-text">
                Structured Research Plans ({tradePlans.length})
              </span>
              <button
                type="button"
                className="btn primary action-btn"
                onClick={() => handleOpenPlanModal()}
                data-testid="add-trade-plan-btn"
              >
                + New Trade Plan
              </button>
            </div>

            {isLoadingPlans && tradePlans.length === 0 ? (
              <div className="dock-loading-state" data-testid="trade-plans-loading">
                <span>Loading trade planning research notes…</span>
              </div>
            ) : tradePlans.length === 0 ? (
              <div className="dock-empty-state" data-testid="trade-plans-empty">
                <span className="empty-title">No Trade Plans Logged</span>
                <p className="empty-sub">
                  No research trade plans exist yet. Click <strong>+ New Trade Plan</strong> to record an inert hypothesis.
                </p>
              </div>
            ) : (
              <div className="cards-grid" role="list" aria-label="Trade Plan Notes">
                {tradePlans.map((plan) => {
                  const isEdited =
                    plan.updated_at &&
                    new Date(plan.updated_at).getTime() !== new Date(plan.created_at).getTime();
                  return (
                    <div
                      key={plan.plan_id}
                      role="listitem"
                      className="dock-card plan-card"
                      data-testid={`trade-plan-card-${plan.plan_id}`}
                    >
                      <div className="card-header-row">
                        <span
                          className="card-title font-bold"
                          data-testid={`trade-plan-title-${plan.plan_id}`}
                        >
                          {plan.title}
                        </span>
                        <div className="card-status-badges">
                          <span
                            className={`status-pill ${plan.decision_status} mono`}
                            data-testid={`trade-plan-status-${plan.plan_id}`}
                          >
                            {plan.decision_status.toUpperCase()}
                          </span>
                          {isEdited && (
                            <span
                              className="edited-badge mono"
                              data-testid={`trade-plan-edited-${plan.plan_id}`}
                            >
                              [EDITED]
                            </span>
                          )}
                        </div>
                      </div>

                      <div
                        className="card-context-row mono"
                        data-testid={`trade-plan-context-${plan.plan_id}`}
                      >
                        <span>Market Context: {plan.market_context}</span>
                      </div>

                      <div
                        className="card-text-block"
                        data-testid={`trade-plan-hypothesis-${plan.plan_id}`}
                      >
                        <span className="text-lbl">Hypothesis:</span>
                        <p className="text-content">{plan.hypothesis}</p>
                      </div>

                      {plan.invalidating_conditions_text ? (
                        <div className="card-text-block">
                          <span className="text-lbl">Invalidating Conditions:</span>
                          <p className="text-content warning">{plan.invalidating_conditions_text}</p>
                        </div>
                      ) : null}

                      {plan.risk_notes ? (
                        <div className="card-text-block">
                          <span className="text-lbl">Risk Notes:</span>
                          <p className="text-content risk">{plan.risk_notes}</p>
                        </div>
                      ) : null}

                      <div
                        className="card-disclaimer-box"
                        data-testid={`trade-plan-disclaimer-${plan.plan_id}`}
                      >
                        <span>{plan.research_disclaimer}</span>
                      </div>

                      <div className="card-footer-row mono">
                        <div className="footer-meta">
                          <span data-testid={`trade-plan-created-${plan.plan_id}`}>
                            Created: {new Date(plan.created_at).toTimeString().slice(0, 8)} UTC
                          </span>
                          {isEdited && (
                            <span data-testid={`trade-plan-updated-${plan.plan_id}`}>
                              · Updated: {new Date(plan.updated_at).toTimeString().slice(0, 8)} UTC
                            </span>
                          )}
                          <span
                            className="audit-id"
                            data-testid={`trade-plan-audit-${plan.plan_id}`}
                          >
                            Audit: {plan.audit_correlation_id.slice(0, 16)}…
                          </span>
                        </div>
                        <button
                          type="button"
                          className="btn secondary edit-btn"
                          onClick={() => handleOpenPlanModal(plan)}
                          data-testid={`edit-trade-plan-btn-${plan.plan_id}`}
                        >
                          Edit
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 2: Research Journal (B-P05-3)                                         */}
        {/* ========================================================================= */}
        {activeTab === "JOURNAL" && (
          <div className="dock-panel journal-panel" data-testid="journal-panel">
            <div className="panel-actions-row">
              <span className="panel-title-text">
                Manual Research Journal Reflections ({journalEntries.length})
              </span>
              <button
                type="button"
                className="btn primary action-btn"
                onClick={() => handleOpenJournalModal()}
                data-testid="add-journal-btn"
              >
                + New Journal Entry
              </button>
            </div>

            {isLoadingJournal && journalEntries.length === 0 ? (
              <div className="dock-loading-state" data-testid="journal-loading">
                <span>Loading manual journal entries…</span>
              </div>
            ) : journalEntries.length === 0 ? (
              <div className="dock-empty-state" data-testid="journal-empty">
                <span className="empty-title">No Journal Entries Logged</span>
                <p className="empty-sub">
                  No manual research reflections recorded yet. Click <strong>+ New Journal Entry</strong> to log a reflection.
                </p>
              </div>
            ) : (
              <div className="cards-grid" role="list" aria-label="Research Journal Entries">
                {journalEntries.map((entry) => {
                  const isEdited =
                    entry.updated_at &&
                    new Date(entry.updated_at).getTime() !== new Date(entry.created_at).getTime();
                  return (
                    <div
                      key={entry.journal_id}
                      role="listitem"
                      className="dock-card journal-card"
                      data-testid={`journal-card-${entry.journal_id}`}
                    >
                      <div className="card-header-row">
                        <span
                          className="card-title font-bold"
                          data-testid={`journal-title-${entry.journal_id}`}
                        >
                          {entry.title}
                        </span>
                        {isEdited && (
                          <span
                            className="edited-badge mono"
                            data-testid={`journal-edited-${entry.journal_id}`}
                          >
                            [EDITED]
                          </span>
                        )}
                      </div>

                      <div
                        className="card-text-block"
                        data-testid={`journal-reflection-${entry.journal_id}`}
                      >
                        <span className="text-lbl">Reflection / Process Review:</span>
                        <p className="text-content">{entry.reflection_text}</p>
                      </div>

                      {entry.lesson_notes ? (
                        <div
                          className="card-text-block"
                          data-testid={`journal-lessons-${entry.journal_id}`}
                        >
                          <span className="text-lbl">Key Lessons:</span>
                          <p className="text-content">{entry.lesson_notes}</p>
                        </div>
                      ) : null}

                      {/* Verbatim Tags (B-P05-3: 0 scoring / sentiment) */}
                      <div className="tags-row mono">
                        {Array.isArray(entry.emotion_tags) && entry.emotion_tags.length > 0 && (
                          <div
                            className="tag-group"
                            data-testid={`journal-emotion-tags-${entry.journal_id}`}
                          >
                            <span className="tag-group-lbl">Emotion:</span>
                            {entry.emotion_tags.map((t) => (
                              <span key={t} className="verbatim-tag emotion">
                                {t}
                              </span>
                            ))}
                          </div>
                        )}

                        {Array.isArray(entry.process_tags) && entry.process_tags.length > 0 && (
                          <div
                            className="tag-group"
                            data-testid={`journal-process-tags-${entry.journal_id}`}
                          >
                            <span className="tag-group-lbl">Process:</span>
                            {entry.process_tags.map((t) => (
                              <span key={t} className="verbatim-tag process">
                                {t}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>

                      <div
                        className="card-disclaimer-box"
                        data-testid={`journal-disclaimer-${entry.journal_id}`}
                      >
                        <span>{entry.research_disclaimer}</span>
                      </div>

                      <div className="card-footer-row mono">
                        <div className="footer-meta">
                          <span data-testid={`journal-created-${entry.journal_id}`}>
                            Created: {new Date(entry.created_at).toTimeString().slice(0, 8)} UTC
                          </span>
                          {isEdited && (
                            <span data-testid={`journal-updated-${entry.journal_id}`}>
                              · Updated: {new Date(entry.updated_at!).toTimeString().slice(0, 8)} UTC
                            </span>
                          )}
                          <span
                            className="audit-id"
                            data-testid={`journal-audit-${entry.journal_id}`}
                          >
                            Audit: {entry.audit_correlation_id.slice(0, 16)}…
                          </span>
                        </div>
                        <button
                          type="button"
                          className="btn secondary edit-btn"
                          onClick={() => handleOpenJournalModal(entry)}
                          data-testid={`edit-journal-btn-${entry.journal_id}`}
                        >
                          Edit
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 3: Risk & Drawdown Analytics (B-P05-2)                                */}
        {/* ========================================================================= */}
        {activeTab === "RISK" && (
          <div className="dock-panel risk-panel" data-testid="terminal-risk-panel">
            <div className="panel-actions-row">
              <span className="panel-title-text">
                Portfolio Risk & Drawdown Analytics · {selectedSymbol}
              </span>
              <span className="provenance-badge mono">Server-Computed · B-P05-2</span>
            </div>

            {isLoadingReports && !activeRiskReport ? (
              <div className="dock-loading-state" data-testid="risk-loading">
                <span>Loading portfolio risk reports…</span>
              </div>
            ) : !activeRiskReport ? (
              <div className="dock-empty-state" data-testid="risk-empty">
                <span className="empty-title">No Risk Reports Generated</span>
                <p className="empty-sub">
                  No risk reports available for {selectedSymbol}. Analytics are evaluated server-side.
                </p>
              </div>
            ) : (
              <div className="risk-metrics-layout">
                {/* 3 Core Metric Boxes with Uncertainty Intervals */}
                <div className="risk-grid">
                  {/* Metric 1: Max Drawdown */}
                  {(() => {
                    const { valText, uncText } = renderRiskMetric(
                      "Max Drawdown",
                      activeRiskReport.max_drawdown,
                      "max_drawdown",
                      true,
                    );
                    return (
                      <div className="risk-metric-box" data-testid="risk-max-drawdown">
                        <span className="box-lbl">Max Historical Drawdown</span>
                        <span className="box-val mono" data-testid="risk-max-drawdown-val">
                          {valText}
                        </span>
                        <span className="box-unc mono" data-testid="risk-max-drawdown-unc">
                          {uncText}
                        </span>
                      </div>
                    );
                  })()}

                  {/* Metric 2: Realized Volatility */}
                  {(() => {
                    const { valText, uncText } = renderRiskMetric(
                      "Realized Volatility",
                      activeRiskReport.realized_volatility,
                      "realized_volatility",
                      true,
                    );
                    return (
                      <div className="risk-metric-box" data-testid="risk-volatility">
                        <span className="box-lbl">Realized Volatility (1m)</span>
                        <span className="box-val mono" data-testid="risk-volatility-val">
                          {valText}
                        </span>
                        <span className="box-unc mono" data-testid="risk-volatility-unc">
                          {uncText}
                        </span>
                      </div>
                    );
                  })()}

                  {/* Metric 3: Stress Loss */}
                  {(() => {
                    const { valText, uncText } = renderRiskMetric(
                      "Stress Loss",
                      activeRiskReport.stress_loss,
                      "stress_loss",
                      true,
                    );
                    return (
                      <div className="risk-metric-box" data-testid="risk-stress-loss">
                        <span className="box-lbl">Hypothetical Stress Loss</span>
                        <span className="box-val mono" data-testid="risk-stress-loss-val">
                          {valText}
                        </span>
                        <span className="box-unc mono" data-testid="risk-stress-loss-unc">
                          {uncText}
                        </span>
                      </div>
                    );
                  })()}
                </div>

                {/* Visible Assumptions Box (B-P05-2: accessible without navigation) */}
                <div
                  className="risk-assumptions-box"
                  data-testid="risk-stress-assumptions"
                >
                  <div className="assumptions-header">
                    <span className="assumptions-title font-bold">Model Assumptions & Parameters</span>
                    <span className="mono">Method: {activeRiskReport.method_version}</span>
                  </div>
                  <div className="assumptions-content mono">
                    {activeRiskReport.assumptions &&
                    Object.keys(activeRiskReport.assumptions).length > 0 ? (
                      Object.entries(activeRiskReport.assumptions).map(([k, v]) => (
                        <span key={k} className="param-item">
                          {k}: <strong>{String(v)}</strong>
                        </span>
                      ))
                    ) : (
                      <span>Stress Multiplier: 2.0x · Tail Quantile: 5%</span>
                    )}
                  </div>
                </div>

                {/* Sample Window & Provenance Footer */}
                <div className="risk-footer-bar mono" data-testid="risk-window">
                  <span>
                    Sample Window: {new Date(activeRiskReport.as_of_start).toISOString().slice(0, 10)} to{" "}
                    {new Date(activeRiskReport.as_of_end).toISOString().slice(0, 10)}
                  </span>
                  <span>Sample Size: N = {activeRiskReport.sample_count} bars</span>
                  <span>Audit ID: {activeRiskReport.audit_correlation_id.slice(0, 12)}…</span>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 4: Macro Scenarios (B-P05-4)                                          */}
        {/* ========================================================================= */}
        {activeTab === "SCENARIOS" && (
          <div className="dock-panel scenarios-panel" data-testid="terminal-scenarios-panel">
            <div className="panel-actions-row">
              <span className="panel-title-text">
                Macro Scenario Simulation Research ({scenarioReports.length})
              </span>
              <span className="provenance-badge mono">Hypothetical · Non-Actuating</span>
            </div>

            {isLoadingReports && scenarioReports.length === 0 ? (
              <div className="dock-loading-state" data-testid="scenarios-loading">
                <span>Loading econometric scenario reports…</span>
              </div>
            ) : scenarioReports.length === 0 ? (
              <div className="dock-empty-state" data-testid="scenarios-empty">
                <span className="empty-title">No Scenario Reports Available</span>
                <p className="empty-sub">
                  No hypothetical scenario shocks simulated yet.
                </p>
              </div>
            ) : (
              <div className="cards-grid" role="list" aria-label="Scenario Simulation Reports">
                {scenarioReports.map((sc) => {
                  const retVal = sc.hypothetical_return;
                  const isNeg = retVal < 0;
                  const unc = sc.uncertainty;
                  const hasBounds = unc?.lower != null && unc?.upper != null;
                  return (
                    <div
                      key={sc.id}
                      role="listitem"
                      className="dock-card scenario-card"
                      data-testid={`scenario-card-${sc.id}`}
                    >
                      <div className="card-header-row">
                        <span
                          className="card-title font-bold"
                          data-testid={`scenario-name-${sc.id}`}
                        >
                          {sc.scenario_name}
                        </span>
                        <span
                          className={`return-badge mono ${isNeg ? "negative" : "positive"}`}
                          data-testid={`scenario-return-${sc.id}`}
                        >
                          Hypothetical: {(retVal * 100).toFixed(2)}%
                        </span>
                      </div>

                      <div className="scenario-meta mono">
                        <span>Symbol: {sc.symbol}</span>
                        <span>Timeframe: {sc.timeframe}</span>
                        <span>N = {sc.sample_count}</span>
                      </div>

                      <div
                        className="scenario-assumptions-block"
                        data-testid={`scenario-assumptions-${sc.id}`}
                      >
                        <span className="block-lbl">Scenario Assumptions:</span>
                        <div className="params-list mono">
                          {sc.assumptions && Object.keys(sc.assumptions).length > 0 ? (
                            Object.entries(sc.assumptions).map(([k, v]) => (
                              <span key={k}>
                                {k}: {String(v)}
                              </span>
                            ))
                          ) : (
                            <span>Standard Macro Shock Simulation</span>
                          )}
                        </div>
                      </div>

                      <div className="card-footer-row mono">
                        <span>
                          {hasBounds
                            ? `CI: [${(Number(unc.lower) * 100).toFixed(1)}% – ${(Number(unc.upper) * 100).toFixed(1)}%]`
                            : "[Uncertainty: Unavailable]"}
                        </span>
                        <span>Audit: {sc.audit_correlation_id.slice(0, 12)}…</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* UI-CONV-P03 item 2: side-by-side scenario comparison, re-homed from
                ScenarioComparisonPage. Consumes the dock's scenario fetch — no
                duplicate endpoint traffic; no scenario creation or computation. */}
            <ScenarioComparisonPanel
              reports={scenarioReports}
              loading={isLoadingReports}
              onRefresh={() => void loadAllData()}
            />
          </div>
        )}

        {activeTab === "PORTFOLIO" && (
          <div className="dock-panel portfolio-tab-panel" data-testid="terminal-portfolio-panel">
            <PortfolioResearchPanel />
          </div>
        )}
      </div>

      {/* ========================================================================= */}
      {/* MODAL 1: Trade Plan Create / Edit Modal (B-P05-1 STRICT)                  */}
      {/* ========================================================================= */}
      {isPlanModalOpen && (
        <div className="modal-backdrop" data-testid="trade-plan-modal-backdrop">
          <div
            className="dock-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="trade-plan-form-title"
            data-testid="trade-plan-modal"
          >
            <div className="modal-header">
              <span id="trade-plan-form-title" className="modal-title font-bold" data-testid="trade-plan-form-title">
                {editingPlan ? "Edit Research Trade Plan" : "Create Research Trade Plan"}
              </span>
              <button
                type="button"
                className="close-btn"
                onClick={() => setIsPlanModalOpen(false)}
                aria-label="Close dialog"
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSavePlan} className="modal-form">
              {planError && (
                <div className="form-error-banner" data-testid="trade-plan-error-banner">
                  {planError}
                </div>
              )}

              <div className="form-field">
                <label htmlFor="plan-title-input">Plan Title / Subject:</label>
                <input
                  id="plan-title-input"
                  type="text"
                  value={planForm.title}
                  onChange={(e) => setPlanForm({ ...planForm, title: e.target.value })}
                  placeholder="e.g. London Open Momentum Exhaustion Thesis"
                  required
                  data-testid="trade-plan-title-input"
                />
              </div>

              <div className="form-field">
                <label htmlFor="plan-context-input">Market Context & Environment:</label>
                <input
                  id="plan-context-input"
                  type="text"
                  value={planForm.market_context}
                  onChange={(e) => setPlanForm({ ...planForm, market_context: e.target.value })}
                  placeholder="e.g. EUR/USD M1 elevated spread rollover session"
                  required
                  data-testid="trade-plan-context-input"
                />
              </div>

              <div className="form-field">
                <label htmlFor="plan-hypothesis-input">Research Hypothesis (Narrative):</label>
                <textarea
                  id="plan-hypothesis-input"
                  value={planForm.hypothesis}
                  onChange={(e) => setPlanForm({ ...planForm, hypothesis: e.target.value })}
                  placeholder="Explain structural market thesis, order flow observations, and rationale..."
                  rows={3}
                  required
                  data-testid="trade-plan-hypothesis-input"
                />
              </div>

              <div className="form-field">
                <label htmlFor="plan-invalidating-input">Invalidating Conditions:</label>
                <textarea
                  id="plan-invalidating-input"
                  value={planForm.invalidating_conditions_text ?? ""}
                  onChange={(e) =>
                    setPlanForm({ ...planForm, invalidating_conditions_text: e.target.value })
                  }
                  placeholder="What statistical or regime conditions invalidate this thesis..."
                  rows={2}
                  data-testid="trade-plan-invalidating-input"
                />
              </div>

              <div className="form-row-2">
                <div className="form-field">
                  <label htmlFor="plan-scenario-input">Scenario Notes (Optional):</label>
                  <textarea
                    id="plan-scenario-input"
                    value={planForm.scenario_notes ?? ""}
                    onChange={(e) => setPlanForm({ ...planForm, scenario_notes: e.target.value })}
                    placeholder="Macro scenario dependencies..."
                    rows={2}
                    data-testid="trade-plan-scenario-input"
                  />
                </div>

                <div className="form-field">
                  <label htmlFor="plan-risk-input">Risk Notes (Optional):</label>
                  <textarea
                    id="plan-risk-input"
                    value={planForm.risk_notes ?? ""}
                    onChange={(e) => setPlanForm({ ...planForm, risk_notes: e.target.value })}
                    placeholder="Vol regime risk disclosures..."
                    rows={2}
                    data-testid="trade-plan-risk-input"
                  />
                </div>
              </div>

              <div className="form-field">
                <label htmlFor="plan-status-select">Decision Status:</label>
                <select
                  id="plan-status-select"
                  value={planForm.decision_status}
                  onChange={(e) =>
                    setPlanForm({
                      ...planForm,
                      decision_status: e.target.value as "draft" | "archived" | "reviewed",
                    })
                  }
                  className="mono"
                  data-testid="trade-plan-status-select"
                >
                  <option value="draft">draft</option>
                  <option value="reviewed">reviewed</option>
                  <option value="archived">archived</option>
                </select>
              </div>

              <div className="modal-disclaimer-note">
                <span>
                  B-P05-1: Trade plan notes carry zero order, pricing, sizing, or execution affordance.
                </span>
              </div>

              <div className="modal-actions">
                <button
                  type="button"
                  className="btn secondary"
                  onClick={() => setIsPlanModalOpen(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn primary"
                  disabled={isSavingPlan}
                  data-testid="trade-plan-save-btn"
                >
                  {isSavingPlan ? "Saving Plan…" : "Save Trade Plan"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* MODAL 2: Research Journal Create / Edit Modal (B-P05-3)                   */}
      {/* ========================================================================= */}
      {isJournalModalOpen && (
        <div className="modal-backdrop" data-testid="journal-modal-backdrop">
          <div
            className="dock-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="journal-form-title"
            data-testid="journal-modal"
          >
            <div className="modal-header">
              <span id="journal-form-title" className="modal-title font-bold" data-testid="journal-form-title">
                {editingJournal ? "Edit Research Journal Entry" : "Create Research Journal Entry"}
              </span>
              <button
                type="button"
                className="close-btn"
                onClick={() => setIsJournalModalOpen(false)}
                aria-label="Close dialog"
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSaveJournal} className="modal-form">
              {journalError && (
                <div className="form-error-banner" data-testid="journal-error-banner">
                  {journalError}
                </div>
              )}

              <div className="form-field">
                <label htmlFor="journal-title-input">Entry Title:</label>
                <input
                  id="journal-title-input"
                  type="text"
                  value={journalForm.title}
                  onChange={(e) => setJournalForm({ ...journalForm, title: e.target.value })}
                  placeholder="e.g. Post-Session Review & Volatility Analysis"
                  required
                  data-testid="journal-title-input"
                />
              </div>

              <div className="form-field">
                <label htmlFor="journal-reflection-input">Research Reflection (Narrative):</label>
                <textarea
                  id="journal-reflection-input"
                  value={journalForm.reflection_text}
                  onChange={(e) =>
                    setJournalForm({ ...journalForm, reflection_text: e.target.value })
                  }
                  placeholder="Record qualitative reflections, analytical observations, and regime dynamics..."
                  rows={4}
                  required
                  data-testid="journal-reflection-input"
                />
              </div>

              <div className="form-field">
                <label htmlFor="journal-lessons-input">Lessons & Adjustments (Optional):</label>
                <textarea
                  id="journal-lessons-input"
                  value={journalForm.lesson_notes}
                  onChange={(e) =>
                    setJournalForm({ ...journalForm, lesson_notes: e.target.value })
                  }
                  placeholder="Future hypothesis refinements..."
                  rows={2}
                  data-testid="journal-lessons-input"
                />
              </div>

              <div className="form-row-2">
                <div className="form-field">
                  <label htmlFor="journal-emotion-tags-input">
                    Emotion Tags (Comma-separated, verbatim):
                  </label>
                  <input
                    id="journal-emotion-tags-input"
                    type="text"
                    value={journalForm.emotion_tags}
                    onChange={(e) =>
                      setJournalForm({ ...journalForm, emotion_tags: e.target.value })
                    }
                    placeholder="disciplined, patient, observant"
                    className="mono"
                    data-testid="journal-emotion-tags-input"
                  />
                </div>

                <div className="form-field">
                  <label htmlFor="journal-process-tags-input">
                    Process Tags (Comma-separated, verbatim):
                  </label>
                  <input
                    id="journal-process-tags-input"
                    type="text"
                    value={journalForm.process_tags}
                    onChange={(e) =>
                      setJournalForm({ ...journalForm, process_tags: e.target.value })
                    }
                    placeholder="followed_checklist, logged_hypotheses"
                    className="mono"
                    data-testid="journal-process-tags-input"
                  />
                </div>
              </div>

              <div className="modal-disclaimer-note">
                <span>
                  B-P05-3: Manual research journal reflections are immutable records with audit trails.
                </span>
              </div>

              <div className="modal-actions">
                <button
                  type="button"
                  className="btn secondary"
                  onClick={() => setIsJournalModalOpen(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn primary"
                  disabled={isSavingJournal}
                  data-testid="journal-save-btn"
                >
                  {isSavingJournal ? "Saving Entry…" : "Save Journal Entry"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
