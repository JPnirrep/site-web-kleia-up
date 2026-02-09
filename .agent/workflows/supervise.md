---
description: Superviser la session KLEIA-UP et produire un rapport de cohérence
---

# Workflow : Supervision KLEIA-UP

## Objectif
Analyser l'état du repo, vérifier la cohérence, produire un rapport court, et proposer des corrections si nécessaire.

## Étapes

// turbo-all

1. Vérifier les fichiers modifiés :
```powershell
git status --porcelain
```

2. Lister les commits récents (contexte) :
```powershell
git log --oneline -n 10
```

3. **Produire le rapport de supervision** selon le format défini dans `.agent/rules/supervisor.md` :
   - 🚨 Alertes (problèmes critiques)
   - 💡 Suggestions (améliorations optionnelles)
   - ✅ Todo prochaine session
   - 📝 Documentation à mettre à jour

4. **Si corrections nécessaires** :
   - Proposer le passage en mode développeur
   - Après implémentation → relancer automatiquement la supervision

5. **En fin de session** :
   - Mettre à jour `README.md` avec les changements de la session
   - Proposer le push via `/check-site`

## Notes
- Ce workflow ne modifie PAS le code directement
- Il analyse et propose, l'utilisateur valide
- Répertoire : `c:\Users\JP\Documents\GitHub\site-web-kleia-up\site-web-kleia-up`
