"""Runtime diagnostics that are safe to expose as health metadata."""

from __future__ import annotations

import platform
import time
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Literal, TypeAlias

from starter_kit import __version__

if TYPE_CHECKING:
    from starter_kit.config import Settings

CheckStatus: TypeAlias = Literal["pass", "warn", "fail"]
HealthStatus: TypeAlias = Literal["ok", "degraded", "unhealthy"]


@dataclass(frozen=True, slots=True)
class CheckOutcome:
    """Result returned by a pluggable health check."""

    name: str
    status: CheckStatus = "pass"
    detail: str = "ready"


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Measured health-check outcome included in a report."""

    name: str
    status: CheckStatus
    detail: str
    duration_ms: float


HealthCheck: TypeAlias = Callable[[], CheckOutcome]


@dataclass(frozen=True, slots=True)
class HealthReport:
    """Serializable snapshot of application and runtime health."""

    status: HealthStatus
    app_name: str
    version: str
    environment: str
    build_commit: str
    python_version: str
    platform: str
    timestamp: str
    checks: tuple[CheckResult, ...]

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-ready representation of the report."""
        return asdict(self)


def runtime_check() -> CheckOutcome:
    """Confirm that the Python runtime can execute application code."""
    return CheckOutcome(name="runtime", detail="Python runtime is responsive")


def collect_health(
    settings: Settings,
    *,
    now: datetime | None = None,
    checks: Sequence[HealthCheck] | None = None,
    timer: Callable[[], float] = time.perf_counter,
) -> HealthReport:
    """Collect deterministic application and runtime health metadata."""
    current_time = now or datetime.now(tz=UTC)
    if current_time.tzinfo is None:
        raise ValueError("Health report timestamps must be timezone-aware")

    active_checks = (runtime_check,) if checks is None else tuple(checks)
    results = tuple(_run_check(check, timer=timer) for check in active_checks)
    statuses = {result.status for result in results}
    status: HealthStatus
    if "fail" in statuses:
        status = "unhealthy"
    elif "warn" in statuses:
        status = "degraded"
    else:
        status = "ok"

    return HealthReport(
        status=status,
        app_name=settings.app_name,
        version=__version__,
        environment=settings.environment,
        build_commit=settings.build_commit,
        python_version=platform.python_version(),
        platform=f"{platform.system().lower()}-{platform.machine().lower()}",
        timestamp=current_time.astimezone(UTC).isoformat().replace("+00:00", "Z"),
        checks=results,
    )


def _run_check(check: HealthCheck, *, timer: Callable[[], float]) -> CheckResult:
    started_at = timer()
    try:
        outcome = check()
    except Exception as error:
        check_name = getattr(check, "__name__", check.__class__.__name__)
        if not isinstance(check_name, str):  # pragma: no cover - defensive for unusual callables
            check_name = check.__class__.__name__
        return CheckResult(
            name=check_name,
            status="fail",
            detail=f"Raised {type(error).__name__}",
            duration_ms=_elapsed_ms(started_at, timer()),
        )
    return CheckResult(
        name=outcome.name,
        status=outcome.status,
        detail=outcome.detail,
        duration_ms=_elapsed_ms(started_at, timer()),
    )


def _elapsed_ms(started_at: float, finished_at: float) -> float:
    return round(max(0.0, finished_at - started_at) * 1000, 3)
