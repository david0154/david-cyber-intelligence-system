"""
Bug Bounty Platform API
Full REST API for submission, validation, admin
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from datetime import datetime
from loguru import logger

from bounty.models import get_db, init_db, compute_hash
from bounty.ai_validator import AIValidator
from bounty.cvss_scorer import CVSSScorer

# Init DB on startup
try:
    init_db()
except Exception as e:
    logger.error(f"[Bounty] DB init error: {e}")

app = FastAPI(
    title="DAVID Bug Bounty Platform",
    description="AI-powered bug bounty system by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd",
    version="1.0.0",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

validator = AIValidator()
scorer = CVSSScorer()
UPLOAD_DIR = os.path.join("data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class ReportSubmit(BaseModel):
    title: str
    description: str
    target: str
    reporter: Optional[str] = "anonymous"
    vuln_type: Optional[str] = "other"


@app.get("/")
def root():
    return {"platform": "DAVID Bug Bounty", "version": "1.0.0",
            "developer": "Devil Pvt Ltd & Nexuzy Tech Pvt Ltd"}


@app.post("/report/submit")
def submit_report(report: ReportSubmit):
    """Submit a new vulnerability report."""
    # Duplicate check
    report_hash = compute_hash(report.title, report.description, report.target)
    conn = get_db()
    existing = conn.execute("SELECT id FROM reports WHERE hash=?",
                            (report_hash,)).fetchone()
    if existing:
        conn.close()
        return {"status": "duplicate", "message": "This report already exists.",
                "duplicate_of": existing["id"]}

    # AI Validation
    validation = validator.validate(report.dict())

    now = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO reports
        (title, description, target, vuln_type, severity, cvss_score,
         status, reporter, ai_validated, ai_feedback, reward, hash,
         created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        report.title, report.description, report.target,
        validation["vuln_type"], validation["severity"],
        validation["cvss_score"], validation["auto_status"],
        report.reporter, 1 if validation["valid"] else 0,
        validation["ai_feedback"], validation["suggested_reward"],
        report_hash, now, now
    ))
    conn.commit()
    report_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()

    return {
        "status": "submitted",
        "report_id": report_id,
        "validation": validation,
    }


@app.post("/report/{report_id}/upload")
async def upload_file(report_id: int,
                      file: UploadFile = File(...),
                      file_type: str = Form("screenshot")):
    """Upload screenshot or PoC file for a report."""
    safe_name = f"{report_id}_{file_type}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, safe_name)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    conn = get_db()
    field = "screenshot_path" if file_type == "screenshot" else "poc_path"
    conn.execute(f"UPDATE reports SET {field}=? WHERE id=?", (path, report_id))
    conn.commit()
    conn.close()
    return {"status": "ok", "file": safe_name}


@app.get("/reports")
def list_reports(status: Optional[str] = None, limit: int = 20):
    """List all reports (admin)."""
    conn = get_db()
    if status:
        rows = conn.execute(
            "SELECT * FROM reports WHERE status=? ORDER BY created_at DESC LIMIT ?",
            (status, limit)).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM reports ORDER BY created_at DESC LIMIT ?",
            (limit,)).fetchall()
    conn.close()
    return {"reports": [dict(r) for r in rows]}


@app.get("/report/{report_id}")
def get_report(report_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM reports WHERE id=?", (report_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Report not found")
    return dict(row)


@app.post("/report/{report_id}/approve")
def approve_report(report_id: int, reward: float = 0):
    """Admin: approve and reward."""
    conn = get_db()
    now = datetime.utcnow().isoformat()
    conn.execute(
        "UPDATE reports SET status='APPROVED', reward=?, updated_at=? WHERE id=?",
        (reward, now, report_id)
    )
    if reward > 0:
        row = conn.execute("SELECT reporter FROM reports WHERE id=?", (report_id,)).fetchone()
        if row:
            conn.execute(
                "INSERT INTO rewards (report_id, user, amount, issued_at) VALUES (?,?,?,?)",
                (report_id, row["reporter"], reward, now)
            )
    conn.commit()
    conn.close()
    return {"status": "approved", "report_id": report_id, "reward": reward}


@app.post("/report/{report_id}/reject")
def reject_report(report_id: int, reason: str = ""):
    conn = get_db()
    now = datetime.utcnow().isoformat()
    conn.execute(
        "UPDATE reports SET status='REJECTED', ai_feedback=?, updated_at=? WHERE id=?",
        (reason, now, report_id)
    )
    conn.commit()
    conn.close()
    return {"status": "rejected", "report_id": report_id}


@app.get("/stats")
def get_stats():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    approved = conn.execute("SELECT COUNT(*) FROM reports WHERE status='APPROVED'").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM reports WHERE status='PENDING' OR status='VERIFIED'").fetchone()[0]
    total_rewards = conn.execute("SELECT SUM(reward) FROM reports WHERE status='APPROVED'").fetchone()[0] or 0
    by_severity = {}
    for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        count = conn.execute("SELECT COUNT(*) FROM reports WHERE severity=?", (sev,)).fetchone()[0]
        by_severity[sev] = count
    conn.close()
    return {
        "total_reports": total,
        "approved": approved,
        "pending": pending,
        "total_rewards_issued": total_rewards,
        "by_severity": by_severity,
    }
