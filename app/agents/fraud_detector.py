from typing import Dict, List, Tuple
from app.sources.base import NormalizedJob

class FraudDetector:
    SUSPICIOUS_KEYWORDS = [
        "registration fee", "training fee", "security deposit", "pay to apply",
        "laptop deposit", "telegram recruitment", "whatsapp only", "earn 1 lakh daily",
        "no experience 50k stipend", "data entry typist", "copy paste job",
        "pay upfront", "purchase equipment", "gift card"
    ]

    @classmethod
    def analyze_job(cls, job: NormalizedJob) -> Tuple[str, List[str], Dict[str, str]]:
        """
        Analyzes job for fraud and scam signals.
        Returns: (quality_status, flags_list, audit_dict)
        quality_status: VERIFIED, LOW_RISK, REVIEW, SUSPICIOUS
        """
        flags = []
        text_content = f"{job.title} {job.raw_description} {job.responsibilities} {job.requirements} {job.stipend_salary}".lower()
        
        # Check suspicious keywords
        for kw in cls.SUSPICIOUS_KEYWORDS:
            if kw in text_content:
                flags.append(f"Contains suspicious phrase: '{kw}'")
                
        # Check payment request
        payment_requested = any(p in text_content for p in ["registration fee", "training fee", "deposit", "pay upfront"])
        if payment_requested:
            flags.append("EXPLICIT PAYMENT / FEE DEMAND DETECTED")

        # Check contact channels
        if "telegram" in text_content and "linkedin" not in job.job_url:
            flags.append("Recruitment via Telegram only")
        if "whatsapp" in text_content and "company" not in text_content:
            flags.append("Recruitment via WhatsApp only")

        # Determine status
        if payment_requested or len(flags) >= 2:
            status = "SUSPICIOUS"
        elif len(flags) == 1:
            status = "REVIEW"
        elif any(domain in job.job_url for domain in ["linkedin.com", "naukri.com", "indeed.com", "internshala.com", "wellfound.com", "glassdoor.co.in", "foundit.in", "cutshort.io"]):
            status = "VERIFIED"
        else:
            status = "LOW_RISK"

        audit = {
            "Company Verified": "Yes" if status in ["VERIFIED", "LOW_RISK"] else "Needs Review",
            "Application Domain": "Legitimate" if "https://" in job.job_url else "Unverified",
            "Payment Requested": "Yes (Scam)" if payment_requested else "No",
            "Suspicious Signals": ", ".join(flags) if flags else "None detected",
            "Quality Status": status
        }

        return status, flags, audit
