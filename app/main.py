import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db, init_db, models
from app.database.repositories import seed_default_user_and_profile
from app.agents.job_discovery import JobDiscoveryAgent
from app.browser.application_runner import ApplicationRunner
from app.services.scheduler import DiscoveryScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TheButler")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Autonomous AI Agent for Finding and Applying to Data Analyst Internships"
)

@app.on_event("startup")
def on_startup():
    init_db()
    db = SessionLocal()
    seed_default_user_and_profile(db)
    db.close()
    # Start background scheduler
    DiscoveryScheduler.start()

from app.database import SessionLocal

@app.get("/")
def read_root():
    return {
        "status": "online",
        "agent": settings.APP_NAME,
        "version": settings.VERSION,
        "mode": settings.APPLICATION_MODE
    }

@app.get("/api/profile")
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(models.Profile).first()
    if not profile:
        profile = seed_default_user_and_profile(db)
    return {
        "full_name": profile.full_name,
        "email": profile.email,
        "target_role": profile.target_role,
        "preferred_locations": profile.preferred_locations,
        "application_mode": profile.application_mode,
        "skills": [s.name for s in profile.skills],
        "projects": [{"name": p.name, "tech": p.technologies} for p in profile.projects]
    }

@app.post("/api/discover")
def trigger_job_discovery(db: Session = Depends(get_db)):
    res = JobDiscoveryAgent.run_discovery(db)
    return {"message": "Job discovery completed successfully", "results": res}

@app.get("/api/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    results = []
    for j in jobs:
        match = db.query(models.JobMatch).filter(models.JobMatch.job_id == j.id).first()
        results.append({
            "id": j.id,
            "title": j.title,
            "company": j.company_name,
            "location": j.location,
            "is_remote": j.is_remote,
            "source": j.source_platform,
            "match_score": match.overall_score if match else 0.0,
            "quality_status": j.quality_status,
            "url": j.job_url
        })
    return {"count": len(results), "jobs": results}

@app.post("/api/applications/{app_id}/approve")
def approve_and_apply(app_id: int, db: Session = Depends(get_db)):
    res = ApplicationRunner.execute_application(db, app_id)
    return res
