from sqlalchemy.orm import Session
from app.database import models
import datetime

DEFAULT_SKILLS = [
    ("Python", "Programming"),
    ("SQL", "Database"),
    ("PostgreSQL", "Database"),
    ("MySQL", "Database"),
    ("Excel", "Analytics"),
    ("Power BI", "Visualization"),
    ("Tableau", "Visualization"),
    ("Pandas", "Data Processing"),
    ("NumPy", "Data Processing"),
    ("Matplotlib", "Visualization"),
    ("Seaborn", "Visualization"),
    ("Jupyter Notebook", "Tools"),
    ("Data Cleaning", "Analytics"),
    ("Data Analysis", "Analytics"),
    ("Data Visualization", "Visualization"),
    ("ETL", "Data Engineering"),
    ("Apache Airflow", "Data Engineering"),
    ("Git/GitHub", "Tools")
]

DEFAULT_PROJECTS = [
    {
        "name": "SkyMetrics",
        "description": "Cloud-based data pipeline & analytics platform processing high-volume metric feeds. Built end-to-end automated ETL workflows using Apache Airflow and PostgreSQL, surfacing key business KPIs on an interactive Power BI dashboard.",
        "technologies": "Python, SQL, PostgreSQL, Apache Airflow, Power BI, Git",
        "github_url": "https://github.com/Hameeem/SkyMetrics",
        "demo_url": "https://skymetrics.demo.app"
    },
    {
        "name": "DataflowX",
        "description": "Automated ETL workflow & real-time data processing engine. Performed deep data cleaning and aggregation on raw datasets using Pandas and NumPy, storing structured outputs in MySQL for interactive Tableau visualizations.",
        "technologies": "Python, Pandas, NumPy, MySQL, Tableau, Data Analysis",
        "github_url": "https://github.com/Hameeem/DataflowX",
        "demo_url": "https://dataflowx.demo.app"
    },
    {
        "name": "Netflix Dashboard",
        "description": "Interactive exploratory data analysis & visualization dashboard analyzing 8,000+ streaming titles. Uncovered content trends, genre distributions, and release patterns using Python data analysis and Excel/Power BI reporting.",
        "technologies": "Python, Pandas, Seaborn, Excel, Power BI, Data Visualization",
        "github_url": "https://github.com/Hameeem/Netflix-Dashboard",
        "demo_url": "https://netflix-analytics.demo.app"
    }
]

MASTER_RESUME_TEXT = """# HAMEEM
**Data Analyst Intern | Computer Science Student**
Bangalore, Karnataka, India | Email: hameem@example.com | Phone: +91 9876543210
[LinkedIn](https://linkedin.com/in/hameem-da) | [GitHub](https://github.com/Hameeem) | [Portfolio](https://hameem.dev)

---

## PROFESSIONAL SUMMARY
Dedicated Computer Science student with strong expertise in Data Analytics, SQL query optimization, Python data processing, and Power BI visualization. Passionate about leveraging data pipelines, ETL tools, and statistical analysis to drive actionable business insights. Looking for a Remote / Work From Home Data Analyst Internship.

---

## EDUCATION
**B.Tech in Computer Science & Engineering** | CGPA: 8.8 / 10.0 (Expected 2026)
*Relevant Coursework:* Data Structures & Algorithms, Database Management Systems (DBMS), SQL, Data Analysis, Statistics, Object-Oriented Programming.

---

## TECHNICAL SKILLS
- **Languages & Databases:** Python, SQL (PostgreSQL, MySQL), Excel
- **Data Analytics & Tools:** Pandas, NumPy, Data Cleaning, Data Analysis, Data Visualization, Jupyter Notebook
- **Visualization:** Power BI, Tableau, Matplotlib, Seaborn
- **Data Engineering:** ETL, Apache Airflow, Git/GitHub

---

## FEATURED PROJECTS

### SkyMetrics — Cloud Analytics & Pipeline Platform
- Built end-to-end automated ETL workflows using **Apache Airflow**, extracting and transforming 50K+ daily log events into **PostgreSQL**.
- Designed interactive **Power BI** dashboards tracking key operational KPIs, reducing executive report generation time by 40%.
- Applied advanced **SQL** queries (window functions, subqueries, complex joins) for data aggregation and validation.

### DataflowX — Automated Data Processing & Visualization Engine
- Developed custom data cleaning pipelines using **Python (Pandas, NumPy)** to normalize unstructured datasets across 15+ sources.
- Integrated cleaned dataset with **MySQL** and authored **Tableau** visualizations to highlight metric variances.
- Engineered automated data quality checks, eliminating duplicate entries and ensuring 99.5% data accuracy.

### Netflix Content Analytics & Executive Dashboard
- Conducted Exploratory Data Analysis (EDA) on 8,000+ streaming entries using **Pandas**, **Seaborn**, and **Matplotlib**.
- Built an interactive **Excel** & **Power BI** dashboard showcasing global genre distribution, rating trends, and regional content expansion.
- Documented findings in a structured technical report highlighting content acquisition recommendations.
"""

def seed_default_user_and_profile(db: Session) -> models.Profile:
    existing_profile = db.query(models.Profile).first()
    if existing_profile:
        return existing_profile
        
    user = models.User(
        email="hameem@example.com",
        name="Hameem"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    profile = models.Profile(
        user_id=user.id,
        full_name="Hameem",
        email="hameem@example.com",
        phone="+91 9876543210",
        city="Bangalore",
        state="Karnataka",
        country="India",
        linkedin_url="https://linkedin.com/in/hameem-da",
        github_url="https://github.com/Hameeem",
        portfolio_url="https://hameem.dev",
        degree="B.Tech in Computer Science & Engineering",
        university="Indian University",
        branch="Computer Science",
        graduation_year=2026,
        cgpa="8.8 / 10.0",
        relevant_coursework="Data Structures, DBMS, SQL, Data Analysis, Statistics",
        target_role="Data Analyst Intern",
        preferred_locations=["Remote", "Work From Home", "India"],
        exclude_onsite=False,
        min_match_score=75,
        max_exp_years=1,
        application_mode="APPROVAL_REQUIRED",
        daily_limit=10
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    # Add Skills
    for skill_name, category in DEFAULT_SKILLS:
        skill = models.Skill(profile_id=profile.id, name=skill_name, category=category)
        db.add(skill)
        
    # Add Projects
    for proj_data in DEFAULT_PROJECTS:
        proj = models.Project(
            profile_id=profile.id,
            name=proj_data["name"],
            description=proj_data["description"],
            technologies=proj_data["technologies"],
            github_url=proj_data["github_url"],
            demo_url=proj_data["demo_url"]
        )
        db.add(proj)
        
    # Add Master Resume
    master_resume = models.Resume(
        profile_id=profile.id,
        title="Master Resume — Hameem Data Analyst",
        resume_type="MASTER",
        content_markdown=MASTER_RESUME_TEXT
    )
    db.add(master_resume)
    
    # Initialize default Job Sources
    default_sources = [
        "LinkedIn Jobs", "Naukri", "Indeed", "Internshala", 
        "Wellfound", "Glassdoor", "Foundit", "Cutshort"
    ]
    for source_name in default_sources:
        source = models.JobSource(name=source_name, is_enabled=True)
        db.add(source)
        
    db.commit()
    db.refresh(profile)
    return profile
