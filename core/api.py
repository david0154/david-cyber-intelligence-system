"""
FastAPI Backend v2 - All endpoints + Dashboard API
FIXED: Proper startup, CORS, error handling
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
from loguru import logger
import os

from core.task_router import TaskRouter
from core.threat_scorer import ThreatScorer

app = FastAPI(
    title="DAVID CYBER INTELLIGENCE SYSTEM",
    description="Advanced AI Cybersecurity Platform v2.0 — Devil Pvt Ltd & Nexuzy Tech Pvt Ltd",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve dashboard
if os.path.exists("dashboard"):
    app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

router_engine = TaskRouter()
scorer = ThreatScorer()


class QueryRequest(BaseModel):
    module: str
    params: Optional[dict] = {}


class ScoreUpdate(BaseModel):
    module: str
    score: float


@app.get("/", response_class=HTMLResponse)
def dashboard():
    dash_path = os.path.join("dashboard", "index.html")
    if os.path.exists(dash_path):
        return FileResponse(dash_path)
    return HTMLResponse("""
    <html><body style='background:#0a0a0a;color:#00ff41;font-family:monospace;padding:40px'>
    <h1>&#9632; DAVID CYBER INTELLIGENCE SYSTEM v2.0</h1>
    <p>API running. <a href='/docs' style='color:#00ff41'>View API Docs</a></p>
    <p>Developer: Devil Pvt Ltd &amp; Nexuzy Tech Pvt Ltd</p>
    </body></html>
    """)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "loaded_modules": list(router_engine._engines.keys()),
        "developer": "Devil Pvt Ltd & Nexuzy Tech Pvt Ltd",
    }


@app.post("/analyze")
def analyze(req: QueryRequest):
    result = router_engine.route(req.module, req.params or {})
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result


@app.get("/score")
def get_score():
    return scorer.report()


@app.post("/score/update")
def update_score(upd: ScoreUpdate):
    scorer.update(upd.module, upd.score)
    return scorer.report()


# --- Security Tool Endpoints ---

@app.get("/api/wazuh/alerts")
def wazuh_alerts(limit: int = 20):
    return router_engine.route("wazuh", {"limit": limit})


@app.post("/api/zap/scan")
def zap_scan(url: str):
    return router_engine.route("zap", {"url": url})


@app.post("/api/openvas/scan")
def openvas_scan(target: str):
    return router_engine.route("openvas", {"target": target})


@app.post("/api/hydra/test")
def hydra_test(target: str, service: str = "ssh"):
    return router_engine.route("hydra", {"target": target, "service": service})


@app.get("/api/cloudflare/stats")
def cloudflare_stats(zone_id: str = ""):
    return router_engine.route("cloudflare", {"zone_id": zone_id})


@app.post("/api/deepexploit")
def deepexploit(target: str):
    return router_engine.route("deepexploit", {"target": target})


@app.post("/api/osint")
def osint(target: str):
    return router_engine.route("osint", {"target": target})


@app.post("/api/pentest")
def pentest(target: str):
    return router_engine.route("pentest", {"target": target})


@app.post("/api/malware")
def malware(file_path: str):
    return router_engine.route("malware", {"file_path": file_path})


@app.post("/api/geo")
def geo(ip: str):
    return router_engine.route("geo", {"ip": ip})


@app.post("/api/chat")
def chat(query: str):
    return router_engine.route("chat", {"query": query})


# --- WebSocket for live alerts ---
@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"echo": data, "status": "live"})
    except Exception:
        pass
