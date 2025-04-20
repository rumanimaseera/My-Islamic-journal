# 🔄 Converted feedback.py (Firebase)
import streamlit as st
import base64
from database import save_feedback

# Streamlit setup
st.set_page_config(page_title="Feedback | Islamic Journal", page_icon="📝")

# Function to encode image to base64
def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return None

# Background image setup
image_path = r"C:\Users\91887\VMJ_new\photos\vintage2.jpg"
image_base64 = get_base64_of_image(image_path)

if image_base64:
    st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("data:image/webp;base64,{image_base64}") no-repeat center center fixed;
        background-size: cover;
        font-family: Georgia, serif;
        color: #4a2e1f;
    }}
    textarea {{
        background-color: rgba(140, 85, 50, 0.85) !important;
        border-radius: 8px !important;
        padding: 10px !important;
        font-size: 16px !important;
        font-family: Georgia, serif !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        color: #f5e8d3 !important;
        width: 100% !important;
        max-width: 600px;
        margin: 0 auto !important;
        display: block !important;
    }}
    div.stButton > button {{
        background-color: #5a3820;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 8px 20px;
        font-family: Georgia, serif;
        display: block;
        margin: 10px auto;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# AUTH CHECK
if "user" not in st.session_state:
    st.warning("⚠ Please log in to view your journal.")
    st.stop()

user_id = st.session_state["user"]

# Page content
st.markdown("<h1 style='text-align: center;'>📢 Feedback</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>We appreciate your thoughts! Please share your feedback below.</p>", unsafe_allow_html=True)

# Feedback input
feedback_text = st.text_area("Your feedback")

# Submit button
if st.button("Submit"):
    if feedback_text.strip():
        save_feedback(user_id, feedback_text)
        st.success("✅ Thank you for your feedback!")
    else:
        st.error("⚠ Please enter some feedback before submitting.")
