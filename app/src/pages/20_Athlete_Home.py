import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}!")
st.write("### Fuel your performance, track your progress!")
st.write("Manage your nutrition to stay at the top of your game.")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Daily Nutrition Dashboard',
                type='primary',
                use_container_width=True,
                key='btn_daily'):
        st.switch_page('pages/21_Athlete_Daily_Nutrition.py')

with col2:
    if st.button('Log a Meal',
                type='primary',
                use_container_width=True,
                key='btn_log'):
        st.switch_page('pages/22_Athlete_Log_Meal.py')

with col3:
    if st.button('Weekly History & Goals',
                type='primary',
                use_container_width=True,
                key='btn_history'):
        st.switch_page('pages/23_Athlete_Weekly_History.py')

st.divider()
st.write("#### Why Nutrition Matters for Athletes")
st.write("""
- **Performance**: Proper fueling directly impacts speed, strength, and endurance
- **Recovery**: High-protein meals after training accelerate muscle repair
- **Consistency**: Tracking daily intake keeps you on target for your goals
- **Game Day**: The right carb-to-protein ratio primes you for peak output
""")
