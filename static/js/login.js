import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-analytics.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyAvWgTWCkYPHHgOIDYj5VdB020wVHbS3tc",
  authDomain: "newsanalyser-6ffa9.firebaseapp.com",
  projectId: "newsanalyser-6ffa9",
  storageBucket: "newsanalyser-6ffa9.appspot.com",
  messagingSenderId: "53185007768",
  appId: "1:53185007768:web:d2af3c718df4a0595280ed",
  measurementId: "G-VRQS7HCFYJ"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const googleSignInBtn = document.getElementById('google-sign-in-btn');
const userDisplay = document.getElementById('user-info');
const loginForm = document.getElementById('login-form');
const dashboard = document.getElementById('dashboard');

const provider = new GoogleAuthProvider();

googleSignInBtn.addEventListener('click', () => {
  signInWithPopup(auth, provider)
    .then((result) => {
      const user = result.user;
      console.log(`Signed in as ${user.displayName}`);
      userDisplay.textContent = `Welcome, ${user.displayName}!`;
      const useremail = user.email;
      fetch('http://127.0.0.1:8000/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: useremail, name: user.displayName })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to send user data to the server');
        }
        console.log('User data sent to the server successfully', useremail);
        // Redirect to index.html
        window.location.href = "/index";})
      .catch(error => {
        console.error(error.message);
      });
    })
    .catch((error) => {
      console.error(error.message);
    });
});
