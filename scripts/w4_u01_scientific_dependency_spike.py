#!/usr/bin/env python
"""W4-U01 scientific dependency install/import/smoke reporter.

Run after installing candidate packages in an evidence virtual environment.
Outputs JSON with resolved versions and deterministic smoke-test values.
"""

from __future__ import annotations

import importlib
import json
import platform
import sys
from importlib import metadata
from typing import Any

CANDIDATES = (
    ("numpy", "numpy"),
    ("pandas", "pandas"),
    ("scipy", "scipy"),
)


def smoke(import_name: str, module: Any) -> dict[str, Any]:
    if import_name == "numpy":
        arr = module.array([1.0, 2.0, 3.0])
        return {"mean": float(module.mean(arr)), "shape": list(arr.shape)}
    if import_name == "pandas":
        series = module.Series([1.0, 2.0, 3.0])
        return {"mean": float(series.mean()), "rows": int(series.shape[0])}
    if import_name == "scipy":
        stats = importlib.import_module("scipy.stats")
        corr = stats.pearsonr([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
        statistic = getattr(corr, "statistic", corr[0])
        return {"pearsonr": float(statistic)}
    raise AssertionError(f"unsupported candidate: {import_name}")


def main() -> int:
    results: list[dict[str, Any]] = []
    for package, import_name in CANDIDATES:
        item: dict[str, Any] = {"package": package, "import_name": import_name}
        try:
            module = importlib.import_module(import_name)
            item["version"] = metadata.version(package)
            item["smoke"] = smoke(import_name, module)
            item["status"] = "PASS"
        except Exception as exc:  # noqa: BLE001 - evidence records exact failure
            item["status"] = "FAIL"
            item["error"] = f"{exc.__class__.__name__}: {exc}"
        results.append(item)
    payload = {
        "python_version": sys.version,
        "platform": platform.platform(),
        "results": results,
        "overall_status": "PASS" if all(item["status"] == "PASS" for item in results) else "FAIL",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
