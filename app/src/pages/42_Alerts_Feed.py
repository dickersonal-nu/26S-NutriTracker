import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Alerts Feed", page_icon="🔔")
SideBarLinks()


if "role" not in st.session_state or st.session_state["role"] != "admin":
    st.error("You must be logged in as an Admin to view this page.")
    st.stop()

API_BASE = "http://api:4000"


st.title("🔔 Alerts Feed")
st.markdown("View active system alerts and dismiss them when resolved.")
st.divider()


col1, col2 = st.columns([2, 2])
with col1:
    severity_filter = st.selectbox(
        "Filter by Severity",
        ["All", "critical", "warning", "info"],
    )
with col2:
    show_resolved = st.radio(
        "Show",
        ["Unresolved", "Resolved"],
        horizontal=True,
    )

resolved_param = "true" if show_resolved == "Resolved" else "false"

params = {"resolved": resolved_param}
if severity_filter != "All":
    params["severity"] = severity_filter


try:
    r = requests.get(f"{API_BASE}/admin/alerts", params=params, timeout=5)
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


SEVERITY_COLOR = {
    "critical": "🔴",
    "warning":  "🟡",
    "info":     "🔵",
}


if not alerts:
    st.info("No alerts match the selected filters.")
else:
    for alert in alerts:
        alert_id = alert.get("alert_id")
        title    = alert.get("title", "Untitled")
        detail   = alert.get("detail", "")
        severity = alert.get("severity", "info")
        created  = alert.get("created_at", "")
        icon     = SEVERITY_COLOR.get(severity, "⚪")

        with st.container(border=True):
            left, right = st.columns([5, 1])
            with left:
                st.markdown(f"#### {icon} {title}")
                st.markdown(f"**Severity:** `{severity}` &nbsp;|&nbsp; **Created:** {created}")
                if detail:
                    st.markdown(f"> {detail}")
            with right:
                if show_resolved == "Unresolved":
                    if st.button("Dismiss", key=f"dismiss_{alert_id}", use_container_width=True):
                        try:
                            resp = requests.delete(
                                f"{API_BASE}/admin/alerts/{alert_id}",
                                timeout=5,
                            )
                            if resp.status_code == 200:
                                st.success(f"Alert {alert_id} dismissed.")
                                st.rerun()
                            else:
                                st.error(f"Error: {resp.status_code}")
                        except Exception as e:
                            st.error(f"Could not reach API: {e}")
                else:
                    resolved_at = alert.get("resolved_at", "")
                    st.markdown(f"✅ Resolved  \n`{resolved_at}`")