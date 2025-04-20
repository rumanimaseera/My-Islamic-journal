# 🔄 Converted database.py (Firebase Only)
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Save user
def save_user(username, password):
    user_data = {
        "username": username,
        "password": password
    }
    db.collection("users").document(username).set(user_data)

# Authenticate user
def authenticate_user(username, password):
    doc = db.collection("users").document(username).get()
    if doc.exists and doc.to_dict()["password"] == password:
        return True
    return False

# Save journal entry
def save_journal_entry(user_id, entry_text, mood, translation="", reference="", mood_output=""):
    timestamp = datetime.datetime.now().isoformat()
    entry = {
        "user_id": user_id,
        "entry_text": entry_text,
        "mood": mood,
        "translation": translation,
        "reference": reference,
        "mood_output": mood_output,
        "date": timestamp,
        "created_at": timestamp
    }
    db.collection("journal_entries").add(entry)

# Fetch journal entries by date range
def fetch_entries(user_id, start_date, end_date):
    return db.collection("journal_entries") \
             .where("user_id", "==", user_id) \
             .where("created_at", ">=", start_date.isoformat()) \
             .where("created_at", "<=", end_date.isoformat()) \
             .stream()

# Fetch entry by ID (for display)
def fetch_entry_by_id(entry_id):
    docs = db.collection("journal_entries").where("id", "==", entry_id).stream()
    for doc in docs:
        return doc.to_dict()
    return None

# Save feedback
def save_feedback(user_id, feedback):
    timestamp = datetime.datetime.now().isoformat()
    feedback_data = {
        "user_id": user_id,
        "feedback": feedback,
        "created_at": timestamp
    }
    db.collection("feedback").add(feedback_data)
