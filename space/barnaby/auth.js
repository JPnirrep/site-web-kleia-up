/**
 * KLEIA SECURE AUTH V2.0 - FIREBASE SHIELD
 * Powered by ANTIGRAVITY & OPENCODE
 */

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getFirestore, doc, getDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "AIzaSyDIxL6BkN_J2nrgVuLB-bjG3L45lvQT_oE",
    authDomain: "kleia-audit-jp-2026.firebaseapp.com",
    projectId: "kleia-audit-jp-2026",
    storageBucket: "kleia-audit-jp-2026.firebasestorage.app",
    messagingSenderId: "1078553327416",
    appId: "1:1078553327416:web:6aaaba93afee2e130f33cd"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

document.getElementById('loginBtn').addEventListener('click', async function() {
    const firstname = document.getElementById('firstname').value.trim();
    const secretcode = document.getElementById('secretcode').value.trim();
    const isVisitor = document.getElementById('isVisitor').checked;
    const errorMsg = document.getElementById('errorMessage');

    errorMsg.style.display = 'none';

    // 1. MODE VISITEUR (Reste local pour la fluidité)
    if (isVisitor) {
        sessionStorage.setItem('kleia_auth', 'true');
        sessionStorage.setItem('kleia_role', 'visitor');
        sessionStorage.setItem('kleia_user', 'Visiteur');
        window.location.href = 'index.html';
        return;
    }

    if (!firstname || !secretcode) return;

    console.log("Tentative de connexion pour:", firstname);

    try {
        // 2. VÉRIFICATION CLOUD (FIREBASE SHIELD)
        const docRef = doc(db, "access_tokens", secretcode);
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
            const data = docSnap.data();
            console.log("Jeton trouvé, propriétaire:", data.owner);
            
            // Vérification du prénom associé au jeton
            if (data.owner.toLowerCase() === firstname.toLowerCase()) {
                console.log("Auth Succès !");
                sessionStorage.setItem('kleia_auth', 'true');
                sessionStorage.setItem('kleia_role', data.role || 'client');
                sessionStorage.setItem('kleia_user', data.owner);
                window.location.href = 'index.html';
            } else {
                console.warn("Propriétaire ne correspond pas:", data.owner, "vs", firstname);
                throw new Error("Identité non concordante");
            }
        } else {
            console.warn("Jeton non trouvé dans Firestore");
            throw new Error("Jeton invalide");
        }
    } catch (error) {
        console.error("Auth Error Detail:", error);
        errorMsg.textContent = "Erreur de protocole : " + (error.message === "Failed to fetch" ? "Connexion Cloud impossible (vérifiez votre internet ou protocole local)" : error.message);
        errorMsg.style.display = 'block';
    }
});

document.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        document.getElementById('loginBtn').click();
    }
});
