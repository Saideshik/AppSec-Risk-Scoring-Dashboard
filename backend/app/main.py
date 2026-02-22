from fastapi import FastAPI
from .routers import apps, findings, metrics

app = FastAPI(title="AppSec Risk Scoring Dashboard API")

app.include_router(apps.router)
app.include_router(findings.router)
app.include_router(metrics.router)

@app.get("/health")
def health():
    return {"ok": True}
