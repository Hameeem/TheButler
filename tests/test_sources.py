import pytest
from app.sources.linkedin import LinkedInSource
from app.sources.naukri import NaukriSource

def test_linkedin_source_fetch():
    src = LinkedInSource()
    jobs = src.fetch_jobs(limit=2)
    assert len(jobs) > 0
    assert jobs[0].source_platform == "LinkedIn Jobs"
    assert jobs[0].job_key is not None

def test_naukri_source_fetch():
    src = NaukriSource()
    jobs = src.fetch_jobs(limit=2)
    assert len(jobs) > 0
    assert jobs[0].source_platform == "Naukri"
