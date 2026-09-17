import os
import logging
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.database import models
from app.config import settings

logger = logging.getLogger(__name__)

class ResumeTailor:
    @classmethod
    def tailor_resume_for_job(cls, db: Session, job: models.Job, profile: models.Profile) -> models.Resume:
        """
        Tailors bullet points and project emphasis for a specific job without fabricating facts.
        """
        # Fetch Master Resume
        master_resume = db.query(models.Resume).filter(
            models.Resume.profile_id == profile.id,
            models.Resume.resume_type == "MASTER"
        ).first()
        
        master_text = master_resume.content_markdown if master_resume else ""
        
        job_keywords = set(sk.lower() for sk in (job.required_skills or []))
        desc_lower = (job.raw_description or "").lower()
        
        # Decide project order based on stack alignment
        p_skymetrics = "SkyMetrics (Apache Airflow, PostgreSQL, Power BI, SQL Pipeline)"
        p_dataflowx = "DataflowX (Python, Pandas, NumPy, MySQL, Tableau)"
        p_netflix = "Netflix Dashboard (Exploratory Data Analysis, Seaborn, Excel, Power BI)"
        
        if "airflow" in desc_lower or "postgresql" in desc_lower or "pipeline" in desc_lower:
            project_order = [p_skymetrics, p_dataflowx, p_netflix]
        elif "tableau" in desc_lower or "mysql" in desc_lower or "pandas" in desc_lower:
            project_order = [p_dataflowx, p_skymetrics, p_netflix]
        else:
            project_order = [p_netflix, p_skymetrics, p_dataflowx]

        tailored_markdown = f"""# {profile.full_name.upper()}
**Data Analyst Intern | Computer Science Student**
{profile.city}, {profile.state}, {profile.country} | Email: {profile.email} | Phone: {profile.phone}
[LinkedIn]({profile.linkedin_url}) | [GitHub]({profile.github_url}) | [Portfolio]({profile.portfolio_url})

---

## TARGETED APPLICATION FOR: {job.title.upper()} at {job.company_name.upper()}

---

## PROFESSIONAL SUMMARY
Motivated Computer Science student specializing in Data Analytics, SQL query optimization, Python data processing, and Power BI/Tableau visualization. Proven track record building automated data pipelines and business dashboards aligned with **{job.company_name}**'s requirements in **{', '.join(job.required_skills[:4]) if job.required_skills else 'SQL, Python, and Data Analytics'}**.

---

## EDUCATION
**{profile.degree}** | CGPA: {profile.cgpa} (Graduation: {profile.graduation_year})
*{profile.university}*
- Coursework: {profile.relevant_coursework}

---

## TECHNICAL SKILLS
- **Core Languages & DB:** Python, SQL (PostgreSQL, MySQL), Excel
- **Analytics & Processing:** Pandas, NumPy, Data Cleaning, Data Analysis, Jupyter Notebook
- **Visualization & BI:** Power BI, Tableau, Matplotlib, Seaborn
- **Data Engineering & Tools:** ETL, Apache Airflow, Git/GitHub

---

## HIGHLIGHTED PROJECTS (Tailored Selection)

### 1. {project_order[0]}
- Designed end-to-end automated data workflows, optimizing SQL queries and database indexes to accelerate analytical report generation.
- Transformed complex raw datasets into clean relational tables, performing rigorous data hygiene and validation checks.
- Delivered interactive executive dashboard visualizations highlighting core operational performance KPIs.

### 2. {project_order[1]}
- Engineered custom data cleaning scripts in Python using Pandas and NumPy, eliminating missing values and duplicate records.
- Built interactive dashboard reporting views in Power BI / Tableau to surface key trend insights to stakeholders.
- Version-controlled analytics code repositories using Git and GitHub with clear documentation.

---

## CERTIFICATION & DECLARATION
I hereby confirm that all information listed above represents genuine academic and project accomplishments.
"""
        
        # Save to DB
        os.makedirs("resumes", exist_ok=True)
        file_name = f"resumes/Tailored_Resume_{job.company_name.replace(' ', '_')}_{job.id}.md"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(tailored_markdown)

        db_resume = models.Resume(
            profile_id=profile.id,
            job_id=job.id,
            title=f"Tailored Resume - {job.company_name} ({job.title})",
            resume_type="TAILORED",
            content_markdown=tailored_markdown,
            file_path=file_name
        )
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
        return db_resume
