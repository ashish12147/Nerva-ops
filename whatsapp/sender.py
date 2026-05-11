from __future__ import annotations

import os

import httpx

from agent.settings import load_settings


async def send_text_message(to: str, body: str) -> dict:
    settings = load_settings().whatsapp
    if not settings.enabled:
        return {"ok": False, "skipped": True, "reason": "WhatsApp sending disabled."}

    token = os.getenv(settings.access_token_env, "")
    phone_number_id = os.getenv(settings.phone_number_id_env, "")
    if not token or not phone_number_id:
        return {"ok": False, "error": "WhatsApp token or phone number ID is missing."}

    url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"preview_url": True, "body": body[:4000]},
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, json=payload, headers=headers)
        return {"ok": response.is_success, "status_code": response.status_code, "body": response.text}
