import firebase_admin
from firebase_admin import credentials, firestore

# Path to your Firebase configuration file
cred = credentials.Certificate("firebase_config.json")  # Don't change the .json file

# Initialize Firebase with the credentials
firebase_admin.initialize_app(cred)

# Initialize Firestore (Database)
db = firestore.client()
