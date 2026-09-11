import type { SymbolQuote } from "../../live/types";

type Props = {
  quotes: Record<string, SymbolQuote>;
  expectedSymbols?: string[];
};

function formatPrice(value: string, symbol: string): string {
  const n = Number(value);
  if (Number.isNaN(n)) return value;
  if (symbol.includes("BTC") || symbol.includes("ETH") || symbol.includes("XAU")) {
    return n.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  return n.toLocaleString(undefined, { minimumFractionDigits: 5, maximumFractionDigits: 5 });
}

export function LivePriceTable({ quotes, expectedSymbols = [] }: Props) {
  const symbols = Array.from(
    new Set([...expectedSymbols, ...Object.keys(quotes)]),
  ).sort();

  if (symbols.length === 0) {
    return (
      <section className="panel span-12">
        <h2>Live Prices</h2>
        <p className="muted">
          No live quotes yet. Start the feed and ensure the WebSocket is connected.
        </p>
      </section>
    );
  }

  return (
    <section className="panel span-12">
      <h2>Live Prices</h2>
      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Class</th>
              <th>TF</th>
              <th>Open</th>
              <th>High</th>
              <th>Low</th>
              <th>Last</th>
              <th>Volume</th>
              <th>Bar time</th>
              <th>Updated</th>
            </tr>
          </thead>
          <tbody>
            {symbols.map((symbol) => {
              const q = quotes[symbol];
              if (!q) {
                return (
                  <tr key={symbol}>
                    <td className="mono">{symbol}</td>
                    <td colSpan={9} className="muted">
                      Waiting for tick…
                    </td>
                  </tr>
                );
              }
              const flashClass =
                q.flash === "up" ? "flash-up" : q.flash === "down" ? "flash-down" : "";
              return (
                <tr key={symbol} className={flashClass}>
                  <td className="mono">{q.symbol}</td>
                  <td>{q.marketClass}</td>
                  <td className="mono">{q.timeframe}</td>
                  <td className="mono num">{formatPrice(q.open, q.symbol)}</td>
                  <td className="mono num">{formatPrice(q.high, q.symbol)}</td>
                  <td className="mono num">{formatPrice(q.low, q.symbol)}</td>
                  <td className={`mono num last-price ${flashClass}`}>
                    {formatPrice(q.close, q.symbol)}
                  </td>
                  <td className="mono num">{q.volume ?? "—"}</td>
                  <td className="mono muted">{q.openTime}</td>
                  <td className="mono muted">{q.updatedAt}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}
