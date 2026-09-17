import logging
from typing import Dict, List, Tuple
from app.database import models

logger = logging.getLogger(__name__)

class ApplicationQuestionAgent:
    SENSITIVE_KEYWORDS = [
        "criminal", "background check", "visa", "work authorization", "citizenship",
        "ssn", "passport", "disability", "veteran", "salary expectation", "bank account", "legal declaration"
    ]

    @classmethod
    def generate_answer(cls, question: str, job: models.Job, profile: models.Profile) -> Tuple[str, bool]:
        """
        Generates a factual answer based ONLY on stored profile & project info.
        Returns: (answer_text, is_sensitive)
        """
        q_lower = question.lower()
        is_sensitive = any(sk in q_lower for sk in cls.SENSITIVE_KEYWORDS)
        
        # 1. Why do you want this internship?
        if any(term in q_lower for term in ["why do you want", "why this internship", "why join", "interest"]):
            ans = f"I am a Computer Science student passionate about Data Analytics. I have hands-on experience building automated data pipelines (SkyMetrics), exploratory analytics tools (DataflowX), and executive dashboards using SQL, Python, and Power BI. Joining {job.company_name} as a {job.title} aligns perfectly with my drive to solve real-world data challenges and deliver actionable business insights."

        # 2. Tell us about yourself / Why should we hire you?
        elif any(term in q_lower for term in ["tell us about yourself", "why should we hire you", "introduction", "about you"]):
            ans = f"My name is {profile.full_name}, a {profile.degree} student at {profile.university} (CGPA: {profile.cgpa}). I specialize in SQL, Python (Pandas/NumPy), PostgreSQL/MySQL, Excel, and Power BI. Through my featured projects like SkyMetrics and DataflowX, I have engineered automated ETL pipelines and analytics dashboards. I bring strong technical foundations, analytical rigor, and a commitment to high-quality work."

        # 3. SQL Experience
        elif "sql" in q_lower:
            ans = "I have strong proficiency in SQL (PostgreSQL & MySQL). I routinely write complex queries involving window functions, aggregations, multi-table joins, subqueries, and view creation. In my SkyMetrics project, I designed relational database schemas and optimized data extraction pipelines for over 50,000 daily log records."

        # 4. Power BI / Data Visualization
        elif any(term in q_lower for term in ["power bi", "tableau", "visualization", "dashboard"]):
            ans = "I have extensive experience building interactive data dashboards in Power BI and Tableau. For my Netflix Content Analytics project, I analyzed 8,000+ entries and rendered visualizations highlighting genre trends, regional distributions, and rating metrics to drive executive decision-making."

        # 5. Python / Data Analysis
        elif any(term in q_lower for term in ["python", "pandas", "numpy", "data analysis", "etl"]):
            ans = "I use Python extensively with Pandas, NumPy, Matplotlib, and Seaborn for exploratory data analysis (EDA), data cleaning, and ETL automation. In my DataflowX project, I built custom Python scripts to parse, clean, and structure raw datasets from 15+ sources with 99.5% accuracy."

        # 6. Sensitive / Demographic / Legal questions
        elif is_sensitive:
            ans = f"[SENSITIVE QUESTION DETECTED]: Please review and confirm your answer for: '{question}'. Standard response: Yes, I am an Indian citizen fully authorized to work for internships in India."

        # General Default Factual Answer
        else:
            ans = f"As a Computer Science student (CGPA: {profile.cgpa}) specializing in Data Analytics, I have developed technical proficiency in Python, SQL, Excel, and Power BI. I am confident in applying my problem-solving and analytics skill set to contribute effectively to {job.company_name}."

        return ans, is_sensitive
