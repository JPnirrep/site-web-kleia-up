# KLEIA-UP - Règles du Workspace

## Contexte
Site web statique pour KLEIA-UP, hébergé sur GitHub Pages.
- **URL de production** : https://jpnirrep.github.io/site-web-kleia-up/
- **Hébergement** : GitHub Pages (déploiement automatique sur push)

## Règles d'automatisation

### Vérification visuelle (Push + Preview)
Quand je demande de :
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

## ✅ Historique (Session v2.5-SEO-PERF)
- [x] **Audit WCAG** : Vérifier les contrastes du nouveau menu (Bourgogne sur Crème) pour l'accessibilité.
- [x] **Previews Sociaux** : Optimiser les balises OpenGraph (OG:Image) pour garantir une belle apparence lors du partage sur LinkedIn/Instagram.
- [x] **Minification CSS** : Étudier l'ajout d'un script de minification pour `main.css`.

## ⏩ À faire (Prochaine Session)
- [ ] *Définir les objectifs de la prochaine session*
