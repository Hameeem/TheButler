import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database import SessionLocal, models
from app.database.repositories import seed_default_user_and_profile

st.set_page_config(page_title="Settings — TheButler", page_icon="⚙️", layout="wide")

st.title("⚙️ SYSTEM SETTINGS & JOB SOURCES")
st.caption("Configure location priority tiers, minimum score thresholds, and platform sources.")

db = SessionLocal()
profile = seed_default_user_and_profile(db)

st.markdown("### 📍 Location Hierarchy Settings")
st.info("""
- **Tier 1 (Highest Priority):** Remote / Work From Home India  
- **Tier 2:** Hybrid positions in India  
- **Tier 3:** On-site positions in India  
""")

exclude_onsite = st.checkbox("Exclude On-site Roles Completely", value=profile.exclude_onsite)
min_score = st.slider("Minimum Job Match Threshold (%)", 50, 95, profile.min_match_score)
app_mode = st.selectbox("Application Mode", ["APPROVAL_REQUIRED", "MANUAL", "AUTOMATIC"], index=0 if profile.application_mode=="APPROVAL_REQUIRED" else 1)

st.markdown("### 🔌 Enabled Job Sources")
sources = db.query(models.JobSource).all()

source_states = {}
for src in sources:
    source_states[src.id] = st.checkbox(f"{src.name} (Status: {src.status})", value=src.is_enabled, key=f"sett_src_{src.id}")

if st.button("Save Settings"):
    profile.exclude_onsite = exclude_onsite
    profile.min_match_score = min_score
    profile.application_mode = app_mode
    
    for src in sources:
        src.is_enabled = source_states[src.id]
        
    db.commit()
    st.success("Settings updated successfully!")

db.close()
