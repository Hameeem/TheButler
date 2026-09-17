import logging
import requests
from typing import Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class NotificationService:
    @classmethod
    def send_daily_report(cls, summary: Dict[str, Any]) -> bool:
        """
        Sends a clean daily job report summary.
        Can output to webhook (Discord/Slack), log, or Streamlit notification toast.
        """
        report_text = f"""
📢 **DAILY JOB REPORT — THEBUTLER**

Jobs discovered today: {summary.get('total_discovered', 0)}
Relevant unique jobs: {summary.get('unique_jobs', 0)}
Strong matches (>= {settings.MIN_MATCH_SCORE}%): {summary.get('shortlisted', 0)}

Applications waiting for approval: {summary.get('shortlisted', 0)}
        """
        logger.info(report_text)
        
        if settings.NOTIFICATION_WEBHOOK_URL:
            try:
                requests.post(settings.NOTIFICATION_WEBHOOK_URL, json={"content": report_text}, timeout=5)
                return True
            except Exception as e:
                logger.error(f"Failed to post to webhook: {e}")
        return True
