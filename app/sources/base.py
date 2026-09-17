from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel, Field
import hashlib

class NormalizedJob(BaseModel):
    job_key: str = Field(description="Unique hash or platform ID identifying the job listing")
    title: str
    company_name: str
    location: str
    is_remote: bool = False
    is_hybrid: bool = False
    is_internship: bool = True
    experience_req: str = "0-1 years"
    stipend_salary: Optional[str] = None
    source_platform: str
    job_url: str
    application_url: Optional[str] = None
    raw_description: str
    responsibilities: Optional[str] = ""
    requirements: Optional[str] = ""
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    date_posted: Optional[str] = "Recently"
    
    @staticmethod
    def generate_job_key(platform: str, company: str, title: str, location: str) -> str:
        raw_str = f"{platform.lower()}:{company.lower()}:{title.lower()}:{location.lower()}"
        return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()[:16]

class JobSource(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def fetch_jobs(self, query: str = "Data Analyst Intern", location: str = "Remote India", limit: int = 10) -> List[NormalizedJob]:
        """
        Fetch and normalize jobs from this platform.
        Must handle exceptions gracefully and return a list of NormalizedJob.
        """
        pass
