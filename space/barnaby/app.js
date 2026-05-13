/* 
   LOGIC ENGINE BARNABY V3.1 - SECURITY & ROLES
   Powered by OPENCODE
*/

let currentData = null;
const userRole = sessionStorage.getItem('kleia_role') || 'visitor';
const userName = sessionStorage.getItem('kleia_user') || 'Visiteur';

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('../../coaching_data/barnaby/barnaby_state.json');
        if (!response.ok) throw new Error('Données introuvables');
        currentData = await response.json();
        
        initDashboard(currentData);
        applyRoleRestrictions();
    } catch (error) {
        console.error("Erreur :", error);
    }
});

function applyRoleRestrictions() {
    if (userRole === 'visitor') {
        // Masquer tous les éléments marqués comme privés
        document.querySelectorAll('.private-content').forEach(el => {
            el.style.display = 'none';
        });
        console.log("KLEIA : Mode Visiteur activé (contenu restreint)");
    }
}

function initDashboard(data) {
    initRadarChart(data.baseline_scores);
    renderGauges(data.baseline_scores);
    
    // Par défaut, on affiche le module 1 (H1)
    renderSessionView(1); 
    renderRoadmapMenu(data.content.roadmap);
}

function renderRoadmapMenu(roadmap) {
    const container = document.getElementById('roadmap-container');
    
    // FILTRAGE : Si visiteur, on ne garde que H1
    const visibleRoadmap = (userRole === 'visitor') 
        ? roadmap.filter(r => r.session === 1)
        : roadmap;

    container.innerHTML = visibleRoadmap.map(r => `
        <div class="roadmap-item ${r.status.toLowerCase()} ${r.session === 1 ? 'active' : ''}" 
             onclick="switchSession(${r.session})" id="nav-h${r.session}">
            <span style="font-size: 0.7rem; color: var(--color-gold); font-weight: 800;">H${r.session}</span>
            <p style="font-size: 0.85rem; font-weight: 600;">${r.title}</p>
        </div>
    `).join('');
}

function switchSession(sessionId) {
    const zone = document.getElementById('main-content-zone');
    zone.style.opacity = '0';
    
    setTimeout(() => {
        document.querySelectorAll('.roadmap-item').forEach(el => el.classList.remove('active'));
        const activeNav = document.getElementById(`nav-h${sessionId}`);
        if (activeNav) activeNav.classList.add('active');
        
        renderSessionView(sessionId);
        zone.style.opacity = '1';
    }, 300);
}

function renderSessionView(sessionId) {
    const analysisZone = document.getElementById('analysis-content');
    
    const basePath = "../../coaching_data/barnaby/";
    const resolvePath = (file) => (file && file.startsWith('http')) ? file : `${basePath}${file}`;

    const sessionInfo = currentData.sessions_content[sessionId];
    const videoFile = currentData.assets[`video_h${sessionId}`];
    const replayFile = currentData.assets[`replay_h${sessionId}`];
    const reportFile = currentData.assets[`report_h${sessionId}`];

    let videoHTML = '';
    if (videoFile || replayFile) {
        videoHTML = `<div class="video-grid" style="display: grid; grid-template-columns: ${replayFile && videoFile ? '1fr 1fr' : '1fr'}; gap: 20px; margin-top: 30px;">`;
        
        if (replayFile) {
            videoHTML += `
                <div class="video-container">
                    <h3 style="color: var(--color-gold); font-size: 0.9rem; margin-bottom: 15px; text-transform: uppercase;">🎥 Replay de la Session</h3>
                    <div style="background: #000; border-radius: 15px; overflow: hidden; position: relative; padding-top: 56.25%;">
                        <video id="replay-video" controls playsinline style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
                            <source src="${resolvePath(replayFile)}" type="video/mp4">
                        </video>
                    </div>
                </div>`;
        }

        if (videoFile) {
            videoHTML += `
                <div class="video-container">
                    <h3 style="color: var(--color-gold); font-size: 0.9rem; margin-bottom: 15px; text-transform: uppercase;">👁️ Vidéo d'Analyse</h3>
                    <div style="background: #000; border-radius: 15px; overflow: hidden; position: relative; padding-top: 56.25%;">
                        <video id="audit-video" controls playsinline style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
                            <source src="${resolvePath(videoFile)}" type="video/mp4">
                        </video>
                    </div>
                </div>`;
        }
        
        videoHTML += `</div>`;
    }

    if (sessionInfo) {
        analysisZone.innerHTML = `
            <div class="dynamic-title-bar">
                <h2 class="card-title" style="margin-bottom: 0;">📋 ${sessionInfo.title}</h2>
                <div class="actions-group" style="display: flex; gap: 10px;">
                    ${reportFile ? `<a href="${resolvePath(reportFile)}" target="_blank" class="btn-premium private-content">📄 Compte-rendu détaillé</a>` : ''}
                </div>
            </div>
            
            <div class="interaction-zone" style="background: rgba(255,255,255,0.02); padding: 30px; border-radius: 20px; border-left: 3px solid var(--color-gold); margin-bottom: 40px;">
                <h3 style="color: var(--color-gold); margin-bottom: 15px;">${sessionInfo.synthesis_title}</h3>
                <p style="font-size: 0.95rem; opacity: 0.8; line-height: 1.6;">
                    ${sessionInfo.synthesis_text}
                </p>
            </div>
            ${videoHTML}
        `;
    } else {
        analysisZone.innerHTML = `
            <h2 class="card-title">🚀 H${sessionId} : ${currentData.content.roadmap[sessionId-1].title}</h2>
            <div style="background: rgba(255,255,255,0.02); padding: 40px; border-radius: 16px; text-align: center; border: 1px dashed var(--glass-border);">
                <p style="opacity: 0.5;">Cette séance n'a pas encore eu lieu.</p>
                <p style="font-size: 0.8rem; margin-top: 10px; color: var(--color-gold);">Prépare tes forces pour la suite du voyage.</p>
            </div>
        `;
    }forces pour la suite du voyage.</p>
            </div>
        `;
    }
    
    // Réappliquer les restrictions après chaque changement de vue
    applyRoleRestrictions();
}

function logout() {
    sessionStorage.clear();
    window.location.href = 'login.html';
}

function initRadarChart(scores) {
    const canvas = document.getElementById('radarChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
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
    if (!container) return;
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
