import logging
from typing import List
from app.sources.base import JobSource, NormalizedJob

logger = logging.getLogger(__name__)

class LinkedInSource(JobSource):
    def __init__(self):
        super().__init__("LinkedIn Jobs")

    def fetch_jobs(self, query: str = "Data Analyst Intern", location: str = "Remote India", limit: int = 10) -> List[NormalizedJob]:
        jobs = []
        try:
            # Simulated / structured public LinkedIn jobs feed for Data Analyst Internships
            raw_jobs = [
                {
                    "title": "Data Analyst Intern - Remote India",
                    "company": "TechMetrics Analytics",
                    "location": "Remote, India",
                    "is_remote": True,
                    "is_hybrid": False,
                    "is_internship": True,
                    "exp": "0-1 years",
                    "stipend": "₹25,000 - ₹35,000 / month",
                    "job_url": "https://www.linkedin.com/jobs/view/100101",
                    "app_url": "https://www.linkedin.com/jobs/view/100101",
                    "desc": "Seeking a Data Analyst Intern proficient in SQL, Python, and Power BI. You will build automated dashboards, perform data cleaning on customer churn logs, and analyze revenue metrics.",
                    "resp": "Write complex SQL queries; Build Power BI reports; Clean datasets with Pandas; Present analytics to team.",
                    "req": "Strong knowledge of SQL, Python, Excel, Power BI; Pursuing CS or related degree.",
                    "skills": ["Python", "SQL", "Power BI", "Excel", "Pandas", "Data Cleaning"]
                },
                {
                    "title": "Junior Data Analytics Intern",
                    "company": "InnoData Solutions",
                    "location": "Bangalore (Remote Available)",
                    "is_remote": True,
                    "is_hybrid": True,
                    "is_internship": True,
                    "exp": "Fresher",
                    "stipend": "₹20,000 / month",
                    "job_url": "https://www.linkedin.com/jobs/view/100102",
                    "app_url": "https://www.linkedin.com/jobs/view/100102",
                    "desc": "Join our data science & analytics team as a Junior Data Analyst Intern. Focus on PostgreSQL query optimization, ETL automation, and Tableau visualization.",
                    "resp": "Optimize DB queries; Maintain ETL scripts with Airflow; Build Tableau dashboards.",
                    "req": "PostgreSQL, MySQL, Python, Tableau, ETL fundamentals, Git.",
                    "skills": ["Python", "SQL", "PostgreSQL", "MySQL", "Tableau", "ETL", "Git/GitHub"]
                },
                {
                    "title": "Business Intelligence & Data Analyst Intern",
                    "company": "CloudSphere India",
                    "location": "Remote, India",
                    "is_remote": True,
                    "is_hybrid": False,
                    "is_internship": True,
                    "exp": "0-1 years",
                    "stipend": "₹30,000 / month",
                    "job_url": "https://www.linkedin.com/jobs/view/100103",
                    "app_url": "https://cloudsphere.io/careers/apply/bi-intern",
                    "desc": "Work remotely with our global BI engineering team. You will build executive dashboards, transform raw data pipelines, and run statistical exploratory data analysis.",
                    "resp": "Develop Power BI dashboards; Clean messy datasets; Generate automated monthly KPI reports.",
                    "req": "Python, SQL, Power BI, Excel, Pandas, NumPy, Seaborn.",
                    "skills": ["Python", "SQL", "Power BI", "Excel", "Pandas", "NumPy", "Seaborn"]
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
                    preferred_skills=["Airflow", "PostgreSQL"],
                    date_posted="1 day ago"
                ))
        except Exception as e:
            logger.error(f"Error fetching from LinkedIn Jobs: {e}")
        return jobs
