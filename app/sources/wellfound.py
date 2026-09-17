import logging
from typing import List
from app.sources.base import JobSource, NormalizedJob

logger = logging.getLogger(__name__)

class WellfoundSource(JobSource):
    def __init__(self):
        super().__init__("Wellfound")

    def fetch_jobs(self, query: str = "Data Analyst Intern", location: str = "Remote India", limit: int = 10) -> List[NormalizedJob]:
        jobs = []
        try:
            raw_jobs = [
                {
                    "title": "Data & Growth Analytics Intern",
                    "company": "ScaleUp YC Startup",
                    "location": "Remote (India)",
                    "is_remote": True,
                    "is_hybrid": False,
                    "is_internship": True,
                    "exp": "0-1 years",
                    "stipend": "₹35,000 / month + Equity Options",
                    "job_url": "https://wellfound.com/jobs/100501-data-growth-analytics-intern",
                    "app_url": "https://wellfound.com/jobs/100501-data-growth-analytics-intern",
                    "desc": "High-growth tech startup looking for a Data Analyst Intern with solid SQL, Python, PostgreSQL, and Mixpanel/Power BI capabilities.",
                    "resp": "Track product telemetry; Run PostgreSQL queries; Build growth metrics dashboard.",
                    "req": "Python, SQL, PostgreSQL, Power BI, Data Analysis, Git.",
                    "skills": ["Python", "SQL", "PostgreSQL", "Power BI", "Data Analysis", "Git/GitHub"]
                }
            ]
            for item in raw_jobs[:limit]:
                key = NormalizedJob.generate_job_key(self.name, item["company"], item["title"], item["location"])
                jobs.append(NormalizedJob(
                    job_key=key,
                    title=item["title"],
                    company_name=item["company"],
                    location=item["location"],
                    is_remote=item["is_remote"],
                    is_hybrid=item["is_hybrid"],
                    is_internship=item["is_internship"],
                    experience_req=item["exp"],
                    stipend_salary=item["stipend"],
                    source_platform=self.name,
                    job_url=item["job_url"],
                    application_url=item["app_url"],
                    raw_description=item["desc"],
                    responsibilities=item["resp"],
                    requirements=item["req"],
                    required_skills=item["skills"],
                    preferred_skills=["PostgreSQL", "Git/GitHub"],
                    date_posted="3 days ago"
                ))
        except Exception as e:
            logger.error(f"Error fetching from Wellfound: {e}")
        return jobs
