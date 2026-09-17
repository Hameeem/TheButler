import pytest
from app.sources.base import NormalizedJob
from app.services.deduplication import DeduplicationService

def test_deduplication():
    job1 = NormalizedJob(
        job_key="k1",
        title="Data Analyst Intern",
        company_name="Acme Analytics",
        location="Remote, India",
        source_platform="LinkedIn Jobs",
        job_url="https://linkedin.com/1",
        raw_description="Python SQL Power BI"
    )
    job2 = NormalizedJob(
        job_key="k2",
        title="Data Analyst Intern",
        company_name="Acme Analytics",
        location="Remote, India",
        source_platform="Naukri",
        job_url="https://naukri.com/1",
        raw_description="Python SQL Power BI"
    )
    
    unique = DeduplicationService.group_duplicates([job1, job2])
    assert len(unique) == 1
    assert "LinkedIn Jobs" in unique[0].source_platform
    assert "Naukri" in unique[0].source_platform
