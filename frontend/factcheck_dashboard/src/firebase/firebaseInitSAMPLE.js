// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "[ADD YOUR KEYS HERE]",
  authDomain: "[ADD YOUR KEYS HERE]",
  projectId: "[ADD YOUR KEYS HERE]",
  storageBucket:"[ADD YOUR KEYS HERE]",
  messagingSenderId: "[ADD YOUR KEYS HERE]",
  appId: "[ADD YOUR KEYS HERE]",
  measurementId: "[ADD YOUR KEYS HERE]",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);