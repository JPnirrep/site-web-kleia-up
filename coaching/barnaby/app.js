/* 
   LOGIC ENGINE BARNABY V3.0 - NAVIGATION MENU & CLEANUP
   Powered by OPENCODE
*/

let currentData = null;

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/coaching_data/barnaby/barnaby_state.json');
        if (!response.ok) throw new Error('Données introuvables');
        currentData = await response.json();
        
        initDashboard(currentData);
    } catch (error) {
        console.error("Erreur :", error);
    }
});

function initDashboard(data) {
    initRadarChart(data.baseline_scores);
    renderGauges(data.baseline_scores);
    
    // Par défaut, on affiche le module 1 (H1)
    renderSessionView(1); 
    renderRoadmapMenu(data.content.roadmap);
}

function renderRoadmapMenu(roadmap) {
    const container = document.getElementById('roadmap-container');
    container.innerHTML = roadmap.map(r => `
        <div class="roadmap-item ${r.status.toLowerCase()} ${r.session === 1 ? 'active' : ''}" 
             onclick="switchSession(${r.session})" id="nav-h${r.session}">
            <span style="font-size: 0.7rem; color: var(--color-gold); font-weight: 800;">H${r.session}</span>
            <p style="font-size: 0.85rem; font-weight: 600;">${r.title}</p>
        </div>
    `).join('');
}

function switchSession(sessionId) {
    // Animation de transition
    const zone = document.getElementById('main-content-zone');
    zone.style.opacity = '0';
    
    setTimeout(() => {
        // Mise à jour visuelle du menu
        document.querySelectorAll('.roadmap-item').forEach(el => el.classList.remove('active'));
        document.getElementById(`nav-h${sessionId}`).classList.add('active');
        
        renderSessionView(sessionId);
        zone.style.opacity = '1';
    }, 300);
}

function renderSessionView(sessionId) {
    const analysisZone = document.getElementById('analysis-content');
    
    if (sessionId === 1) {
        // MODULE H1 : ACCUEIL & DIAGNOSTIC
        analysisZone.innerHTML = `
            <div class="dynamic-title-bar">
                <h2 class="card-title" style="margin-bottom: 0;">📋 H1 : Diagnostic & Échanges</h2>
                <a href="/coaching_data/barnaby/diagnostic_officiel.html" target="_blank" class="btn-premium">📄 Voir Document Officiel</a>
            </div>
            
            <div class="interaction-zone" style="background: rgba(255,255,255,0.02); padding: 25px; border-radius: 16px; border-left: 2px solid var(--color-gold);">
                <h3 style="color: var(--color-gold); margin-bottom: 15px;">Compte-rendu de la séance</h3>
                <p style="font-size: 0.95rem; opacity: 0.8;">[Bientôt disponible] Le compte-rendu détaillé de l'échange initial sera injecté ici.</p>
                <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1);">
                    <h3 style="color: var(--color-gold); margin-bottom: 15px;">Vidéo de l'échange</h3>
                    <p style="font-size: 0.85rem; font-style: italic; opacity: 0.6;">Le replay de la visioconférence sera accessible dans cet espace.</p>
                </div>
            </div>

            <div style="margin-top: 40px;">
                <h3 style="color: var(--color-gold); font-family: var(--font-title); margin-bottom: 20px;">Synthèse de l'Audit</h3>
                ${currentData.content.analysis.map(sec => `
                    <div style="margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 15px;">
                        <h4 style="font-size: 1rem; margin-bottom: 10px;">${sec.title}</h4>
                        <p style="font-size: 0.85rem; opacity: 0.6;">${sec.details}</p>
                    </div>
                `).join('')}
            </div>
        `;
    } else {
        // AUTRES MODULES (H2 à H8)
        analysisZone.innerHTML = `
            <h2 class="card-title">🚀 H${sessionId} : ${currentData.content.roadmap[sessionId-1].title}</h2>
            <div style="background: rgba(255,255,255,0.02); padding: 40px; border-radius: 16px; text-align: center; border: 1px dashed var(--glass-border);">
                <p style="opacity: 0.5;">Cette séance n'a pas encore eu lieu.</p>
                <p style="font-size: 0.8rem; margin-top: 10px; color: var(--color-gold);">Prépare tes forces pour la suite du voyage.</p>
            </div>
        `;
    }
}

// Graphiques (inchangés mais encapsulés)
function initRadarChart(scores) {
    const ctx = document.getElementById('radarChart').getContext('2d');
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ["Regard", "Ancrage", "Geste", "Débit", "Relief", "Présence"],
            datasets: [{
                data: [scores.non_verbal.contact_visuel, scores.non_verbal.ancrage_sol, scores.non_verbal.gestuelle, scores.para_verbal.maitrise_debit, scores.para_verbal.relief_vocal, scores.verbal.presence],
                backgroundColor: 'rgba(139, 29, 61, 0.3)',
                borderColor: '#D4AF37',
                borderWidth: 2
            }]
        },
        options: {
            scales: { r: { grid: { color: 'rgba(255,255,255,0.1)' }, angleLines: { color: 'rgba(255,255,255,0.1)' }, ticks: { display: false }, suggestedMin: 0, suggestedMax: 10 } },
            plugins: { legend: { display: false } }
        }
    });
}

function renderGauges(scores) {
    const container = document.getElementById('gauges-container');
    const metrics = [
        { label: "Non-Verbal", score: (scores.non_verbal.contact_visuel + scores.non_verbal.ancrage_sol + scores.non_verbal.gestuelle) / 3 },
        { label: "Para-Verbal", score: (scores.para_verbal.maitrise_debit + scores.para_verbal.relief_vocal) / 2 },
        { label: "Verbal", score: scores.verbal.presence }
    ];
    container.innerHTML = metrics.map(m => `
        <div style="margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.7rem; margin-bottom: 5px; opacity: 0.6;">
                <span>${m.label.toUpperCase()}</span>
                <span>${m.score.toFixed(1)}/10</span>
            </div>
            <div class="gauge-bar"><div class="gauge-fill" style="width: ${m.score * 10}%"></div></div>
        </div>
    `).join('');
}
