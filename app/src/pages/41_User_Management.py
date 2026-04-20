"""
41_User_Management.py
Laura Smith — User Management (Wireframe 7)
Routes used: PUT 4.1 (update role), DELETE (deactivate user)
"""

import streamlit as st
import requests

API_BASE = "http://api:4000/admin"

st.set_page_config(page_title="User Management", page_icon="👥", layout="wide")
st.title("👥 User Management")
st.caption("Admin · Laura Smith")

@st.cache_data(ttl=30)
def fetch_users():
    try:
        r = requests.get(f"{API_BASE}/users")
        return r.json().get("users", [])
    except Exception:
        # Mock data
        return [
            {"user_id": 1,  "username": "laurasmith",  "email": "laura@example.com",  "role": "admin",   "is_active": True},
            {"user_id": 2,  "username": "ryang",        "email": "ryan@example.com",   "role": "staff",   "is_active": True},
            {"user_id": 3,  "username": "jsmith42",     "email": "j42@example.com",    "role": "student", "is_active": True},
            {"user_id": 4,  "username": "inactive_usr", "email": "old@example.com",    "role": "guest",   "is_active": False},
        ]

users = fetch_users()

col1, col2 = st.columns([2, 1])
with col1:
    search = st.text_input("🔍 Search by username or email", placeholder="Type to filter...")
with col2:
    role_filter = st.selectbox("Filter by role", ["All", "admin", "staff", "student", "nutrition_manager", "guest"])

active_filter = st.checkbox("Show active users only", value=True)

filtered = users
if search:
    filtered = [u for u in filtered if search.lower() in u["username"].lower() or search.lower() in u["email"].lower()]
if role_filter != "All":
    filtered = [u for u in filtered if u["role"] == role_filter]
if active_filter:
    filtered = [u for u in filtered if u["is_active"]]

st.caption(f"Showing {len(filtered)} of {len(users)} users")
st.divider()

ROLES = ["student", "staff", "admin", "nutrition_manager", "guest"]

for user in filtered:
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        with col1:
            status_icon = "🟢" if user["is_active"] else "🔴"
            st.markdown(f"**{user['username']}** {status_icon}")
            st.caption(user["email"])

        with col2:
            st.caption("User ID")
            st.write(f"#{user['user_id']}")

        with col3:
            new_role = st.selectbox(
                "Role",
                options=ROLES,
                index=ROLES.index(user["role"]) if user["role"] in ROLES else 0,
                key=f"role_{user['user_id']}",
            )
            if new_role != user["role"]:
                if st.button("Save", key=f"save_{user['user_id']}", type="primary"):
                    resp = requests.put(
                        f"{API_BASE}/users/{user['user_id']}/role",
                        json={"role": new_role},
                    )
                    if resp.status_code == 200:
                        st.success(f"Role updated to {new_role}")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Failed to update role")

        with col4:
            if user["is_active"]:
                if st.button("🚫 Deactivate", key=f"deact_{user['user_id']}", type="secondary"):
                    resp = requests.delete(f"{API_BASE}/users/{user['user_id']}")
                    if resp.status_code == 200:
                        st.warning(f"User {user['username']} deactivated")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Failed to deactivate user")
            else:
                st.caption("Inactive")
