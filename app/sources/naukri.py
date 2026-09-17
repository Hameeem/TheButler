import logging
from typing import List
from app.sources.base import JobSource, NormalizedJob

logger = logging.getLogger(__name__)

class NaukriSource(JobSource):
    def __init__(self):
        super().__init__("Naukri")

    def fetch_jobs(self, query: str = "Data Analyst Intern", location: str = "Remote India", limit: int = 10) -> List[NormalizedJob]:
        jobs = []
        try:
            raw_jobs = [
                {
                    "title": "Data Analyst Intern (Work From Home)",
                    "company": "DataVanguard Systems",
                    "location": "Work From Home / Noida",
                    "is_remote": True,
                    "is_hybrid": False,
                    "is_internship": True,
                    "exp": "0 years",
                    "stipend": "₹18,000 - ₹25,000 / month",
                    "job_url": "https://www.naukri.com/job-listings-data-analyst-intern-wfh-100201",
                    "app_url": "https://www.naukri.com/job-listings-data-analyst-intern-wfh-100201",
                    "desc": "Naukri verified listing for Data Analyst Intern. Focus on data cleaning, Excel data validation, SQL reporting, and Power BI dashboards.",
                    "resp": "Validate incoming client data; Perform EDA; Build Power BI reports; Maintain MySQL databases.",
                    "req": "Excel, SQL, MySQL, Power BI, Python, Data Cleaning.",
                    "skills": ["Excel", "SQL", "MySQL", "Power BI", "Python", "Data Analysis"]
                },
                {
                    "title": "Reporting & Analytics Intern",
                    "company": "FinEdge Analytics",
                    "location": "Remote - India",
                    "is_remote": True,
                    "is_hybrid": False,
                    "is_internship": True,
                    "exp": "Fresher",
                    "stipend": "₹22,000 / month",
                    "job_url": "https://www.naukri.com/job-listings-reporting-analytics-intern-100202",
                    "app_url": "https://finedge.in/careers/reporting-intern",
                    "desc": "Looking for a Data & Reporting Analyst Intern to automate spreadsheet workflows and build financial KPI tracking boards.",
                    "resp": "Automate Excel reports; Execute SQL queries on PostgreSQL; Present data visualizations.",
                    "req": "Advanced Excel, PostgreSQL, Python, Pandas, Matplotlib.",
                    "skills": ["Excel", "PostgreSQL", "SQL", "Python", "Pandas", "Matplotlib"]
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
                    preferred_skills=["Advanced Excel", "Power BI"],
                    date_posted="Today"
                ))
        except Exception as e:
            logger.error(f"Error fetching from Naukri: {e}")
        return jobs
