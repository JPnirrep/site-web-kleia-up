# Archive - Challenge de Pâques 2026

> Ce document contient l'intégralité du code et de la logique déployée pour le Challenge de Pâques 2026 de KLEIA-UP. 

## 🥚 Détails Techniques
- **Période** : 7 au 10 avril 2026
- **Objectif** : Inscription au challenge via popup et capture de leads.
- **Canaux** : Redirection vers PDF (Drive) et Groupe WhatsApp.

---

## 💻 Code Source JavaScript (`js/paques-popup.js`)

```javascript
/**
 * 🥚 KLEIA-UP - POP-UP CHALLENGE DE PÂQUES 2026
 * Design: Blanc Perle Noble / Version Intégrale (Compacte)
 * Deployment: Final Production Build (v1.1)
 */

(function() {
    const POPUP_ID = 'paques-challenge-popup';
    const STORAGE_KEY = 'kleia_paques_closed_2026';
    const WHATSAPP_LINK = 'https://chat.whatsapp.com/EfmYUfLlnnn7PWnfmItHQW';
    const PDF_LINK = 'https://drive.google.com/file/d/1WTu-2xrKLWlSuYPswdVjbbE4kQZQ61hO/view?usp=drive_link';

    // Verification de la session
    if (localStorage.getItem(STORAGE_KEY)) return;

    const style = document.createElement('style');
    style.textContent = `
        #\${POPUP_ID}-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(26, 26, 26, 0.45); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);
            z-index: 100000; display: flex; align-items: center; justify-content: center;
            opacity: 0; transition: opacity 0.6s ease; padding: 10px;
        }

        #\${POPUP_ID}-content {
            background: #FDFCF0; width: 100%; max-width: 960px; max-height: 98vh;
            border-radius: 40px; position: relative; box-shadow: 0 40px 100px rgba(88, 0, 23, 0.25);
            transform: translateY(30px); transition: all 0.7s cubic-bezier(0.19, 1, 0.22, 1);
            padding: 40px; border: 1px solid rgba(139, 29, 61, 0.05); text-align: left;
            overflow-y: auto;
        }

        #\${POPUP_ID}-overlay.active { opacity: 1; }
        #\${POPUP_ID}-overlay.active #\${POPUP_ID}-content { transform: translateY(0); }

        .paques-close {
            position: absolute; top: 20px; right: 20px; width: 36px; height: 36px;
            background: rgba(139, 29, 61, 0.05); border-radius: 50%;
            display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 100;
        }

        .paques-grid { display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 40px; align-items: center; }

        .paques-left { padding-right: 15px; border-right: 1px solid rgba(139, 29, 61, 0.08); }
        .paques-logo { height: 70px; margin-bottom: 25px; }
        
        .paques-title {
            font-family: 'Ranade', sans-serif; font-weight: 800; font-size: 1.9rem;
            line-height: 1.1; color: #1A1A1A; margin-bottom: 12px;
        }

        .paques-title em { font-style: italic; color: #8B1D3D; display: block; }
        .paques-subtitle { 
            font-size: 0.95rem; color: #8B1D3D; font-weight: 700; margin-bottom: 25px; 
            letter-spacing: 1px; text-transform: uppercase; display: inline-block;
        }

        .paques-context { 
            color: #333; font-size: 0.95rem; line-height: 1.55; margin-bottom: 25px; 
            background: rgba(255,255,255,0.4); padding: 15px; border-radius: 15px;
        }
        .paques-highlight { font-weight: 800; color: #8B1D3D; }

        .paques-right { display: flex; flex-direction: column; gap: 20px; }

        .paques-programme {
            background: rgba(139, 29, 61, 0.04); border-radius: 20px; padding: 20px;
            border: 1px solid rgba(139, 29, 61, 0.06); margin-bottom: 5px;
        }

        .paques-prog-item { display: flex; gap: 10px; margin-bottom: 10px; font-size: 0.88rem; line-height: 1.35; }
        .paques-prog-item:last-child { margin-bottom: 0; }

        .paques-right-box {
            background: #FFF; padding: 30px; border-radius: 25px;
            box-shadow: 0 15px 40px rgba(139, 29, 61, 0.08);
            border: 1px solid rgba(139, 29, 61, 0.05);
        }

        .paques-form { display: grid; gap: 12px; }
        .paques-input {
            width: 100%; padding: 16px 20px; border-radius: 15px; font-family: 'Ranade', sans-serif;
            border: 1px solid rgba(139, 29, 61, 0.1); background: #fafafa; font-size: 1rem; outline: none;
        }

        .paques-btn {
            background: linear-gradient(135deg, #8B1D3D 0%, #D70040 100%);
            color: #FFF; padding: 18px; border-radius: 15px; border: none;
            font-family: 'Ranade', sans-serif; font-weight: 800; font-size: 1rem;
            text-transform: uppercase; cursor: pointer; margin-top: 5px;
            box-shadow: 0 8px 25px rgba(139, 29, 61, 0.3); transition: all 0.3s ease;
        }
        .paques-btn:hover { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(139, 29, 61, 0.4); }

        .paques-footer { margin-top: 20px; font-size: 0.85rem; color: #777; font-style: italic; text-align: center; }

        @media (max-width: 900px) {
            .paques-grid { grid-template-columns: 1fr; gap: 30px; }
            .paques-left { border-right: none; padding-right: 0; }
            #\${POPUP_ID}-content { padding: 30px; }
            .paques-logo { height: 60px; }
        }
    \`;
    document.head.appendChild(style);

    const popupHTML = \`
        <div id="\${POPUP_ID}-overlay">
            <div id="\${POPUP_ID}-content">
                <div class="paques-close" id="\${POPUP_ID}-close" aria-label="Fermer">
                    <svg viewBox="0 0 24 24" fill="none" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </div>

                <div class="paques-grid">
                    <div class="paques-left">
                        <img src="assets/logo_kleia.png" class="paques-logo" alt="Logo KLEIA-UP">
                        <h2 class="paques-title">Arrêtez de convaincre,<br><em>commencez à rayonner</em></h2>
                        <p class="paques-subtitle">✨ Challenge de Pâques (du 7 au 10 avril) ✨</p>
                        
                        <div class="paques-context">
                            ✨ <span class="paques-highlight">BIENVENUE DANS VOTRE ZONE DE PUISSANCE !</span> ✨<br><br>
                            "Arrêtez de convaincre, commencez à rayonner : 4 jours pour desserrer le frein à main de votre puissance naturelle."<br><br>
                            Vous avez déjà votre Kit de Survie, vous connaissez donc l'équation. Ici, on passe de la théorie à la biologie. Pour une femme HPS, l'affirmation de soi est le moteur de sa liberté, quel que soit son métier. 🚀
                        </div>

                        <div class="paques-programme">
                            <p style="margin-bottom: 15px; font-weight: 800; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px;">VOTRE TRAVERSÉE :</p>
                            <div class="paques-prog-item"><span>1️⃣</span> <p><strong>Mardi 7 :</strong> Desserrer le frein (physiologie).</p></div>
                            <div class="paques-prog-item"><span>2️⃣</span> <p><strong>Mercredi 8 :</strong> Ouvrir ton rayonnement (présence).</p></div>
                            <div class="paques-prog-item"><span>3️⃣</span> <p><strong>Jeudi 9 :</strong> Poser tes limites avec élégance.</p></div>
                            <div class="paques-prog-item"><span>4️⃣</span> <p><strong>Vendredi 10 :</strong> Mastermind & Ancrage sensoriel.</p></div>
                        </div>
                    </div>

                    <div class="paques-right">
                        <div class="paques-right-box">
                            <form id="\${POPUP_ID}-form" class="paques-form">
                                <input type="text" id="paques-name" class="paques-input" placeholder="Ton prénom" required>
                                <input type="email" id="paques-email" class="paques-input" placeholder="Ton email privé" required>
                                <input type="tel" id="paques-whatsapp" class="paques-input" placeholder="Ton numéro WhatsApp (Optionnel)">
                                <button type="submit" class="paques-btn" id="paques-submit">JE M'INSCRIS AU CHALLENGE</button>
                                <p class="paques-footer">Un seul clic pour faire partie de la communauté et recevoir votre kit de survie</p>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    \`;

    document.body.insertAdjacentHTML('beforeend', popupHTML);

    const overlay = document.getElementById(\`\${POPUP_ID}-overlay\`);
    const closeBtn = document.getElementById(\`\${POPUP_ID}-close\`);

    setTimeout(() => { overlay.classList.add('active'); }, 1800);

    const closePopup = () => {
        overlay.classList.remove('active');
        setTimeout(() => overlay.remove(), 600);
        localStorage.setItem(STORAGE_KEY, 'true');
    };

    closeBtn.onclick = closePopup;
    overlay.onclick = (e) => { if (e.target === overlay) closePopup(); };

    document.getElementById(\`\${POPUP_ID}-form\`).onsubmit = function(e) {
        e.preventDefault();
        const submitBtn = document.getElementById('paques-submit');
        submitBtn.disabled = true;
        submitBtn.innerHTML = "RAYONNEMENT EN COURS...";

        const formData = new FormData();
        formData.append('name', document.getElementById('paques-name').value);
        formData.append('email', document.getElementById('paques-email').value);
        formData.append('subject', 'CHALLENGE-PAQUES-2026');
        formData.append('message', 'Inscription Challenge. WhatsApp: ' + (document.getElementById('paques-whatsapp').value || 'Non renseigné'));

        fetch('php/contact-reach.php', { method: 'POST', body: formData })
        .then(response => {
            if (response.ok) {
                submitBtn.innerHTML = "VALIDÉ ! ✨";
                submitBtn.style.background = "#25D366";
                setTimeout(() => {
                    window.open(PDF_LINK, '_blank');
                    window.location.href = WHATSAPP_LINK;
                    localStorage.setItem(STORAGE_KEY, 'true');
                }, 1000);
            } else { throw new Error(); }
        })
        .catch(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = "RÉESSAYER";
        });
    };
})();
```

---

## 🎨 Design System
- **Couleur Primaire** : `#8B1D3D` (Bordeaux Noble)
- **Couleur Secondaire** : `#FDFCF0` (Perle / Crème)
- **Action** : Gradient `#8B1D3D` vers `#D70040`
- **Animations** : `blur(15px)`, `translateY(30px)` vers `0`, `cubic-bezier(0.19, 1, 0.22, 1)`.
