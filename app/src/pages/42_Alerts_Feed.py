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

# ---------- filters ----------
col1, col2 = st.columns([2, 2])
with col1:
    type_filter = st.selectbox(
        "Filter by alert type",
        ["All", "exceeded_max", "below_min", "system"],
    )
with col2:
    show_read = st.radio("Show", ["Unread", "Read"], horizontal=True)

# ---------- fetch ----------
is_read = "true" if show_read == "Read" else "false"
params = {"is_read": is_read}
if type_filter != "All":
    params["alert_type"] = type_filter

try:
    r = requests.get(f"{API_BASE}/alerts", params=params, timeout=5)
    if r.status_code == 200:
        alerts = r.json().get("alerts", [])
    else:
        st.error(f"API error {r.status_code}")
        alerts = []
except Exception as e:
    st.error(f"Could not reach API: {e}")
    alerts = []

st.markdown(f"**{len(alerts)} alert(s) found.**")
st.divider()

# ---------- display ----------
TYPE_ICON = {
    "exceeded_max": "🔴",
    "below_min":    "🟡",
    "system":       "🔵",
}

if not alerts:
    st.info("No alerts match the selected filters.")
else:
    for alert in alerts:
        alert_id   = alert.get("alert_id")
        alert_type = alert.get("alert_type", "system")
        message    = alert.get("message", "")
        triggered  = alert.get("triggered_at", "")
        read       = alert.get("is_read", False)
        icon       = TYPE_ICON.get(alert_type, "⚪")

        with st.container(border=True):
            left, right = st.columns([5, 1])

            with left:
                st.markdown(f"#### {icon} {alert_type}")
                st.markdown(f"{message}")
                if triggered:
                    try:
                        dt = datetime.fromisoformat(triggered)
                        st.caption(f"🕐 {dt.strftime('%b %d, %Y at %I:%M %p')}")
                    except Exception:
                        st.caption(triggered)

            with right:
                if not read:
                    if st.button("Dismiss", key=f"dismiss_{alert_id}", use_container_width=True):
                        try:
                            resp = requests.delete(f"{API_BASE}/alerts/{alert_id}", timeout=5)
                            if resp.status_code == 200:
                                st.success(f"Alert {alert_id} dismissed.")
                                st.rerun()
                            else:
                                st.error(f"Error: {resp.status_code}")
                        except Exception as e:
                            st.error(f"Could not reach API: {e}")
                else:
                    st.caption("✅ Read")
