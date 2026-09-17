import pytest
from app.sources.base import NormalizedJob
from app.agents.fraud_detector import FraudDetector

def test_fraud_detector_scam():
    scam_job = NormalizedJob(
        job_key="scam_key",
        title="Data Entry Intern",
        company_name="Unknown Scammer",
        location="Remote",
        source_platform="Unknown",
        job_url="http://scam-link.com",
        raw_description="Earn 1 lakh daily. Requires registration fee of 500 rs pay upfront.",
        stipend_salary="₹100,000"
    )
    
    status, flags, audit = FraudDetector.analyze_job(scam_job)
    assert status == "SUSPICIOUS"
    assert len(flags) > 0
