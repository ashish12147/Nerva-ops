from __future__ import annotations

from uuid import uuid4

from ai.chatgpt_bridge import build_chatgpt_helper_prompt


def route_command(text: str, sender: str = "local") -> dict:
    stripped = text.strip()
    if not stripped:
        raise ValueError("Empty command")

    if stripped == "/status":
        return {"reply": "Nerva Ops is online.", "sender": sender}

    if stripped == "/help":
        return {
            "reply": "Commands: /status, /help, /settings, /recon <domain>, /scan <url> safe, /report <task_id>, /approve <task_id>, /stop <task_id>, /ask_claude <task_id>, /gpt <task_id> <AGENT_RESPONSE>",
            "sender": sender,
        }

    if stripped == "/settings":
        return {"reply": "Open the dashboard at http://localhost:8080/settings", "sender": sender}

    if stripped.startswith("/gpt "):
        return {"reply": "Received manual ChatGPT helper response. Validation pipeline will be wired next.", "sender": sender}

    if stripped.startswith("/ask_gpt_prompt"):
        task_id = f"help_{uuid4().hex[:8]}"
        prompt = build_chatgpt_helper_prompt(
            task_id=task_id,
            current_task="User requested external reasoning help.",
            target_scope="Use only authorized assets configured in Nerva Ops settings.",
            previous_results="No previous results supplied.",
            problem=stripped,
        )
        return {"reply": prompt, "task_id": task_id, "sender": sender}

    if stripped.startswith("/scan ") or stripped.startswith("/recon "):
        task_id = f"task_{uuid4().hex[:8]}"
        return {
            "reply": "Task accepted for safe planning. Execution worker will be connected next.",
            "task_id": task_id,
            "command": stripped,
            "sender": sender,
        }

    return {"reply": "Unknown command. Send /help.", "sender": sender}
