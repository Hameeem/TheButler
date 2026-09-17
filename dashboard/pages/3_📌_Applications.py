import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database import SessionLocal, models

st.set_page_config(page_title="Applications Tracker — TheButler", page_icon="📌", layout="wide")

st.title("📌 APPLICATION TRACKER & KANBAN BOARD")
st.caption("Track the lifecycle of your Data Analyst internship applications.")

db = SessionLocal()
applications = db.query(models.Application).all()

statuses = ["SHORTLISTED", "REVIEW_REQUIRED", "APPLIED", "INTERVIEW", "OFFER", "REJECTED"]
cols = st.columns(len(statuses))

for idx, status_name in enumerate(statuses):
    with cols[idx]:
        st.markdown(f"### {status_name.replace('_', ' ')}")
        apps_in_status = [a for a in applications if a.status == status_name]
        st.caption(f"{len(apps_in_status)} applications")
        st.markdown("---")
        
        for app_obj in apps_in_status:
            job = app_obj.job
            with st.container():
                st.markdown(f"""
                <div style="border:1px solid #ccc; border-radius:8px; padding:10px; margin-bottom:10px; background:#ffffff;">
                    <b style="color:#1976D2;">{job.title}</b><br/>
                    <small>🏢 {job.company_name}</small><br/>
                    <small>📍 {job.location}</small><br/>
                    <small>🎯 Score: <b>{app_obj.match_score}%</b></small>
                </div>
                """, unsafe_allow_html=True)
                
                # Move status selectbox
                new_status = st.selectbox(
                    "Move Status",
                    statuses,
                    index=statuses.index(app_obj.status),
                    key=f"status_sel_{app_obj.id}"
                )
                if new_status != app_obj.status:
                    app_obj.status = new_status
                    db.commit()
                    st.success("Updated status!")
                    st.rerun()

db.close()
