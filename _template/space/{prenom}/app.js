/*
   LOGIC ENGINE - DASHBOARD COACHING V3.1
   Powered by OPENCODE
   Template: _template/space/{prenom}/app.js
*/

let currentData = null;
const userRole = sessionStorage.getItem('kleia_role') || 'visitor';
const userName = sessionStorage.getItem('kleia_user') || 'Visiteur';

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/coaching_data/{prenom}/{prenom}_state.json');
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
        document.querySelectorAll('.private-content').forEach(el => {
            el.style.display = 'none';
        });
        console.log("KLEIA : Mode Visiteur activé (contenu restreint)");
    }
}

function initDashboard(data) {
    initRadarChart(data.baseline_scores);
    renderGauges(data.baseline_scores);
    renderSessionView(1);
    renderRoadmapMenu(data.content.roadmap);
}

function renderRoadmapMenu(roadmap) {
    const container = document.getElementById('roadmap-container');
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
    document.querySelectorAll('.roadmap-item').forEach(el => el.classList.remove('active'));
    const navEl = document.getElementById(`nav-h${sessionId}`);
    if (navEl) navEl.classList.add('active');
    renderSessionView(sessionId);
}

function renderSessionView(sessionId) {
    if (!currentData) return;
    const analysis = document.getElementById('analysis-content');
    const session = currentData.content.analysis.find(a => a.id === `session_${sessionId}`)
        || { title: `Session H${sessionId}`, details: "Contenu à venir.", items: [] };

    analysis.innerHTML = `
        <h2 class="card-title">${session.title}</h2>
        <p style="opacity: 0.7; margin-bottom: 20px; font-size: 0.95rem;">${session.details}</p>
        ${session.items ? session.items.map(item => `
            <div style="background: rgba(255,255,255,0.02); border-radius: 12px; padding: 15px 20px; margin-bottom: 12px; border-left: 3px solid var(--color-gold);">
                <strong style="color: var(--color-gold); font-size: 0.85rem;">${item.indicator}</strong>
                <p style="font-size: 0.85rem; margin-top: 5px;">${item.observation}</p>
                <p style="font-size: 0.75rem; opacity: 0.5; margin-top: 3px;">Impact : ${item.impact}</p>
            </div>
        `).join('') : '<p style="opacity: 0.3;">En attente du contenu de cette séance.</p>'}
    `;
}

function initRadarChart(scores) {
    const ctx = document.getElementById('radarChart').getContext('2d');
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: Object.keys(scores),
            datasets: [{
                label: 'Baseline',
                data: Object.values(scores).map(s => {
                    // Support both nested and flat structures
                    if (typeof s === 'object') return Object.values(s).reduce((a, b) => a + b, 0) / Object.values(s).length;
                    return s;
                }),
                backgroundColor: 'rgba(139, 29, 61, 0.2)',
                borderColor: '#D4AF37',
                borderWidth: 2,
                pointBackgroundColor: '#D4AF37',
                pointBorderColor: '#fff',
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: { legend: { display: false } },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 10,
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    angleLines: { color: 'rgba(255,255,255,0.1)' },
                    pointLabels: { color: '#fff', font: { family: 'Ranade', size: 10 } },
                    ticks: { display: false }
                }
            }
        }
    });
}

function renderGauges(scores) {
    const container = document.getElementById('gauges-container');
    container.innerHTML = Object.entries(scores).map(([key, val]) => {
        const score = typeof val === 'object' ? Object.values(val).reduce((a, b) => a + b, 0) / Object.values(val).length : val;
        return `
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem;">
                    <span>${key.replace(/_/g, ' ')}</span>
                    <span style="color: var(--color-gold);">${score}/10</span>
                </div>
                <div class="gauge-bar"><div class="gauge-fill" style="width: ${score * 10}%;"></div></div>
            </div>
        `;
    }).join('');
}

function logout() {
    sessionStorage.clear();
    window.location.href = 'login.html';
}