import logging
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.database import models
from app.browser.playwright_manager import PlaywrightBrowserManager
from app.resume.tailor import ResumeTailor
from app.agents.application_agent import ApplicationQuestionAgent

logger = logging.getLogger(__name__)

class ApplicationRunner:
    @classmethod
    def execute_application(cls, db: Session, application_id: int) -> Dict[str, Any]:
        """
        Executes an approved application. Generates tailored resume, pre-populates application answers,
        runs Playwright automation (or handoff card), and updates application status in DB.
        """
        app_record = db.query(models.Application).filter(models.Application.id == application_id).first()
        if not app_record:
            return {"success": False, "message": "Application record not found."}
            
        job = app_record.job
        profile = db.query(models.Profile).first()

        # Step 1: Tailor Resume
        tailored_resume = ResumeTailor.tailor_resume_for_job(db, job, profile)
        app_record.tailored_resume_id = tailored_resume.id

        # Step 2: Generate Question Answers
        standard_questions = [
            "Why do you want this internship?",
            "Tell us about yourself and why you are a fit.",
            "What is your experience with SQL and data visualization?"
        ]
        answers_dict = {}
        for q in standard_questions:
            ans, is_sens = ApplicationQuestionAgent.generate_answer(q, job, profile)
            answers_dict[q] = ans
            db_answer = models.ApplicationAnswer(
                application_id=app_record.id,
                question=q,
                answer=ans,
                is_sensitive=is_sens,
                is_user_reviewed=True
            )
            db.add(db_answer)

        # Step 3: Run Playwright Browser Automation with compliance check
        profile_data = {
            "full_name": profile.full_name,
            "email": profile.email,
            "phone": profile.phone
        }
        
        success, msg, handoff_reason = PlaywrightBrowserManager.attempt_application_fill(
            job_url=job.application_url or job.job_url,
            profile_data=profile_data,
            resume_path=tailored_resume.file_path,
            answers=answers_dict
        )

        if success:
            app_record.status = "APPLIED"
            app_record.applied_date = models.datetime.datetime.utcnow()
            app_record.notes = f"Submitted automatically via Playwright runner. {msg}"
        else:
            app_record.status = "APPROVED"  # Ready for 1-click manual handoff
            app_record.notes = f"Manual Handoff Needed ({handoff_reason}): {msg}"

        db.commit()
        return {
            "success": True,
            "status": app_record.status,
            "message": msg,
            "resume_path": tailored_resume.file_path,
            "handoff_reason": handoff_reason
        }
