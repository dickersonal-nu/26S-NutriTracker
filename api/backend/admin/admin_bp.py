import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Metrics & Audit", page_icon="📊")
SideBarLinks()


if "role" not in st.session_state or st.session_state["role"] != "admin":
    st.error("You must be logged in as an Admin to view this page.")
    st.stop()

API_BASE = "http://api:4000"

st.title("📊 Metrics & Audit")
st.markdown("Monitor system health, browse reports, and review the audit trail.")
st.divider()


tab1, tab2, tab3 = st.tabs(["📈 System Metrics", "📋 Reports", "📝 Audit Log"])



with tab1:
    st.subheader("System Metrics")

    since_date = st.date_input(
        "Show metrics since (optional)",
        value=None,
        key="metrics_since",
    )

    params = {}
    if since_date:
        params["since"] = str(since_date)

    if st.button("Load Metrics", key="load_metrics"):
        try:
            r = requests.get(f"{API_BASE}/admin/metrics", params=params, timeout=5)
            if r.status_code == 200:
                data    = r.json()
                metrics = data.get("metrics", [])
                st.markdown(f"**{data.get('count', 0)} metric(s) found.**")

                if metrics:
                    # Show as a table
                    st.dataframe(
                        metrics,
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.info("No metrics found for the selected date range.")
            elif r.status_code == 400:
                st.error(r.json().get("error", "Bad request."))
            else:
                st.error(f"API error {r.status_code}")
        except Exception as e:
            st.error(f"Could not reach API: {e}")



with tab2:
    st.subheader("Generated Reports")

    col1, col2 = st.columns([3, 1])
    with col1:
        report_type = st.selectbox(
            "Filter by type (optional)",
            ["All", "nutrition", "usage", "financial"],
            key="report_type",
        )
    with col2:
        report_limit = st.number_input("Limit", min_value=1, max_value=100, value=20, key="rep_limit")

    if st.button("Load Reports", key="load_reports"):
        params = {"limit": report_limit}
        if report_type != "All":
            params["type"] = report_type

        try:
            r = requests.get(f"{API_BASE}/admin/reports", params=params, timeout=5)
            if r.status_code == 200:
                data    = r.json()
                reports = data.get("reports", [])
                st.markdown(f"**{data.get('count', 0)} report(s) found.**")

                if reports:
                    for rep in reports:
                        with st.expander(
                            f"📄 {rep.get('title', 'Untitled')} "
                            f"— `{rep.get('report_type', '')}` "
                            f"| {rep.get('created_at', '')}"
                        ):
                            content = rep.get("content", "")
                            if content:
                                st.markdown(content)
                            else:
                                st.markdown("*No content available.*")
                else:
                    st.info("No reports found.")
            else:
                st.error(f"API error {r.status_code}")
        except Exception as e:
            st.error(f"Could not reach API: {e}")



with tab3:
    st.subheader("Audit Log")

    col1, col2 = st.columns([3, 1])
    with col1:
        action_filter = st.selectbox(
            "Filter by action (optional)",
            ["All", "update_role", "push_menu_update", "deactivate_user"],
            key="audit_action",
        )
    with col2:
        audit_limit = st.number_input("Limit", min_value=1, max_value=200, value=50, key="audit_limit")

    if st.button("Load Audit Log", key="load_audit"):
        params = {"limit": audit_limit}
        if action_filter != "All":
            params["action"] = action_filter

        try:
            r = requests.get(f"{API_BASE}/admin/audit-logs", params=params, timeout=5)
            if r.status_code == 200:
                data = r.json()
                logs = data.get("logs", [])
                st.markdown(f"**{data.get('count', 0)} log(s) found.**")

                if logs:
                    st.dataframe(
                        logs,
                        use_container_width=True,
                        hide_index=True,
                        column_order=["log_id", "timestamp", "action", "target_type", "target_id", "detail"],
                    )
                else:
                    st.info("No audit log entries found.")
            else:
                st.error(f"API error {r.status_code}")
        except Exception as e:
            st.error(f"Could not reach API: {e}")