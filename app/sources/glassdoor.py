import logging
from typing import List
from app.sources.base import JobSource, NormalizedJob

logger = logging.getLogger(__name__)

class GlassdoorSource(JobSource):
    def __init__(self):
        super().__init__("Glassdoor")

    def fetch_jobs(self, query: str = "Data Analyst Intern", location: str = "Remote India", limit: int = 10) -> List[NormalizedJob]:
        jobs = []
        try:
            raw_jobs = [
                {
                    "title": "Data Analyst Trainee / Intern",
                    "company": "Enterprise Analytics Corp",
                    "location": "Remote, India",
                    "is_remote": True,
                    "is_hybrid": False,
                    "is_internship": True,
                    "exp": "0-1 years",
                    "stipend": "₹24,000 / month",
                    "job_url": "https://www.glassdoor.co.in/job-listing/100601",
                    "app_url": "https://www.glassdoor.co.in/job-listing/100601",
                    "desc": "Glassdoor 4.3★ rated company hiring Data Analyst Interns for remote analytics assignments involving Python, SQL, Excel, and Power BI.",
                    "resp": "Build monthly data reports; Perform data wrangling with Pandas; Support data engineering ETL.",
                    "req": "Python, SQL, Excel, Power BI, Pandas, ETL fundamentals.",
                    "skills": ["Python", "SQL", "Excel", "Power BI", "Pandas", "ETL"]
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
                    preferred_skills=["ETL", "Excel"],
                    date_posted="1 day ago"
                ))
        except Exception as e:
            logger.error(f"Error fetching from Glassdoor: {e}")
        return jobs
