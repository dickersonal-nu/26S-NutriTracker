"""
43_Metrics_Audit.py
Laura Smith — System Metrics + Audit Logs
Routes used: GET 4.2 (metrics), GET 4.3 (audit logs), GET 4.5 (reports)
"""

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

API_BASE = "http://api:4000/admin"

st.set_page_config(page_title="Metrics & Audit Logs", page_icon="📊", layout="wide")
SideBarLinks()
st.title("📊 System Metrics & Audit Logs")
st.caption("Admin · Laura Smith")

tab1, tab2, tab3 = st.tabs(["📈 System Metrics", "📋 Reports", "📝 Audit Logs"])


# ==================== TAB 1: METRICS ====================
with tab1:
    st.subheader("System Metrics")

    since = st.date_input("Show metrics since", value=None, help="Leave blank for all")

    @st.cache_data(ttl=60)
    def fetch_metrics(since_str=None):
        params = {}
        if since_str:
            params["since"] = since_str
        try:
            r = requests.get(f"{API_BASE}/metrics", params=params, timeout=5)
            return r.json().get("metrics", [])
        except Exception:
            return []

    metrics = fetch_metrics(str(since) if since else None)

    if metrics:
        df = pd.DataFrame(metrics)

        # summary cards from latest values
        col1, col2, col3, col4 = st.columns(4)
        latest = {m["metric_type"]: m["value"] for m in metrics[:6]}
        with col1:
            st.metric("Active Users",       latest.get("active_users", "—"))
        with col2:
            st.metric("API Req/min",        latest.get("api_requests_per_min", "—"))
        with col3:
            st.metric("Avg DB Query (ms)",  latest.get("db_query_avg_ms", "—"))
        with col4:
            st.metric("Error Rate (%)",     latest.get("error_rate", "—"))

        st.divider()

        with st.expander("Raw metrics data"):
            st.dataframe(df, use_container_width=True)
    else:
        st.info("No metrics available.")


# ==================== TAB 2: REPORTS ====================
with tab2:
    st.subheader("Generated Reports")

    col1, col2 = st.columns([3, 1])
    with col1:
        report_type = st.selectbox(
            "Filter by type",
            ["All", "nutrition_summary", "trend_analysis"],
            key="report_type",
        )
    with col2:
        report_limit = st.number_input("Limit", min_value=1, max_value=100, value=20, key="rep_limit")

    if st.button("Load Reports", key="load_reports"):
        params = {"limit": report_limit}
        if report_type != "All":
            params["type"] = report_type
        try:
            r = requests.get(f"{API_BASE}/reports", params=params, timeout=5)
            if r.status_code == 200:
                data    = r.json()
                reports = data.get("reports", [])
                st.markdown(f"**{data.get('count', 0)} report(s) found.**")

                if reports:
                    for rep in reports:
                        status_icon = "✅" if rep.get("status") == "complete" else "⏳"
                        with st.expander(
                            f"{status_icon} {rep.get('title', 'Untitled')} "
                            f"— `{rep.get('report_type', '')}` "
                            f"| {rep.get('status', '')} "
                            f"| {rep.get('generated_at', 'pending')}"
                        ):
                            st.write(f"**Report ID:** {rep.get('report_id')}")
                            st.write(f"**Created by user:** {rep.get('created_by', 'system')}")
                            if rep.get('file_path'):
                                st.write(f"**File:** {rep['file_path']}")
                else:
                    st.info("No reports found.")
            else:
                st.error(f"API error {r.status_code}")
        except Exception as e:
            st.error(f"Could not reach API: {e}")


# ==================== TAB 3: AUDIT LOGS ====================
with tab3:
    st.subheader("Audit Logs")

    col1, col2 = st.columns([2, 1])
    with col1:
        action_filter = st.selectbox(
            "Filter by action",
            ["All", "INSERT", "UPDATE", "DELETE"],
        )
    with col2:
        limit = st.number_input("Max rows", min_value=10, max_value=500, value=50, step=10)

    @st.cache_data(ttl=30)
    def fetch_audit_logs(action=None, limit=50):
        params = {"limit": limit}
        if action and action != "All":
            params["action"] = action
        try:
            r = requests.get(f"{API_BASE}/audit-logs", params=params, timeout=5)
            return r.json().get("logs", [])
        except Exception:
            return []

    logs = fetch_audit_logs(action_filter if action_filter != "All" else None, limit)

    if logs:
        st.caption(f"{len(logs)} log entries")

        ACTION_ICON = {
            "INSERT": "➕",
            "UPDATE": "🔄",
            "DELETE": "🗑️",
        }

        for log in logs:
            icon = ACTION_ICON.get(log.get("action"), "📝")
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"{icon} **{log.get('action')}** on `{log.get('table_name')}`")
                    old = log.get("old_values")
                    new = log.get("new_values")
                    if old:
                        st.caption(f"Old: {old}")
                    if new:
                        st.caption(f"New: {new}")
                    if log.get("user_id"):
                        st.caption(f"By user #{log['user_id']}")
                with c2:
                    ts = log.get("performed_at", "")
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(ts)
                        st.caption(dt.strftime("%b %d\n%I:%M %p"))
                    except Exception:
                        st.caption(ts)
    else:
        st.info("No audit log entries found.")

    if st.button("🔄 Refresh logs"):
        st.cache_data.clear()
        st.rerun()
