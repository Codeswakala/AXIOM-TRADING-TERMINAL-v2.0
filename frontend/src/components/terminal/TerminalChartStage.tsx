import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useTerminal } from "./TerminalContext";
import { PriceChart, type OverlayLine } from "../chart/PriceChart";
import type { CandleBar, ChartType } from "../../chart/types";
import {
  createChartResearchAnnotation,
  deleteChartResearchAnnotation,
  fetchAdvisorySignals,
  fetchCandles,
  fetchChartResearchAnnotations,
  fetchIndicatorSeries,
  seedChartHistory,
  updateChartResearchAnnotation,
  type AdvisorySignal,
  type ApiCandle,
  type CandleSeriesResult,
  type ChartResearchAnnotation,
  type IndicatorResult,
  type IndicatorSeriesEnvelope,
  type LineIndicatorResult,
  type MacdIndicatorResult,
  type MultiIndicatorResult,
} from "../../api/client";
import { timeframeCodeOf, timeframeMinutesOf, type TimeframeCode } from "../../api/timeframes";
import {
  DIRECT_PILL_IDS,
  ENGINES,
  INDICATOR_UI,
  MARKET_STRUCTURE_DISCLOSURE,
  indicatorUiOf,
  paletteEntryFor,
  type IndicatorEngine,
} from "../../api/indicatorRegistry";
import {
  DRAWING_TOOLS,
  drawingLabelRejection,
  drawingToolOf,
  type ChartDrawing,
  type DrawingGeometry,
  type DrawingToolId,
} from "../../api/drawingTools";
import type { CoordinateConverters } from "./ChartDrawingOverlay";
import { IndicatorPane } from "./IndicatorPane";
import { ConfluenceStrip } from "./ConfluenceStrip";
import { SessionContextStrip } from "./SessionContextStrip";
import "./TerminalMultiPane.css";

export type TimeframeOption = "1m" | "5m" | "15m" | "1h" | "4h" | "1d";

export interface TerminalChartStageProps {
  className?: string;
  initialTimeframe?: TimeframeOption;
  initialChartType?: ChartType;
}

function parseBar(c: ApiCandle): CandleBar {
  return {
    time: Math.floor(new Date(c.open_time).getTime() / 1000),
    open: Number(c.open),
    high: Number(c.high),
    low: Number(c.low),
    close: Number(c.close),
    volume: c.volume ? Number(c.volume) : null,
    source: c.source ?? "synthetic",
  };
}

/**
 * TerminalChartStage
 *
 * Centrepiece candlestick charting engine for the AXIOM Institutional Trading Terminal (P03).
 * Integrates TradingView lightweight-charts with dynamic CSS token resolution (getComputedToken).
 *
 * Adheres strictly to:
 * - B-P03-1: 100% token purity via getComputedToken resolver
 * - B-P03-2 / TD-029: Timeframe honesty — DATA-P02 makes the notice true:
 *   it renders from the SERVER series discriminant (native / aggregated /
 *   unavailable), never from a timeframe label comparison.
 * - B-P03-3: Overlays are presentation-only (0 analytical signaling or trade bias)
 * - B-P03-4 / GA-050: Inert research annotations with strict rejection of order fields
 * - B-P03-5 / TD-028: Visual distinction between seed:synthetic and live:simulated bars
 * - T-1: Zero actuation controls
 * - T-6: Data honesty (never fabricate bars — DATA-P02 M3 removes the
 *   client-side M1 fallback: unaggregated M1 bars are never passed off as a
 *   higher timeframe again; M6: partial buckets are excluded server-side)
 * - DATA-P02 M7: session context (Tokyo/London/New York, fixed UTC windows)
 * - CHART-P01 (F-CHART-1): the indicator pills drive REAL series — computed
 *   server-side, insufficiency disclosed as a typed state, provenance never
 *   exceeding the underlying bars'. Indicators describe data, they never
 *   advise a trade.
 * - SAL-2 (Internal) presentation surface
 */
export function TerminalChartStage({
  className = "",
  initialTimeframe = "1m",
  initialChartType = "candlestick",
}: TerminalChartStageProps) {
  const { selectedSymbol, selectedQuote, liveMarket } = useTerminal();
  const [timeframe, setTimeframe] = useState<TimeframeOption>(initialTimeframe);
  const [chartType, setChartType] = useState<ChartType>(initialChartType);

  // CHART-P01: real indicator state. `activeIndicators` are registry ids; the
  // results are the server's typed per-indicator payloads (computed /
  // insufficient), and `indicatorMeta` carries the series provenance the
  // computation ran over (M6).
  const [activeIndicators, setActiveIndicators] = useState<string[]>([]);
  const [indicatorResults, setIndicatorResults] = useState<Record<string, IndicatorResult>>({});
  const [indicatorMeta, setIndicatorMeta] = useState<IndicatorSeriesEnvelope | null>(null);
  const [indicatorError, setIndicatorError] = useState<string | null>(null);

  // CHART-P02 M5/M6: toolbar menus + the pane budget policy.
  const [openEngineMenu, setOpenEngineMenu] = useState<IndicatorEngine | null>(null);
  const [paneBudgetRefusal, setPaneBudgetRefusal] = useState<string | null>(null);
  // CHART-P02 M7: the price pane's visible time range (zoom/pan) — panes track it.
  const [visibleRange, setVisibleRange] = useState<{ from: number; to: number } | null>(null);

  // CHART-P03 drawing tools (M1/M2/M5): anchors are (price, time) — pixels
  // exist only momentarily at conversion time and are never persisted.
  const [drawingTool, setDrawingTool] = useState<DrawingToolId | null>(null);
  const [pendingAnchor, setPendingAnchor] = useState<{ price: number; time: number } | null>(null);
  const [selectedDrawingId, setSelectedDrawingId] = useState<string | null>(null);
  const [drawingError, setDrawingError] = useState<string | null>(null);
  const coordinateApiRef = useRef<CoordinateConverters | null>(null);
  const canvasContainerRef = useRef<HTMLDivElement | null>(null);

  /** M6 policy, stated: at most MAX_PANE_INDICATORS concurrent pane charts;
   * each pane is 90px; the price pane keeps a 280px minimum. A refusal is
   * EXPLICIT (status strip entry + the toggle does not activate) — never a
   * silently dropped indicator. */
  const MAX_PANE_INDICATORS = 3;
  const activePaneCount = activeIndicators.filter((id) => indicatorUiOf(id)?.pane === "pane").length;

  // DATA-P02 M4: the series STATE is the server's typed discriminant.
  const [series, setSeries] = useState<CandleSeriesResult | null>(null);
  const [isLoadingCandles, setIsLoadingCandles] = useState(false);
  const [candleError, setCandleError] = useState<string | null>(null);
  const [hoveredBar, setHoveredBar] = useState<CandleBar | null>(null);

  // Annotations state (B-P03-4)
  const [annotations, setAnnotations] = useState<ChartResearchAnnotation[]>([]);
  const [isAnnotationModalOpen, setIsAnnotationModalOpen] = useState(false);
  const [annotationText, setAnnotationText] = useState("");
  const [annotationPrice, setAnnotationPrice] = useState("");
  const [annotationError, setAnnotationError] = useState<string | null>(null);
  const [isSavingAnnotation, setIsSavingAnnotation] = useState(false);

  // Seed notification state (B-P03-5)
  const [isSeeding, setIsSeeding] = useState(false);
  const [seedNotice, setSeedNotice] = useState<string | null>(null);

  const symbolKey = selectedSymbol.replace("/", "");
  const seriesKind = series?.kind ?? "unavailable";
  const seriesDetail = series?.kind === "unavailable" ? series.detail : null;
  const backendCode: TimeframeCode = timeframeCodeOf(timeframe);
  const backendMinutes = timeframeMinutesOf(backendCode);
  const excludedPartialBuckets =
    series?.kind === "aggregated" ? series.excludedPartialBuckets : 0;

  const historicalBars = useMemo<CandleBar[]>(() => {
    if (!series || series.kind === "unavailable") return [];
    return series.bars.map(parseBar);
  }, [series]);

  // CHART-P01 M1/M3: indicator series come from the server, computed over the
  // same window the chart displays. The candle series itself is never
  // refetched by a toggle (S3) — only the indicator endpoint is called.
  const activeRef = useRef<string[]>([]);
  activeRef.current = activeIndicators;

  const refreshIndicators = useCallback(
    async (ids: string[]) => {
      if (ids.length === 0) return;
      try {
        const envelope = await fetchIndicatorSeries({
          symbol: symbolKey,
          timeframe: backendCode,
          indicators: ids,
        });
        setIndicatorMeta(envelope);
        setIndicatorError(null);
        setIndicatorResults((prev) => ({ ...prev, ...envelope.indicators }));
      } catch (err) {
        setIndicatorError(err instanceof Error ? err.message : "Indicator series request failed");
        setIndicatorResults({});
        setIndicatorMeta(null);
      }
    },
    [symbolKey, backendCode],
  );

  useEffect(() => {
    // Timeframe/symbol switch invalidates cached indicator results and
    // re-fetches whichever indicators are active (their series window
    // changed). Toggling alone never refetches the candle series.
    setIndicatorResults({});
    setIndicatorMeta(null);
    setIndicatorError(null);
    if (activeRef.current.length > 0) {
      void refreshIndicators(activeRef.current);
    }
  }, [symbolKey, timeframe, refreshIndicators]);

  const toggleIndicator = (id: string) => {
    if (activeIndicators.includes(id)) {
      setActiveIndicators((prev) => prev.filter((i) => i !== id));
      setPaneBudgetRefusal(null);
      return;
    }
    // M6: the pane budget refuses EXPLICITLY — the indicator is not enabled.
    if (indicatorUiOf(id)?.pane === "pane" && activePaneCount >= MAX_PANE_INDICATORS) {
      setPaneBudgetRefusal(
        `${id}: pane budget reached — at most ${MAX_PANE_INDICATORS} pane indicators concurrently; the indicator was NOT enabled`,
      );
      return;
    }
    setPaneBudgetRefusal(null);
    setActiveIndicators((prev) => [...prev, id]);
    void refreshIndicators([id]);
  };

  // 1. Fetch the typed candle series on symbol or timeframe switch.
  //    Aggregated series re-fetch when a new M1 minute closes (the live quote
  //    minute advances) so the last completed bucket stays current.
  const liveMinuteKey =
    seriesKind === "aggregated" && selectedQuote?.openTime
      ? selectedQuote.openTime.slice(0, 16)
      : null;

  useEffect(() => {
    let isCancelled = false;
    async function loadCandles() {
      setIsLoadingCandles(true);
      setCandleError(null);
      try {
        const result = await fetchCandles({
          symbol: symbolKey,
          timeframe: backendCode,
          limit: 100,
          order: "asc",
        });
        if (isCancelled) return;
        setSeries(result);
        if (result.kind === "unavailable") {
          setCandleError(result.detail);
        }
      } catch {
        if (!isCancelled) {
          setCandleError("No historical candle records available for active timeframe");
          setSeries(null);
        }
      } finally {
        if (!isCancelled) setIsLoadingCandles(false);
      }
    }
    void loadCandles();
    return () => {
      isCancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [symbolKey, timeframe, liveMinuteKey]);

  // 2. Fetch existing research annotations & advisory signals
  const [chartSignals, setChartSignals] = useState<AdvisorySignal[]>([]);

  useEffect(() => {
    let isCancelled = false;
    async function loadAnnotationsAndSignals() {
      try {
        const [data, sigs] = await Promise.all([
          fetchChartResearchAnnotations({ symbol: symbolKey, timeframe }),
          fetchAdvisorySignals({ symbol: symbolKey, limit: 5 }).catch(() => []),
        ]);
        if (!isCancelled) {
          setAnnotations(data);
          setChartSignals(sigs);
        }
      } catch {
        if (!isCancelled) {
          setAnnotations([]);
          setChartSignals([]);
        }
      }
    }
    void loadAnnotationsAndSignals();
    return () => {
      isCancelled = true;
    };
  }, [symbolKey, timeframe]);

  // 3. Merge the live M1 tick ONLY into a native M1 series (DATA-P02 M4/M6:
  //    an aggregated bucket is a different granularity — a 1-minute live bar
  //    must never be merged into an H1/H4/D1 series).
  const chartBars = useMemo(() => {
    if (seriesKind !== "native") return historicalBars;

    if (!selectedQuote) return historicalBars;

    const liveTime = Math.floor(new Date(selectedQuote.openTime || selectedQuote.updatedAt).getTime() / 1000);
    const liveBar: CandleBar = {
      time: liveTime,
      open: Number(selectedQuote.open),
      high: Number(selectedQuote.high),
      low: Number(selectedQuote.low),
      close: Number(selectedQuote.close),
      volume: selectedQuote.volume ? Number(selectedQuote.volume) : null,
      source: "simulated",
    };

    if (historicalBars.length === 0) return [liveBar];

    const lastIdx = historicalBars.length - 1;
    const lastBar = historicalBars[lastIdx];

    if (lastBar.time === liveTime) {
      const updated = [...historicalBars];
      updated[lastIdx] = liveBar;
      return updated;
    }

    if (liveTime > lastBar.time) {
      return [...historicalBars, liveBar];
    }

    return historicalBars;
  }, [historicalBars, selectedQuote, seriesKind]);

  // Detect bar provenance distribution (B-P03-5). DATA-P02: aggregated bars
  // may carry the joined marker "seed:synthetic+live:simulated" (R4) — the
  // counts are contains-based so a mixed series is reported as mixed, never
  // collapsed into a single claim.
  const provenanceStats = useMemo(() => {
    const total = chartBars.length;
    if (total === 0) {
      return { seedCount: 0, liveCount: 0, primaryProvenance: "none", provenanceClass: "none" };
    }
    const liveCount = chartBars.filter((b) => (b.source ?? "").includes("simulated")).length;
    const seedCount = chartBars.filter((b) => (b.source ?? "").includes("synthetic")).length;
    const hasLive = liveCount > 0;
    const hasSeed = seedCount > 0;
    const primaryProvenance =
      hasLive && hasSeed
        ? "seed:synthetic + live:simulated"
        : hasLive
          ? "live:simulated"
          : hasSeed
            ? "seed:synthetic"
            : "none";
    const provenanceClass = hasLive && hasSeed ? "mixed" : hasLive ? "live-simulated" : "seed-synthetic";
    return { seedCount, liveCount, primaryProvenance, provenanceClass };
  }, [chartBars]);

  // CHART-P01 derived presentation state. Only COMPUTED results become
  // series; insufficient/unavailable results render as typed disclosures and
  // never as lines (M4/M6).
  const overlayLines = useMemo<OverlayLine[]>(() => {
    const lines: OverlayLine[] = [];
    const pushPoints = (
      id: string,
      label: string,
      points: Array<{ time: number; value: number }>,
    ) => {
      if (points.length === 0) return;
      const palette = paletteEntryFor(id);
      lines.push({ id, label, colorToken: palette.colorToken, style: palette.style, points });
    };
    for (const id of activeIndicators) {
      const def = indicatorUiOf(id);
      const result = indicatorResults[id];
      if (!def || def.pane !== "overlay" || !result || result.shape === "insufficient") continue;
      if (result.shape === "line") {
        pushPoints(
          id,
          def.label,
          result.points
            .filter((p) => p.value !== null && Number.isFinite(Number(p.value)))
            .map((p) => ({ time: Math.floor(Date.parse(p.time) / 1000), value: Number(p.value) })),
        );
      } else if (result.shape === "band") {
        for (const key of ["upper", "middle", "lower"] as const) {
          pushPoints(
            `${id}:${key}`,
            `${def.label} ${key}`,
            result.points
              .filter((p) => p[key] !== null && Number.isFinite(Number(p[key])))
              .map((p) => ({ time: Math.floor(Date.parse(p.time) / 1000), value: Number(p[key]) })),
          );
        }
      } else if (result.shape === "multi") {
        // S2: deterministic (colour, style) assignment per named line.
        for (const [name, line] of Object.entries(result.lines)) {
          pushPoints(
            `${id}:${name}`,
            `${def.label} ${name}`,
            (line ?? [])
              .filter((p) => p.value !== null && Number.isFinite(Number(p.value)))
              .map((p) => ({ time: Math.floor(Date.parse(p.time) / 1000), value: Number(p.value) })),
          );
        }
      }
    }
    return lines;
  }, [activeIndicators, indicatorResults]);

  const paneEntries = useMemo(() => {
    const entries: Array<{
      id: string;
      def: NonNullable<ReturnType<typeof indicatorUiOf>>;
      result: LineIndicatorResult | MacdIndicatorResult | MultiIndicatorResult;
    }> = [];
    for (const id of activeIndicators) {
      const def = indicatorUiOf(id);
      const result = indicatorResults[id];
      if (!def || def.pane !== "pane") continue;
      if (!result || result.shape === "insufficient" || result.shape === "band") continue;
      entries.push({ id, def, result });
    }
    return entries;
  }, [activeIndicators, indicatorResults]);

  const indicatorStatusEntries = useMemo(() => {
    const meta = indicatorMeta;
    const seriesSource = provenanceStats.primaryProvenance;
    return activeIndicators.map((id) => {
      const def = indicatorUiOf(id);
      const label = def?.label ?? id;
      const result = indicatorResults[id];
      if (indicatorError) {
        return { id, label, text: `${label}: indicator series request failed — ${indicatorError}` };
      }
      if (meta?.seriesKind === "unavailable") {
        return {
          id,
          label,
          text: `${label}: series unavailable — ${meta.detail ?? "insufficient M1 coverage"}`,
        };
      }
      if (!result) {
        return { id, label, text: `${label}: loading…` };
      }
      if (result.shape === "insufficient") {
        const detailSuffix = result.detail ? ` · ${result.detail}` : "";
        const structureSuffix =
          indicatorUiOf(id)?.engine === "MarketStructure" ? ` · ${MARKET_STRUCTURE_DISCLOSURE}` : "";
        return {
          id,
          label,
          text: `${label}: insufficient history (${result.required} required, ${result.available} available) — no series rendered${detailSuffix}${structureSuffix}`,
        };
      }
      const aggregatedSuffix =
        meta?.seriesKind === "aggregated"
          ? ` · computed over aggregated ${meta.timeframe} series${
              (meta.excludedPartialBuckets ?? 0) > 0
                ? ` (${meta.excludedPartialBuckets} partial bucket(s) excluded)`
                : ""
            }`
          : ` · computed over native ${meta?.timeframe ?? backendCode} series`;
      const structureSuffix =
        indicatorUiOf(id)?.engine === "MarketStructure" ? ` · ${MARKET_STRUCTURE_DISCLOSURE}` : "";
      return {
        id,
        label,
        text: `${label}: computed server-side${aggregatedSuffix} · derived from ${
          seriesSource === "none" ? "the displayed OHLC series" : seriesSource
        } OHLC${structureSuffix}`,
      };
    });
  }, [activeIndicators, indicatorResults, indicatorMeta, indicatorError, provenanceStats.primaryProvenance, backendCode]);

  // CHART-P03 M3/M4 — annotation surfacing, honestly split by anchor class:
  //  - content.geometry (kind + handles)        -> chart drawings at their
  //    (price, time) anchors (new notes AND drawings).
  //  - content.price_level without geometry     -> a horizontal price line,
  //    marked legacy "price-anchored, time unknown" (the price is real data;
  //    the time is not invented).
  //  - content.visual.x_percent/y_percent or
  //    neither                                  -> the legacy list: off-chart,
  //    clearly unanchored. NO fabricated anchor.
  const drawingsOnChart = useMemo<ChartDrawing[]>(() => {
    const out: ChartDrawing[] = [];
    const lastBar = historicalBars.length > 0 ? historicalBars[historicalBars.length - 1] : null;
    for (const ann of annotations) {
      const content = ann.content as {
        geometry?: DrawingGeometry;
        price_level?: unknown;
        note?: unknown;
        text?: unknown;
        visual?: { x_percent?: unknown; y_percent?: unknown };
      };
      if (content.geometry && Array.isArray(content.geometry.handles)) {
        const handles = content.geometry.handles
          .filter((h) => typeof h.price === "number" && typeof h.time_iso === "string")
          .map((h) => ({
            price: h.price,
            time: Math.floor(Date.parse(h.time_iso) / 1000),
          }));
        if (handles.length > 0) {
          out.push({
            id: ann.id,
            kind: content.geometry.kind,
            handles,
            label: content.geometry.label,
          });
        }
        continue;
      }
      if (content.price_level != null && lastBar) {
        // Price-only legacy note: horizontal line at the real price.
        out.push({
          id: ann.id,
          kind: "hline",
          handles: [{ price: Number(content.price_level), time: lastBar.time }],
          label: `price-anchored note (time unknown)`,
          legacy: true,
        });
      }
    }
    return out;
  }, [annotations, historicalBars]);

  const legacyUnanchoredNotes = useMemo(() => {
    const out: Array<{ id: string; text: string }> = [];
    for (const ann of annotations) {
      const content = ann.content as {
        geometry?: unknown;
        price_level?: unknown;
        note?: unknown;
        text?: unknown;
        drawing_kind?: unknown;
        visual?: unknown;
      };
      if (content.geometry || content.price_level != null) continue;
      const text = (content.note ?? content.text ?? content.drawing_kind ?? "research note") as string;
      out.push({ id: ann.id, text });
    }
    return out;
  }, [annotations]);

  // CHART-P03 M6: drawings persist through the existing audited annotation
  // contract — geometry travels in content; never a parallel path.
  const persistDrawing = async (
    kind: DrawingToolId,
    handles: Array<{ price: number; time: number }>,
    label?: string,
  ) => {
    setDrawingError(null);
    if (label) {
      const rejected = drawingLabelRejection(label);
      if (rejected) {
        setDrawingError(`Forbidden actuation term '${rejected}' in drawing label.`);
        return;
      }
    }
    try {
      const created = await createChartResearchAnnotation({
        artifact_type: "chart_research_drawing",
        // CHART-P03 fix (disclosed): the symbol must be the SAME key the
        // list endpoint filters on (symbolKey, no slash) — drawings saved
        // with the display symbol ("EUR/USD") never matched the fetch and
        // vanished on reload.
        chart_context: {
          symbol: symbolKey,
          timeframe,
          resolution:
            seriesKind === "aggregated" ? "aggregated" : seriesKind === "native" ? "native" : "unavailable",
        },
        content: {
          geometry: {
            kind,
            handles: handles.map((h) => ({
              price: h.price,
              time_iso: new Date(h.time * 1000).toISOString(),
            })),
            label,
          },
        },
        // The annotation contract requires >= 1 source artifact; the chart
        // context itself is the honest source for an operator-authored
        // drawing (the same convention ChartWorkspaceSurface uses).
        source_artifact_ids: [`chart-context:${symbolKey}:${timeframe}`],
        research_status: "research_only",
      });
      setAnnotations((prev) => [created, ...prev]);
    } catch (err) {
      setDrawingError(err instanceof Error ? err.message : "Failed to persist drawing");
    }
  };

  const handleDrawingHandlesChanged = async (id: string, handles: ChartDrawing["handles"]) => {
    const ann = annotations.find((a) => a.id === id);
    if (!ann) return;
    const content = ann.content as { geometry?: DrawingGeometry };
    if (!content.geometry) return;
    const nextGeometry: DrawingGeometry = {
      ...content.geometry,
      handles: handles.map((h) => ({
        price: h.price,
        time_iso: new Date(h.time * 1000).toISOString(),
      })),
    };
    setAnnotations((prev) =>
      prev.map((a) => (a.id === id ? { ...a, content: { ...a.content, geometry: nextGeometry } } : a)),
    );
    try {
      await updateChartResearchAnnotation({ annotationId: id, content: { geometry: nextGeometry } });
    } catch (err) {
      setDrawingError(err instanceof Error ? err.message : "Failed to update drawing");
    }
  };

  const handleDeleteDrawing = async () => {
    if (!selectedDrawingId) return;
    const id = selectedDrawingId;
    setSelectedDrawingId(null);
    setAnnotations((prev) => prev.filter((a) => a.id !== id));
    try {
      await deleteChartResearchAnnotation(id);
    } catch (err) {
      setDrawingError(err instanceof Error ? err.message : "Failed to delete drawing");
    }
  };

  // CHART-P03 S1 — placement: the chart click is converted to (price, time)
  // via the PriceChart coordinate bridge; the second anchor completes a
  // two-handle drawing. A pending anchor is visibly stated, never hidden.
  // NOTE: lightweight-charts consumes bubble-phase clicks on its canvases,
  // so the placement listener is attached in the CAPTURE phase — it runs
  // before the library's handlers and is never blocked by them.
  const drawingToolRef = useRef<DrawingToolId | null>(null);
  const pendingAnchorRef = useRef<{ price: number; time: number } | null>(null);
  drawingToolRef.current = drawingTool;
  pendingAnchorRef.current = pendingAnchor;

  const placeAnchor = (clientX: number, clientY: number) => {
    const toolId = drawingToolRef.current;
    if (!toolId) return;
    const api = coordinateApiRef.current;
    const containerEl = canvasContainerRef.current;
    if (!api || !containerEl) return;
    const rect = containerEl.getBoundingClientRect();
    const x = clientX - rect.left;
    const y = clientY - rect.top;
    const price = api.coordinateToPrice(y);
    const time = api.coordinateToTime(x);
    const tool = drawingToolOf(toolId);
    if (!tool) return;
    if (tool.id === "text") {
      setAnnotationPrice(String(price));
      setDrawingTool(null);
      setPendingAnchor(null);
      setIsAnnotationModalOpen(true);
      return;
    }
    if (tool.handles === 1) {
      void persistDrawing(tool.id, [{ price, time }]);
      setDrawingTool(null);
      setPendingAnchor(null);
      return;
    }
    const first = pendingAnchorRef.current;
    if (!first) {
      setPendingAnchor({ price, time });
      return;
    }
    void persistDrawing(tool.id, [first, { price, time }]);
    setPendingAnchor(null);
    setDrawingTool(null);
  };

  useEffect(() => {
    const el = canvasContainerRef.current;
    if (!el) return;
    const listener = (e: MouseEvent) => placeAnchor(e.clientX, e.clientY);
    // Capture phase: fires before lightweight-charts' own handlers.
    el.addEventListener("click", listener, true);
    return () => el.removeEventListener("click", listener, true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Handle research annotation save (B-P03-4)
  const handleSaveAnnotation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!annotationText.trim()) return;

    // Strict T-1 Guardrail: Reject execution / order fields
    const forbiddenOrderMarkers = ["entry", "stop_loss", "take_profit", "position_size", "lot", "order"];
    for (const marker of forbiddenOrderMarkers) {
      if (annotationText.toLowerCase().includes(marker)) {
        setAnnotationError(`Forbidden actuation term '${marker}' in research annotation.`);
        return;
      }
    }

    setIsSavingAnnotation(true);
    setAnnotationError(null);
    try {
      // DATA-P02 M5: resolution reflects what ACTUALLY happened — the series
      // discriminant, never a hardcoded non-1m ⇒ "resampled" inference.
      const resolution =
        seriesKind === "aggregated" ? "aggregated" : seriesKind === "native" ? "native" : "unavailable";
      // CHART-P03 M1/M3: every NEW note is anchored (price, time). The price
      // is the operator's explicit level or the last visible bar's close; the
      // time is the last visible bar — the note is created against the
      // current display, so both anchors are real, not invented.
      const lastBar = historicalBars.length > 0 ? historicalBars[historicalBars.length - 1] : null;
      const anchorPrice = annotationPrice ? Number(annotationPrice) : lastBar ? lastBar.close : null;
      const created = await createChartResearchAnnotation({
        artifact_type: "chart_research_annotation",
        // Same CHART-P03 fix: symbolKey, matching the list-endpoint filter.
        chart_context: {
          symbol: symbolKey,
          timeframe,
          resolution,
        },
        content: {
          note: annotationText.trim(),
          price_level: annotationPrice ? Number(annotationPrice) : null,
          created_at: new Date().toISOString(),
          geometry: {
            kind: "text",
            handles: [
              {
                price: anchorPrice,
                time_iso: new Date((lastBar ? lastBar.time : Date.now() / 1000) * 1000).toISOString(),
              },
            ],
            label: annotationText.trim().slice(0, 60),
          },
        },
        // CHART-P03 fix (disclosed): the previous source_artifact_ids: [] was
        // rejected by the contract (min 1 item) — notes saved from the stage
        // were 422-ing. The chart context is the honest source.
        source_artifact_ids: [`chart-context:${symbolKey}:${timeframe}`],
        research_status: "research_only",
      });
      setAnnotations((prev) => [created, ...prev]);
      setAnnotationText("");
      setAnnotationPrice("");
      setIsAnnotationModalOpen(false);
    } catch (err) {
      setAnnotationError(err instanceof Error ? err.message : "Failed to save research annotation");
    } finally {
      setIsSavingAnnotation(false);
    }
  };

  // Handle seed synthetic history (B-P03-5)
  const handleSeedHistory = async () => {
    setIsSeeding(true);
    setSeedNotice(null);
    try {
      await seedChartHistory();
      setSeedNotice("Seeded 80 synthetic historical bars. Marked as seed:synthetic.");
      // Trigger reload of candles through the typed series endpoint.
      const refreshed = await fetchCandles({
        symbol: symbolKey,
        timeframe: backendCode,
        limit: 100,
        order: "asc",
      });
      setSeries(refreshed);
    } catch (err) {
      setSeedNotice(err instanceof Error ? err.message : "Seeding request failed");
    } finally {
      setIsSeeding(false);
    }
  };

  return (
    <div
      className={`terminal-chart-stage ${className}`}
      data-testid="terminal-chart-stage"
      role="region"
      aria-label="Primary Candlestick Chart Stage"
    >
      {/* Top Chart Toolbar */}
      <div className="chart-toolbar" data-testid="chart-toolbar">
        {/* Left: Active Instrument & Timeframes */}
        <div className="chart-toolbar-left">
          <span className="chart-active-symbol-badge" data-testid="chart-symbol-badge">
            {selectedSymbol}
          </span>

          {/* Timeframe Controls (B-P03-2) */}
          <div className="chart-timeframe-group" role="group" aria-label="Timeframe Selection">
            {(["1m", "5m", "15m", "1h", "4h", "1d"] as const).map((tf) => (
              <button
                key={tf}
                type="button"
                className={`chart-tf-btn ${timeframe === tf ? "active" : ""}`}
                onClick={() => setTimeframe(tf)}
                data-testid={`chart-tf-${tf}`}
              >
                {tf.toUpperCase()}
              </button>
            ))}
          </div>

          {/* Chart Style Toggles */}
          <div className="chart-style-group" role="group" aria-label="Chart Style Selection">
            {(["candlestick", "bar", "line", "area"] as const).map((st) => (
              <button
                key={st}
                type="button"
                className={`chart-style-btn ${chartType === st ? "active" : ""}`}
                onClick={() => setChartType(st)}
                data-testid={`chart-style-${st}`}
              >
                {st.charAt(0).toUpperCase() + st.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Center: Technical Indicators — CHART-P02 M5 toolbar scaling.
            The three most-used indicators stay direct pills (no more
            interactions than today); every other registry indicator is one
            engine-menu open away, and ACTIVE indicators from the menus
            surface as pills in the tray below — visible at a glance without
            opening a menu. */}
        <div className="chart-toolbar-center">
          <div className="chart-overlays-group" role="group" aria-label="Technical Indicators">
            {INDICATOR_UI.filter((def) => DIRECT_PILL_IDS.includes(def.id as never)).map((def) => (
              <button
                key={def.id}
                type="button"
                className={`chart-overlay-pill ${activeIndicators.includes(def.id) ? "active" : ""}`}
                onClick={() => toggleIndicator(def.id)}
                aria-pressed={activeIndicators.includes(def.id)}
                data-testid={def.testid}
                title={`${def.label} — computed server-side from the displayed series; descriptive, never prescriptive`}
              >
                {def.label}
              </button>
            ))}
            {ENGINES.map((engine) => (
              <div className="indicator-engine-menu" key={engine}>
                <button
                  type="button"
                  className={`engine-menu-button ${openEngineMenu === engine ? "open" : ""}`}
                  onClick={() => setOpenEngineMenu(openEngineMenu === engine ? null : engine)}
                  aria-haspopup="menu"
                  aria-expanded={openEngineMenu === engine}
                  data-testid={`engine-menu-button-${engine.toLowerCase()}`}
                >
                  {engine} ▾
                </button>
                {openEngineMenu === engine ? (
                  <div
                    className="engine-menu-popover"
                    role="menu"
                    data-testid={`engine-menu-${engine.toLowerCase()}`}
                  >
                    {INDICATOR_UI.filter((def) => def.engine === engine).map((def) => (
                      <button
                        key={def.id}
                        type="button"
                        role="menuitem"
                        className={`engine-menu-item ${activeIndicators.includes(def.id) ? "active" : ""}`}
                        onClick={() => {
                          toggleIndicator(def.id);
                          setOpenEngineMenu(null);
                        }}
                        data-testid={`indicator-item-${def.id}`}
                      >
                        {def.label}
                        <span className="engine-menu-pane-tag mono">{def.pane}</span>
                      </button>
                    ))}
                  </div>
                ) : null}
              </div>
            ))}
          </div>
        </div>

        {/* CHART-P02 M5: the active tray — every active indicator visible at a
            glance without opening a menu (click to toggle off). */}
        {activeIndicators.filter((id) => !DIRECT_PILL_IDS.includes(id as never)).length > 0 ? (
          <div className="chart-active-indicator-tray" data-testid="chart-active-indicator-tray">
            {activeIndicators
              .filter((id) => !DIRECT_PILL_IDS.includes(id as never))
              .map((id) => (
                <button
                  key={id}
                  type="button"
                  className="active-tray-pill"
                  onClick={() => toggleIndicator(id)}
                  data-testid={`active-tray-${id}`}
                  title={`${indicatorUiOf(id)?.label ?? id} active — click to remove`}
                >
                  {indicatorUiOf(id)?.label ?? id} ✕
                </button>
              ))}
          </div>
        ) : null}

        {/* CHART-P03 drawing tools (M5): visible tool state; drawings are
            inert research artifacts — geometry only, never trade semantics. */}
        <div className="chart-drawing-tools" role="group" aria-label="Drawing Tools">
          {DRAWING_TOOLS.map((tool) => (
            <button
              key={tool.id}
              type="button"
              className={`chart-drawing-tool-btn ${drawingTool === tool.id ? "active" : ""}`}
              onClick={() => {
                setDrawingTool(drawingTool === tool.id ? null : tool.id);
                setPendingAnchor(null);
              }}
              aria-pressed={drawingTool === tool.id}
              data-testid={`drawing-tool-${tool.id}`}
              title={`${tool.label} — ${tool.description}`}
            >
              {tool.label}
            </button>
          ))}
          {selectedDrawingId ? (
            <button
              type="button"
              className="chart-drawing-tool-btn delete"
              onClick={() => void handleDeleteDrawing()}
              data-testid="drawing-delete-btn"
              title="Remove the selected drawing (audited deletion)"
            >
              Delete
            </button>
          ) : null}
        </div>

        {/* Right: Research Annotations, Seed & Feed Controls */}
        <div className="chart-toolbar-right">
          <button
            type="button"
            className="chart-action-btn note-btn"
            onClick={() => setIsAnnotationModalOpen(true)}
            data-testid="chart-add-annotation-btn"
            title={
              legacyUnanchoredNotes.length > 0
                ? `${annotations.length} total · ${legacyUnanchoredNotes.length} unanchored legacy notes listed below the chart`
                : `${annotations.length} anchored notes and drawings`
            }
          >
            + Note ({annotations.length})
          </button>

          <button
            type="button"
            className="chart-action-btn seed-btn"
            onClick={handleSeedHistory}
            disabled={isSeeding}
            data-testid="chart-seed-btn"
            title="Inject 80 synthetic OHLC bars into database (seed:synthetic)"
          >
            {isSeeding ? "Seeding…" : "Seed (Synthetic)"}
          </button>

          <button
            type="button"
            className={`chart-action-btn feed-btn ${liveMarket.feedStats?.running ? "running" : ""}`}
            onClick={() =>
              liveMarket.feedStats?.running ? void liveMarket.stopFeed() : void liveMarket.startFeed()
            }
            data-testid="chart-feed-toggle-btn"
          >
            {liveMarket.feedStats?.running ? "Stop Feed" : "Start Feed"}
          </button>
        </div>
      </div>

      {/* Timeframe Honesty & Provenance Status Banner (B-P03-2 / B-P03-5 / TD-029).
          DATA-P02 M5: the notice renders from the SERVER discriminant. */}
      <div className="chart-provenance-bar" data-testid="chart-provenance-bar">
        <div className="provenance-item">
          <span className="provenance-lbl">Timeframe:</span>
          <span className="provenance-val mono">{backendCode}</span>
          {series === null ? null : seriesKind === "native" ? (
            <span className="native-tag" data-testid="timeframe-native-notice">
              Native M1 Stream
            </span>
          ) : seriesKind === "aggregated" ? (
            <span className="resampled-tag" data-testid="timeframe-resampled-notice">
              Resampled from M1 stream · wall-clock aligned {backendMinutes}-minute buckets
              {excludedPartialBuckets > 0
                ? ` · ${excludedPartialBuckets} partial bucket(s) excluded`
                : ""}
            </span>
          ) : (
            <span className="unavailable-tag" data-testid="timeframe-unavailable-tag">
              No {backendCode} series — insufficient coverage
            </span>
          )}
        </div>

        <div className="provenance-item">
          <span className="provenance-lbl">Provenance:</span>
          <span
            className={`provenance-badge ${provenanceStats.provenanceClass}`}
            data-testid="chart-provenance-badge"
          >
            {provenanceStats.primaryProvenance}
          </span>
          <span className="provenance-breakdown mono">
            ({provenanceStats.liveCount} live · {provenanceStats.seedCount} seed)
          </span>
        </div>

        {seedNotice ? (
          <div className="seed-alert-toast" data-testid="seed-alert-toast">
            {seedNotice}
          </div>
        ) : null}
      </div>

      {/* CHART-P03 — drawing placement status: always visible when a tool is
          armed, an anchor is pending, or a drawing error occurred. */}
      {drawingTool || pendingAnchor || drawingError ? (
        <div className="drawing-status-strip" data-testid="drawing-status-strip" role="status">
          {drawingTool ? (
            <span className="drawing-tool-active mono" data-testid="drawing-tool-active">
              tool: {drawingToolOf(drawingTool)?.label ?? drawingTool}
            </span>
          ) : null}
          {pendingAnchor && drawingTool ? (
            <span className="drawing-pending-anchor mono" data-testid="drawing-pending-anchor">
              first anchor set at {pendingAnchor.price.toFixed(5)} — click the second point
            </span>
          ) : null}
          {drawingError ? (
            <span className="drawing-error mono" data-testid="drawing-error">
              {drawingError}
            </span>
          ) : null}
        </div>
      ) : null}

      {/* DATA-P02 M7 — session context strip (presentation over existing data) */}
      <SessionContextStrip bars={chartBars} hoveredBar={hoveredBar} />

      {/* CHART-P01 M4/M5/M6 — indicator status strip: every active indicator
          discloses what it is derived from and what series it ran over.
          Insufficient history is stated with required/available counts and
          NO series is rendered. */}
      {activeIndicators.length > 0 ? (
        <div className="chart-indicator-status" data-testid="chart-indicator-status" role="status">
          {indicatorStatusEntries.map((entry) => (
            <div
              key={entry.id}
              className={`indicator-status-entry ${
                indicatorResults[entry.id]?.shape === "insufficient" || indicatorMeta?.seriesKind === "unavailable"
                  ? "insufficient"
                  : ""
              }`}
              data-testid={`indicator-status-${entry.id.toLowerCase()}`}
            >
              <span className="indicator-status-dot mono">◆</span>
              <span className="indicator-status-text mono">{entry.text}</span>
            </div>
          ))}
          {paneBudgetRefusal ? (
            <div className="pane-budget-refusal mono" data-testid="pane-budget-refusal">
              {paneBudgetRefusal}
            </div>
          ) : null}
          <div className="indicator-status-anchor mono" data-testid="indicator-status-anchor">
            Indicators describe data, they never advise a trade.
          </div>
          {activePaneCount > 0 ? (
            <div className="pane-budget-meta mono" data-testid="pane-budget-meta">
              pane budget: <span data-testid="pane-budget-indicator">{activePaneCount}</span>/
              {MAX_PANE_INDICATORS} (policy: price pane keeps a 280px minimum)
            </div>
          ) : null}
        </div>
      ) : null}

      {/* Signal Overlay Markers Banner (P04) */}
      {chartSignals.length > 0 ? (
        <div className="chart-signals-overlay-bar" data-testid="chart-signals-overlay-bar">
          <span className="overlay-bar-lbl mono">ADVISORY SIGNALS:</span>
          {chartSignals.slice(0, 3).map((sig) => {
            const isLong = sig.signal_direction.toUpperCase().includes("LONG") || sig.signal_direction.toUpperCase().includes("BUY") || sig.signal_direction.toUpperCase().includes("POSITIVE");
            const isShort = sig.signal_direction.toUpperCase().includes("SHORT") || sig.signal_direction.toUpperCase().includes("SELL") || sig.signal_direction.toUpperCase().includes("NEGATIVE");
            const conf = sig.calibrated_confidence != null ? `${(sig.calibrated_confidence * 100).toFixed(1)}%` : "Uncalibrated";
            return (
              <div
                key={sig.signal_id}
                className={`chart-signal-chip ${isLong ? "positive" : isShort ? "negative" : "neutral"} mono`}
                data-testid={`chart-signal-marker-${sig.signal_id}`}
                title={`Model: ${sig.model_artifact_id} v${sig.model_version} · State: ${sig.signal_state}`}
              >
                <span className="chip-dir">{isLong ? "▲ POSITIVE" : isShort ? "▼ NEGATIVE" : "◆ NEUTRAL"}</span>
                <span className="chip-conf">({conf})</span>
              </div>
            );
          })}
        </div>
      ) : null}

      {/* Main Chart Canvas Area */}
      <div
        ref={canvasContainerRef}
        className={`chart-canvas-container ${drawingTool ? "drawing-active" : ""}`}
        data-testid="chart-canvas-container"
        data-active-overlay-lines={overlayLines.length}
        data-active-indicator-panes={paneEntries.length}
        data-drawings-count={drawingsOnChart.length}
        data-drawings-json={JSON.stringify(drawingsOnChart.map((d) => ({ id: d.id, kind: d.kind, handles: d.handles })))}
        data-annotations-count={annotations.length}
        data-active-indicator-ids={activeIndicators.join(",")}
        data-price-range-from={visibleRange ? String(visibleRange.from) : ""}
        data-price-range-to={visibleRange ? String(visibleRange.to) : ""}
      >
        {isLoadingCandles && chartBars.length === 0 ? (
          <div className="chart-state-msg loading" data-testid="chart-loading-state">
            <span className="msg-text">Loading historical candle series…</span>
          </div>
        ) : seriesKind === "unavailable" ? (
          <div className="chart-state-msg empty" data-testid="timeframe-unavailable-state">
            <span className="empty-icon">∅</span>
            <span className="msg-title">
              No {backendCode} Series for {selectedSymbol}
            </span>
            <p className="msg-desc">
              {candleError ?? seriesDetail ?? "insufficient M1 coverage"}. The chart renders
              absence, not an improvised series. Click <strong>Seed (Synthetic)</strong> to inject
              history or <strong>Start Feed</strong> to stream simulated M1 ticks.
            </p>
          </div>
        ) : chartBars.length === 0 ? (
          <div className="chart-state-msg empty" data-testid="chart-empty-state">
            <span className="empty-icon">⌁</span>
            <span className="msg-title">No Candle Data for {selectedSymbol}</span>
            <p className="msg-desc">
              Series is empty for active timeframe ({timeframe}). Click <strong>Seed (Synthetic)</strong> to
              inject 80 historical bars or <strong>Start Feed</strong> to begin live simulated streaming.
            </p>
          </div>
        ) : (
          <PriceChart
            bars={chartBars}
            chartType={chartType}
            symbol={selectedSymbol}
            height={480}
            onBarHover={setHoveredBar}
            overlayLines={overlayLines}
            onVisibleTimeRangeChange={setVisibleRange}
            drawings={drawingsOnChart}
            selectedDrawingId={selectedDrawingId}
            onDrawingSelect={setSelectedDrawingId}
            onDrawingHandlesChanged={(id, handles) => void handleDrawingHandlesChanged(id, handles)}
            onCoordinateApiReady={(api) => {
              coordinateApiRef.current = api;
            }}
          />
        )}
      </div>

      {/* POLISH-P01 M5 — evidence confluence: a score with an uncertainty
          band, NON-ACTUATING, over simulated data. No verdict. */}
      <ConfluenceStrip
        indicatorResults={indicatorResults}
        closeSeries={chartBars.map((b) => b.close)}
      />

      {/* CHART-P01 S2 — separate-pane indicators (RSI/MACD/ATR): their own
          charts, so the price pane's scale is never distorted. */}
      {paneEntries.length > 0 ? (
        <div className="chart-indicator-pane-region" data-testid="chart-indicator-pane-region">
          {paneEntries.map(({ id, def, result }) => (
            <IndicatorPane
              key={id}
              testid={`indicator-pane-${id.toLowerCase()}`}
              label={def.label}
              series={result}
              height={90}
              visibleRange={visibleRange}
            />
          ))}
        </div>
      ) : null}

      {/* CHART-P03 M4 — legacy unanchored annotations: listed off-chart,
          honestly labelled; never given a fabricated chart position. */}
      {legacyUnanchoredNotes.length > 0 ? (
        <div className="legacy-annotation-list" data-testid="legacy-annotation-list" role="list">
          <span className="legacy-annotation-heading mono">
            LEGACY NOTES — UNANCHORED ({legacyUnanchoredNotes.length}): saved before
            price/time anchoring; their chart position is unknown and is not invented.
          </span>
          {legacyUnanchoredNotes.map((note) => (
            <span key={note.id} className="legacy-annotation-item mono" data-testid={`legacy-note-${note.id}`}>
              · {note.text}
            </span>
          ))}
        </div>
      ) : null}

      {/* Research Annotations Modal / Drawer (B-P03-4 / GA-050) */}
      {isAnnotationModalOpen ? (
        <div className="annotation-dialog-overlay" data-testid="annotation-dialog-overlay">
          <div
            className="annotation-dialog"
            role="dialog"
            aria-label="Create Research Annotation"
            data-testid="annotation-dialog"
          >
            <div className="annotation-dialog-header">
              <span className="dialog-title">CHART RESEARCH ANNOTATION</span>
              <button
                type="button"
                className="dialog-close-btn"
                onClick={() => setIsAnnotationModalOpen(false)}
                aria-label="Close dialog"
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSaveAnnotation} className="annotation-form">
              <div className="form-group">
                <label htmlFor="annotation-text-input">Research Note / Technical Rationale:</label>
                <textarea
                  id="annotation-text-input"
                  className="annotation-textarea"
                  placeholder="Enter research markup or price level context (e.g. Major resistance level at 1.0850)..."
                  value={annotationText}
                  onChange={(e) => setAnnotationText(e.target.value)}
                  required
                  data-testid="annotation-text-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="annotation-price-input">Target Price Level (Optional):</label>
                <input
                  id="annotation-price-input"
                  type="text"
                  className="annotation-price-input mono"
                  placeholder="1.08500"
                  value={annotationPrice}
                  onChange={(e) => setAnnotationPrice(e.target.value)}
                  data-testid="annotation-price-input"
                />
              </div>

              {annotationError ? (
                <div className="annotation-error-banner" data-testid="annotation-error-banner">
                  {annotationError}
                </div>
              ) : null}

              <div className="annotation-dialog-footer">
                <span className="annotation-disclaimer">
                  Inert research markup only. No execution or trade triggers.
                </span>
                <div className="dialog-actions">
                  <button
                    type="button"
                    className="btn secondary"
                    onClick={() => setIsAnnotationModalOpen(false)}
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="btn primary"
                    disabled={isSavingAnnotation || !annotationText.trim()}
                    data-testid="annotation-save-btn"
                  >
                    {isSavingAnnotation ? "Saving…" : "Save Annotation"}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      ) : null}
    </div>
  );
}
