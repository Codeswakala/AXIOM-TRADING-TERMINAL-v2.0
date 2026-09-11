/**
 * ChartWorkspaceSurface
 *
 * OBS-CONV2-4 full discharge (UI-CONV-P02 R1 transport package): relocated from
 * pages/ChartWorkspacePage.tsx into components/chart/ so that no orphaned,
 * unrouted PAGE file remains in the tree. The legacy `ChartWorkspacePage`
 * composition is retained as a REFERENCED legacy presentation surface used
 * solely by the historical UI-003-P05 completion checkpoint tests; it is not
 * routed by the workspace registry (post-absorption routing uses
 * ChartWorkspaceRedirect -> /?view=chart per B-CONV2-2).
 *
 * All shared exports keep their original names and contracts:
 *   CHART_ANNOTATION_UI_DISCLAIMER, ProfessionalMarketOverview,
 *   MarketStatusCards, MarketWorkspaceStateNotice, ChartAccessibleSummary,
 *   ChartOverlayControls, ChartResearchMarkerLayer, ChartResearchMarkerList,
 *   ChartResearchAnnotationLayer, ChartWorkspacePage (legacy composition).
 *
 * Research-only presentation surface: no actuation, no client-side inference,
 * no external feed authority (T-1 / T-6 / C-1).
 */

import { useEffect, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { useChartState } from "../../chart/useChartState";
import { useChartData } from "../../hooks/useChartData";
import { PriceChart } from "./PriceChart";
import type { ChartTimeframe, ChartType } from "../../chart/types";
import { StatusPill } from "../StatusPill";
import {
  createChartResearchAnnotation,
  fetchAdvisorySignals,
  fetchCandles,
  fetchChartResearchAnnotations,
  seedChartHistory,
  type AdvisorySignal,
  type ChartResearchAnnotation,
} from "../../api/client";
import {
  addSymbolToWatchlist,
  DEFAULT_MARKET_WORKSPACE_PREFERENCE,
  loadMarketWorkspacePreference,
  MarketWatchlistPanel,
  persistMarketWorkspacePreference,
  removeSymbolFromWatchlist,
  type MarketWatchlist,
  type MarketWorkspacePreference,
} from "../../market/marketWatchlists";
import { ContextualAssistantPanel } from "../../workstation/ai/ContextualAssistantPanel";
import { Panel, PanelHeader } from "../ui";

export const CHART_ANNOTATION_UI_DISCLAIMER =
  "Chart research annotations are research notes only — not financial advice, not a signal, not an order, and not an instruction. AXIOM does not act.";

type DrawingKind = "research_note" | "research_zone" | "trend_guide";

type ChartOverlayKey = "annotations" | "researchMarkers" | "sourceProvenance";

type ChartOverlayVisibility = Record<ChartOverlayKey, boolean>;

type ChartAnnotationLayerProps = {
  annotations: ChartResearchAnnotation[];
};

type ProfessionalMarketOverviewProps = {
  symbol: string;
  timeframe: ChartTimeframe;
  chartType: ChartType;
  barCount: number;
  connectionState: string;
  feedRunning: boolean;
  lastLiveAt: string | null;
  sourceSummary: string | null;
};

type ChartOverlayControlsProps = {
  visibility: ChartOverlayVisibility;
  onToggle: (key: ChartOverlayKey) => void;
};

type ChartResearchMarkerProps = {
  signals: AdvisorySignal[];
  visible: boolean;
};

function textValue(value: unknown, fallback = "—"): string {
  return typeof value === "string" && value.trim() ? value : fallback;
}

function numberValue(value: unknown, fallback: number): number {
  return typeof value === "number" && Number.isFinite(value) ? value : fallback;
}

function drawingKind(annotation: ChartResearchAnnotation): string {
  return textValue(annotation.content.drawing_kind, "research_note");
}

function annotationText(annotation: ChartResearchAnnotation): string {
  return textValue(annotation.content.text, "Research markup");
}

function visualPosition(annotation: ChartResearchAnnotation, index: number): { left: string; top: string } {
  const visual = annotation.content.visual;
  const payload = visual && typeof visual === "object" ? (visual as Record<string, unknown>) : {};
  const x = numberValue(payload.x_percent, 16 + (index % 4) * 18);
  const y = numberValue(payload.y_percent, 18 + (index % 3) * 18);
  return { left: `${Math.max(5, Math.min(84, x))}%`, top: `${Math.max(8, Math.min(82, y))}%` };
}

export function ProfessionalMarketOverview({
  symbol,
  timeframe,
  chartType,
  barCount,
  connectionState,
  feedRunning,
  lastLiveAt,
  sourceSummary,
}: ProfessionalMarketOverviewProps) {
  return (
    <Panel
      className="span-12 professional-market-overview"
      aria-label="Professional market workspace overview"
      header={
        <PanelHeader
          title="Professional Market Workspace"
          subtitle="Chart-centered market observation over existing governed data only. No client-side inference, no authoritative recompute, no authoritative venue feed, and no execution pathway."
          headingLevel={2}
        />
      }
    >
      <dl className="market-overview-grid" aria-label="Market workspace data-source inventory">
        <div>
          <dt>Active market</dt>
          <dd className="mono">{symbol}</dd>
        </div>
        <div>
          <dt>Timeframe</dt>
          <dd className="mono">{timeframe}</dd>
        </div>
        <div>
          <dt>Chart type</dt>
          <dd>{chartType}</dd>
        </div>
        <div>
          <dt>Bars</dt>
          <dd>{barCount}</dd>
        </div>
        <div>
          <dt>Simulated feed</dt>
          <dd>{feedRunning ? "live:simulated running" : "live:simulated stopped"}</dd>
        </div>
        <div>
          <dt>Connection</dt>
          <dd>{connectionState}</dd>
        </div>
        <div>
          <dt>Last simulated update</dt>
          <dd>{lastLiveAt ?? "No simulated update yet"}</dd>
        </div>
        <div>
          <dt>Source inventory</dt>
          <dd>{sourceSummary ?? "seed:synthetic and CSV provenance displayed after load"}</dd>
        </div>
      </dl>
      <p className="seed-banner" role="note">
        <strong>Non-authoritative data posture:</strong> <span className="mono">seed:synthetic</span>{" "}
        is chart context only, <span className="mono">live:simulated</span> is a governed simulated
        stream, and CSV labels are historical ingest provenance. This workspace never labels
        simulated data as authoritative live venue data.
      </p>
    </Panel>
  );
}

export function MarketStatusCards({
  symbol,
  timeframe,
  barCount,
  connectionState,
  feedRunning,
  lastLiveAt,
  sourceSummary,
}: Pick<
  ProfessionalMarketOverviewProps,
  "symbol" | "timeframe" | "barCount" | "connectionState" | "feedRunning" | "lastLiveAt" | "sourceSummary"
>) {
  const cards = [
    {
      label: "Market focus",
      value: `${symbol} · ${timeframe}`,
      note: "Registry-backed chart workspace context",
    },
    {
      label: "Data posture",
      value: "live:simulated",
      note: "Governed simulated stream; not an external venue feed",
    },
    {
      label: "Series depth",
      value: `${barCount} bars`,
      note: sourceSummary ?? "seed:synthetic / CSV provenance appears after load",
    },
    {
      label: "Connection state",
      value: connectionState,
      note: feedRunning ? "simulated stream running" : "simulated stream stopped",
    },
    {
      label: "Latest update",
      value: lastLiveAt ?? "No simulated update yet",
      note: "Timestamp is observational only",
    },
  ];
  return (
    <section className="panel span-12 market-status-card-section" aria-label="Market status overview cards">
      <h2>Market Status Overview</h2>
      <div className="market-status-card-grid">
        {cards.map((card) => (
          <article className="market-status-card" key={card.label}>
            <span className="ix-metadata">{card.label}</span>
            <strong>{card.value}</strong>
            <small>{card.note}</small>
          </article>
        ))}
      </div>
    </section>
  );
}

export function MarketWorkspaceStateNotice({ state, message }: { state: "loading" | "empty" | "error"; message: string }) {
  const role = state === "error" ? "alert" : "status";
  return (
    <div className={`market-state-notice ${state}`} role={role} aria-label={`Market workspace ${state} state`}>
      <strong>{state === "loading" ? "Loading market context" : state === "empty" ? "No governed market rows" : "Market context unavailable"}</strong>
      <span>{message}</span>
      <small>Research-only presentation. No inference, no action, no order path.</small>
    </div>
  );
}

export function ChartAccessibleSummary({
  symbol,
  timeframe,
  chartType,
  barCount,
  sourceSummary,
}: Pick<ProfessionalMarketOverviewProps, "symbol" | "timeframe" | "chartType" | "barCount" | "sourceSummary">) {
  return (
    <div className="chart-accessible-summary" role="status" aria-label="Accessible chart summary">
      {symbol} {timeframe} {chartType} chart. Visible series contains {barCount} bars. Source
      provenance: {sourceSummary ?? "not loaded yet; synthetic and simulated labels remain visible"}.
    </div>
  );
}

export function ChartOverlayControls({ visibility, onToggle }: ChartOverlayControlsProps) {
  const controls: { key: ChartOverlayKey; label: string; description: string }[] = [
    { key: "annotations", label: "Show annotations", description: "Existing chart research annotations" },
    { key: "researchMarkers", label: "Show research markers", description: "Read-only advisory research badges" },
    { key: "sourceProvenance", label: "Show source provenance", description: "Synthetic and simulated data labels" },
  ];
  return (
    <section className="chart-overlay-controls" aria-label="Chart overlay presentation controls">
      <h2>Chart Overlays</h2>
      <p className="muted">
        Presentation toggles only. Overlays render existing governed artifacts and do not generate,
        infer, mutate, or act.
      </p>
      <div className="chart-overlay-toggle-row">
        {controls.map((control) => (
          <button
            key={control.key}
            type="button"
            className={`btn ${visibility[control.key] ? "primary" : ""}`}
            aria-pressed={visibility[control.key]}
            onClick={() => onToggle(control.key)}
          >
            {control.label}
            <span className="sr-only"> — {control.description}</span>
          </button>
        ))}
      </div>
    </section>
  );
}

function markerPosition(index: number): { left: string; top: string } {
  return { left: `${Math.min(82, 18 + (index % 4) * 18)}%`, top: `${Math.min(78, 22 + (index % 3) * 16)}%` };
}

export function ChartResearchMarkerLayer({ signals, visible }: ChartResearchMarkerProps) {
  if (!visible) return null;
  return (
    <div className="chart-research-marker-layer" aria-label="Read-only chart research markers layer">
      {signals.map((signal, index) => (
        <article
          key={signal.signal_id}
          className={`chart-research-marker signal-${signal.signal_state}`}
          style={markerPosition(index)}
          aria-label={`Read-only research marker ${index + 1}`}
          data-readonly="true"
          data-result-action="navigate"
        >
          <strong>{signal.signal_state.replace(/_/g, " ")}</strong>
          <span>{signal.symbol} · {signal.timeframe}</span>
          <small>Existing advisory record · {signal.state_reason}</small>
          <small>Confidence: {signal.calibrated_confidence == null ? "uncertain" : `${(signal.calibrated_confidence * 100).toFixed(1)}% calibrated`}</small>
        </article>
      ))}
    </div>
  );
}

export function ChartResearchMarkerList({ signals, visible }: ChartResearchMarkerProps) {
  if (!visible) return null;
  return (
    <section className="panel span-12 chart-marker-list" aria-label="Read-only research marker list">
      <h2>Research Markers</h2>
      <p className="muted">
        Existing advisory records shown as inert research context. These are not instructions, not
        generated by the chart, and not executable actions.
      </p>
      {signals.length === 0 ? (
        <p className="muted" role="status">No existing advisory records are available for this chart context.</p>
      ) : null}
      <div className="chart-marker-card-grid">
        {signals.map((signal) => (
          <article key={signal.signal_id} className="chart-marker-card" data-readonly="true">
            <strong>{signal.symbol} · {signal.timeframe}</strong>
            <span className="signal-state-badge signal-warning">{signal.signal_state}</span>
            <small>Provenance: existing advisory record {signal.signal_id}</small>
            <small>Lineage: {signal.experiment_id} · {signal.model_artifact_id}</small>
            <small>Uncertainty: {signal.calibrated_confidence == null ? "not calibrated" : `${(signal.calibrated_confidence * 100).toFixed(1)}% calibrated`}</small>
            <small>Research-only marker · {signal.state_reason}</small>
          </article>
        ))}
      </div>
    </section>
  );
}

export function ChartResearchAnnotationLayer({ annotations }: ChartAnnotationLayerProps) {
  return (
    <div className="chart-research-layer" aria-label="Chart research annotations layer">
      {annotations.length === 0 ? (
        <div className="chart-annotation-empty" role="status">
          No chart research annotations yet. Add an operator-authored research markup.
        </div>
      ) : null}
      {annotations.map((annotation, index) => (
        <article
          key={annotation.id}
          className={`chart-annotation-marker ${drawingKind(annotation)}`}
          style={visualPosition(annotation, index)}
          aria-label={`Chart research annotation ${index + 1}`}
        >
          <strong>{drawingKind(annotation).replace(/_/g, " ")}</strong>
          <span>{annotationText(annotation)}</span>
          <small>
            Sources: {annotation.source_artifact_ids.join(", ")} · {annotation.research_status}
          </small>
        </article>
      ))}
    </div>
  );
}

export function ChartWorkspacePage() {
  const { isAuthenticated } = useAuth();
  const chart = useChartState();
  const data = useChartData(chart.state, isAuthenticated);
  const [busy, setBusy] = useState(false);
  const [annotationBusy, setAnnotationBusy] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);
  const [annotationError, setAnnotationError] = useState<string | null>(null);
  const [sourceSummary, setSourceSummary] = useState<string | null>(null);
  const [annotations, setAnnotations] = useState<ChartResearchAnnotation[]>([]);
  const [researchMarkers, setResearchMarkers] = useState<AdvisorySignal[]>([]);
  const [markerError, setMarkerError] = useState<string | null>(null);
  const [overlayVisibility, setOverlayVisibility] = useState<ChartOverlayVisibility>({
    annotations: true,
    researchMarkers: true,
    sourceProvenance: true,
  });
  const [marketPreference, setMarketPreference] = useState<MarketWorkspacePreference>(
    DEFAULT_MARKET_WORKSPACE_PREFERENCE,
  );
  const [watchlistBusy, setWatchlistBusy] = useState(false);
  const [watchlistError, setWatchlistError] = useState<string | null>(null);
  const [annotationTextValue, setAnnotationTextValue] = useState(
    "Operator research note linked to governed chart context.",
  );
  const [annotationKind, setAnnotationKind] = useState<DrawingKind>("research_note");
  const [linkedSourceIds, setLinkedSourceIds] = useState("chart-context");

  useEffect(() => {
    if (!isAuthenticated) return;
    void reloadAnnotations();
    // eslint-disable-next-line react-hooks/exhaustive-deps -- reload is presentation fetch only
  }, [isAuthenticated, chart.state.symbol, chart.state.timeframe]);

  useEffect(() => {
    if (!isAuthenticated) return;
    void reloadResearchMarkers();
    // eslint-disable-next-line react-hooks/exhaustive-deps -- marker reload is read-only presentation fetch
  }, [isAuthenticated, chart.state.symbol, chart.state.timeframe]);

  useEffect(() => {
    if (!isAuthenticated) return;
    let cancelled = false;
    async function restoreMarketPreference() {
      try {
        const restored = await loadMarketWorkspacePreference();
        if (!cancelled) {
          setMarketPreference(restored);
          setOverlayVisibility({
            annotations: restored.overlay_visibility.annotations,
            researchMarkers: restored.overlay_visibility.research_markers,
            sourceProvenance: restored.overlay_visibility.source_provenance,
          });
          setWatchlistError(null);
        }
      } catch (e) {
        if (!cancelled) {
          setWatchlistError(e instanceof Error ? e.message : "Failed to load market watchlist");
        }
      }
    }
    void restoreMarketPreference();
    return () => {
      cancelled = true;
    };
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return (
      <div className="page-header">
        <div>
          <h1>Chart Workspace</h1>
          <p className="error-text">Authentication required. Sign in to view charts and research annotations.</p>
        </div>
      </div>
    );
  }

  async function reloadAnnotations() {
    try {
      const rows = await fetchChartResearchAnnotations({
        symbol: chart.state.symbol,
        timeframe: chart.state.timeframe,
        limit: 50,
      });
      setAnnotations(rows);
      setAnnotationError(null);
    } catch (e) {
      setAnnotationError(e instanceof Error ? e.message : "Failed to load annotations");
    }
  }

  async function reloadResearchMarkers() {
    try {
      const rows = await fetchAdvisorySignals({
        symbol: chart.state.symbol,
        timeframe: chart.state.timeframe,
        limit: 12,
      });
      setResearchMarkers(rows);
      setMarkerError(null);
    } catch (e) {
      setMarkerError(e instanceof Error ? e.message : "Failed to load research markers");
    }
  }

  async function onStart() {
    setBusy(true);
    setActionError(null);
    try {
      // Seed history first (request-scoped DB), then start live stream
      await seedChartHistory();
      await data.reload();
      await data.startFeed();
      await new Promise((r) => setTimeout(r, 300));
      await data.reload();
      await refreshSourceSummary();
      await reloadAnnotations();
    } catch (e) {
      setActionError(e instanceof Error ? e.message : "Failed to start feed");
    } finally {
      setBusy(false);
    }
  }

  async function refreshSourceSummary() {
    try {
      const series = await fetchCandles({
        symbol: chart.state.symbol,
        timeframe: chart.state.timeframe,
        limit: 500,
        order: "asc",
      });
      if (series.kind === "unavailable") {
        setSourceSummary(series.detail);
        return;
      }
      const counts: Record<string, number> = {};
      for (const r of series.bars) {
        const src = r.source ?? "unknown";
        counts[src] = (counts[src] ?? 0) + 1;
      }
      const parts = Object.entries(counts).map(([k, v]) => `${k}=${v}`);
      setSourceSummary(parts.join(" · ") || "no rows");
    } catch {
      setSourceSummary(null);
    }
  }

  async function onSeedOnly() {
    setBusy(true);
    setActionError(null);
    try {
      await seedChartHistory();
      await data.reload();
      await refreshSourceSummary();
    } catch (e) {
      setActionError(e instanceof Error ? e.message : "Seed failed");
    } finally {
      setBusy(false);
    }
  }

  async function onStop() {
    setBusy(true);
    try {
      await data.stopFeed();
    } catch (e) {
      setActionError(e instanceof Error ? e.message : "Failed to stop feed");
    } finally {
      setBusy(false);
    }
  }

  async function onCreateAnnotation() {
    setAnnotationBusy(true);
    setAnnotationError(null);
    try {
      const parsedSources = linkedSourceIds
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean);
      const sourceIds =
        parsedSources.length > 0
          ? parsedSources
          : [`chart-context:${chart.state.symbol}:${chart.state.timeframe}`];
      const created = await createChartResearchAnnotation({
        artifact_type: annotationKind === "research_note" ? "chart_research_annotation" : "chart_research_drawing",
        chart_context: {
          market_class: chart.state.symbol === "BTCUSD" ? "crypto" : "forex",
          symbol: chart.state.symbol,
          timeframe: chart.state.timeframe,
          anchor: {
            mode: "operator_visible_window",
            visible_bars: data.bars.length,
          },
        },
        content: {
          drawing_kind: annotationKind,
          text: annotationTextValue,
          visual: {
            x_percent: Math.min(78, 16 + (annotations.length % 4) * 18),
            y_percent: Math.min(72, 18 + (annotations.length % 3) * 18),
          },
        },
        source_artifact_ids: sourceIds,
        provenance: {
          ui_surface: "ChartWorkspacePage",
          operator_authored: true,
          ai_assisted: false,
          presentation_only: true,
        },
        uncertainty: { method: "not_applicable_operator_markup" },
        research_status: "research_only",
      });
      setAnnotations((current) => [created, ...current]);
      setAnnotationTextValue("Operator research note linked to governed chart context.");
    } catch (e) {
      setAnnotationError(e instanceof Error ? e.message : "Failed to create annotation");
    } finally {
      setAnnotationBusy(false);
    }
  }

  const primaryWatchlist = marketPreference.watchlists[0] ?? DEFAULT_MARKET_WORKSPACE_PREFERENCE.watchlists[0];

  function preferenceWithWatchlist(watchlist: MarketWatchlist): MarketWorkspacePreference {
    return {
      ...marketPreference,
      active_symbol: chart.state.symbol,
      active_timeframe: chart.state.timeframe,
      watchlists: [watchlist, ...marketPreference.watchlists.slice(1)],
    };
  }

  async function saveMarketPreference(next: MarketWorkspacePreference) {
    setWatchlistBusy(true);
    setWatchlistError(null);
    setMarketPreference(next);
    try {
      await persistMarketWorkspacePreference(next);
    } catch (e) {
      setWatchlistError(e instanceof Error ? e.message : "Failed to persist market watchlist");
    } finally {
      setWatchlistBusy(false);
    }
  }

  async function onAddWatchlistSymbol(symbol: string, timeframe: ChartTimeframe) {
    const nextWatchlist = addSymbolToWatchlist(primaryWatchlist, symbol, timeframe);
    await saveMarketPreference(preferenceWithWatchlist(nextWatchlist));
  }

  async function onRemoveWatchlistSymbol(symbol: string) {
    const nextWatchlist = removeSymbolFromWatchlist(primaryWatchlist, symbol);
    await saveMarketPreference(preferenceWithWatchlist(nextWatchlist));
  }

  function toggleOverlayVisibility(key: ChartOverlayKey) {
    setOverlayVisibility((current) => ({ ...current, [key]: !current[key] }));
  }

  const conn =
    data.connectionState === "connected"
      ? "ok"
      : data.connectionState === "connecting" || data.connectionState === "reconnecting"
        ? "loading"
        : "error";

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Chart Workspace</h1>
          <p className="muted">
            Institutional candlestick workspace with inert chart research annotations. Presentation
            only — no client-side inference, no authoritative analytics recompute, no AI-assisted
            annotation generation in W5-U03, and no execution controls.
          </p>
        </div>
      </div>

      <p className="advisory-disclaimer" role="note">
        <strong>Research markup only.</strong> {CHART_ANNOTATION_UI_DISCLAIMER}
      </p>

      <div className="panel-grid">
        <section className="panel span-12 chart-toolbar" aria-label="Chart controls">
          <div className="chart-controls">
            <label className="field-inline">
              <span>Symbol</span>
              <select
                aria-label="Chart symbol"
                value={chart.state.symbol}
                onChange={(e) => chart.setSymbol(e.target.value)}
              >
                {chart.availableSymbols.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </label>
            <label className="field-inline">
              <span>Timeframe</span>
              <select
                aria-label="Chart timeframe"
                value={chart.state.timeframe}
                onChange={(e) => chart.setTimeframe(e.target.value as ChartTimeframe)}
              >
                {chart.availableTimeframes.map((tf) => (
                  <option key={tf} value={tf}>
                    {tf}
                  </option>
                ))}
              </select>
            </label>
            <fieldset className="chart-type-group" aria-label="Chart type">
              <legend className="sr-only">Chart type</legend>
              {(
                [
                  ["candlestick", "Candles"],
                  ["line", "Line"],
                  ["area", "Area"],
                ] as [ChartType, string][]
              ).map(([id, label]) => (
                <button
                  key={id}
                  type="button"
                  className={`btn ${chart.state.chartType === id ? "primary" : ""}`}
                  aria-pressed={chart.state.chartType === id}
                  onClick={() => chart.setChartType(id)}
                >
                  {label}
                </button>
              ))}
            </fieldset>
            <div className="feed-actions">
              <button type="button" className="btn primary" disabled={busy} onClick={() => void onStart()}>
                Start live feed
              </button>
              <button type="button" className="btn" disabled={busy} onClick={() => void onStop()}>
                Stop feed
              </button>
              <button type="button" className="btn" disabled={busy} onClick={() => void onSeedOnly()}>
                Seed history
              </button>
              <button type="button" className="btn" disabled={busy} onClick={() => void data.reload()}>
                Reload history
              </button>
            </div>
          </div>
          <div className="chart-status-row">
            <StatusPill state={conn} label={`WS ${data.connectionState}`} />
            <span className={`badge ${data.feedRunning ? "up" : "degraded"}`}>
              feed {data.feedRunning ? "running" : "stopped"}
            </span>
            <span className="badge stub mono">
              {chart.state.symbol} · {chart.state.timeframe} · {chart.state.chartType}
            </span>
            <span className="muted mono">
              bars={data.bars.length}
              {data.lastLiveAt ? ` · last live ${data.lastLiveAt}` : ""}
            </span>
            {/* Color is not sole signal: text labels above for up/down series colors */}
            <span className="a11y-legend" aria-hidden={false}>
              <span className="legend-up">▲ Up</span>
              <span className="legend-down">▼ Down</span>
            </span>
          </div>
          {/* C-2: synthetic seed is non-authoritative — shown explicitly in UI */}
          <p className="seed-banner" role="note">
            <strong>Data provenance:</strong> bars with source{" "}
            <span className="mono">seed:synthetic</span> are{" "}
            <strong>non-authoritative</strong> chart-context only (not real market history).{" "}
            Live ticks use <span className="mono">live:simulated</span>; CSV ingest uses its own
            source labels.{" "}
            {sourceSummary ? (
              <span className="mono muted">Counts: {sourceSummary}</span>
            ) : (
              <span className="muted">Load or seed data to see source counts.</span>
            )}
          </p>
          {actionError || data.error ? (
            <p className="error-text">{actionError ?? data.error}</p>
          ) : null}
        </section>

        <section className="panel span-12 chart-panel">
          <h2>
            {chart.state.symbol} · {chart.state.timeframe}
          </h2>
          {data.loadState === "loading" ? (
            <MarketWorkspaceStateNotice state="loading" message="Loading existing historical candles…" />
          ) : null}
          {data.loadState === "empty" ? (
            <MarketWorkspaceStateNotice
              state="empty"
              message="No governed candles for this symbol/timeframe. Seed synthetic context or ingest historical CSV data."
            />
          ) : null}
          {data.loadState === "error" ? (
            <MarketWorkspaceStateNotice state="error" message={data.error ?? "Failed to load market context"} />
          ) : null}
          {data.connectionState === "disconnected" || data.connectionState === "error" ? (
            <p className="muted" role="status">
              Live WebSocket is {data.connectionState}. Historical view still works; start feed and
              ensure you are signed in for live updates.
            </p>
          ) : null}
          <ChartAccessibleSummary
            symbol={chart.state.symbol}
            timeframe={chart.state.timeframe}
            chartType={chart.state.chartType}
            barCount={data.bars.length}
            sourceSummary={sourceSummary}
          />
          <div className="chart-annotation-stage" aria-label="Price chart with research annotations">
            {(data.loadState === "ready" || data.bars.length > 0) && (
              <PriceChart
                bars={data.bars}
                chartType={chart.state.chartType}
                symbol={chart.state.symbol}
              />
            )}
            {overlayVisibility.annotations ? <ChartResearchAnnotationLayer annotations={annotations} /> : null}
            <ChartResearchMarkerLayer signals={researchMarkers} visible={overlayVisibility.researchMarkers} />
          </div>
        </section>

        <MarketWatchlistPanel
          watchlist={primaryWatchlist}
          availableSymbols={chart.availableSymbols}
          availableTimeframes={chart.availableTimeframes}
          selectedSymbol={chart.state.symbol}
          selectedTimeframe={chart.state.timeframe}
          busy={watchlistBusy}
          error={watchlistError}
          onAddSymbol={(symbol, timeframe) => void onAddWatchlistSymbol(symbol, timeframe)}
          onRemoveSymbol={(symbol) => void onRemoveWatchlistSymbol(symbol)}
          onSelectSymbol={(symbol) => chart.setSymbol(symbol)}
        />
        <ProfessionalMarketOverview
          symbol={chart.state.symbol}
          timeframe={chart.state.timeframe}
          chartType={chart.state.chartType}
          barCount={data.bars.length}
          connectionState={data.connectionState}
          feedRunning={data.feedRunning}
          lastLiveAt={data.lastLiveAt}
          sourceSummary={sourceSummary}
        />
        <MarketStatusCards
          symbol={chart.state.symbol}
          timeframe={chart.state.timeframe}
          barCount={data.bars.length}
          connectionState={data.connectionState}
          feedRunning={data.feedRunning}
          lastLiveAt={data.lastLiveAt}
          sourceSummary={sourceSummary}
        />
        <section className="panel span-12" aria-label="Market overlay controls">
          <ChartOverlayControls visibility={overlayVisibility} onToggle={toggleOverlayVisibility} />
          {markerError ? <p className="error-text">{markerError}</p> : null}
        </section>

        <ChartResearchMarkerList signals={researchMarkers} visible={overlayVisibility.researchMarkers} />

        <section className="panel span-12 chart-annotation-panel" aria-label="Chart research annotation controls">
          <h2>Chart Research Annotations</h2>
          <p className="muted">
            Operator-authored drawing tools create inert research markups only. They write to the
            annotation store and audit trail; they do not emit signals, place orders, size positions,
            or modify accounts.
          </p>
          <div className="chart-annotation-form">
            <label className="field">
              <span>Drawing tool</span>
              <select
                value={annotationKind}
                onChange={(e) => setAnnotationKind(e.target.value as DrawingKind)}
              >
                <option value="research_note">Research note</option>
                <option value="research_zone">Research zone</option>
                <option value="trend_guide">Trend guide</option>
              </select>
            </label>
            <label className="field">
              <span>Research text</span>
              <textarea
                value={annotationTextValue}
                onChange={(e) => setAnnotationTextValue(e.target.value)}
                rows={3}
              />
            </label>
            <label className="field">
              <span>Source artifact ids</span>
              <input
                value={linkedSourceIds}
                onChange={(e) => setLinkedSourceIds(e.target.value)}
                placeholder="signal-1, report-1"
              />
            </label>
            <button
              type="button"
              className="btn primary"
              disabled={annotationBusy || !annotationTextValue.trim()}
              onClick={() => void onCreateAnnotation()}
            >
              Add research markup
            </button>
            <button type="button" className="btn" onClick={() => void reloadAnnotations()}>
              Reload annotations
            </button>
          </div>
          {annotationError ? <p className="error-text">{annotationError}</p> : null}
          <div className="chart-annotation-list" aria-label="Persisted chart research annotations">
            {annotations.map((annotation) => (
              <article key={annotation.id} className="chart-annotation-card">
                <strong>{drawingKind(annotation).replace(/_/g, " ")}</strong>
                <span>{annotationText(annotation)}</span>
                <small className="mono">{annotation.id}</small>
                <small>Sources: {annotation.source_artifact_ids.join(", ")}</small>
                <small>{annotation.disclaimer}</small>
              </article>
            ))}
          </div>
        </section>

        <section className="panel span-12" data-ui008-mount="contextual-assistant-panel" aria-label="Contextual Assistant mount point">
          <ContextualAssistantPanel />
        </section>
      </div>
    </>
  );
}
