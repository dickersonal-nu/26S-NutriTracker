"""
42_Alerts_Feed.py
Laura Smith — Alerts Feed (Wireframe 8)
Routes used: GET 4.6 (alerts), DELETE (dismiss alert)
"""

import streamlit as st
import requests
from datetime import datetime
from modules.nav import SideBarLinks

API_BASE = "http://api:4000/admin"

st.set_page_config(page_title="Alerts Feed", page_icon="🔔", layout="wide")
SideBarLinks()
st.title("🔔 Alerts Feed")
st.caption("Admin · Laura Smith")

@st.cache_data(ttl=15)
def fetch_alerts(show_resolved=False):
    try:
        r = requests.get(f"{API_BASE}/alerts", params={"resolved": str(show_resolved).lower()})
        return r.json().get("alerts", [])
    except Exception:
        # Mock data for dev
        return [
            {"alert_id": 1, "title": "Low inventory: Dining Hall A",   "severity": "high",   "message": "Milk stock below threshold.",         "created_at": "2026-04-17T08:00:00", "resolved": False},
            {"alert_id": 2, "title": "Menu update failed",              "severity": "medium", "message": "West Village push returned 500.",     "created_at": "2026-04-17T09:15:00", "resolved": False},
            {"alert_id": 3, "title": "New user spike",                  "severity": "low",    "message": "35 new registrations in 1 hour.",     "created_at": "2026-04-17T10:30:00", "resolved": False},
            {"alert_id": 4, "title": "DB backup completed",             "severity": "low",    "message": "Nightly backup finished successfully.", "created_at": "2026-04-16T23:00:00", "resolved": True},
        ]

col1, col2 = st.columns([3, 1])
with col1:
    severity_filter = st.selectbox("Filter by severity", ["All", "high", "medium", "low"])
with col2:
    show_resolved = st.toggle("Show resolved", value=False)

alerts = fetch_alerts(show_resolved)

if severity_filter != "All":
    alerts = [a for a in alerts if a["severity"] == severity_filter]

unresolved_count = len([a for a in alerts if not a.get("resolved")])
st.caption(f"{unresolved_count} unresolved alert{'s' if unresolved_count != 1 else ''}")
st.divider()

SEVERITY_ICON  = {"high": "🔴", "medium": "🟡", "low": "🔵"}
SEVERITY_COLOR = {"high": "#ff4b4b", "medium": "#ffa600", "low": "#1f77b4"}

if not alerts:
    st.info("No alerts to display.")
else:
    for alert in alerts:
        sev  = alert.get("severity", "low")
        icon = SEVERITY_ICON.get(sev, "⚪")
        resolved = alert.get("resolved", False)

        with st.container(border=True):
            col1, col2 = st.columns([5, 1])

            with col1:
                st.markdown(f"**{icon} {alert['title']}**")
                st.caption(alert.get("message", ""))
                ts = alert.get("created_at", "")
                if ts:
                    try:
                        dt = datetime.fromisoformat(ts)
                        st.caption(f"🕐 {dt.strftime('%b %d, %Y at %I:%M %p')}")
                    except Exception:
                        st.caption(ts)

            with col2:
                if not resolved:
                    if st.button("✓ Dismiss", key=f"dismiss_{alert['alert_id']}", type="primary"):
                        resp = requests.delete(f"{API_BASE}/alerts/{alert['alert_id']}")
                        if resp.status_code == 200:
                            st.success("Dismissed")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error("Failed to dismiss")
                else:
                    st.caption("✅ Resolved")
