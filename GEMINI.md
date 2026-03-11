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
├── index.html          # Page principale
├── css/                # Styles CSS
├── assets/             # Images et ressources
├── scripts/            # Scripts d'automatisation (PowerShell)
│   └── verify-visual.ps1
└── .agent/workflows/   # Workflows Antigravity
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
├── index.html          # Page principale
├── css/                # Styles CSS
├── assets/             # Images et ressources
├── scripts/            # Scripts d'automatisation (PowerShell)
│   └── verify-visual.ps1
├── GEMINI.md           # Règles du workspace
└── .agent/
    ├── workflows/      # Workflows Antigravity
    │   ├── check-site.md
    │   └── supervise.md
    └── rules/          # Règles agent
        └── supervisor.md
```

## Contraintes techniques
- Site statique (HTML/CSS/JS vanilla)
- Compatible Hostinger (si migration future)
- Pas de serveur backend requis
- Build GitHub Pages : ~45 secondes après push

## ✅ Historique (Session v2.9-GLASSMORPHISM)
- [x] **Unification Globale** : Standardisation du header premium fixe sur `entreprises.html`, `particuliers.html` et `manifeste.html`.
- [x] **Transparence & Blur** : Fix critique de l'effet Glassmorphism (ivoire translucide / flou 25px).
- [x] **Correctifs UI/UX** : Recalage du bandeau de logos et redimensionnement du blob (Sandrina) sur la page Particuliers.
- [x] **Optimisation Structurelle** : Ajustement des paddings Hero pour compenser les headers fixes.

## 🎯 TODO PROCHAINE SESSION
- [ ] **Formulaire Hostinger Reach** : Finaliser l'intégration et la stratégie d'envoi du formulaire modal (`#modal-contact` dans `entreprises.html`) vers Hostinger (gestion de la validation de saisie, traitement des données reçues).
