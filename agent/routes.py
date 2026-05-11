from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agent.settings import load_raw_settings, save_settings
from agent.command_router import route_command

router = APIRouter()


class CommandRequest(BaseModel):
    text: str
    sender: str = "local"


@router.get("/status")
def status() -> dict[str, str]:
    return {"status": "online", "agent": "nerva-ops"}


@router.get("/settings")
def get_settings() -> dict:
    return load_raw_settings()


@router.put("/settings")
def update_settings(payload: dict) -> dict[str, str]:
    save_settings(payload)
    return {"status": "saved"}


@router.post("/command")
def command(payload: CommandRequest) -> dict:
    try:
        return route_command(payload.text, payload.sender)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
