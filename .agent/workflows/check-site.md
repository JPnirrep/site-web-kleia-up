---
description: Vérification visuelle du site KLEIA-UP sur GitHub Pages
---

# Workflow : Vérification visuelle du site KLEIA-UP

## Objectif
Pousser les modifications sur GitHub, attendre la build GitHub Pages, puis ouvrir le site déployé dans Chrome pour vérification visuelle.

## Étapes

// turbo-all

1. Lancer le script de vérification visuelle :
```powershell
powershell -ExecutionPolicy Bypass -File "c:\Users\JP\Documents\GitHub\site-web-kleia-up\site-web-kleia-up\scripts\verify-visual.ps1"
```

## Notes
- Ce workflow est déclenché automatiquement quand tu demandes de "pousser et voir le résultat visuel" ou "vérifier visuellement le site"
- Le script gère automatiquement : `git add`, `git commit`, `git push`, attente de 45s, ouverture de Chrome
- Si aucune modification n'est détectée, le push est ignoré et le site s'ouvre directement
- URL du site : https://jpnirrep.github.io/site-web-kleia-up/
- Répertoire de travail : `c:\Users\JP\Documents\GitHub\site-web-kleia-up\site-web-kleia-up`
