import streamlit as st
import requests
from modules.nav import SideBarLinks

API_BASE = "http://api:4000/admin"

st.set_page_config(layout="wide", page_title="User Management", page_icon="👤")
SideBarLinks()

# ---------- role lookup ----------
ROLES = {1: "student", 2: "athlete", 3: "analyst", 4: "administrator"}
ROLE_IDS = {v: k for k, v in ROLES.items()}

# ---------- update role ----------
st.subheader("Update User Role")

with st.form("update_role_form"):
    user_id_role = st.number_input("User ID", min_value=1, step=1, key="role_uid")
    new_role = st.selectbox("New Role", list(ROLES.values()))
    submitted_role = st.form_submit_button("Update Role", use_container_width=True)

if submitted_role:
    new_role_id = ROLE_IDS[new_role]
    try:
        r = requests.put(
            f"{API_BASE}/users/{int(user_id_role)}/role",
            json={"role_id": new_role_id},
            timeout=5,
        )
        if r.status_code == 200:
            data = r.json()
            st.success(
                f"✅ User {data['user_id']} role updated to "
                f"**{data.get('new_role_name', new_role)}**"
            )
        elif r.status_code == 404:
            st.error(f"User {int(user_id_role)} not found.")
        elif r.status_code == 422:
            st.error(r.json().get("error", "Invalid role."))
        else:
            st.error(f"Unexpected error: {r.status_code}")
    except Exception as e:
        st.error(f"Could not reach API: {e}")

st.divider()

# ---------- deactivate user ----------
st.subheader("Deactivate User")
st.warning("⚠️ This action soft-deletes the user. They will no longer be able to log in.")

with st.form("deactivate_user_form"):
    user_id_deact = st.number_input("User ID", min_value=1, step=1, key="deact_uid")
    confirm = st.checkbox("I understand this will deactivate the user account.")
    submitted_deact = st.form_submit_button("Deactivate User", use_container_width=True)

if submitted_deact:
    if not confirm:
        st.error("Please check the confirmation box before proceeding.")
    else:
        try:
            r = requests.delete(
                f"{API_BASE}/users/{int(user_id_deact)}",
                timeout=5,
            )
            if r.status_code == 200:
                st.success(f"✅ User {int(user_id_deact)} has been deactivated.")
            elif r.status_code == 404:
                st.error(f"User {int(user_id_deact)} not found.")
            else:
                st.error(f"Unexpected error: {r.status_code}")
        except Exception as e:
            st.error(f"Could not reach API: {e}")
