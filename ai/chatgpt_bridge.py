from __future__ import annotations


def build_chatgpt_helper_prompt(
    task_id: str,
    current_task: str,
    target_scope: str,
    previous_results: str,
    problem: str,
) -> str:
    return f"""COPY THIS INTO CHATGPT:

You are helping my authorized local security testing assistant continue a legal security testing task.

Return your answer in this exact format only:

```AGENT_RESPONSE
{{
  "summary": "short explanation",
  "next_action": "what the local agent should do next",
  "commands": [
    {{
      "tool": "allowed tool name",
      "command": "safe command to run",
      "purpose": "why this command is needed",
      "risk_level": "low/medium/high",
      "requires_user_approval": true
    }}
  ],
  "files_to_create": [
    {{
      "path": "relative/file/path",
      "content": "full file content here"
    }}
  ],
  "report_notes": ["important note"],
  "stop_conditions": ["when the agent should stop and ask me"]
}}
```

Rules:
- Only help with authorized testing.
- Do not suggest destructive actions.
- Do not suggest credential attacks, malware, evasion, persistence, or unauthorized exploitation.
- Prefer safe recon, validation, reporting, and debugging.
- If exploitation is needed, mark it as requires_user_approval=true.
- Output only the AGENT_RESPONSE block.
- No extra explanation outside the block.

Task ID:
{task_id}

Current task:
{current_task}

Target/scope:
{target_scope}

Previous results:
{previous_results}

Problem:
{problem}
"""
