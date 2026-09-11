"""V2 BE-3 P1 provider contract — fixture-only, credential-free, network-denied.

Constitutional P1 boundary (BO-V2-BE-3-P1-001 §3; plan v3.0.0 A.4a):
- ``P1_NETWORK_ENABLED`` is hard False; the only transport type is
  ``FixtureTransport`` (file-reading, cannot be parameterized with a URL);
- constructing an adapter with any other transport raises a security-logged
  refusal;
- live-entry invocation raises a security-logged refusal;
- the credential resolver ALWAYS reports absent and never reads any
  environment variable;
- the URL builder returns an inert ``PlannedRequest`` nothing can execute.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

from app.v2.errors.contract import V2Error, V2ErrorCode

#: Hard P1 constant. Validated at adapter construction. Never configurable.
P1_NETWORK_ENABLED: Final[bool] = False

#: The only host a future (P2+) request could ever target. P1 builds inert
#: PlannedRequest values only; nothing accepts them for execution.
ALLOWED_PROVIDER_HOST: Final[str] = "api.twelvedata.com"


class CredentialState:
    """Explicit credential states. P1 knows only ABSENT."""

    ABSENT: Final[str] = "absent"


class FixtureCredentialResolver:
    """P1 resolver: always absent; never touches the environment.

    PLAN-005 closure: this class contains no ``os.environ``/``os.getenv``
    access and no reference to any provider-secret variable name. A real
    Operator key can never enter P1 process memory through this path.
    """

    def get(self, provider_id: str) -> str:
        return CredentialState.ABSENT


class FixtureTransport:
    """The only P1 transport: reads workspace-reviewed static fixture files.

    Cannot be parameterized with a URL, host, or request; performs no I/O
    beyond local fixture files under its fixed root.
    """

    def __init__(self, fixtures_root: Path) -> None:
        self._root = Path(fixtures_root)

    @property
    def kind(self) -> str:
        return "fixture"

    def load(self, fixture_name: str) -> dict[str, Any]:
        """Load a named fixture. Name is a bare filename — no path traversal."""
        if "/" in fixture_name or "\\" in fixture_name or ".." in fixture_name:
            raise V2Error(
                code=V2ErrorCode.VALIDATION_FAILED,
                detail="Invalid fixture name",
                status_code=400,
            )
        path = self._root / fixture_name
        if not path.is_file():
            raise V2Error(
                code=V2ErrorCode.DATA_UNAVAILABLE,
                detail="Fixture not available",
                status_code=404,
            )
        return json.loads(path.read_text())


@dataclass(frozen=True, slots=True)
class PlannedRequest:
    """Inert P2-design value object. NOTHING in P1 accepts this for execution.

    Rendered forms always redact the key parameter.
    """

    host: str
    path: str
    params: dict[str, str] = field(default_factory=dict)

    def redacted(self) -> str:
        safe = {k: ("[REDACTED]" if k.lower() == "apikey" else v) for k, v in self.params.items()}
        query = "&".join(f"{k}={v}" for k, v in sorted(safe.items()))
        return f"https://{self.host}{self.path}?{query}"


def plan_request(path: str, params: dict[str, str]) -> PlannedRequest:
    """Build an inert PlannedRequest against the fixed allowlisted host."""
    return PlannedRequest(host=ALLOWED_PROVIDER_HOST, path=path, params=dict(params))


@dataclass(frozen=True, slots=True)
class ProviderDescriptor:
    """Truthful provider self-description."""

    provider_id: str
    display_name: str
    source_status: str  # always "architecture_candidate" in P1
    entitlement_status: str  # always "unverified" in P1
    transport_kind: str  # always "fixture" in P1
    network_enabled: bool  # always False in P1


def _security_logged_refusal(action: str, detail: str) -> V2Error:
    """P1 boundary refusal: SECURITY-log-only accountability model.

    DEL-002 approved rationale: these refusals fire at adapter construction
    or direct live-entry invocation — programmatic contexts with NO
    authenticated actor, session, request, or correlation available (no P1
    API surface reaches these paths; the provider APIs are read-only status
    reads). A V2 audit event requires an actor and a database session,
    neither of which exists here; fabricating a synthetic actor would
    violate the no-fabricated-state invariant. The refusal is therefore
    recorded as a structured SECURITY log line (action name only, no
    sensitive content) plus a safe V2Error. If a future authorized scope
    ever exposes these paths behind an authenticated surface, that scope
    must upgrade the refusal to a full BE-1 audit event as part of its own
    Build Order.
    """
    from app.core.logging import get_logger

    get_logger(__name__, category="SECURITY").warning(
        "P1 provider boundary refusal: action=%s", action
    )
    return V2Error(code=V2ErrorCode.VALIDATION_FAILED, detail=detail, status_code=400)


class ProviderAdapter:
    """Base adapter enforcing the P1 fixture-only boundary."""

    provider_id: str = "unknown"
    display_name: str = "Unknown"

    def __init__(
        self,
        transport: FixtureTransport,
        credentials: FixtureCredentialResolver | None = None,
    ) -> None:
        if P1_NETWORK_ENABLED is not False:  # pragma: no cover — hard invariant
            raise _security_logged_refusal("network_flag", "P1 network flag violated")
        if not isinstance(transport, FixtureTransport):
            raise _security_logged_refusal(
                "provider.network_refused",
                "P1 permits fixture transport only",
            )
        self._transport = transport
        self._credentials = credentials or FixtureCredentialResolver()

    # ------------------------------------------------------------------ #
    # Live entry points exist ONLY as refusal stubs in P1 (plan A.4a §3). #
    # ------------------------------------------------------------------ #

    def fetch_live(self, *_: Any, **__: Any) -> None:
        raise _security_logged_refusal(
            "provider.live_refused", "Live provider access is not authorized in P1"
        )

    def connect(self, *_: Any, **__: Any) -> None:
        raise _security_logged_refusal(
            "provider.live_refused", "Live provider access is not authorized in P1"
        )

    def descriptor(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider_id=self.provider_id,
            display_name=self.display_name,
            source_status="architecture_candidate",
            entitlement_status="unverified",
            transport_kind=self._transport.kind,
            network_enabled=P1_NETWORK_ENABLED,
        )
