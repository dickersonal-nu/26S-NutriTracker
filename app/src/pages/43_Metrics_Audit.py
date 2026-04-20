"""
43_Metrics_Audit.py
Laura Smith — System Metrics + Audit Logs
Routes used: GET 4.2 (metrics), GET 4.3 (audit logs)
"""

import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:5000/admin"

st.set_page_config(page_title="Metrics & Audit Logs", page_icon="📊", layout="wide")
st.title("📊 System Metrics & Audit Logs")
st.caption("Admin · Laura Smith")

tab1, tab2 = st.tabs(["📈 System Metrics", "📋 Audit Logs"])


with tab1:
    st.subheader("System Metrics")

    since = st.date_input("Show metrics since", value=None, help="Leave blank for all")

    @st.cache_data(ttl=60)
    def fetch_metrics(since_str=None):
        params = {}
        if since_str:
            params["since"] = since_str
        try:
            r = requests.get(f"{API_BASE}/metrics", params=params)
            return r.json().get("metrics", [])
        except Exception:
            # Mock data
            return [
                {"metric_id": 1, "name": "active_users",       "value": 28,    "recorded_at": "2026-04-17T10:00:00"},
                {"metric_id": 2, "name": "meals_served_today",  "value": 412,   "recorded_at": "2026-04-17T10:00:00"},
                {"metric_id": 3, "name": "api_requests_hour",   "value": 1840,  "recorded_at": "2026-04-17T10:00:00"},
                {"metric_id": 4, "name": "db_query_avg_ms",     "value": 23,    "recorded_at": "2026-04-17T10:00:00"},
                {"metric_id": 5, "name": "active_users",        "value": 21,    "recorded_at": "2026-04-16T10:00:00"},
                {"metric_id": 6, "name": "meals_served_today",  "value": 388,   "recorded_at": "2026-04-16T10:00:00"},
            ]

    metrics = fetch_metrics(str(since) if since else None)

    if metrics:
        df = pd.DataFrame(metrics)

        col1, col2, col3, col4 = st.columns(4)
        latest = {m["name"]: m["value"] for m in metrics[:4]}
        with col1:
            st.metric("Active Users",         latest.get("active_users",      "—"))
        with col2:
            st.metric("Meals Served Today",   latest.get("meals_served_today","—"))
        with col3:
            st.metric("API Requests/hr",      latest.get("api_requests_hour", "—"))
        with col4:
            st.metric("Avg DB Query (ms)",    latest.get("db_query_avg_ms",   "—"))

        st.divider()

        meals_df = df[df["name"] == "meals_served_today"].copy()
        if not meals_df.empty:
            meals_df["recorded_at"] = pd.to_datetime(meals_df["recorded_at"])
            meals_df = meals_df.sort_values("recorded_at")
            st.line_chart(meals_df.set_index("recorded_at")["value"], use_container_width=True)

        with st.expander("Raw metrics data"):
            st.dataframe(df, use_container_width=True)
    else:
        st.info("No metrics available.")


with tab2:
    st.subheader("Audit Logs")

    col1, col2 = st.columns([2, 1])
    with col1:
        action_filter = st.selectbox(
            "Filter by action",
            ["All", "update_role", "deactivate_user", "push_menu_update", "login", "logout"],
        )
    with col2:
        limit = st.number_input("Max rows", min_value=10, max_value=500, value=50, step=10)

    @st.cache_data(ttl=30)
    def fetch_audit_logs(action=None, limit=50):
        params = {"limit": limit}
        if action and action != "All":
            params["action"] = action
        try:
            r = requests.get(f"{API_BASE}/audit-logs", params=params)
            return r.json().get("logs", [])
        except Exception:
            return [
                {"log_id": 1, "action": "update_role",      "target_type": "user", "target_id": 3,  "detail": "Role changed from 'guest' to 'student'", "timestamp": "2026-04-17T09:00:00"},
                {"log_id": 2, "action": "push_menu_update",  "target_type": "dining_hall", "target_id": 5, "detail": "Menu updated for 2026-04-18 — 12 items", "timestamp": "2026-04-17T08:45:00"},
                {"log_id": 3, "action": "deactivate_user",   "target_type": "user", "target_id": 4,  "detail": "User 'inactive_usr' deactivated",        "timestamp": "2026-04-16T17:30:00"},
                {"log_id": 4, "action": "update_role",       "target_type": "user", "target_id": 2,  "detail": "Role changed from 'student' to 'staff'",  "timestamp": "2026-04-15T11:00:00"},
            ]

    logs = fetch_audit_logs(action_filter if action_filter != "All" else None, limit)

    if logs:
        df_logs = pd.DataFrame(logs)
        st.caption(f"{len(df_logs)} log entries")

        ACTION_ICON = {
            "update_role":      "🔄",
            "deactivate_user":  "🚫",
            "push_menu_update": "📋",
            "login":            "🔓",
            "logout":           "🔒",
        }

        for log in logs:
            icon = ACTION_ICON.get(log["action"], "📝")
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"{icon} **{log['action']}** — {log['detail']}")
                    st.caption(f"{log['target_type'].title()} ID #{log['target_id']}")
                with c2:
                    ts = log.get("timestamp", "")
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
