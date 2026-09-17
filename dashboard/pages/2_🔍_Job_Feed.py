import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database import SessionLocal, models
from dashboard.components.job_card import render_job_card

st.set_page_config(page_title="Job Feed — TheButler", page_icon="🔍", layout="wide")

st.title("🔍 DISCOVERED INTERNSHIP FEED")
st.caption("Search, filter, and inspect Data Analyst internship listings discovered across 8 platforms.")

db = SessionLocal()

# Sidebar Filters
st.sidebar.markdown("### 🎛️ Job Feed Filters")

search_term = st.sidebar.text_input("Search Title or Company", "")
remote_filter = st.sidebar.selectbox("Work Arrangement", ["All Arrangements", "Remote / WFH Only", "Hybrid", "On-site"])
min_score = st.sidebar.slider("Min Match Score (%)", 0, 100, 70)
platform_filter = st.sidebar.selectbox("Job Source Platform", ["All Sources", "LinkedIn Jobs", "Naukri", "Indeed", "Internshala", "Wellfound", "Glassdoor", "Foundit", "Cutshort"])
quality_filter = st.sidebar.selectbox("Quality Risk Filter", ["All Listings", "Verified / Low Risk Only", "Needs Review"])

# Fetch Jobs from DB
query = db.query(models.Job)

if remote_filter == "Remote / WFH Only":
    query = query.filter(models.Job.is_remote == True)
elif remote_filter == "Hybrid":
    query = query.filter(models.Job.is_hybrid == True)

if platform_filter != "All Sources":
    query = query.filter(models.Job.source_platform.contains(platform_filter))

if quality_filter == "Verified / Low Risk Only":
    query = query.filter(models.Job.quality_status.in_(["VERIFIED", "LOW_RISK"]))

jobs = query.all()

# Apply score & search filters
filtered_jobs = []
for j in jobs:
    match = j.matches[0] if j.matches else None
    score = match.overall_score if match else 0.0
    
    if score >= min_score:
        if search_term:
            if search_term.lower() in j.title.lower() or search_term.lower() in j.company_name.lower():
                filtered_jobs.append((j, match))
        else:
            filtered_jobs.append((j, match))

st.markdown(f"Displaying **{len(filtered_jobs)}** jobs matching your criteria.")

def handle_apply(job_id: int):
    profile = db.query(models.Profile).first()
    existing_app = db.query(models.Application).filter(models.Application.job_id == job_id).first()
    if not existing_app:
        app_obj = models.Application(
            job_id=job_id,
            profile_id=profile.id,
            status="REVIEW_REQUIRED" if profile.application_mode == "APPROVAL_REQUIRED" else "SHORTLISTED",
            match_score=75.0
        )
        db.add(app_obj)
        db.commit()
    st.success(f"Job shortlisted for application review! Check the Dashboard tab.")

for job_obj, match_obj in filtered_jobs:
    render_job_card(job_obj, match_obj, on_apply_callback=handle_apply)

db.close()
