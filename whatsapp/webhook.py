from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, Request, Response

from agent.command_router import route_command
from agent.settings import load_settings
from whatsapp.sender import send_text_message

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])


@router.get("/webhook")
def verify_webhook(request: Request) -> Response:
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    settings = load_settings().whatsapp
    expected = os.getenv(settings.verify_token_env, "")

    if mode == "subscribe" and token == expected and challenge:
        return Response(content=challenge, media_type="text/plain")
    return Response(status_code=403)


@router.post("/webhook")
async def receive_webhook(payload: dict[str, Any]) -> dict[str, str]:
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for message in value.get("messages", []):
                sender = message.get("from", "")
                text = message.get("text", {}).get("body", "")
                if not text:
                    continue
                result = route_command(text, sender)
                reply = result.get("reply", "Command processed.")
                await send_text_message(sender, reply)
    return {"status": "received"}
