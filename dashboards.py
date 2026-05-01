import streamlit as st
from database import emergency_col, users_col, feedback_col


# -------- USER DASHBOARD --------
def user_dashboard():

    st.header("👤 User Dashboard")

    data = emergency_col.find({"user": st.session_state.user})

    for d in data:
        st.info(f"🚑 {d['ambulance']} | ETA: {d['eta']} mins")


# -------- HOSPITAL DASHBOARD --------
def hospital_dashboard():

    st.header("🏥 Hospital Dashboard")

    incoming = emergency_col.find({"status": "en route"})

    for d in incoming:
        st.warning(
            f"🚑 {d['ambulance']} | Patient: {d['user']} | ETA: {d['eta']} mins"
        )


# -------- ADMIN DASHBOARD --------
def admin_dashboard():

    st.header("⚙ Admin Dashboard")

    total_users = users_col.count_documents({"role": "user"})
    hospitals = users_col.count_documents({"role": "hospital"})
    active = emergency_col.count_documents({"status": "en route"})

    col1, col2, col3 = st.columns(3)

    col1.metric("Users", total_users)
    col2.metric("Hospitals", hospitals)
    col3.metric("Active Emergencies", active)

    st.write("### Feedback")

    for f in feedback_col.find():
        st.write(f["message"])