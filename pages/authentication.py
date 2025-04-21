# 🔐 Converted authentication.py (uses Firebase now)
import streamlit as st
import time
import base64
from database import save_user, authenticate_user

st.set_page_config(page_title="🔐 Authentication", layout="centered")

# Background image setup
def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return None

image_path = r"C:\Users\91887\Islamic_journal\photos\vintage2.jpg"
image_base64 = get_base64_of_image(image_path)

if image_base64:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/webp;base64,{image_base64}") no-repeat center center fixed;
            background-size: cover;
        }}
        h1 {{ text-align: center; font-size: 50px; color: #5a3820; font-family: Georgia, serif; }}
        .custom-button {{ background-color: #5a3820 !important; color: white !important; font-size: 16px; font-weight: bold; padding: 10px 15px; border-radius: 8px; border: none; cursor: pointer; transition: 0.3s; width: 140px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); }}
        .custom-button:hover {{ background-color: #9c6b30 !important; }}
        div.stButton > button {{ background-color: rgba(90, 60, 30, 0.7); color: white; border-radius: 10px; padding: 0.5em 1em; font-size: 16px; font-weight: bold; transition: 0.3s ease-in-out; }}
        div.stButton > button:hover {{ background-color: #3B1F1F; transform: scale(1.02); }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Header
st.markdown('<h1>User Authentication</h1>', unsafe_allow_html=True)

# Radio buttons for Login/Register
st.markdown("""
<style>
.stRadio > div[role='radiogroup'] label {
    background-color: rgba(90, 60, 30, 0.7);
    border-radius: 10px;
    padding: 10px 20px;
    color: #5a3820;
    font-weight: bold;
    transition: 0.3s;
    cursor: pointer;
}
.stRadio > div[role='radiogroup'] label:hover {
    background-color: rgba(45, 25, 15, 0.8);
}
</style>
""", unsafe_allow_html=True)

auth_mode = st.radio("Select an option:", ["Login", "Register"], horizontal=True, label_visibility="collapsed", key="auth_mode_radio")

if auth_mode == "Register":
    st.markdown('<h2 style="color: #5a3820; font-family: Georgia, serif;">Create a New Account</h2>', unsafe_allow_html=True)
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Register"):
        if authenticate_user(new_username, new_password):
            st.error("❌ Username already exists. Choose a different one.")
        else:
            save_user(new_username, new_password)
            st.success("✅ Registration Successful! You can now log in.")
            st.balloons()

if auth_mode == "Login":
    st.markdown('<h2 style="color: #5a3820; font-family: Georgia, serif;">Log in to Your Account</h2>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("✅ Login Successful! Redirecting...")
            st.session_state["user"] = username
            time.sleep(1)
            st.switch_page("pages/journal.py")
        else:
            st.error("❌ Invalid Credentials. Try Again.")
