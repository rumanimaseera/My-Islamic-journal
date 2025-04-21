import streamlit as st
import base64
import requests
from datetime import datetime

# 🔹 Set Streamlit Page Config
st.set_page_config(page_title="Home | Islamic Journal", page_icon="📜", layout="wide")

# ========================
# 1) Background Image Setup
# ========================
def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return None

image_path = "photos/vintage2.jpg"  # ✅ Just the relative path
image_base64 = get_base64_of_image(image_path)

if image_base64:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpg;base64,{image_base64}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Background image could not be loaded.")

# ========================
# 2) Hijri Date & Prayer Times
# ========================
def get_hijri_date():
    today = datetime.now().strftime('%d-%m-%Y')
    url = f'https://api.aladhan.com/v1/gToH?date={today}'
    try:
        response = requests.get(url)
        data = response.json()
        if 'data' in data and 'hijri' in data['data']:
            hijri = data['data']['hijri']
            return f"{hijri['day']} {hijri['month']['en']} {hijri['year']}"
        else:
            st.error("Hijri date data not found in the API response.")
            return None
    except Exception as e:
        st.error(f"Error fetching Hijri date: {e}")
        return None

def get_prayer_times(school=0):
    params = {
        'latitude': 19.0760,
        'longitude': 72.8777,
        'method': 2,
        'school': school
    }
    url = 'https://api.aladhan.com/v1/timings'
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data['data']['timings']
    except Exception as e:
        st.error(f"Error fetching prayer times: {e}")
        return None

# ========================
# 3) Page Title / Headers
# ========================
st.markdown('<h1 style="text-align:center; font-size: 50px; color: #5a3820; font-family: Georgia, serif;">📜 Welcome to Virtual Mood Journal</h1>', unsafe_allow_html=True)
st.markdown('<h1 style="text-align:center; font-size: 60px; color: #5a3820; font-family: Traditional Arabic, serif;">بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ</h1>', unsafe_allow_html=True)

# ========================
# 4) Intro & Hadith Box
# ========================
st.markdown("""
    <div style="background: rgba(90, 60, 30, 0.7); padding: 20px; border-radius: 15px; text-align: center;
                font-size: 20px; font-weight: bold; color: white; width: 60%; margin: auto;
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3); font-family: 'Georgia', serif;">
        Express your thoughts, understand your emotions, and receive spiritual guidance. 
        Write your daily experiences, and let our AI guide your soul with personalized duas.
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.85); border-left: 5px solid #5a3820;
                padding: 15px; margin: 40px auto; width: 60%; font-family: 'Georgia', serif;
                text-align: center; font-size: 18px; color: #3b2c20; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                border-radius: 10px;">
        <i>Prophet Muhammad (ﷺ) said:</i><br>
        "Verily, in the remembrance of Allah do hearts find rest."<br><b>(Quran 13:28)</b>
    </div>
""", unsafe_allow_html=True)

# ========================
# 5) Navigation with Session State
# ========================
if "current_section" not in st.session_state:
    st.session_state.current_section = "Home"
    
def navigate_to(section):
    st.write(f"Navigating to: {section}")
    
    # Save current section to session state before clearing
    st.session_state.current_section = section

    if section == "Login":
        # Ensure the page name matches the one in your app structure
        st.switch_page("pages/authentication.py")  # Page name should be 'authentication', not 'authentication.py'
    else:
        # Set the new section after clearing session state
        st.session_state.current_section = section



# ========================
# 6) Buttons & Styling
# ========================
st.markdown("""
<style>
div.stButton > button {
    background-color: rgba(90, 60, 30, 0.7);
    color: white;
    border-radius: 10px;
    padding: 0.5em 1em;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s ease-in-out;
}
div.stButton > button:hover {
    background-color: #3B1F1F;
    transform: scale(1.02);
}
.button-container {
    display: flex;
    justify-content: center;
    margin-top: 30px;
}
.button-inner {
    display: flex;
    justify-content: space-between;
    gap: 40px;
    width: 800px;
}
</style>
""", unsafe_allow_html=True)

# ========================
# 7) Button Actions
# ========================
st.markdown('<div class="button-container"><div class="button-inner">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📖 About Us"):
        navigate_to("About Us")
with col2:
    if st.button("🔑 Login / Register"):
        navigate_to("Login")
with col3:
    if st.button("🌟 Features"):
        navigate_to("Features")
with col4:
    if st.button("🗓️ Islamic Date"):
        navigate_to("Hijri")
with col5:
    if st.button("🕋 Prayer Times"):
        navigate_to("Prayers")

st.markdown('</div></div>', unsafe_allow_html=True)

# ========================
# 8) Render Section Content
# ========================
if st.session_state.current_section == "About Us":
    st.markdown("""
        <div style="background: rgba(90, 60, 30, 0.7); padding: 20px; border-radius: 15px;
                    text-align: center; font-size: 20px; font-weight: bold; color: white;
                    width: 60%; margin: auto; box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
                    font-family: 'Georgia', serif;">
            <h2>📖 About Us</h2>
            <p>Welcome to Virtual Mood Journal, where your emotions meet faith. 
            Our AI-powered system allows you to document your thoughts while receiving 
            personalized Islamic duas for spiritual guidance.</p>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_section == "Features":
    st.markdown("""
        <div style="background: rgba(90, 60, 30, 0.7); padding: 20px; border-radius: 15px;
                    text-align: center; font-size: 20px; font-weight: bold; color: white;
                    width: 60%; margin: auto; box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
                    font-family: 'Georgia', serif;">
            <h2>🌟 Features</h2>
            <ul style="text-align: left;">
                <li>✍️ <b>Write and Reflect</b></li>
                <li>🤖 <b>AI-Powered Guidance</b></li>
                <li>📊 <b>Mood Analytics</b></li>
                <li>🔐 <b>Private & Secure</b></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_section == "Hijri":
    hijri_date = get_hijri_date()
    if hijri_date:
        st.markdown(f"""
            <div style="text-align: center; 
                        font-size: 28px; 
                        font-weight: bold; 
                        color: #5a3820; 
                        font-family: 'Georgia', serif;
                        margin-top: 20px;">
                🗓️ Today's Hijri Date: {hijri_date}
            </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_section == "Prayers":
    st.markdown("### 🕋 Prayer Times (Mumbai, India)")
    timings = get_prayer_times()
    if timings:
        for prayer, time in timings.items():
            st.markdown(f"""
                <div style="background-color: rgba(255,255,255,0.8); 
                            padding: 10px; margin: 10px 0; 
                            border-left: 5px solid #5a3820; 
                            font-size: 18px; font-family: 'Georgia'; 
                            color: #3b2c20; border-radius: 8px;">
                    <b>{prayer}</b>: {time}
                </div>
            """, unsafe_allow_html=True)

# ========================
# 9) Social Media Footer
# ========================
st.markdown(
    """
    <style>
    .footer {
        display: flex;
        justify-content: center;
        margin-top: 40px;
        font-size: 18px;
        font-family: 'Georgia', serif;
    }
    .social-links a {
        color: #5a3820;
        text-decoration: none;
        font-weight: bold;
        margin: 0 15px;
        font-size: 22px;
        transition: 0.3s;
    }
    .social-links a:hover {
        color: #9c6b30;
    }
    </style>
    <div class="footer">
        <div class="social-links">
            <a href="https://www.instagram.com/zyha.deen?igsh=MW51amk4eHVic280Zw==" target="_blank">Instagram</a>
            <a href="https://twitter.com/yourprofile" target="_blank">Twitter</a>
            <a href="https://linkedin.com/in/yourprofile" target="_blank">LinkedIn</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
