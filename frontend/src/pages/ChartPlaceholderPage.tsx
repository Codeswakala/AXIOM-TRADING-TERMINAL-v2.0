export function ChartPlaceholderPage() {
  return (
    <>
      <div className="page-header">
        <div>
          <h1>Chart Workspace</h1>
          <p className="muted">
            Reserved for TradingView Lightweight Charts integration (Wave 1+). This panel
            establishes layout placement only — no charting or market data in W0-U01.
          </p>
        </div>
      </div>

      <div className="panel-grid">
        <section className="panel span-12">
          <h2>Chart Surface (Placeholder)</h2>
          <div className="placeholder-chart" role="img" aria-label="Chart workspace placeholder">
            <div>
              <div style={{ fontWeight: 600, color: "var(--text-primary)" }}>
                TradingView Workspace — Not Initialized
              </div>
              <div style={{ marginTop: "0.5rem" }}>
                Future: multi-timeframe charts, AI overlays, operator drawings
              </div>
            </div>
          </div>
        </section>
      </div>
    </>
  );
}
