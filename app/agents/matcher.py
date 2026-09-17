from typing import List, Dict, Any
from app.database import models
from app.sources.base import NormalizedJob

class JobMatcher:
    @classmethod
    def calculate_match(cls, job: NormalizedJob, profile: models.Profile) -> Dict[str, Any]:
        """
        Calculates multi-factor job-profile match scores and returns detailed breakdown.
        """
        user_skills = set(s.name.lower() for s in profile.skills)
        user_projects = [p.name.lower() + " " + p.technologies.lower() for p in profile.projects]
        
        # 1. Role Match (20%)
        title_lower = job.title.lower()
        target_role_lower = profile.target_role.lower()
        if target_role_lower in title_lower or "data analyst" in title_lower or "analytics intern" in title_lower:
            role_score = 95.0
        elif "business intelligence" in title_lower or "bi intern" in title_lower or "data science intern" in title_lower:
            role_score = 88.0
        elif "reporting analyst" in title_lower or "business analyst" in title_lower:
            role_score = 80.0
        else:
            role_score = 60.0

        # 2. Skill Match (30%)
        job_req_skills = set(sk.lower() for sk in job.required_skills)
        matched_skills = []
        missing_skills = []

        if job_req_skills:
            for job_sk in job_req_skills:
                # Fuzzy skill match check
                if any(u_sk in job_sk or job_sk in u_sk for u_sk in user_skills):
                    matched_skills.append(job_sk.capitalize())
                else:
                    missing_skills.append(job_sk.capitalize())
            skill_score = (len(matched_skills) / len(job_req_skills)) * 100.0
        else:
            # Fallback keyword extraction from description
            desc_lower = job.raw_description.lower()
            matched_count = sum(1 for u_sk in user_skills if u_sk in desc_lower)
            matched_skills = [u_sk.title() for u_sk in user_skills if u_sk in desc_lower]
            skill_score = min(100.0, (matched_count / 5.0) * 100.0)

        # 3. Experience Match (15%)
        exp_text = (job.experience_req or "").lower()
        if any(term in exp_text for term in ["fresher", "0", "0-1", "0 to 1", "intern", "student"]):
            exp_score = 100.0
        elif "1-2" in exp_text or "1 year" in exp_text:
            exp_score = 85.0
        else:
            exp_score = 60.0

        # 4. Education Match (10%)
        edu_score = 100.0  # CS B.Tech student fits virtually all analyst intern roles

        # 5. Location & Remote Match (15%)
        if job.is_remote:
            remote_score = 100.0
            location_score = 100.0
        elif job.is_hybrid:
            remote_score = 75.0
            location_score = 85.0
        else:
            remote_score = 50.0 if not profile.exclude_onsite else 0.0
            location_score = 70.0

        # 6. Project Relevance Match (10%)
        project_hits = 0
        for proj_text in user_projects:
            if any(req.lower() in proj_text for req in job_req_skills):
                project_hits += 1
        project_score = min(100.0, max(70.0, project_hits * 30.0))

        # Overall Weighted Score Calculation
        overall_score = (
            (role_score * 0.20) +
            (skill_score * 0.30) +
            (exp_score * 0.15) +
            (edu_score * 0.10) +
            (location_score * 0.05) +
            (remote_score * 0.10) +
            (project_score * 0.10)
        )
        overall_score = round(overall_score, 1)

        # Generate Explanation
        explanation_lines = [
            f"Role Match: {role_score}%",
            f"Skill Match: {round(skill_score, 1)}%",
            f"Experience Match: {exp_score}%",
            f"Education Match: {edu_score}%",
            f"Location Match: {location_score}%",
            f"Remote Preference: {remote_score}%",
            f"Project Relevance: {round(project_score, 1)}%"
        ]

        return {
            "role_score": role_score,
            "skill_score": round(skill_score, 1),
            "experience_score": exp_score,
            "education_score": edu_score,
            "location_score": location_score,
            "remote_score": remote_score,
            "project_score": round(project_score, 1),
            "overall_score": overall_score,
            "strong_matches": matched_skills if matched_skills else ["Python", "SQL", "Excel"],
            "missing_skills": missing_skills,
            "match_explanation": "\n".join(explanation_lines)
        }
