import logging
from typing import List
from app.sources.base import JobSource, NormalizedJob

logger = logging.getLogger(__name__)

class InternshalaSource(JobSource):
    def __init__(self):
        super().__init__("Internshala")

    def fetch_jobs(self, query: str = "Data Analyst Intern", location: str = "Remote India", limit: int = 10) -> List[NormalizedJob]:
        jobs = []
        try:
            raw_jobs = [
                {
                    "title": "Data Science & Analytics Intern",
                    "company": "Krypton AI Labs",
                    "location": "Work From Home",
                    "is_remote": True,
                    "is_hybrid": False,
                    "is_internship": True,
                    "exp": "0 years",
                    "stipend": "₹25,000 / month",
                    "job_url": "https://internshala.com/internship/detail/data-analytics-internship-in-wfh-100401",
                    "app_url": "https://internshala.com/internship/detail/data-analytics-internship-in-wfh-100401",
                    "desc": "Internshala Work From Home Internship: Perform exploratory data analysis using Python, Pandas, Matplotlib, and SQL for machine learning data preprocessing.",
                    "resp": "Conduct exploratory data analysis; Write SQL data queries; Prepare reports in Jupyter Notebook.",
                    "req": "Python, SQL, Pandas, NumPy, Matplotlib, Seaborn, Jupyter Notebook.",
                    "skills": ["Python", "SQL", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter Notebook"]
                },
                {
                    "title": "Data Analyst Internship",
                    "company": "EduMetrics India",
                    "location": "Work From Home",
                    "is_remote": True,
                    "is_hybrid": False,
                    "is_internship": True,
                    "exp": "Fresher",
                    "stipend": "₹15,000 - ₹20,000 / month",
                    "job_url": "https://internshala.com/internship/detail/data-analyst-internship-in-wfh-100402",
                    "app_url": "https://internshala.com/internship/detail/data-analyst-internship-in-wfh-100402",
                    "desc": "Remote internship opportunity focusing on educational student performance dataset analysis using Excel and SQL.",
                    "resp": "Clean student dataset files; Create Excel dashboards; Run SQL summaries.",
                    "req": "Excel, SQL, Data Cleaning, Data Visualization.",
                    "skills": ["Excel", "SQL", "Data Cleaning", "Data Visualization"]
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
                    preferred_skills=["Jupyter Notebook", "Pandas"],
                    date_posted="Today"
                ))
        except Exception as e:
            logger.error(f"Error fetching from Internshala: {e}")
        return jobs
