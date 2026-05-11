from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class NvidiaSettings(BaseModel):
    enabled: bool = True
    api_key_env: str = "NVIDIA_API_KEY"
    base_url_env: str = "NVIDIA_BASE_URL"
    model_env: str = "NVIDIA_MODEL"
    temperature: float = 0.2
    max_tokens: int = 2048


class ClaudeCliSettings(BaseModel):
    enabled: bool = True
    executable_env: str = "CLAUDE_CLI_PATH"
    mode: str = "coding_helper"
    timeout_seconds: int = 180


class ChatGPTBridgeSettings(BaseModel):
    enabled: bool = True
    require_manual_pasteback: bool = True


class AISettings(BaseModel):
    nvidia: NvidiaSettings = Field(default_factory=NvidiaSettings)
    claude_cli: ClaudeCliSettings = Field(default_factory=ClaudeCliSettings)
    chatgpt_bridge: ChatGPTBridgeSettings = Field(default_factory=ChatGPTBridgeSettings)


class WhatsAppSettings(BaseModel):
    enabled: bool = False
    access_token_env: str = "WHATSAPP_ACCESS_TOKEN"
    phone_number_id_env: str = "WHATSAPP_PHONE_NUMBER_ID"
    verify_token_env: str = "WHATSAPP_VERIFY_TOKEN"
    max_direct_file_mb: int = 100


class SecuritySettings(BaseModel):
    require_scope_match: bool = True
    require_approval_for_medium_risk: bool = True
    require_approval_for_high_risk: bool = True
    default_rate_limit_rps: int = 2
    allowed_domains: list[str] = Field(default_factory=list)
    blocked_domains: list[str] = Field(default_factory=lambda: ["localhost", "127.0.0.1", "0.0.0.0"])
    banned_shell_patterns: list[str] = Field(default_factory=list)


class ToolConfig(BaseModel):
    enabled: bool = True
    risk: str = "low"


class ReportsSettings(BaseModel):
    output_dir: str = "reports/output"
    formats: list[str] = Field(default_factory=lambda: ["markdown", "html"])
    include_screenshots: bool = True


class UploadSettings(BaseModel):
    provider: str = "local"
    local_output_dir: str = "uploads"
    public_base_url: str = ""


class DashboardSettings(BaseModel):
    enabled: bool = True
    admin_password_env: str = "NERVA_DASHBOARD_ADMIN_PASSWORD"


class AppSettings(BaseModel):
    app: dict[str, Any] = Field(default_factory=dict)
    owner: dict[str, Any] = Field(default_factory=dict)
    ai: AISettings = Field(default_factory=AISettings)
    whatsapp: WhatsAppSettings = Field(default_factory=WhatsAppSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    tools: dict[str, ToolConfig] = Field(default_factory=dict)
    reports: ReportsSettings = Field(default_factory=ReportsSettings)
    uploads: UploadSettings = Field(default_factory=UploadSettings)
    dashboard: DashboardSettings = Field(default_factory=DashboardSettings)


def settings_path() -> Path:
    return Path(os.getenv("NERVA_SETTINGS_PATH", "config/settings.yaml"))


def example_settings_path() -> Path:
    return Path("config/settings.example.yaml")


def load_raw_settings(path: Path | None = None) -> dict[str, Any]:
    selected = path or settings_path()
    if not selected.exists():
        selected = example_settings_path()
    with selected.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_settings(path: Path | None = None) -> AppSettings:
    return AppSettings.model_validate(load_raw_settings(path))


def save_settings(data: dict[str, Any], path: Path | None = None) -> None:
    selected = path or settings_path()
    selected.parent.mkdir(parents=True, exist_ok=True)
    with selected.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False)


def env_value(env_name: str, default: str = "") -> str:
    return os.getenv(env_name, default)
