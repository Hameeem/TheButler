import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database import SessionLocal, models
from app.components import header
from app.agents.job_discovery import JobDiscoveryAgent
from app.browser.application_runner import ApplicationRunner
from app.resume.tailor import ResumeTailor

st.set_page_config(page_title="Dashboard — TheButler", page_icon="📊", layout="wide")

st.title("📊 AGENT DASHBOARD & APPROVAL QUEUE")

db = SessionLocal()

# Top Action Button to Trigger Discovery
col_top1, col_top2 = st.columns([3, 1])
with col_top1:
    st.caption("Real-time summary of internship discovery, AI matching, and approval queue.")
with col_top2:
    if st.button("🔄 Run Discovery Agent Now", type="primary"):
        with st.spinner("Searching 8 job sources, deduplicating & scoring jobs..."):
            res = JobDiscoveryAgent.run_discovery(db)
            st.success(f"Discovery complete! Discovered {res['total_discovered']} jobs, {res['shortlisted']} shortlisted for approval.")
            st.rerun()

# Gather Metrics
jobs = db.query(models.Job).all()
applications = db.query(models.Application).all()

total_jobs = len(jobs)
relevant_jobs = len([j for j in jobs if j.matches and j.matches[0].overall_score >= 75])
remote_jobs = len([j for j in jobs if j.is_remote])
approval_required = len([a for a in applications if a.status in ["REVIEW_REQUIRED", "SHORTLISTED", "APPROVED"]])
applied = len([a for a in applications if a.status == "APPLIED"])
interviews = len([a for a in applications if a.status == "INTERVIEW"])
offers = len([a for a in applications if a.status == "OFFER"])

# Metrics Ribbon
c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
c1.metric("Jobs Found", total_jobs)
c2.metric("Relevant Jobs", relevant_jobs)
c3.metric("Remote Jobs", remote_jobs)
c4.metric("Shortlisted", len([a for a in applications if a.status == "SHORTLISTED"]))
c5.metric("Awaiting Approval", approval_required, delta="Action Required", delta_color="inverse")
c6.metric("Submitted", applied)
c7.metric("Interviews", interviews)

st.markdown("---")

# Section: Applications Awaiting Approval
st.subheader("🛡️ HUMAN APPROVAL GATE — APPLICATIONS READY FOR REVIEW")
st.info("By default, TheButler requires your explicit approval before submitting any job application.")

pending_apps = [a for a in applications if a.status in ["REVIEW_REQUIRED", "SHORTLISTED", "APPROVED"]]

if not pending_apps:
    st.success("🎉 No applications currently awaiting approval! Click 'Run Discovery Agent Now' to fetch new listings.")
else:
    for app_item in pending_apps:
        job = app_item.job
        match = job.matches[0] if job.matches else None
        score = match.overall_score if match else app_item.match_score
        
        with st.expander(f"📌 REVIEW REQUIRED: {job.title} at {job.company_name} (Match: {score}% | {job.location})", expanded=True):
            st.markdown(f"""
            **Company:** {job.company_name}  
            **Role:** {job.title}  
            **Source:** {job.source_platform}  
            **Location:** {job.location} {'🏠 (Remote)' if job.is_remote else ''}  
            **Stipend:** {job.stipend_salary or 'Unspecified'}  
            **Quality Risk Status:** `{job.quality_status}`
            """)
            
            st.markdown("##### 🎯 Match Explanation")
            st.code(match.match_explanation if match else "High profile alignment detected.", language="text")
            
            t1, t2, t3 = st.tabs(["📄 Tailored Resume Preview", "💬 Application Answers", "🌐 Target Job Page"])
            
            with t1:
                profile = db.query(models.Profile).first()
                tailored = ResumeTailor.tailor_resume_for_job(db, job, profile)
                st.markdown(tailored.content_markdown)
                
            with t2:
                st.write("✓ **Why do you want this internship?**")
                st.info(f"I am a CS student with experience in SQL, Python, Power BI, and automated ETL pipelines (SkyMetrics). Joining {job.company_name} fits my goal of applying data analysis to business problems.")
                st.write("✓ **Tell us about your experience with SQL and visualization:**")
                st.info("Proficient in writing complex PostgreSQL/MySQL window functions, joins, aggregations, and designing interactive Power BI dashboards.")
                
            with t3:
                st.markdown(f"**Application URL:** [{job.application_url}]({job.application_url})")
                
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                if st.button(f"✅ APPROVE & SUBMIT ({job.company_name})", key=f"approve_{app_item.id}", type="primary"):
                    with st.spinner("Running browser automation & submitting application..."):
                        exec_res = ApplicationRunner.execute_application(db, app_item.id)
                        st.success(f"Result: {exec_res['message']}")
                        st.rerun()
            with col_b2:
                if st.button(f"❌ REJECT ({job.company_name})", key=f"reject_{app_item.id}"):
                    app_item.status = "REJECTED"
                    db.commit()
                    st.warning("Application rejected.")
                    st.rerun()
            with col_b3:
                st.link_button(f"📋 Manual Handoff ({job.company_name})", job.application_url or job.job_url)

db.close()
