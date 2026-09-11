import React from "react";
import "./TerminalMultiPane.css";

export interface TerminalMultiPaneLayoutProps {
  topTicker?: React.ReactNode;
  leftSlot?: React.ReactNode;
  centreSlot?: React.ReactNode;
  rightSlot?: React.ReactNode;
  bottomSlot?: React.ReactNode;
  className?: string;
  /** Accessible name of the centre slot; the research stage re-labels it. */
  centreAriaLabel?: string;
}

export interface TerminalSlotPlaceholderProps {
  title: string;
  phase: string;
  description: string;
}

export function TerminalSlotPlaceholder({
  title,
  phase,
  description,
}: TerminalSlotPlaceholderProps) {
  const testId = `placeholder-${title.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`;
  return (
    <div className="terminal-slot-placeholder" data-testid={testId}>
      <div className="placeholder-header">
        <span className="placeholder-title">{title}</span>
        <span className="placeholder-phase-badge">{phase}</span>
      </div>
      <div className="placeholder-body">
        <span className="placeholder-icon" aria-hidden="true">
          ⌁
        </span>
        <p className="placeholder-desc">{description}</p>
        <span className="placeholder-status-tag">Docked Slot · Scaffold Ready</span>
      </div>
    </div>
  );
}

/**
 * TerminalMultiPaneLayout
 *
 * Full-bleed multi-pane grid container with docked panel slots:
 * - Top Ticker: Persistent live ticker header
 * - Left Dock: Watchlist slot (P02)
 * - Centre Stage: Candlestick chart stage (P03)
 * - Right Dock: Signals & Spread telemetry slot (P02/P04)
 * - Bottom Dock: Risk, Journal & Scenarios analytics drawer (P05)
 *
 * Adheres to:
 * - T-1: Zero actuation controls
 * - T-6: Data honesty
 * - Doc 16 Brand Standards & Pure Token Consumption
 * - SAL-2 (Internal) presentation container
 */
export function TerminalMultiPaneLayout({
  topTicker,
  leftSlot,
  centreSlot,
  rightSlot,
  bottomSlot,
  className = "",
  centreAriaLabel = "Primary Candlestick Chart Stage",
}: TerminalMultiPaneLayoutProps) {
  return (
    <div
      className={`terminal-multipane-layout ${className}`}
      data-testid="terminal-multipane-layout"
    >
      {/* Top Persistent Global Ticker Bar */}
      <header
        className="terminal-ticker-region"
        role="banner"
        aria-label="Global Terminal Ticker Bar"
        data-testid="terminal-ticker-region"
      >
        {topTicker}
      </header>

      {/* Main Multi-Pane Trading Stage (Left, Centre, Right) */}
      <div className="terminal-stage-grid" data-testid="terminal-stage-grid">
        {/* Left Dock: Watchlist & Market Instruments */}
        <aside
          className="terminal-slot terminal-slot-left"
          role="complementary"
          aria-label="Market Watchlist Dock"
          data-testid="terminal-slot-left"
        >
          {leftSlot ?? (
            <TerminalSlotPlaceholder
              title="Market Watchlist"
              phase="P02"
              description="Multi-asset watchlist & quote selection"
            />
          )}
        </aside>

        {/* Centre Stage: Primary Candlestick Chart Stage (re-labelled by the research stage) */}
        <main
          className="terminal-slot terminal-slot-centre"
          role="main"
          aria-label={centreAriaLabel}
          data-testid="terminal-slot-centre"
        >
          {centreSlot ?? (
            <TerminalSlotPlaceholder
              title="Primary Candlestick Chart Stage"
              phase="P03"
              description="TradingView candlestick chart stage & technical analysis workspace"
            />
          )}
        </main>

        {/* Right Dock: Signals & Spread Telemetry */}
        <aside
          className="terminal-slot terminal-slot-right"
          role="complementary"
          aria-label="Signals & Telemetry Dock"
          data-testid="terminal-slot-right"
        >
          {rightSlot ?? (
            <TerminalSlotPlaceholder
              title="Signals & Spread Telemetry"
              phase="P02 / P04"
              description="Advisory ML signals, uncertainty stream & candle-derived spread telemetry"
            />
          )}
        </aside>
      </div>

      {/* Bottom Dock: Trade Plans, Journal, Scenarios & Analytics */}
      <section
        className="terminal-slot terminal-slot-bottom"
        role="region"
        aria-label="Terminal Analytics Dock"
        data-testid="terminal-slot-bottom"
      >
        {bottomSlot ?? (
          <TerminalSlotPlaceholder
            title="Terminal Analytics Dock"
            phase="P05"
            description="Trade planning notes, manual journal reflections & econometric scenarios"
          />
        )}
      </section>
    </div>
  );
}
