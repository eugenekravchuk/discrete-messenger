import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getStorage } from "firebase/storage";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyAWMRWX_dZirFTvSwJAHqTdZ9-vKWXyukg",
  authDomain: "encrypted-messenger-ebd72.firebaseapp.com",
  projectId: "encrypted-messenger-ebd72",
  storageBucket: "encrypted-messenger-ebd72.appspot.com",
  messagingSenderId: "746606905003",
  appId: "1:746606905003:web:5cd6e506190ffb2ea759ee",
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const auth = getAuth();
export const storage = getStorage();
export const db = getFirestore();
