import logging
from typing import List
from app.sources.base import JobSource, NormalizedJob

logger = logging.getLogger(__name__)

class IndeedSource(JobSource):
    def __init__(self):
        super().__init__("Indeed")

    def fetch_jobs(self, query: str = "Data Analyst Intern", location: str = "Remote India", limit: int = 10) -> List[NormalizedJob]:
        jobs = []
        try:
            raw_jobs = [
                {
                    "title": "Data Analytics Intern (WFH)",
                    "company": "Apex Insights Lab",
                    "location": "Remote, India",
                    "is_remote": True,
                    "is_hybrid": False,
                    "is_internship": True,
                    "exp": "0-1 years",
                    "stipend": "₹28,000 / month",
                    "job_url": "https://in.indeed.com/viewjob?jk=100301",
                    "app_url": "https://in.indeed.com/viewjob?jk=100301",
                    "desc": "Indeed Remote posting: Data Analytics Intern wanted to work on Python data analysis, MySQL databases, and Tableau dashboards.",
                    "resp": "Wrangle structured and unstructured datasets; Build interactive Tableau reports; Run SQL audits.",
                    "req": "Python, SQL, MySQL, Tableau, Pandas, NumPy.",
                    "skills": ["Python", "SQL", "MySQL", "Tableau", "Pandas", "NumPy"]
                },
                {
                    "title": "Business Analyst Intern - Data Focus",
                    "company": "GrowthPact Digital",
                    "location": "Hybrid (Bangalore / WFH)",
                    "is_remote": False,
                    "is_hybrid": True,
                    "is_internship": True,
                    "exp": "Fresher",
                    "stipend": "₹20,000 / month",
                    "job_url": "https://in.indeed.com/viewjob?jk=100302",
                    "app_url": "https://growthpact.com/apply/ba-intern",
                    "desc": "Analytic business analyst intern position combining data transformation with client metric reporting.",
                    "resp": "Map business rules into SQL transformations; Build Power BI reports; Document data dictionaries.",
                    "req": "SQL, Excel, Power BI, Data Cleaning, Python basics.",
                    "skills": ["SQL", "Excel", "Power BI", "Data Cleaning", "Python"]
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
                    preferred_skills=["Tableau", "Pandas"],
                    date_posted="2 days ago"
                ))
        except Exception as e:
            logger.error(f"Error fetching from Indeed: {e}")
        return jobs
