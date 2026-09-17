import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database import SessionLocal, models
from app.database.repositories import seed_default_user_and_profile, MASTER_RESUME_TEXT

st.set_page_config(page_title="Profile & Resume — TheButler", page_icon="👤", layout="wide")

st.title("👤 PROFILE & MASTER RESUME MANAGER")
st.caption("Manage your personal information, skills, projects, and master resume template.")

db = SessionLocal()
profile = seed_default_user_and_profile(db)

tab1, tab2, tab3, tab4 = st.tabs(["📋 Personal Details & Education", "🛠️ Skills List", "🚀 Featured Projects", "📄 Master Resume"])

with tab1:
    with st.form("personal_details_form"):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name", value=profile.full_name)
            email = st.text_input("Email Address", value=profile.email)
            phone = st.text_input("Phone Number", value=profile.phone or "")
            city = st.text_input("City", value=profile.city)
            state = st.text_input("State", value=profile.state)
        with col2:
            linkedin_url = st.text_input("LinkedIn URL", value=profile.linkedin_url or "")
            github_url = st.text_input("GitHub URL", value=profile.github_url or "")
            portfolio_url = st.text_input("Portfolio URL", value=profile.portfolio_url or "")
            degree = st.text_input("Degree", value=profile.degree)
            cgpa = st.text_input("CGPA", value=profile.cgpa)
            
        save_p = st.form_submit_button("Save Personal Info")
        if save_p:
            profile.full_name = full_name
            profile.email = email
            profile.phone = phone
            profile.city = city
            profile.state = state
            profile.linkedin_url = linkedin_url
            profile.github_url = github_url
            profile.portfolio_url = portfolio_url
            profile.degree = degree
            profile.cgpa = cgpa
            db.commit()
            st.success("Personal details updated!")

with tab2:
    st.markdown("### Verified Skills (Initial 18 Skills)")
    current_skills = [s.name for s in profile.skills]
    skills_text = st.text_area("Edit Skills (comma separated)", value=", ".join(current_skills), height=100)
    if st.button("Update Skills List"):
        # Clear existing skills and add new
        db.query(models.Skill).filter(models.Skill.profile_id == profile.id).delete()
        new_skills_list = [s.strip() for s in skills_text.split(",") if s.strip()]
        for sk_name in new_skills_list:
            db.add(models.Skill(profile_id=profile.id, name=sk_name, category="Technical"))
        db.commit()
        st.success(f"Updated skills list! Total skills: {len(new_skills_list)}")

with tab3:
    st.markdown("### Featured Projects")
    for proj in profile.projects:
        with st.expander(f"📁 {proj.name}"):
            st.write(f"**Description:** {proj.description}")
            st.write(f"**Technologies:** `{proj.technologies}`")
            st.write(f"**GitHub:** [{proj.github_url}]({proj.github_url})")

with tab4:
    st.markdown("### Master Resume Template")
    master_res = db.query(models.Resume).filter(
        models.Resume.profile_id == profile.id,
        models.Resume.resume_type == "MASTER"
    ).first()
    
    current_md = master_res.content_markdown if master_res else MASTER_RESUME_TEXT
    edited_md = st.text_area("Markdown Master Resume", value=current_md, height=400)
    
    if st.button("Save Master Resume"):
        if master_res:
            master_res.content_markdown = edited_md
        else:
            db.add(models.Resume(
                profile_id=profile.id,
                title="Master Resume",
                resume_type="MASTER",
                content_markdown=edited_md
            ))
        db.commit()
        st.success("Master resume saved!")

db.close()
