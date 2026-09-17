import streamlit as st

def render_metrics_summary(stats: dict):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Jobs Discovered", stats.get("total_jobs", 0), delta="Today")
    with col2:
        st.metric("Relevant Matches", stats.get("relevant_jobs", 0), delta="High Match")
    with col3:
        st.metric("Remote / WFH", stats.get("remote_jobs", 0), delta="Tier 1")
    with col4:
        st.metric("Awaiting Approval", stats.get("approval_required", 0), delta="Action Needed")
    with col5:
        st.metric("Submitted / Applied", stats.get("applied", 0), delta="Completed")
