import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Admin Home", page_icon="🛡️")
SideBarLinks()


if "role" not in st.session_state or st.session_state["role"] != "admin":
    st.error("You must be logged in as an Admin to view this page.")
    st.stop()


st.title("🛡️ Admin Dashboard")
st.markdown(f"Welcome back, **{st.session_state.get('first_name', 'Admin')}**.")
st.divider()

API_BASE = "http://api:4000"

col1, col2, col3, col4 = st.columns(4)

try:
    r = requests.get(f"{API_BASE}/admin/alerts", params={"resolved": "false"}, timeout=5)
    unresolved = r.json().get("count", "—") if r.status_code == 200 else "—"
except Exception:
    unresolved = "—"

try:
    r = requests.get(f"{API_BASE}/admin/alerts",
                     params={"resolved": "false", "severity": "critical"}, timeout=5)
    critical = r.json().get("count", "—") if r.status_code == 200 else "—"
except Exception:
    critical = "—"


try:
    r = requests.get(f"{API_BASE}/admin/audit-logs", params={"limit": 5}, timeout=5)
    recent_logs = r.json().get("logs", []) if r.status_code == 200 else []
except Exception:
    recent_logs = []


try:
    r = requests.get(f"{API_BASE}/admin/reports", params={"limit": 5}, timeout=5)
    report_count = r.json().get("count", "—") if r.status_code == 200 else "—"
except Exception:
    report_count = "—"

col1.metric("🔔 Open Alerts",    unresolved)
col2.metric("🚨 Critical Alerts", critical)
col3.metric("📋 Recent Reports",  report_count)
col4.metric("📝 Audit Log Size",  "Live")

st.divider()

st.subheader("Recent Activity")

if recent_logs:
    for log in recent_logs:
        ts        = log.get("timestamp", "")
        action    = log.get("action", "")
        target    = log.get("target_type", "")
        detail    = log.get("detail", "")
        st.markdown(f"- `{ts}` &nbsp; **{action}** on *{target}* — {detail}")
else:
    st.info("No recent audit log entries found.")

st.divider()

st.subheader("Quick Navigation")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 👤 User Management")
    st.markdown("Update user roles or deactivate accounts.")
    if st.button("Go to User Management", use_container_width=True):
        st.switch_page("pages/41_User_Management.py")

with c2:
    st.markdown("### 🔔 Alerts Feed")
    st.markdown("View and dismiss system alerts.")
    if st.button("Go to Alerts Feed", use_container_width=True):
        st.switch_page("pages/42_Alerts_Feed.py")

with c3:
    st.markdown("### 📊 Metrics & Audit")
    st.markdown("Browse system metrics, reports, and audit logs.")
    if st.button("Go to Metrics & Audit", use_container_width=True):
        st.switch_page("pages/43_Metrics_Audit.py")
