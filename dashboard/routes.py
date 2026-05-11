from __future__ import annotations

from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from agent.settings import load_raw_settings, save_settings

router = APIRouter()


@router.get("/settings", response_class=HTMLResponse)
def settings_page() -> str:
    data = load_raw_settings()
    ai = data.get("ai", {})
    whatsapp = data.get("whatsapp", {})
    security = data.get("security", {})
    owner = data.get("owner", {})

    return f"""
    <html>
      <head>
        <title>Nerva Ops Settings</title>
        <style>
          body {{ font-family: system-ui, sans-serif; max-width: 980px; margin: 32px auto; background: #0b0f19; color: #e5e7eb; }}
          .card {{ background: #111827; border: 1px solid #1f2937; border-radius: 18px; padding: 22px; margin: 18px 0; }}
          label {{ display: block; font-weight: 700; margin-top: 14px; }}
          input, textarea, select {{ width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #374151; background: #030712; color: #e5e7eb; }}
          button {{ padding: 12px 18px; border: 0; border-radius: 12px; cursor: pointer; font-weight: 800; }}
          .muted {{ color: #9ca3af; }}
        </style>
      </head>
      <body>
        <h1>Nerva Ops Settings</h1>
        <p class="muted">Secrets entered here are saved locally to config/settings.yaml or environment variables. Never commit real tokens.</p>
        <form method="post" action="/settings/save">
          <div class="card">
            <h2>Owner</h2>
            <label>Owner WhatsApp Number</label>
            <input name="owner_whatsapp_number" value="{owner.get('whatsapp_number', '')}" placeholder="919999999999" />
            <label>Display Name</label>
            <input name="owner_display_name" value="{owner.get('display_name', 'Boss')}" />
          </div>

          <div class="card">
            <h2>AI Providers</h2>
            <label>NVIDIA Enabled</label>
            <select name="nvidia_enabled"><option value="true">true</option><option value="false">false</option></select>
            <label>NVIDIA API Key Environment Name</label>
            <input name="nvidia_api_key_env" value="{ai.get('nvidia', {}).get('api_key_env', 'NVIDIA_API_KEY')}" />
            <label>NVIDIA Model Environment Name</label>
            <input name="nvidia_model_env" value="{ai.get('nvidia', {}).get('model_env', 'NVIDIA_MODEL')}" />
            <label>Claude CLI Enabled</label>
            <select name="claude_enabled"><option value="true">true</option><option value="false">false</option></select>
            <label>Claude CLI Executable Environment Name</label>
            <input name="claude_executable_env" value="{ai.get('claude_cli', {}).get('executable_env', 'CLAUDE_CLI_PATH')}" />
          </div>

          <div class="card">
            <h2>WhatsApp Cloud API</h2>
            <label>WhatsApp Enabled</label>
            <select name="whatsapp_enabled"><option value="false">false</option><option value="true">true</option></select>
            <label>Access Token Environment Name</label>
            <input name="whatsapp_access_token_env" value="{whatsapp.get('access_token_env', 'WHATSAPP_ACCESS_TOKEN')}" />
            <label>Phone Number ID Environment Name</label>
            <input name="whatsapp_phone_number_id_env" value="{whatsapp.get('phone_number_id_env', 'WHATSAPP_PHONE_NUMBER_ID')}" />
            <label>Webhook Verify Token Environment Name</label>
            <input name="whatsapp_verify_token_env" value="{whatsapp.get('verify_token_env', 'WHATSAPP_VERIFY_TOKEN')}" />
          </div>

          <div class="card">
            <h2>Scope Guard</h2>
            <label>Allowed Domains, one per line</label>
            <textarea name="allowed_domains" rows="6">{"\n".join(security.get('allowed_domains', []))}</textarea>
            <label>Blocked Domains, one per line</label>
            <textarea name="blocked_domains" rows="6">{"\n".join(security.get('blocked_domains', []))}</textarea>
          </div>

          <button type="submit">Save Settings</button>
        </form>
      </body>
    </html>
    """


@router.post("/settings/save")
def save_settings_form(
    owner_whatsapp_number: str = Form(""),
    owner_display_name: str = Form("Boss"),
    nvidia_enabled: str = Form("true"),
    nvidia_api_key_env: str = Form("NVIDIA_API_KEY"),
    nvidia_model_env: str = Form("NVIDIA_MODEL"),
    claude_enabled: str = Form("true"),
    claude_executable_env: str = Form("CLAUDE_CLI_PATH"),
    whatsapp_enabled: str = Form("false"),
    whatsapp_access_token_env: str = Form("WHATSAPP_ACCESS_TOKEN"),
    whatsapp_phone_number_id_env: str = Form("WHATSAPP_PHONE_NUMBER_ID"),
    whatsapp_verify_token_env: str = Form("WHATSAPP_VERIFY_TOKEN"),
    allowed_domains: str = Form(""),
    blocked_domains: str = Form(""),
) -> RedirectResponse:
    data = load_raw_settings()
    data.setdefault("owner", {})
    data["owner"].update({"whatsapp_number": owner_whatsapp_number, "display_name": owner_display_name})
    data.setdefault("ai", {}).setdefault("nvidia", {})
    data["ai"]["nvidia"].update({"enabled": nvidia_enabled == "true", "api_key_env": nvidia_api_key_env, "model_env": nvidia_model_env})
    data.setdefault("ai", {}).setdefault("claude_cli", {})
    data["ai"]["claude_cli"].update({"enabled": claude_enabled == "true", "executable_env": claude_executable_env})
    data.setdefault("whatsapp", {})
    data["whatsapp"].update({
        "enabled": whatsapp_enabled == "true",
        "access_token_env": whatsapp_access_token_env,
        "phone_number_id_env": whatsapp_phone_number_id_env,
        "verify_token_env": whatsapp_verify_token_env,
    })
    data.setdefault("security", {})
    data["security"]["allowed_domains"] = [line.strip() for line in allowed_domains.splitlines() if line.strip()]
    data["security"]["blocked_domains"] = [line.strip() for line in blocked_domains.splitlines() if line.strip()]
    save_settings(data)
    return RedirectResponse("/settings", status_code=303)
