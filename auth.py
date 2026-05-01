import streamlit as st
import bcrypt
from database import users_col


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)


# -------- SIGNUP --------
def signup():

    st.subheader("Create Account")

    with st.form("signup"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Account Type", ["user", "hospital"])

        submit = st.form_submit_button("Register")

        if submit:
            if not username or not password:
                st.error("Fill all fields")
                return

            if users_col.find_one({"username": username}):
                st.error("User already exists")
                return

            users_col.insert_one({
                "username": username,
                "email": email,
                "password": hash_password(password),
                "role": role
            })

            st.success("Account created")


# -------- LOGIN --------
def login():

    st.subheader("Login")

    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submit = st.form_submit_button("Login")

        if submit:
            user = users_col.find_one({"username": username})

            if user and verify_password(password, user["password"]):
                st.session_state.user = username
                st.session_state.role = user["role"]
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")