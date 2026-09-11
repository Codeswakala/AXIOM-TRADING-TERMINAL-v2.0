"""V2 BE-3 P2 network transport — BO-V2-BE-3-P2-001 §3.2.

Single contract-test ``NetworkTransport``:
- exact fixed allowlisted host ``api.twelvedata.com``;
- HTTPS + certificate verification only (no insecure switch exists);
- fixed 5s connect / 15s read timeouts;
- no caller-supplied URL/host, no off-host redirects, no WebSocket/streaming;
- constructible ONLY through the authenticated contract-test endpoint
  dependency chain (enforced by a construction token + import-boundary test);
- the P1 socket guard remains active for every non-P2 test.

The HTTP client library is imported lazily INSIDE the execute method so the
P1 static forbidden-import scan of the providers package remains meaningful
for all non-transport modules, and no client object exists at import time.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from app.v2.errors.contract import V2Error, V2ErrorCode
from app.v2.marketdata.providers.contract import ALLOWED_PROVIDER_HOST, PlannedRequest

CONNECT_TIMEOUT_SECONDS: Final[float] = 5.0
READ_TIMEOUT_SECONDS: Final[float] = 15.0

#: Construction token: only the contract-test runner (inside the
#: authenticated endpoint dependency chain) knows this sentinel. Tests assert
#: no other module references it.
_CONSTRUCTION_TOKEN: Final[object] = object()


def construction_token() -> object:
    """Returned only to the runner module (import-boundary enforced)."""
    return _CONSTRUCTION_TOKEN


@dataclass(frozen=True, slots=True)
class TransportResult:
    """Non-payload transport outcome. ``body`` is transient and must be
    discarded by the caller after validation/hashing (never persisted)."""

    status_code: int
    body: bytes  # transient in memory only — hashed then discarded
    latency_ms: float


class NetworkTransport:
    """The ONLY component permitted to perform provider network I/O."""

    kind = "network"

    def __init__(self, token: object) -> None:
        if token is not _CONSTRUCTION_TOKEN:
            from app.core.logging import get_logger

            get_logger(__name__, category="SECURITY").warning(
                "P2 transport boundary refusal: action=transport.unauthorized_construction"
            )
            raise V2Error(
                code=V2ErrorCode.VALIDATION_FAILED,
                detail="Transport construction not authorized",
                status_code=400,
            )

    def execute(self, planned: PlannedRequest, *, apikey: str) -> TransportResult:
        """Execute one allowlisted HTTPS request. Never follows off-host
        redirects; never logs the full URL; body returned transiently."""
        if planned.host != ALLOWED_PROVIDER_HOST:
            raise V2Error(
                code=V2ErrorCode.VALIDATION_FAILED,
                detail="Host not allowlisted",
                status_code=400,
            )
        import time

        import httpx  # lazy: no client exists at import time

        params = dict(planned.params)
        params["apikey"] = apikey  # request-scope only; never logged/persisted
        started = time.monotonic()
        with httpx.Client(
            verify=True,
            follow_redirects=False,
            timeout=httpx.Timeout(
                connect=CONNECT_TIMEOUT_SECONDS,
                read=READ_TIMEOUT_SECONDS,
                write=READ_TIMEOUT_SECONDS,
                pool=CONNECT_TIMEOUT_SECONDS,
            ),
        ) as client:
            response = client.get(
                f"https://{planned.host}{planned.path}", params=params
            )
        latency_ms = (time.monotonic() - started) * 1000.0
        return TransportResult(
            status_code=response.status_code,
            body=response.content,
            latency_ms=latency_ms,
        )
