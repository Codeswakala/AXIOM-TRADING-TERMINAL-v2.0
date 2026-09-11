/**
 * CHART-P03 — drawing overlay (M1/M2/S1).
 *
 * Renders persisted drawings as an SVG layer over the chart, converting
 * (price, time) anchors to pixels AT DRAW TIME via the converters passed in
 * (the chart's own timeToCoordinate / priceToCoordinate). Never the reverse:
 * nothing persists pixels.
 *
 * Interaction (S1): click selects; dragging a handle re-anchors it — the new
 * pixel position is converted back to (price, time) and reported upward as
 * data, not coordinates. This component is converter-driven precisely so it
 * is testable in jsdom and provable in the browser.
 */

import { useEffect, useRef, useState } from "react";
import type { ChartDrawing } from "../../api/drawingTools";

export interface CoordinateConverters {
  timeToCoordinate: (time: number) => number;
  priceToCoordinate: (price: number) => number;
  coordinateToTime: (x: number) => number;
  coordinateToPrice: (y: number) => number;
}

export interface ChartDrawingOverlayProps {
  drawings: ChartDrawing[];
  converters: CoordinateConverters | null;
  width: number;
  height: number;
  selectedId: string | null;
  onSelect: (id: string | null) => void;
  onHandlesChanged: (id: string, handles: ChartDrawing["handles"]) => void;
}

const FIB_LEVELS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];

export function ChartDrawingOverlay({
  drawings,
  converters,
  width,
  height,
  selectedId,
  onSelect,
  onHandlesChanged,
}: ChartDrawingOverlayProps) {
  const [drag, setDrag] = useState<{
    drawingId: string;
    handleIndex: number;
  } | null>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const drawingsRef = useRef<ChartDrawing[]>(drawings);
  const onHandlesChangedRef = useRef(onHandlesChanged);
  drawingsRef.current = drawings;
  onHandlesChangedRef.current = onHandlesChanged;

  useEffect(() => {
    if (!drag) return;
    const move = (e: PointerEvent) => {
      const svg = svgRef.current;
      if (!svg || !converters) return;
      const drawing = drawingsRef.current.find((d) => d.id === drag.drawingId);
      if (!drawing) return;
      const rect = svg.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const time = converters.coordinateToTime(x);
      const price = converters.coordinateToPrice(y);
      const next = drawing.handles.map((h, i) => (i === drag.handleIndex ? { price, time } : h));
      onHandlesChangedRef.current(drag.drawingId, next);
    };
    const up = () => setDrag(null);
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
    return () => {
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", up);
    };
  }, [drag, converters]);

  if (!converters) return null;

  const toXy = (handles: ChartDrawing["handles"]) =>
    handles.map((h) => ({
      x: converters.timeToCoordinate(h.time),
      y: converters.priceToCoordinate(h.price),
      price: h.price,
      time: h.time,
    }));

  return (
    <svg
      ref={svgRef}
      className="chart-drawing-overlay"
      data-testid="chart-drawing-overlay"
      width={width}
      height={height}
      style={{ position: "absolute", inset: 0, pointerEvents: "none", zIndex: 5 }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onSelect(null);
      }}
    >
      {drawings.map((d) => {
        const pts = toXy(d.handles);
        const selected = d.id === selectedId;
        const stroke = selected ? "var(--ix-color-electric-blue)" : "var(--ix-color-accent)";
        const common = {
          pointerEvents: "auto" as const,
          cursor: "pointer",
          onClick: (e: React.MouseEvent) => {
            e.stopPropagation();
            onSelect(d.id);
          },
        };
        const handleProps = (handleIndex: number) => ({
          ...common,
          cursor: "move",
          onPointerDown: (e: React.PointerEvent) => {
            e.stopPropagation();
            setDrag({ drawingId: d.id, handleIndex });
          },
        });
        if (d.kind === "hline") {
          const p = pts[0];
          return (
            <g key={d.id} data-testid={`drawing-${d.id}`}>
              <line x1={0} x2={width} y1={p.y} y2={p.y} stroke={stroke} strokeWidth={selected ? 2 : 1.5} {...common} />
              <circle cx={width / 2} cy={p.y} r={4} fill={stroke} data-testid={`drawing-handle-${d.id}-0`} {...handleProps(0)} />
            </g>
          );
        }
        if (d.kind === "ray" || d.kind === "trendline") {
          const a = pts[0];
          const b = pts[1];
          if (!a || !b) return null;
          const extend = d.kind === "ray";
          const dx = b.x - a.x;
          const dy = b.y - a.y;
          const x2 = extend ? (dx >= 0 ? width : 0) : b.x;
          const t = dx !== 0 ? (x2 - a.x) / dx : 0;
          const y2 = a.y + dy * t;
          return (
            <g key={d.id} data-testid={`drawing-${d.id}`}>
              <line x1={a.x} y1={a.y} x2={x2} y2={y2} stroke={stroke} strokeWidth={selected ? 2 : 1.5} {...common} />
              <circle cx={a.x} cy={a.y} r={4} fill={stroke} data-testid={`drawing-handle-${d.id}-0`} {...handleProps(0)} />
              <circle cx={b.x} cy={b.y} r={4} fill={stroke} data-testid={`drawing-handle-${d.id}-1`} {...handleProps(1)} />
            </g>
          );
        }
        if (d.kind === "rect" || d.kind === "fib") {
          const a = pts[0];
          const b = pts[1];
          if (!a || !b) return null;
          const x = Math.min(a.x, b.x);
          const y = Math.min(a.y, b.y);
          const w = Math.abs(b.x - a.x);
          const h = Math.abs(b.y - a.y);
          return (
            <g key={d.id} data-testid={`drawing-${d.id}`}>
              {d.kind === "rect" ? (
                <rect x={x} y={y} width={w} height={h} fill="rgb(37 99 235 / 8%)" stroke={stroke} strokeWidth={selected ? 2 : 1.5} {...common} />
              ) : (
                FIB_LEVELS.map((level) => {
                  const ly = a.y + (b.y - a.y) * level;
                  return (
                    <line
                      key={level}
                      x1={x}
                      x2={x + w}
                      y1={ly}
                      y2={ly}
                      stroke={stroke}
                      strokeWidth={1}
                      strokeDasharray="3 3"
                      {...common}
                      data-testid={`drawing-fib-level-${d.id}-${level}`}
                    />
                  );
                })
              )}
              <circle cx={a.x} cy={a.y} r={4} fill={stroke} data-testid={`drawing-handle-${d.id}-0`} {...handleProps(0)} />
              <circle cx={b.x} cy={b.y} r={4} fill={stroke} data-testid={`drawing-handle-${d.id}-1`} {...handleProps(1)} />
            </g>
          );
        }
        if (d.kind === "text") {
          const p = pts[0];
          return (
            <g key={d.id} data-testid={`drawing-${d.id}`}>
              <circle cx={p.x} cy={p.y} r={5} fill={stroke} {...common} />
              {d.label ? (
                <text x={p.x + 8} y={p.y - 8} fill={stroke} fontSize={11} fontFamily="monospace" {...common}>
                  {d.label}
                </text>
              ) : null}
            </g>
          );
        }
        return null;
      })}
    </svg>
  );
}
