from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import streamlit as st
import pandas as pd
import torch
import os
import time
import base64

# 🔄 Firebase
import firebase_admin
from firebase_admin import credentials, firestore

# ✅ Replace this with your Firebase credentials path
FIREBASE_CREDENTIAL_PATH = "your-firebase-key.json"

# Initialize Firebase (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIAL_PATH)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to encode image to Base64
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
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Background image could not be loaded.")

if "user" not in st.session_state:
    st.warning("⚠ Please log in to view your journal.")
    st.stop()

user_id = st.session_state["user"]

if "redirect_to_journal" in st.session_state:
    del st.session_state["redirect_to_journal"]
    st.switch_page("pages/journal.py")

@st.cache_resource
def load_model():
    model_name = "lrei/distilroberta-base-emolit"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

DUAS_CSV_FILE = "duas.csv"

@st.cache_data
def get_dua_for_mood(mood):
    try:
        if not os.path.exists(DUAS_CSV_FILE):
            st.error("❌ ERROR: Dua CSV file not found!")
            return None, None, None

        df = pd.read_csv(DUAS_CSV_FILE, encoding="utf-8")  
        df["Mood"] = df["Mood"].str.lower().str.strip()
        mood = mood.lower().strip()

        result = df[df["Mood"] == mood]

        if result.empty:
            return None, None, None

        dua = result.iloc[0].get("Dua (Arabic)", "No Dua Available")
        translation = result.iloc[0].get("Dua Translation", "No Translation Available")
        reference = result.iloc[0].get("Dua Reference", "No Reference Available")

        return dua, translation, reference
    except Exception as e:
        st.error(f"❌ CSV Error: {e}")
        return None, None, None

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
        background-color: rgba(165, 120, 80, 0.85) !important;        
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

st.markdown('<h1 style="text-align:center; font-size: 50px; color: #5a3820; font-family: Georgia, serif;">🌙 Virtual Mood Journal</h1>', unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center; font-size: 30px; color: #5a3820; font-family: Georgia, serif;">Write about your day, and we will suggest a <strong>Dua</strong> based on your mood.</h1>', unsafe_allow_html=True)

entry_text = st.text_area("✍️ Write about your day:", height=200)

if st.button("🔍 Analyze Mood"):
    if entry_text.strip():
        emotion_pipeline = pipeline(
            "text-classification",
            model="lrei/distilroberta-base-emolit",
            return_all_scores=True,
            device=0 if torch.cuda.is_available() else -1
        )

        emotion_results = emotion_pipeline(entry_text)[0]
        detected_emotion = max(emotion_results, key=lambda x: x['score'])
        detected_emotion_label = detected_emotion['label']
        confidence = detected_emotion['score']

        st.markdown(f"### 🎯 Detected Mood: {detected_emotion_label.capitalize()}")

        dua, translation, reference = get_dua_for_mood(detected_emotion_label)

        if dua:
            st.markdown(f"### 🕌 Recommended Dua")
            st.markdown(f"""
                <div style="background-color: #f8d7da; padding: 10px; border-radius: 10px; border-left: 5px solid #721c24;">
                    <h4 style="color: #721c24;">📜 Arabic:</h4>
                    <p style="font-size: 18px; font-weight: bold; color: #721c24;">{dua}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
                <div style="background-color: #d1ecf1; padding: 10px; border-radius: 10px; border-left: 5px solid #0c5460;">
                    <h4 style="color: #0c5460;">🌍 Translation:</h4>
                    <p style="font-size: 18px; font-weight: bold; color: #0c5460;">{translation}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
                <div style="background-color: #fff3cd; padding: 10px; border-radius: 10px; border-left: 5px solid #856404;">
                    <h4 style="color: #856404;">📖 Reference:</h4>
                    <p style="font-size: 18px; font-weight: bold; color: #856404;">{reference}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ No matching dua found for mood: {detected_emotion_label}")

        # Save entry to Firestore
        db.collection("journal_entries").add({
            "user_id": user_id,
            "entry_text": entry_text,
            "mood": detected_emotion_label,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

        st.success(f"✅ Entry saved! Mood detected: {detected_emotion_label}")

    else:
        st.error("⚠️ Please enter some text before analyzing.")

if st.button("⬅ Back to Journal"):
    st.switch_page("pages/journal.py")

if st.button("💬 Give Feedback"):
    st.switch_page("pages/feedback.py")
