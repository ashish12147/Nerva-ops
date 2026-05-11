from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass

from agent.settings import load_settings


@dataclass
class ClaudeCliResult:
    ok: bool
    stdout: str = ""
    stderr: str = ""
    returncode: int | None = None


class ClaudeCli:
    def __init__(self) -> None:
        settings = load_settings().ai.claude_cli
        self.enabled = settings.enabled
        self.executable = os.getenv(settings.executable_env, "claude")
        self.timeout_seconds = settings.timeout_seconds

    def available(self) -> bool:
        return self.enabled and bool(self.executable)

    def ask(self, prompt: str) -> ClaudeCliResult:
        if not self.available():
            return ClaudeCliResult(ok=False, stderr="Claude CLI is disabled or not configured.")

        try:
            completed = subprocess.run(
                [self.executable],
                input=prompt,
                text=True,
                capture_output=True,
                timeout=self.timeout_seconds,
                check=False,
            )
            return ClaudeCliResult(
                ok=completed.returncode == 0,
                stdout=completed.stdout,
                stderr=completed.stderr,
                returncode=completed.returncode,
            )
        except subprocess.TimeoutExpired as exc:
            return ClaudeCliResult(ok=False, stderr=f"Claude CLI timed out after {self.timeout_seconds}s: {exc}")
        except OSError as exc:
            return ClaudeCliResult(ok=False, stderr=f"Claude CLI could not be started: {exc}")
