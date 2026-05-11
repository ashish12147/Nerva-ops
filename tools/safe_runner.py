from __future__ import annotations

import shlex
import subprocess
from dataclasses import dataclass

from security.guardrails import GuardrailResult, validate_shell_command


ALLOWED_BINARIES = {"httpx", "nuclei", "katana", "python", "python3"}


@dataclass
class ToolRunResult:
    ok: bool
    stdout: str = ""
    stderr: str = ""
    returncode: int | None = None
    guardrail: GuardrailResult | None = None


def run_safe_command(command: str, timeout_seconds: int = 120) -> ToolRunResult:
    guard = validate_shell_command(command)
    if not guard.allowed:
        return ToolRunResult(ok=False, stderr=guard.reason, guardrail=guard)

    args = shlex.split(command)
    if not args:
        return ToolRunResult(ok=False, stderr="Empty command")

    binary = args[0].split("/")[-1]
    if binary not in ALLOWED_BINARIES:
        return ToolRunResult(ok=False, stderr=f"Binary is not allowlisted: {binary}")

    try:
        completed = subprocess.run(args, text=True, capture_output=True, timeout=timeout_seconds, check=False)
        return ToolRunResult(
            ok=completed.returncode == 0,
            stdout=completed.stdout,
            stderr=completed.stderr,
            returncode=completed.returncode,
            guardrail=guard,
        )
    except subprocess.TimeoutExpired as exc:
        return ToolRunResult(ok=False, stderr=f"Command timed out: {exc}", guardrail=guard)
    except OSError as exc:
        return ToolRunResult(ok=False, stderr=f"Command failed to start: {exc}", guardrail=guard)
