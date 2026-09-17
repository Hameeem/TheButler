import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database import SessionLocal, init_db
from app.database import models
from app.database.repositories import seed_default_user_and_profile

st.set_page_config(page_title="First-Run Setup — TheButler", page_icon="🚀", layout="wide")

st.title("🚀 WELCOME TO THEBUTLER")
st.caption("Let's configure your autonomous Data Analyst internship agent in 30 seconds.")

db = SessionLocal()
init_db()
profile = seed_default_user_and_profile(db)

st.markdown("### 🎯 Job Search & Application Preferences")

with st.form("onboarding_form"):
    target_role = st.text_input("Target Role", value=profile.target_role or "Data Analyst Intern")
    
    col1, col2 = st.columns(2)
    with col1:
        work_preference = st.selectbox("Preferred Work Arrangement", ["Remote / Work From Home (Tier 1)", "Hybrid (Tier 2)", "On-site (Tier 3)"])
        country = st.text_input("Target Country", value="India")
    with col2:
        min_match_score = st.slider("Minimum Match Score Threshold (%)", 50, 95, profile.min_match_score)
        app_mode = st.selectbox("Application Mode", ["Approval Required (Default & Recommended)", "Manual", "Automatic"], index=0)
        
    st.markdown("### 🔌 Enabled Job Sources (8 Platforms)")
    sources = db.query(models.JobSource).all()
    enabled_sources = []
    
    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]
    for idx, src in enumerate(sources):
        with cols[idx % 4]:
            is_ch = st.checkbox(src.name, value=src.is_enabled, key=f"src_{src.id}")
            if is_ch:
                enabled_sources.append(src.id)
                
    daily_limit = st.number_input("Daily Application Limit", min_value=1, max_value=50, value=profile.daily_limit)

    submitted = st.form_submit_button("🔥 START JOB SEARCH AGENT")
    
    if submitted:
        profile.target_role = target_role
        profile.min_match_score = min_match_score
        profile.application_mode = "APPROVAL_REQUIRED" if "Approval Required" in app_mode else ("MANUAL" if "Manual" in app_mode else "AUTOMATIC")
        profile.daily_limit = daily_limit
        
        for src in sources:
            src.is_enabled = (src.id in enabled_sources)
            
        db.commit()
        st.success("✅ Configuration saved! TheButler is ready to discover jobs for you.")
        st.info("👉 Open the **📊 Dashboard** or **🔍 Job Feed** tab in the sidebar to run your first discovery!")
db.close()
