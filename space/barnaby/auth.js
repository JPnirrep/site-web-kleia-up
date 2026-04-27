/**
 * KLEIA AUTH SYSTEM V1.0
 * Logic by OPENCODE
 */

document.getElementById('loginBtn').addEventListener('click', function() {
    const firstname = document.getElementById('firstname').value.trim();
    const secretcode = document.getElementById('secretcode').value.trim();
    const isVisitor = document.getElementById('isVisitor').checked;
    const errorMsg = document.getElementById('errorMessage');

    // Reset error
    errorMsg.style.display = 'none';

    // 1. GESTION DU MODE VISITEUR
    if (isVisitor) {
        sessionStorage.setItem('kleia_auth', 'true');
        sessionStorage.setItem('kleia_role', 'visitor');
        sessionStorage.setItem('kleia_user', 'Visiteur');
        window.location.href = 'index.html';
        return;
    }

    // 2. GESTION DU MODE ADMIN (JP & SANDRINA)
    const ADMIN_ID = "adminjp";
    const ADMIN_CODE = "668081ppJ!?";

    if (firstname === ADMIN_ID && secretcode === ADMIN_CODE) {
        sessionStorage.setItem('kleia_auth', 'true');
        sessionStorage.setItem('kleia_role', 'client');
        sessionStorage.setItem('kleia_user', 'Admin');
        window.location.href = 'index.html';
        return;
    }

    // 3. GESTION DU MODE CLIENT (BARNABY)
    const VALID_FIRSTNAME = "Barnaby";
    const VALID_CODE = "KUP-BBN-26-0422";

    // Vérification insensible à la casse pour le prénom
    if (firstname.toLowerCase() === VALID_FIRSTNAME.toLowerCase() && secretcode === VALID_CODE) {
        sessionStorage.setItem('kleia_auth', 'true');
        sessionStorage.setItem('kleia_role', 'client');
        sessionStorage.setItem('kleia_user', VALID_FIRSTNAME);
        window.location.href = 'index.html';
    } else {
        errorMsg.style.display = 'block';
    }
});

// Permettre la validation avec la touche Entrée
document.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        document.getElementById('loginBtn').click();
    }
});
