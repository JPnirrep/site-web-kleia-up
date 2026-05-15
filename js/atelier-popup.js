/**
 * KLEIA-UP - POP-UP ATELIER "Prendre sa place sans forcer"
 * Stockage: PHP JSON (priorite) > Firestore (si dispo) > localStorage (fallback).
 * Periode: 16 mai au 2 juin 2026 12h00.
 */

(function() {
    console.log('[KLEIA] Popup atelier charge');

    // --- Firebase (optionnel, tente l'auth anonyme si le SDK est la) ---
    var db = null;
    if (typeof firebase !== 'undefined') {
        try {
            firebase.initializeApp({
                apiKey: "AIzaSyDIxL6BkN_J2nrgVuLB-bjG3L45lvQT_oE",
                authDomain: "kleia-audit-jp-2026.firebaseapp.com",
                projectId: "kleia-audit-jp-2026",
                storageBucket: "kleia-audit-jp-2026.firebasestorage.app",
                messagingSenderId: "1078553327416",
                appId: "1:1078553327416:web:6aaaba93afee2e130f33cd"
            });
            db = firebase.firestore();
            // Tentative auth anonyme silencieuse
            firebase.auth().signInAnonymously().then(function() {
                console.log('[KLEIA] Firestore auth OK');
            }).catch(function() {
                console.log('[KLEIA] Firestore auth non dispo, utilisera PHP/localStorage');
                db = null;
            });
        } catch(e) {
            console.log('[KLEIA] Firebase init echouee:', e.message);
        }
    }

    var STORAGE_KEY = 'kleia_atelier_closed_2026';
    var PHP_URL = 'php/atelier-subscribe.php';
    var BREVO_PUSH_URL = 'php/brevo-push.php';
    var CONFIRM_URL = 'atelier-place.html';
    var isOnline = (window.location.protocol !== 'file:');

    // --- DATE GUARD (desactive pour test) ---
    // var now = new Date();
    // if (now < new Date('2026-05-16T00:00:00+02:00') || now > new Date('2026-06-02T12:00:00+02:00')) return;

    // --- SESSION GUARD (desactive pour test) ---
    // if (localStorage.getItem(STORAGE_KEY)) return;

    // --- CSS ---
    var s = document.createElement('style');
    s.textContent = '#atelier-place-popup-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(26,26,26,0.45);backdrop-filter:blur(15px);-webkit-backdrop-filter:blur(15px);z-index:100000;display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity 0.6s ease;padding:10px}' +
        '#atelier-place-popup-content{background:#FDFCF0;width:100%;max-width:960px;max-height:98vh;border-radius:40px;position:relative;box-shadow:0 40px 100px rgba(88,0,23,0.25);transform:translateY(30px);transition:all 0.7s cubic-bezier(0.19,1,0.22,1);padding:40px;border:1px solid rgba(139,29,61,0.05);text-align:left;overflow-y:auto}' +
        '#atelier-place-popup-overlay.active{opacity:1}' +
        '#atelier-place-popup-overlay.active #atelier-place-popup-content{transform:translateY(0)}' +
        '.atelier-close{position:absolute;top:20px;right:20px;width:36px;height:36px;background:rgba(139,29,61,0.05);border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:100}' +
        '.atelier-grid{display:grid;grid-template-columns:1.15fr 0.85fr;gap:40px;align-items:center}' +
        '.atelier-left{padding-right:15px;border-right:1px solid rgba(139,29,61,0.08)}' +
        '.atelier-logo{height:70px;margin-bottom:25px}' +
        '.atelier-title{font-family:\'Ranade\',sans-serif;font-weight:800;font-size:1.9rem;line-height:1.1;color:#1A1A1A;margin-bottom:12px}' +
        '.atelier-title em{font-style:italic;color:#8B1D3D;display:block}' +
        '.atelier-subtitle{font-size:0.95rem;color:#8B1D3D;font-weight:700;margin-bottom:25px;letter-spacing:1px;text-transform:uppercase;display:inline-block}' +
        '.atelier-context{color:#333;font-size:0.95rem;line-height:1.55;margin-bottom:20px;background:rgba(255,255,255,0.4);padding:15px;border-radius:15px}' +
        '.atelier-highlight{font-weight:800;color:#8B1D3D}' +
        '.atelier-right{display:flex;flex-direction:column;gap:20px}' +
        '.atelier-programme{background:rgba(139,29,61,0.04);border-radius:20px;padding:20px;border:1px solid rgba(139,29,61,0.06);margin-bottom:5px}' +
        '.atelier-prog-item{display:flex;gap:10px;margin-bottom:10px;font-size:0.88rem;line-height:1.35}' +
        '.atelier-prog-item:last-child{margin-bottom:0}' +
        '.atelier-right-box{background:#FFF;padding:30px;border-radius:25px;box-shadow:0 15px 40px rgba(139,29,61,0.08);border:1px solid rgba(139,29,61,0.05)}' +
        '.atelier-form{display:grid;gap:12px}' +
        '.atelier-input{width:100%;padding:16px 20px;border-radius:15px;font-family:\'Ranade\',sans-serif;border:1px solid rgba(139,29,61,0.1);background:#fafafa;font-size:1rem;outline:none;box-sizing:border-box}' +
        '.atelier-consent{display:flex;align-items:flex-start;gap:10px;font-size:0.78rem;color:#666;line-height:1.4;cursor:pointer}' +
        '.atelier-consent input{margin-top:2px;accent-color:#8B1D3D;min-width:16px;height:16px;cursor:pointer}' +
        '.atelier-consent span{cursor:pointer}' +
        '.atelier-btn{background:linear-gradient(135deg,#8B1D3D 0%,#D70040 100%);color:#FFF;padding:18px;border-radius:15px;border:none;font-family:\'Ranade\',sans-serif;font-weight:800;font-size:1rem;text-transform:uppercase;cursor:pointer;margin-top:5px;box-shadow:0 8px 25px rgba(139,29,61,0.3);transition:all 0.3s ease}' +
        '.atelier-btn:hover{transform:translateY(-2px);box-shadow:0 12px 30px rgba(139,29,61,0.4)}' +
        '.atelier-btn:disabled{opacity:0.6;cursor:not-allowed;transform:none}' +
        '.atelier-footer{margin-top:20px;font-size:0.85rem;color:#777;font-style:italic;text-align:center}' +
        '.atelier-error{color:#D70040;font-size:0.82rem;text-align:center;display:none}' +
        '@media(max-width:900px){.atelier-grid{grid-template-columns:1fr;gap:30px}.atelier-left{border-right:none;padding-right:0}#atelier-place-popup-content{padding:30px}.atelier-logo{height:60px}}';
    document.head.appendChild(s);

    // --- HTML ---
    document.body.insertAdjacentHTML('beforeend',
        '<div id="atelier-place-popup-overlay"><div id="atelier-place-popup-content">' +
        '<div class="atelier-close" id="atelier-place-popup-close" aria-label="Fermer">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></div>' +
        '<div class="atelier-grid"><div class="atelier-left">' +
        '<img src="assets/logo_kleia.png" class="atelier-logo" alt="Logo KLEIA-UP">' +
        '<h2 class="atelier-title">Prendre sa place<br><em>sans forcer</em></h2>' +
        '<p class="atelier-subtitle">Atelier visio — Mardi 2 juin de 12h a 13h</p>' +
        '<div class="atelier-context"><span class="atelier-highlight">Vous sentez-vous encore comme un spectateur de votre propre vie ?</span><br><br>' +
        'Parfois, on a l\'impression d\'avoir un plafond de verre au-dessus de la tete. On attend un signal, une autorisation ou ce fameux sentiment de legitimite qui ne vient jamais. ' +
        'On regarde les autres prendre la parole et occuper l\'espace, pendant qu\'on reste sur la reserve, de peur d\'en faire trop ou de ne pas en faire assez.<br><br>' +
        'Si vous ressentez ces freins, cet atelier est pour vous.</div>' +
        '<div class="atelier-programme">' +
        '<p style="margin-bottom:15px;font-weight:800;text-transform:uppercase;font-size:0.8rem;letter-spacing:1px">Ce que nous allons vivre :</p>' +
        '<div class="atelier-prog-item"><span>1.</span> <p><strong>Immersion de 45 minutes</strong> pour comprendre ce qui vous retient reellement dans l\'ombre.</p></div>' +
        '<div class="atelier-prog-item"><span>2.</span> <p><strong>Pratique de posture</strong> pour tester, en direct, un gain de presence immediat.</p></div>' +
        '<div class="atelier-prog-item"><span>3.</span> <p><strong>Un declic</strong> pour oser faire ce premier pas que vous repoussez depuis trop longtemps.</p></div>' +
        '</div></div><div class="atelier-right"><div class="atelier-right-box">' +
        '<form id="atelier-place-popup-form" class="atelier-form">' +
        '<input type="text" id="atelier-prenom" class="atelier-input" placeholder="Ton prenom" required>' +
        '<input type="text" id="atelier-nom" class="atelier-input" placeholder="Ton nom" required>' +
        '<input type="email" id="atelier-email" class="atelier-input" placeholder="Ton email" required>' +
        '<label class="atelier-consent"><input type="checkbox" id="atelier-consent" required><span>Je consens a recevoir des communications de la part de KLEIA-UP</span></label>' +
        '<p class="atelier-error" id="atelier-place-popup-error"></p>' +
        '<button type="submit" class="atelier-btn" id="atelier-submit">JE M\'INSCRIS A L\'ATELIER</button>' +
        '<p class="atelier-footer">Cessez de forcer. Commencez a habiter votre place.</p>' +
        '</form></div></div></div></div></div>');

    // --- DOM ---
    var overlay = document.getElementById('atelier-place-popup-overlay');
    var closeBtn = document.getElementById('atelier-place-popup-close');

    setTimeout(function() { overlay.classList.add('active'); }, 1800);

    var closePopup = function() {
        overlay.classList.remove('active');
        setTimeout(function() { overlay.remove(); }, 600);
        localStorage.setItem(STORAGE_KEY, 'true');
    };
    closeBtn.onclick = closePopup;
    overlay.onclick = function(e) { if (e.target === overlay) closePopup(); };

    // --- Fonction: sauvegarde locale de fallback ---
    var saveLocally = function(prenom, nom, email) {
        var key = 'kleia_atelier_inscriptions';
        var list = [];
        try { list = JSON.parse(localStorage.getItem(key) || '[]'); } catch(_) {}
        list.push({ prenom: prenom, nom: nom, email: email.toLowerCase(), consent: true, created_at: new Date().toISOString(), source: 'popup-atelier-fallback' });
        localStorage.setItem(key, JSON.stringify(list));
        console.log('[KLEIA] Sauvegarde locale OK (' + list.length + ' entrees)');
    };

    // --- SUBMIT ---
    document.getElementById('atelier-place-popup-form').onsubmit = function(e) {
        e.preventDefault();
        var submitBtn = document.getElementById('atelier-submit');
        var errorEl = document.getElementById('atelier-place-popup-error');
        var consentCb = document.getElementById('atelier-consent');

        if (!consentCb.checked) {
            errorEl.textContent = 'Vous devez accepter de recevoir des communications.';
            errorEl.style.display = 'block';
            return;
        }
        errorEl.style.display = 'none';

        var prenom = document.getElementById('atelier-prenom').value.trim();
        var nom    = document.getElementById('atelier-nom').value.trim();
        var email  = document.getElementById('atelier-email').value.trim();

        submitBtn.disabled = true;
        submitBtn.innerHTML = 'INSCRIPTION EN COURS...';

        // Strategy: Serveur -> PHP (prioritaire, envoie email), Local -> Firestore > localStorage
        var savePromise;

        if (isOnline) {
            // SERVEUR : PHP en priorite (JSON + Firestore Admin + email + Brevo)
            var fd = new FormData();
            fd.append('prenom', prenom);
            fd.append('nom', nom);
            fd.append('email', email);
            fd.append('consent', 'true');
            savePromise = fetch(PHP_URL, { method: 'POST', body: fd }).then(function(r) { return r.json(); }).then(function(d) {
                if (d.status !== 'success') throw new Error(d.message || 'Erreur serveur');
                console.log('[KLEIA] PHP OK (email envoye)');
            });
            // Bonus: aussi sauver dans Firestore client (silencieux)
            if (db) {
                db.collection('atelier_inscriptions').add({
                    prenom: prenom, nom: nom, email: email.toLowerCase(),
                    consent: true, consent_at: new Date().toISOString(),
                    created_at: new Date().toISOString(), brevo_synced: false,
                    brevo_synced_at: null, source: 'popup-atelier'
                }).then(function() {
                    console.log('[KLEIA] Firestore client OK');
                }).catch(function() {});
            }
        } else if (db) {
            // LOCAL : Firestore client
            savePromise = db.collection('atelier_inscriptions').add({
                prenom: prenom, nom: nom, email: email.toLowerCase(),
                consent: true, consent_at: new Date().toISOString(),
                created_at: new Date().toISOString(), brevo_synced: false,
                brevo_synced_at: null, source: 'popup-atelier'
            }).then(function() {
                console.log('[KLEIA] Firestore OK');
            });
        } else {
            // LOCAL : localStorage fallback
            saveLocally(prenom, nom, email);
            savePromise = Promise.resolve();
        }

        savePromise.then(function() {
            // Brevo push (silencieux si indisponible)
            if (isOnline) {
                var bf = new FormData();
                bf.append('prenom', prenom);
                bf.append('nom', nom);
                bf.append('email', email);
                return fetch(BREVO_PUSH_URL, { method: 'POST', body: bf }).catch(function() {
                    console.log('[KLEIA] Brevo push indisponible');
                });
            }
        }).then(function() {
            submitBtn.innerHTML = 'INSCRIT !';
            submitBtn.style.background = '#25D366';
            localStorage.setItem(STORAGE_KEY, 'true');
            setTimeout(function() { window.location.href = CONFIRM_URL; }, 1000);
        }).catch(function(err) {
            console.error('[KLEIA] Erreur:', err);
            saveLocally(prenom, nom, email); // Sauvegarde de secours
            submitBtn.innerHTML = 'INSCRIT !';
            submitBtn.style.background = '#25D366';
            localStorage.setItem(STORAGE_KEY, 'true');
            setTimeout(function() { window.location.href = CONFIRM_URL; }, 1000);
        });
    };
})();
