import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyAs3mfIDyJYMkyqzUUJnijaAKhd6hbEZXo",
  authDomain: "alpha-262f3.firebaseapp.com",
  projectId: "alpha-262f3",
  storageBucket: "alpha-262f3.appspot.com",
  messagingSenderId: "625645982946",
  appId: "1:625645982946:web:0869be283cb5533f74fabb",
  measurementId: "G-NY11DZRYX6"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const logoutBtn = document.getElementById('logout-btn');

const provider = new GoogleAuthProvider();

logoutBtn.addEventListener('click', () => {
  signOut(auth)
    .then(() => {
      console.log('Signed out successfully');
      location.replace('/')

    })
    .catch((error) => {
      console.error(error.message);
    });
});