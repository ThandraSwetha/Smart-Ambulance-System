import streamlit as st
import pymongo

try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Smart_Ambulence_Dispatch"]

    users_col = db["users"]

    users_col.insert_one({"name": "test user"})

    st.success("MongoDB Connected Successfully")

except Exception as e:
    st.error(f"Connection Failed: {e}")