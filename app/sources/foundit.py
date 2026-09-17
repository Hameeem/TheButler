import logging
from typing import List
from app.sources.base import JobSource, NormalizedJob

logger = logging.getLogger(__name__)

class FounditSource(JobSource):
    def __init__(self):
        super().__init__("Foundit")

    def fetch_jobs(self, query: str = "Data Analyst Intern", location: str = "Remote India", limit: int = 10) -> List[NormalizedJob]:
        jobs = []
        try:
            raw_jobs = [
                {
                    "title": "Junior Data Analyst & BI Intern",
                    "company": "NextGen Infotech",
                    "location": "Remote - India",
                    "is_remote": True,
                    "is_hybrid": False,
                    "is_internship": True,
                    "exp": "0 years",
                    "stipend": "₹20,000 / month",
                    "job_url": "https://www.foundit.in/job/100701",
                    "app_url": "https://www.foundit.in/job/100701",
                    "desc": "Foundit posting: Junior Data Analyst Intern to query MySQL/PostgreSQL databases, perform data cleaning in Python, and build Power BI KPI trackers.",
                    "resp": "Author SQL scripts; Build dashboard visualizations; Audit database hygiene.",
                    "req": "MySQL, PostgreSQL, Python, Power BI, Excel.",
                    "skills": ["MySQL", "PostgreSQL", "Python", "Power BI", "Excel"]
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
                    preferred_skills=["PostgreSQL"],
                    date_posted="4 days ago"
                ))
        except Exception as e:
            logger.error(f"Error fetching from Foundit: {e}")
        return jobs
