import streamlit as st
import os
import sys

# Add project root directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import init_db, SessionLocal
from app.database.repositories import seed_default_user_and_profile

st.set_page_config(
    page_title="TheButler — AI Internship Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database on first load
@st.cache_resource
def get_db_session():
    init_db()
    db = SessionLocal()
    seed_default_user_and_profile(db)
    return db

db = get_db_session()

# Sidebar Brand
st.sidebar.image("https://img.icons8.com/isometric-folders/100/robot.png", width=70)
st.sidebar.title("TheButler AI Agent")
st.sidebar.caption("Data Analyst Internship Discovery & Application System")
st.sidebar.markdown("---")

st.sidebar.info("🤖 **Agent Status:** Active\n\n🎯 **Target:** Data Analyst Intern (Remote India)")

# Navigation fallback notice
st.title("🤖 Welcome to TheButler")
st.markdown("""
**TheButler** is your autonomous AI career agent built for discovering, matching, and applying to **Data Analyst & Analytics Internships in India** (prioritizing Work From Home / Remote opportunities).

👈 **Use the Sidebar navigation menu to open:**
- **🚀 Onboarding:** Quick-start configuration wizard.
- **📊 Dashboard:** Metrics overview & pending application approvals.
- **🔍 Job Feed:** Search, filter, and inspect AI match score breakdowns.
- **📌 Applications:** Live Kanban status tracker.
- **👤 Profile:** Manage personal info, skills, projects & master resume.
- **⚙️ Settings:** Configure location tiers, match thresholds & job sources.
""")
