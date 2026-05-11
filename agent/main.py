from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from agent.routes import router as api_router
from dashboard.routes import router as dashboard_router

app = FastAPI(
    title="Nerva Ops",
    description="WhatsApp-controlled, approval-gated AI security testing assistant for authorized assets.",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api")
app.include_router(dashboard_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "nerva-ops"}


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
    <html>
      <head><title>Nerva Ops</title></head>
      <body style='font-family: system-ui; max-width: 760px; margin: 48px auto;'>
        <h1>Nerva Ops</h1>
        <p>Agent is online.</p>
        <p><a href='/settings'>Open settings dashboard</a></p>
        <p><a href='/docs'>Open API docs</a></p>
      </body>
    </html>
    """
