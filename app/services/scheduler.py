import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal, init_db
from app.agents.job_discovery import JobDiscoveryAgent
from app.services.notifications import NotificationService

logger = logging.getLogger(__name__)

class DiscoveryScheduler:
    _scheduler = None

    @classmethod
    def start(cls):
        if cls._scheduler and cls._scheduler.running:
            return
            
        cls._scheduler = BackgroundScheduler()
        # Schedule discovery 2x daily (e.g. 9 AM and 5 PM)
        cls._scheduler.add_job(
            cls.run_scheduled_job,
            trigger="interval",
            hours=12,
            id="job_discovery_task",
            replace_existing=True
        )
        cls._scheduler.start()
        logger.info("DiscoveryScheduler background scheduler started.")

    @classmethod
    def run_scheduled_job(cls):
        logger.info("Running scheduled job discovery...")
        init_db()
        db = SessionLocal()
        try:
            res = JobDiscoveryAgent.run_discovery(db)
            NotificationService.send_daily_report(res)
        except Exception as e:
            logger.error(f"Error in scheduled job: {e}")
        finally:
            db.close()
