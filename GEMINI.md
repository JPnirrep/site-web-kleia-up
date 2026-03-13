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
- [x] **v3.7-STABLE-PREMIUM (13/03/2026)** : Version de référence finale. Activation du formulaire de contact PHP (Option B) avec double notification (Sandrina + JP).
- [x] **Boutons 3D Liftoff** : Élévation de 8px au survol, inversion chromatique blanc/bordeaux.
- [x] **Neutralisation Cache Hostinger** : Configuration .htaccess agressive (max-age=0) et versioning system (?v=3.7).
- [x] **Correction Fondatrice** : Responsive total du blob et du texte sur mobile.
- [x] **Nettoyage Console** : Suppression erreur 404 Favicon, harmonisation LinkedIn.
- [x] **Refonte Offre Signature** : Architecture `.signature-immersive-v2` asymétrique (60/40) premium et l'offre secondaire Conférence.
- [x] **UX/UI Gamification** : Transformation de la section des "Besoins" avec des Flip Cards CSS 3D (retournement au clic) avec reset automatique (Intersection Observer).
- [x] **Cohérence des CTA** : Correction des ancrages stratégiques (REJOINDRE LE MOUVEMENT pointant vers le bas de page `#kit-urgence`).
- [x] **Lisibilité Premium** : Refonte du bouton "JE TÉLÉCHARGE MON KIT" dans le footer (contraste maximal Blanc sur Bordeaux).
- [x] **Restauration Manifeste** : Retour au design premium, unification du header/footer et réactivation du blob vidéo organique (version frugale 350px).
- [x] **Stabilité Globale** : Correction du header translucide (glassmorphism) pour protéger la lisibilité lors du scroll.
- [x] **Transition Individuel / Groupe** : Renommage de `particuliers.html` en `individuel-groupe.html` et harmonisation de la terminologie.
- [x] **Redirection d'Accueil** : Mise à jour de `index.html` pour rediriger vers la page B2C par défaut.

## 🎯 TODO PROCHAINE SESSION
- [ ] **Formulaire Hostinger Reach** : Finaliser l'intégration et la stratégie d'envoi du formulaire modal (`#modal-contact` dans `entreprises.html`).
- [ ] **Audit Responsif Final** : Vérification minutieuse sur tablettes et petits smartphones.
