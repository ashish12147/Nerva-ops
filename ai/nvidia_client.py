from __future__ import annotations

import os
from typing import Any

import httpx

from agent.settings import load_settings


class NvidiaClient:
    def __init__(self) -> None:
        settings = load_settings().ai.nvidia
        self.enabled = settings.enabled
        self.api_key = os.getenv(settings.api_key_env, "")
        self.base_url = os.getenv(settings.base_url_env, "https://integrate.api.nvidia.com/v1")
        self.model = os.getenv(settings.model_env, "meta/llama-3.1-70b-instruct")
        self.temperature = settings.temperature
        self.max_tokens = settings.max_tokens

    def available(self) -> bool:
        return bool(self.enabled and self.api_key)

    async def chat(self, system: str, user: str) -> dict[str, Any]:
        if not self.available():
            return {"ok": False, "error": "NVIDIA client is disabled or missing API key."}

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            return {"ok": True, "response": response.json()}
