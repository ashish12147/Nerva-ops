from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from agent.settings import load_settings


@dataclass
class GuardrailResult:
    allowed: bool
    reason: str
    risk: str = "low"


def host_from_target(target: str) -> str:
    parsed = urlparse(target if "://" in target else f"https://{target}")
    return parsed.hostname or target.strip().split("/")[0]


def is_in_scope(target: str) -> GuardrailResult:
    settings = load_settings().security
    host = host_from_target(target).lower()

    for blocked in settings.blocked_domains:
        blocked = blocked.lower()
        if host == blocked or host.endswith(f".{blocked}"):
            return GuardrailResult(False, f"Target is blocked by policy: {blocked}")

    if not settings.require_scope_match:
        return GuardrailResult(True, "Scope matching disabled by settings.")

    for allowed in settings.allowed_domains:
        allowed = allowed.lower()
        if host == allowed or host.endswith(f".{allowed}"):
            return GuardrailResult(True, f"Target matches allowed scope: {allowed}")

    return GuardrailResult(False, "Target does not match configured allowed scope.")


def validate_shell_command(command: str) -> GuardrailResult:
    settings = load_settings().security
    lowered = command.lower()
    for pattern in settings.banned_shell_patterns:
        if pattern.lower() in lowered:
            return GuardrailResult(False, f"Command contains banned pattern: {pattern}", risk="high")
    return GuardrailResult(True, "Command passed banned-pattern validation.")


def requires_approval(risk: str) -> bool:
    security = load_settings().security
    normalized = risk.lower()
    if normalized == "high":
        return security.require_approval_for_high_risk
    if normalized == "medium":
        return security.require_approval_for_medium_risk
    return False
