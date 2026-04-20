"""
40_Admin_Home.py
Admin Home Page
"""

import streamlit as st

st.set_page_config(page_title="Admin Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ Admin Dashboard")
st.caption("Welcome, Laura Smith · Admin")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Users",      "35",  "+2 this week")
with col2:
    st.metric("Active Alerts",    "4",   "-1 today")
with col3:
    st.metric("Dining Halls Open","22",  "of 30")

st.divider()

st.subheader("Quick Navigation")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("👥 User Management",    use_container_width=True):
        st.switch_page("pages/41_User_Management.py")
with c2:
    if st.button("🔔 Alerts Feed",        use_container_width=True):
        st.switch_page("pages/42_Alerts_Feed.py")
with c3:
    if st.button("📊 System Metrics",     use_container_width=True):
        st.switch_page("pages/43_Metrics_Audit.py")
with c4:
    if st.button("📋 Audit Logs",         use_container_width=True):
        st.switch_page("pages/43_Metrics_Audit.py")
