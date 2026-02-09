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

## Contraintes techniques
- Site statique (HTML/CSS/JS vanilla)
- Compatible Hostinger (si migration future)
- Pas de serveur backend requis
- Build GitHub Pages : ~45 secondes après push
