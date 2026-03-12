# KLEIA-UP - Règles du Workspace

## Contexte
Site web statique pour KLEIA-UP, hébergé sur GitHub Pages.
- **URL de production** : https://jpnirrep.github.io/site-web-kleia-up/
- **Hébergement** : GitHub Pages (déploiement automatique sur push)

## Règles d'automatisation

### Vérification visuelle (Push + Preview)
**NOUVELLE CONSIGNE GLOBALE** : À chaque fois que je fais une itération ou que je modifie le code, tu dois **OBLIGATOIREMENT** rafraîchir la page (lancer le workflow `/check-site`) pour que je puisse vérifier dans Chrome.

Quand je demande de :
- faire une itération, modifier le site
- "pousser les modifications sur GitHub"
- "vérifier visuellement le site"
- "voir le résultat sur le site"
- "push et preview"
- ou toute variante similaire

➡️ **Tu lances automatiquement le workflow `/check-site`** qui exécute le script `scripts/verify-visual.ps1`.

**Tu ne me demandes PAS de copier-coller les commandes dans le terminal** ; tu les exécutes directement via le workflow, grâce à l'annotation `// turbo-all`.

## Structure du projet
```
site-web-kleia-up/
├── index.html           # Redirection vers individuel-groupe.html
├── individuel-groupe.html # Page Individuel / Groupe (ex-particuliers)
├── entreprises.html     # Page Entreprises
├── manifeste.html       # Le Manifeste
├── css/                 # Styles CSS
├── assets/              # Images et ressources
├── scripts/             # Scripts d'automatisation (PowerShell)
│   └── verify-visual.ps1
└── .agent/workflows/    # Workflows Antigravity
    └── check-site.md
```

### Supervision et cohérence (Mode Superviseur)
Quand je demande de :
- "vérifie la cohérence"
- "récap de session"
- "supervise"
- ou toute variante similaire

➡️ **Tu lances automatiquement le workflow `/supervise`** qui produit un rapport court (alertes, suggestions, todo).

**En fin de session** : tu me proposes automatiquement un récap et la mise à jour de la documentation.

### Documentation automatique
À chaque fin de session ou sauvegarde majeure :
- Mettre à jour `README.md` avec les changements
- Documenter les nouveaux workflows/scripts/règles

## Principes de développement
- ❌ Ne jamais casser le code existant
- ✅ Capitaliser sur l'existant
- ✅ Voies simples, efficaces, frugales
- ✅ Design moderne et premium

## Structure du projet
```
site-web-kleia-up/
├── index.html           # Redirection
├── individuel-groupe.html # Page Individuel / Groupe
├── entreprises.html     # Page Entreprises
├── manifeste.html       # Le Manifeste
├── css/                 # Styles CSS
├── assets/              # Images et ressources
├── scripts/             # Scripts d'automatisation (PowerShell)
│   └── verify-visual.ps1
├── GEMINI.md            # Règles du workspace
└── .agent/
    ├── workflows/       # Workflows Antigravity
    │   ├── check-site.md
    │   └── supervise.md
    └── rules/           # Règles agent
        └── supervisor.md
```

## Contraintes techniques
- Site statique (HTML/CSS/JS vanilla)
- Compatible Hostinger (si migration future)
- Pas de serveur backend requis
- Build GitHub Pages : ~45 secondes après push

## ✅ Historique (Session v3.0-B2C-IMMERSION)
- [x] **Refonte Offre Signature** : Remplacement de l'ancienne section sur `particuliers.html` par l'architecture `.signature-immersive-v2` asymétrique (60/40) premium et l'offre secondaire Conférence.
- [x] **UX/UI Gamification** : Transformation de la section des "Besoins" avec des Flip Cards CSS 3D (retournement au clic) avec reset automatique (Intersection Observer).
- [x] **Cohérence des CTA** : Modification de la stratégie de liens (Ancrage interne direct sur la page plutôt que des renvois externes brisés) pour l'intégration au Cercle et au Kit d'Urgence.
- [x] **Transition Individuel / Groupe** : Renommage de `particuliers.html` en `individuel-groupe.html` et harmonisation de la terminologie dans tous les headers du site.
- [x] **Formulaire Hostinger Reach** : Finalisation de l'intégration du formulaire modal et stratégie d'envoi.
- [x] **Redirection d'Accueil** : Mise à jour de `index.html` pour rediriger vers la page Individuel / Groupe par défaut.
- [x] **Optimisation Conversion** : Migration des CTA "Kit d'Urgence" vers le lien TinyURL et simplification du footer en bouton d'action directe.
- [x] **Navigation Unifiée** : Ajout du lien Manifeste sur Entreprises et mise à jour du lien LinkedIn de Sandrina.

## 🎯 TODO PROCHAINE SESSION
- [ ] **Formulaire Hostinger Reach** : Finaliser l'intégration et la stratégie d'envoi du formulaire modal (`#modal-contact` dans `entreprises.html`) vers Hostinger (gestion de la validation de saisie, traitement des données reçues).
