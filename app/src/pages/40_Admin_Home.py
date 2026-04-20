import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}!")
st.write("### Keep the platform running smoothly for everyone!")
st.write("Manage users, monitor alerts, and audit system activity.")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button('User Management',
                type='primary',
                use_container_width=True,
                key='btn_users'):
        st.switch_page('pages/41_User_Management.py')

with col2:
    if st.button('Alerts Feed',
                type='primary',
                use_container_width=True,
                key='btn_alerts'):
        st.switch_page('pages/42_Alerts_Feed.py')

with col3:
    if st.button('System Metrics & Audit Logs',
                type='primary',
                use_container_width=True,
                key='btn_metrics'):
        st.switch_page('pages/43_Metrics_Audit.py')

st.divider()
st.write("#### Why Platform Administration Matters")
st.write("""
- **Access Control**: Keeping roles accurate ensures every user sees the right data
- **Alerts**: Early visibility into issues prevents disruptions for students and staff
- **Metrics**: System health tracking supports reliable service across all dining halls
- **Audit Logs**: A full change history builds trust and supports compliance
""")
