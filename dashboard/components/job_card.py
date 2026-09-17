import streamlit as st

def render_job_card(job, match, on_apply_callback=None):
    with st.container():
        score = match.overall_score if match else 0.0
        badge_color = "green" if score >= 85 else ("orange" if score >= 70 else "red")
        
        st.markdown(f"""
        <div style="border:1px solid #e0e0e0; border-radius:10px; padding:15px; margin-bottom:15px; background-color:#fafafa;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3 style="margin:0; color:#1E88E5;">{job.title}</h3>
                <span style="font-size:18px; font-weight:bold; color:{badge_color}; background:#eef; padding:4px 10px; border-radius:5px;">
                    Match Score: {score}%
                </span>
            </div>
            <p style="margin:5px 0; font-weight:bold; color:#424242;">
                🏢 {job.company_name} | 📍 {job.location} {'🏠 (Remote)' if job.is_remote else ''} | 🌐 {job.source_platform}
            </p>
            <p style="margin:5px 0; font-size:13px; color:#616161;">
                💰 <b>Stipend:</b> {job.stipend_salary or 'Not specified'} | ⏱️ <b>Exp:</b> {job.experience_req} | 🛡️ <b>Quality Risk:</b> {job.quality_status}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"📊 Detailed AI Match Breakdown & Description for {job.title}"):
            if match:
                st.markdown("#### 🎯 Granular Sub-Scores")
                c1, c2, c3, c4 = st.columns(4)
                c1.progress(int(match.role_score), text=f"Role: {match.role_score}%")
                c2.progress(int(match.skill_score), text=f"Skills: {match.skill_score}%")
                c3.progress(int(match.experience_score), text=f"Experience: {match.experience_score}%")
                c4.progress(int(match.remote_score), text=f"Remote: {match.remote_score}%")
                
                st.markdown("#### ✅ Strong Skill Matches")
                st.write(", ".join([f"`{sk}`" for sk in (match.strong_matches or [])]))
                
                if match.missing_skills:
                    st.markdown("#### ⚠️ Preferred / Missing Skills")
                    st.write(", ".join([f"`{sk}`" for sk in match.missing_skills]))
            
            st.markdown("#### 📝 Job Description")
            st.write(job.raw_description)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.link_button("🌐 Open Job Page", job.job_url)
            with col_b:
                if on_apply_callback:
                    if st.button(f"⚡ Select & Generate Application ({job.company_name})", key=f"apply_{job.id}"):
                        on_apply_callback(job.id)
