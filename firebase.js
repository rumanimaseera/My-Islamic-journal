// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAsOQMS2yHqObgfLEDjo6WAV381K2ZQwEU",
  authDomain: "vmj-journal.firebaseapp.com",
  projectId: "vmj-journal",
  storageBucket: "vmj-journal.firebasestorage.app",
  messagingSenderId: "948431781907",
  appId: "1:948431781907:web:bc7b071315422a62e13fe6",
  measurementId: "G-R1SEB2J4B9"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);