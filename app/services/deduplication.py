from typing import List, Dict
import difflib
from app.sources.base import NormalizedJob

class DeduplicationService:
    @staticmethod
    def calculate_similarity(s1: str, s2: str) -> float:
        if not s1 or not s2:
            return 0.0
        return difflib.SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

    @classmethod
    def group_duplicates(cls, jobs: List[NormalizedJob]) -> List[NormalizedJob]:
        """
        Deduplicates a list of NormalizedJob instances.
        If a job is found on multiple platforms (e.g., LinkedIn and Naukri for same company + title),
        merges platform references into the canonical job object.
        """
        unique_jobs: List[NormalizedJob] = []
        
        for job in jobs:
            is_dup = False
            for existing in unique_jobs:
                # Same company and title match (> 85% similarity)
                company_sim = cls.calculate_similarity(job.company_name, existing.company_name)
                title_sim = cls.calculate_similarity(job.title, existing.title)
                
                if company_sim >= 0.8 and title_sim >= 0.8:
                    is_dup = True
                    # Combine source platform info if unique
                    if job.source_platform not in existing.source_platform:
                        existing.source_platform = f"{existing.source_platform}, {job.source_platform}"
                    # Merge unique required skills
                    for sk in job.required_skills:
                        if sk not in existing.required_skills:
                            existing.required_skills.append(sk)
                    break
            if not is_dup:
                unique_jobs.append(job)
                
        return unique_jobs
