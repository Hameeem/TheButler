import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    city = Column(String(100), default="Bangalore")
    state = Column(String(100), default="Karnataka")
    country = Column(String(100), default="India")
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    portfolio_url = Column(String(500), nullable=True)
    
    # Education
    degree = Column(String(255), default="B.Tech in Computer Science and Engineering")
    university = Column(String(255), default="Indian Institute of Technology / VTU")
    branch = Column(String(255), default="Computer Science")
    graduation_year = Column(Integer, default=2026)
    cgpa = Column(String(50), default="8.8 / 10.0")
    relevant_coursework = Column(Text, default="Data Structures, Algorithms, Database Management Systems (DBMS), Statistics, Object Oriented Programming")
    
    # Preferences
    target_role = Column(String(255), default="Data Analyst Intern")
    preferred_locations = Column(JSON, default=lambda: ["Remote", "Work From Home", "India"])
    exclude_onsite = Column(Boolean, default=False)
    min_match_score = Column(Integer, default=75)
    max_exp_years = Column(Integer, default=1)
    application_mode = Column(String(50), default="APPROVAL_REQUIRED") # MANUAL, APPROVAL_REQUIRED, AUTOMATIC
    daily_limit = Column(Integer, default=10)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="profile")
    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(100), default="Technical")
    
    profile = relationship("Profile", back_populates="skills")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    technologies = Column(String(500), nullable=False)
    github_url = Column(String(500), nullable=True)
    demo_url = Column(String(500), nullable=True)
    
    profile = relationship("Profile", back_populates="projects")

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    domain = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    verified_status = Column(Boolean, default=True)
    glassdoor_rating = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_key = Column(String(500), unique=True, index=True, nullable=False)  # Normalized unique hash or ID
    title = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=False)
    is_remote = Column(Boolean, default=False)
    is_hybrid = Column(Boolean, default=False)
    is_internship = Column(Boolean, default=True)
    experience_req = Column(String(100), default="0-1 years")
    stipend_salary = Column(String(255), nullable=True)
    
    source_platform = Column(String(100), nullable=False)  # LinkedIn, Naukri, Indeed, etc.
    job_url = Column(String(1000), nullable=False)
    application_url = Column(String(1000), nullable=True)
    
    raw_description = Column(Text, nullable=False)
    responsibilities = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    required_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    
    date_posted = Column(String(100), nullable=True)
    quality_status = Column(String(50), default="VERIFIED")  # VERIFIED, LOW_RISK, REVIEW, SUSPICIOUS
    quality_flags = Column(JSON, default=list)
    canonical_job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True) # For duplicate grouping
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    matches = relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")

class JobSource(Base):
    __tablename__ = "job_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    is_enabled = Column(Boolean, default=True)
    last_run_at = Column(DateTime, nullable=True)
    jobs_found_last_run = Column(Integer, default=0)
    status = Column(String(50), default="ACTIVE")
    error_message = Column(Text, nullable=True)

class JobMatch(Base):
    __tablename__ = "job_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    
    role_score = Column(Float, default=0.0)
    skill_score = Column(Float, default=0.0)
    experience_score = Column(Float, default=0.0)
    education_score = Column(Float, default=0.0)
    location_score = Column(Float, default=0.0)
    remote_score = Column(Float, default=0.0)
    project_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    
    strong_matches = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    match_explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    job = relationship("Job", back_populates="matches")

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)
    
    title = Column(String(255), default="Master Resume")
    resume_type = Column(String(50), default="MASTER") # MASTER or TAILORED
    content_markdown = Column(Text, nullable=False)
    file_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    
    status = Column(String(50), default="DISCOVERED") 
    # DISCOVERED, ANALYZED, SHORTLISTED, REVIEW_REQUIRED, APPROVED, APPLYING, APPLIED, REJECTED, INTERVIEW, OFFER, WITHDRAWN, FAILED
    
    applied_date = Column(DateTime, nullable=True)
    match_score = Column(Float, default=0.0)
    tailored_resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    notes = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    job = relationship("Job", back_populates="applications")
    answers = relationship("ApplicationAnswer", back_populates="application", cascade="all, delete-orphan")
    events = relationship("ApplicationEvent", back_populates="application", cascade="all, delete-orphan")

class ApplicationAnswer(Base):
    __tablename__ = "application_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    is_sensitive = Column(Boolean, default=False)
    is_user_reviewed = Column(Boolean, default=False)
    
    application = relationship("Application", back_populates="answers")

class ApplicationEvent(Base):
    __tablename__ = "application_events"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    event_type = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    screenshot_path = Column(String(500), nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    application = relationship("Application", back_populates="events")
