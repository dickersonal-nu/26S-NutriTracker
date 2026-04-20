import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}!")
st.write("### Uncover trends, detect outliers, and export insights!")
st.write("Explore campus-wide nutrition data to drive meaningful decisions.")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Filter & Visualize Data',
                type='primary',
                use_container_width=True,
                key='btn_filter'):
        st.switch_page('pages/31_Analyst_Filter_Visualize.py')

with col2:
    if st.button('Configure Data Exports',
                type='primary',
                use_container_width=True,
                key='btn_export'):
        st.switch_page('pages/32_Analyst_Export_Config.py')

with col3:
    if st.button('Detect Outliers',
                type='primary',
                use_container_width=True,
                key='btn_outliers'):
        st.switch_page('pages/33_Analyst_Outliers.py')

st.divider()
st.write("#### Why Data Analysis Matters for Campus Nutrition")
st.write("""
- **Trends**: Identify which dining halls and meal periods drive healthy choices
- **Outliers**: Spot students at nutritional risk before problems escalate
- **Exports**: Share clean datasets with researchers and dining staff
- **Impact**: Data-backed recommendations lead to real menu improvements
""")
