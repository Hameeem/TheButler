import pytest
from app.sources.base import NormalizedJob
from app.agents.matcher import JobMatcher
from app.database import SessionLocal, init_db
from app.database.repositories import seed_default_user_and_profile

def test_job_matcher():
    init_db()
    db = SessionLocal()
    profile = seed_default_user_and_profile(db)
    
    norm_job = NormalizedJob(
        job_key="test_key_1",
        title="Data Analyst Intern",
        company_name="Test Company",
        location="Remote, India",
        is_remote=True,
        source_platform="LinkedIn Jobs",
        job_url="https://example.com/job/1",
        raw_description="Looking for Data Analyst Intern with Python, SQL, Power BI, Pandas skills.",
        required_skills=["Python", "SQL", "Power BI", "Pandas"]
    )
    
    res = JobMatcher.calculate_match(norm_job, profile)
    assert res["overall_score"] >= 80.0
    assert "Python" in res["strong_matches"]
    db.close()
