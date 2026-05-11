from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from agent.settings import load_settings


def write_markdown_report(task_id: str, title: str, notes: list[str]) -> Path:
    settings = load_settings().reports
    output_dir = Path(settings.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{task_id}.md"

    lines = [
        f"# {title}",
        "",
        f"Task ID: `{task_id}`",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Notes",
        "",
    ]
    lines.extend([f"- {note}" for note in notes])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
