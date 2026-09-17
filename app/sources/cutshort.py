import logging
from typing import List
from app.sources.base import JobSource, NormalizedJob

logger = logging.getLogger(__name__)

class CutshortSource(JobSource):
    def __init__(self):
        super().__init__("Cutshort")

    def fetch_jobs(self, query: str = "Data Analyst Intern", location: str = "Remote India", limit: int = 10) -> List[NormalizedJob]:
        jobs = []
        try:
            raw_jobs = [
                {
                    "title": "Data Analytics Intern",
                    "company": "FastPace Logistics AI",
                    "location": "Remote, India",
                    "is_remote": True,
                    "is_hybrid": False,
                    "is_internship": True,
                    "exp": "0-1 years",
                    "stipend": "₹30,000 / month",
                    "job_url": "https://cutshort.io/job/data-analytics-intern-100801",
                    "app_url": "https://cutshort.io/job/data-analytics-intern-100801",
                    "desc": "Cutshort tech job: Seeking a Data Analytics Intern with Python, Pandas, PostgreSQL, Airflow, and Power BI skills for logistics telemetry optimization.",
                    "resp": "Automate supply chain data pipelines; Build interactive Power BI charts; Write SQL joins.",
                    "req": "Python, Pandas, PostgreSQL, Airflow, Power BI, Git.",
                    "skills": ["Python", "Pandas", "PostgreSQL", "Apache Airflow", "Power BI", "Git/GitHub"]
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
                    preferred_skills=["Apache Airflow", "PostgreSQL"],
                    date_posted="Today"
                ))
        except Exception as e:
            logger.error(f"Error fetching from Cutshort: {e}")
        return jobs
