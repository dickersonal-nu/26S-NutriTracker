import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="User Management", page_icon="👤")
SideBarLinks()


if "role" not in st.session_state or st.session_state["role"] != "admin":
    st.error("You must be logged in as an Admin to view this page.")
    st.stop()

API_BASE = "http://api:4000"

st.title("👤 User Management")
st.markdown("Update user roles or deactivate user accounts.")
st.divider()


st.subheader("Update User Role")

with st.form("update_role_form"):
    user_id_role = st.number_input("User ID", min_value=1, step=1, key="role_uid")
    new_role = st.selectbox(
        "New Role",
        ["student", "staff", "admin", "nutrition_manager", "guest"],
    )
    submitted_role = st.form_submit_button("Update Role", use_container_width=True)

if submitted_role:
    try:
        r = requests.put(
            f"{API_BASE}/admin/users/{int(user_id_role)}/role",
            json={"role": new_role},
            timeout=5,
        )
        if r.status_code == 200:
            data = r.json()
            st.success(
                f"✅ User {data['user_id']} role updated: "
                f"**{data['old_role']}** → **{data['new_role']}**"
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
                f"{API_BASE}/admin/users/{int(user_id_deact)}",
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

st.divider()


st.subheader("Push Menu Updates")
st.markdown("Update menu items for a dining hall. Each item requires an ID, name, and calorie count.")

with st.form("menu_update_form"):
    dining_hall_id = st.number_input("Dining Hall ID", min_value=1, step=1)
    effective_date = st.date_input("Effective Date")

    st.markdown("**Items to Update** (enter one per line as `item_id,item_name,calories`)")
    items_text = st.text_area(
        "Items",
        placeholder="1,Grilled Chicken,350\n2,Caesar Salad,220",
        height=120,
    )
    submitted_menu = st.form_submit_button("Push Updates", use_container_width=True)

if submitted_menu:

    items = []
    errors = []
    for i, line in enumerate(items_text.strip().splitlines(), start=1):
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3:
            errors.append(f"Line {i}: expected `item_id,item_name,calories` — got `{line}`")
            continue
        try:
            items.append({
                "item_id":   int(parts[0]),
                "item_name": parts[1],
                "calories":  int(parts[2]),
            })
        except ValueError:
            errors.append(f"Line {i}: item_id and calories must be integers.")

    if errors:
        for err in errors:
            st.error(err)
    elif not items:
        st.error("No valid items to update.")
    else:
        try:
            payload = {
                "dining_hall_id": int(dining_hall_id),
                "items":          items,
                "effective_date": str(effective_date),
            }
            r = requests.put(f"{API_BASE}/admin/menu-updates", json=payload, timeout=5)
            if r.status_code == 200:
                data = r.json()
                st.success(
                    f"✅ Menu updated for dining hall {data['dining_hall_id']} "
                    f"— {data['items_updated']} item(s) effective {data['effective_date']}."
                )
            else:
                st.error(f"Error {r.status_code}: {r.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Could not reach API: {e}")