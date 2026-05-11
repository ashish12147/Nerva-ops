# Nerva Ops

**Nerva Ops is a WhatsApp-controlled, approval-gated AI security testing assistant for authorized assets, local labs, and bug bounty scopes.**

It runs on an always-on laptop or lab machine and gives the owner a boss-style command interface over WhatsApp while keeping risky security actions behind scope checks and explicit approval.

## Repository description

WhatsApp-controlled AI security assistant with NVIDIA API, Claude CLI, scope guardrails, approval gates, reporting, and a settings dashboard for tokens and tool configuration.

## What this is

Nerva Ops is intended for:

- your own applications and infrastructure
- local labs and CTF-style environments
- bug bounty programs where the asset is explicitly in scope
- non-destructive recon, validation, evidence collection, reporting, and workflow automation

## What this is not

Nerva Ops is not for unauthorized access, credential attacks, malware, persistence, evasion, destructive testing, or scanning assets where you do not have permission.

## Architecture

```text
WhatsApp command
  -> FastAPI webhook
  -> command router
  -> task queue
  -> scope guard + risk engine
  -> safe tool runner / AI helper
  -> report / file delivery
```

AI helper layers:

```text
NVIDIA API      = default planner/reasoning layer
Claude CLI      = heavy coding/debugging helper
ChatGPT bridge  = manual copy-paste fallback prompt generator
```

## MVP commands

```text
/status
/help
/recon <domain>
/scan <url> safe
/report <task_id>
/approve <task_id>
/stop <task_id>
/ask_claude <task_id>
/gpt <task_id> <AGENT_RESPONSE block>
/settings
```

## Project layout

```text
agent/          FastAPI app, router, task queue, guardrails
ai/             NVIDIA, Claude CLI, ChatGPT prompt bridge
whatsapp/       WhatsApp webhook and outbound sender
security/       scope and risk validation
tools/          safe wrappers for recon/scanning tools
reports/        Markdown/HTML report generation
dashboard/      settings dashboard frontend/backend skeleton
config/         example settings and allowlists
scripts/        install and service scripts
tests/          starter tests
```

## Settings and secrets

All sensitive values are entered locally through the dashboard or `.env`; they are never committed.

Supported settings include:

- NVIDIA API key and model
- Claude CLI path and mode
- WhatsApp Cloud API token
- WhatsApp phone number ID
- webhook verify token
- allowed scope domains
- blocked domains
- tool enable/disable toggles
- risk approval policy
- report and upload settings

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config/settings.example.yaml config/settings.yaml
uvicorn agent.main:app --reload --host 0.0.0.0 --port 8080
```

## Security defaults

- secrets are loaded from environment variables or local config only
- real API keys are never committed
- commands are validated against an allowlist
- risky actions require approval
- targets must match configured scope
- dangerous shell patterns are blocked before execution

## Status

Initial MVP skeleton in progress.
