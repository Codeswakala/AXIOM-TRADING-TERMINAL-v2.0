"""BO-B-DATA Part B — real historical corpus retrieval (DA tooling, untracked).

Sources (both public, no API key):
  1. OKX history-candles (https://www.okx.com/api/v5/market/history-candles)
     — deep H1 OHLCV pagination, 6 instruments, 2024-08-01 → 2026-08-01 UTC.
  2. Kraken public OHLC (https://api.kraken.com/0/public/OHLC, interval=1440)
     — 2 years of D1 OHLCV, 6 pairs (its H1 window is depth-limited to the
     most recent 720 bars; the daily window spans ~2 years).

Honesty: bars written exactly as returned; unconfirmed OKX candles (confirm
flag != 1) excluded; no gap-filling, no interpolation, no relabeling.
Exchange gaps are real and remain absent.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

START = int(datetime(2024, 8, 1, 0, 0, tzinfo=timezone.utc).timestamp())
END = int(datetime(2026, 8, 1, 0, 0, tzinfo=timezone.utc).timestamp())

OUT_DIR = Path("/home/user/axiom/backend/tests/fixtures/bdata_corpus")

OKX_API = "https://www.okx.com/api/v5/market/history-candles"
KRAKEN_API = "https://api.kraken.com/0/public/OHLC"

OKX_SYMBOLS = ["BTC-USDT", "ETH-USDT", "SOL-USDT", "XRP-USDT", "ADA-USDT", "DOGE-USDT"]
KRAKEN_PAIRS = ["XBTUSD", "ETHUSD", "SOLUSD", "XRPUSD", "ADAUSD", "DOGEUSD"]
KRAKEN_NAMES = ["BTCUSD", "ETHUSD", "SOLUSD", "XRPUSD", "ADAUSD", "DOGEUSD"]


def _get(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (research client; AXIOM B-DATA retrieval)"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


def fetch_okx_h1(inst_id: str) -> list[list]:
    """Deep H1 pagination backwards from END. Rows: [ts_ms, o, h, l, c, vol, ...,
    confirm]; only confirmed candles are kept."""
    rows: dict[int, list] = {}
    after = END * 1000
    attempts = 0
    while True:
        params = urllib.parse.urlencode(
            {"instId": inst_id, "bar": "1H", "limit": "100", "after": str(after)}
        )
        try:
            payload = _get(f"{OKX_API}?{params}")
        except Exception as exc:  # noqa: BLE001
            attempts += 1
            if attempts > 5:
                raise RuntimeError(f"OKX fetch failed for {inst_id}: {exc}") from exc
            time.sleep(2.0 * attempts)
            continue
        if payload.get("code") != "0":
            message = payload.get("msg", "unknown")
            raise RuntimeError(f"OKX error for {inst_id}: {message}")
        data = payload.get("data") or []
        attempts = 0
        if not data:
            break
        earliest = None
        for row in data:
            if row[8] != "1":  # unconfirmed candle — excluded
                continue
            ts = int(row[0]) // 1000
            if ts < START:
                earliest = ts
                continue
            rows[ts] = [ts, row[1], row[2], row[3], row[4], row[5]]
            earliest = ts if earliest is None else min(earliest, ts)
        if earliest is None or earliest <= START * 1000 // 1000:
            break
        after = earliest * 1000 - 1
        time.sleep(0.12)
    return [rows[ts] for ts in sorted(rows) if START <= ts < END]


def fetch_kraken_d1(pair: str) -> list[list]:
    """The Kraken public OHLC daily window (~720 bars ≈ 2 years)."""
    params = urllib.parse.urlencode({"pair": pair, "interval": "1440"})
    payload = _get(f"{KRAKEN_API}?{params}")
    result = payload.get("result") or {}
    key = next(iter(result), None)
    if key is None:
        raise RuntimeError(f"Kraken no result for {pair}: {payload.get('error')}")
    rows = result[key]
    kept: dict[int, list] = {}
    for row in rows:
        ts = int(row[0])
        if START <= ts < END:
            kept[ts] = row
    return [kept[ts] for ts in sorted(kept)]


def write_csv(name: str, rows: list[list], volume_index: int, ts_divisor: int) -> Path:
    out = OUT_DIR / f"{name}.csv"
    with out.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        for row in rows:
            stamp = datetime.fromtimestamp(
                int(row[0]) // ts_divisor, tz=timezone.utc
            ).strftime("%Y-%m-%dT%H:%M:%SZ")
            writer.writerow([stamp, row[1], row[2], row[3], row[4], row[volume_index]])
    return out


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict = {
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "window": {
            "start_utc": datetime.fromtimestamp(START, tz=timezone.utc).isoformat(),
            "end_utc": datetime.fromtimestamp(END, tz=timezone.utc).isoformat(),
        },
        "sources": {
            "okx_h1": {
                "endpoint": OKX_API,
                "instrument_class": "crypto spot, H1 OHLCV, confirmed candles only",
                "license_reference": "OKX public market data; see B-DATA_SOURCE_LICENSE_DECLARATION.md",
            },
            "kraken_d1": {
                "endpoint": KRAKEN_API,
                "instrument_class": "crypto spot, D1 OHLCV",
                "license_reference": "Kraken public market data; see B-DATA_SOURCE_LICENSE_DECLARATION.md",
            },
        },
        "files": {},
    }
    for inst in OKX_SYMBOLS:
        symbol = inst.replace("-", "")
        print(f"[bdata] OKX H1 {inst}…", flush=True)
        rows = fetch_okx_h1(inst)
        path = write_csv(f"okx_{symbol}_H1", rows, volume_index=5, ts_divisor=1)
        digest = sha256(path)
        manifest["files"][path.name] = {
            "source": "okx_h1",
            "instrument": inst,
            "bars": len(rows),
            "first_utc": datetime.fromtimestamp(rows[0][0], tz=timezone.utc).isoformat() if rows else None,
            "last_utc": datetime.fromtimestamp(rows[-1][0], tz=timezone.utc).isoformat() if rows else None,
            "sha256": digest,
        }
        print(f"[bdata]   {len(rows)} bars {path.name} {digest}", flush=True)

    for pair, name in zip(KRAKEN_PAIRS, KRAKEN_NAMES, strict=True):
        print(f"[bdata] Kraken D1 {pair}…", flush=True)
        rows = fetch_kraken_d1(pair)
        path = write_csv(f"kraken_{name}_D1", rows, volume_index=6, ts_divisor=1)
        digest = sha256(path)
        manifest["files"][path.name] = {
            "source": "kraken_d1",
            "instrument": pair,
            "bars": len(rows),
            "first_utc": datetime.fromtimestamp(rows[0][0], tz=timezone.utc).isoformat() if rows else None,
            "last_utc": datetime.fromtimestamp(rows[-1][0], tz=timezone.utc).isoformat() if rows else None,
            "sha256": digest,
        }
        print(f"[bdata]   {len(rows)} bars {path.name} {digest}", flush=True)

    manifest_path = OUT_DIR / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"[bdata] manifest: {manifest_path} sha256={sha256(manifest_path)}")


if __name__ == "__main__":
    main()
