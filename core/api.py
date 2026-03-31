"""
FastAPI Backend Server
DAVID CYBER INTELLIGENCE SYSTEM
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from core.task_router import TaskRouter
from core.threat_scorer import ThreatScorer
import uvicorn

app = FastAPI(
    title="DAVID CYBER INTELLIGENCE SYSTEM",
    description="Advanced AI-Powered Cybersecurity Platform by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd",
    version="1.0.0",
)

router = TaskRouter()
scorer = ThreatScorer()


class QueryRequest(BaseModel):
    module: str
    params: Optional[dict] = {}


class ThreatScoreUpdate(BaseModel):
    module: str
    score: float


@app.get("/")
def root():
    return {
        "system": "DAVID CYBER INTELLIGENCE SYSTEM",
        "version": "1.0.0",
        "developer": "Devil Pvt Ltd & Nexuzy Tech Pvt Ltd",
        "status": "operational",
    }


@app.post("/analyze")
def analyze(request: QueryRequest):
    """Route a request to any module."""
    result = router.route(request.module, request.params or {})
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result


@app.post("/score/update")
def update_score(update: ThreatScoreUpdate):
    scorer.update(update.module, update.score)
    return scorer.report()


@app.get("/score")
def get_score():
    return scorer.report()


@app.get("/health")
def health():
    return {"status": "healthy", "modules": list(router._engines.keys())}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
