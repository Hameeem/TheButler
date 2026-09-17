import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.database import models
from app.sources import ALL_SOURCES
from app.services.deduplication import DeduplicationService
from app.agents.fraud_detector import FraudDetector
from app.agents.matcher import JobMatcher

logger = logging.getLogger(__name__)

class JobDiscoveryAgent:
    @classmethod
    def run_discovery(cls, db: Session, query: str = "Data Analyst Intern", location: str = "Remote India", limit_per_source: int = 5) -> Dict[str, Any]:
        """
        Orchestrates job search across all enabled sources, deduplicates, analyzes fraud risk,
        calculates match scores, and persists to DB.
        """
        profile = db.query(models.Profile).first()
        if not profile:
            from app.database.repositories import seed_default_user_and_profile
            profile = seed_default_user_and_profile(db)

        raw_discovered_jobs = []
        source_summary = {}

        for source in ALL_SOURCES:
            try:
                logger.info(f"Fetching from {source.name}...")
                jobs = source.fetch_jobs(query=query, location=location, limit=limit_per_source)
                raw_discovered_jobs.extend(jobs)
                source_summary[source.name] = len(jobs)
                
                # Update DB source record
                db_source = db.query(models.JobSource).filter(models.JobSource.name == source.name).first()
                if db_source:
                    db_source.last_run_at = models.datetime.datetime.utcnow()
                    db_source.jobs_found_last_run = len(jobs)
                    db_source.status = "ACTIVE"
            except Exception as e:
                logger.error(f"Error in {source.name}: {e}")
                source_summary[source.name] = 0

        # Step 2: Deduplication
        unique_jobs = DeduplicationService.group_duplicates(raw_discovered_jobs)

        saved_count = 0
        shortlisted_count = 0

        for norm_job in unique_jobs:
            # Check existing job by key
            existing = db.query(models.Job).filter(models.Job.job_key == norm_job.job_key).first()
            if existing:
                continue

            # Step 3: Fraud Analysis
            quality_status, flags, audit = FraudDetector.analyze_job(norm_job)

            # Skip suspicious fraud listings from auto-shortlisting
            db_job = models.Job(
                job_key=norm_job.job_key,
                title=norm_job.title,
                company_name=norm_job.company_name,
                location=norm_job.location,
                is_remote=norm_job.is_remote,
                is_hybrid=norm_job.is_hybrid,
                is_internship=norm_job.is_internship,
                experience_req=norm_job.experience_req,
                stipend_salary=norm_job.stipend_salary,
                source_platform=norm_job.source_platform,
                job_url=norm_job.job_url,
                application_url=norm_job.application_url or norm_job.job_url,
                raw_description=norm_job.raw_description,
                responsibilities=norm_job.responsibilities,
                requirements=norm_job.requirements,
                required_skills=norm_job.required_skills,
                preferred_skills=norm_job.preferred_skills,
                date_posted=norm_job.date_posted,
                quality_status=quality_status,
                quality_flags=flags
            )
            db.add(db_job)
            db.commit()
            db.refresh(db_job)
            saved_count += 1

            # Step 4: AI Job Matching
            match_res = JobMatcher.calculate_match(norm_job, profile)
            db_match = models.JobMatch(
                job_id=db_job.id,
                role_score=match_res["role_score"],
                skill_score=match_res["skill_score"],
                experience_score=match_res["experience_score"],
                education_score=match_res["education_score"],
                location_score=match_res["location_score"],
                remote_score=match_res["remote_score"],
                project_score=match_res["project_score"],
                overall_score=match_res["overall_score"],
                strong_matches=match_res["strong_matches"],
                missing_skills=match_res["missing_skills"],
                match_explanation=match_res["match_explanation"]
            )
            db.add(db_match)

            # Step 5: Automatic Shortlisting & Application creation if match meets min score
            if match_res["overall_score"] >= profile.min_match_score and quality_status != "SUSPICIOUS":
                shortlisted_count += 1
                app = models.Application(
                    job_id=db_job.id,
                    profile_id=profile.id,
                    status="REVIEW_REQUIRED" if profile.application_mode == "APPROVAL_REQUIRED" else "SHORTLISTED",
                    match_score=match_res["overall_score"]
                )
                db.add(app)

            db.commit()

        return {
            "total_discovered": len(raw_discovered_jobs),
            "unique_jobs": len(unique_jobs),
            "new_saved": saved_count,
            "shortlisted": shortlisted_count,
            "source_summary": source_summary
        }
