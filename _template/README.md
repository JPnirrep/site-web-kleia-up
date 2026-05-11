# Template Espace Coaching KLEIA-UP

Ce dossier est le **moule** pour créer un espace de coaching privé pour chaque nouveau client de Sandrina.

## Structure du template

```
_template/
├── README.md               ← Ce fichier
├── clone.py                ← Script de duplication automatique
├── space/{prenom}/
│   ├── login.html           ← Page de connexion sécurisée (Firebase Auth)
│   ├── auth.js              ← Moteur d'authentification (jeton unique)
│   ├── index.html           ← Dashboard client (Chart.js, vidéo, analyse, roadmap)
│   ├── app.js               ← Logique du dashboard (rôles, chargement JSON, navigation)
│   ├── style.css            ← Design glassmorphism premium (commun à tous)
│   └── HANDOVER.md          ← Synthèse de fin de session
└── coaching_data/{prenom}/
    ├── {prenom}_state.json  ← Données centrales (scores, roadmap, analyse)
    ├── diagnostic.html      ← Rapport diagnostic PDF (3 pages A4, premium)
    ├── H1_report.html       ← Compte-rendu de séance H1 (format PDF)
    └── README.md            ← Documentation du dossier
```

## Utilisation

### 1. Cloner le template pour un nouveau client

```bash
# Automatique (recommandé)
python _template/clone.py Barnaby

# Ou manuellement : copier _template/space/{prenom}/ → space/{prenom}/
# et _template/coaching_data/{prenom}/ → coaching_data/{prenom}/
```

### 2. Créer le jeton Firebase

1. Aller sur [Firebase Console](https://console.firebase.google.com/) → projet `kleia-audit-jp-2026`
2. Firestore Database → Collection `access_tokens`
3. Créer un document avec :
   - **ID du document** : le code secret unique (format: `XXXX-XXXX-XX-XXXX`)
   - **Champs** :
     - `owner` (string) : Prénom exact du client (ex: `Barnaby`)
     - `role` (string) : `client` (ou `visitor` pour accès limité)
4. Transmettre le lien + code secret au client

### 3. Peupler les données du client

1. `{prenom}_state.json` → Scores baseline, analyse, roadmap des séances
2. `diagnostic.html` → Contenu du diagnostic oratoire
3. `H1_report.html` → Compte-rendu après chaque séance
4. Ajouter la vidéo de la session dans le dossier `coaching_data/{prenom}/`

## Flux de déploiement

```
Nouveau client Sandrina
        │
        ▼
python _template/clone.py Prenom
        │
        ├── space/Prenom/       ← Créé
        └── coaching_data/Prenom/ ← Créé
        │
        ▼
Création jeton Firebase (access_tokens/{code})
        │
        ▼
Remplissage des données (JSON, HTML, vidéo)
        │
        ▼
Lien transmis au client : https://kleia-up.fr/space/Prenom/login.html
```

## Design system

- **Fond** : Noir profond (#000)
- **Primaire** : Bordeaux (#8B1D3D)
- **Accent** : Or (#D4AF37)
- **Texte** : Blanc (#fff)
- **Typo titres** : Syne (Google Fonts)
- **Typo corps** : Ranade (Fontshare)
- **Effets** : Glassmorphism, dégradés, glow radial
- **Responsive** : Grilles adaptatives (desktop → mobile)

## Rôles et sécurité

| Rôle | Accès | Description |
|------|-------|-------------|
| `client` | Complet | Voit tout : dashboard, roadmap complète, vidéo, analyse |
| `visitor` | Restreint | Voit uniquement H1 et les infos publiques |
| admin | Total | JP (jpp180866@gmail.com) via Firebase Auth |

> Prochaine évolution : plateforme e-learning (voir roadmap).