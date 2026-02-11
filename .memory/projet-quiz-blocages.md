# 🎯 Projet Quiz "Blocages Prise de Parole"

## Statut
🟡 **En attente** - Spécifications à compléter

## Concept
Quiz de ~3 minutes pour identifier les blocages des leaders/hypersensibles face à la prise de parole.

## Architecture choisie
**Option B : Quiz intégré au site + Brevo API**

### Pourquoi ce choix ?
- ✅ Design 100% KLEIA-UP (burgundy, Forum/Montserrat)
- ✅ Expérience utilisateur fluide (pas de redirection)
- ✅ Gratuit (API Brevo)
- ✅ Réalisable en site statique

## Structure technique

```
Quiz (8-10 questions)
         ↓
Formulaire (prénom + email)
         ↓
┌────────────────────────────────────┐
│  PAGE RÉSULTAT (sur le site)       │
│  • Profil identifié               │
│  • Points forts / blocages        │
│  • 3 conseils personnalisés       │
│  • CTA vers offre KLEIA           │
└────────────────────────────────────┘
         ↓
Email Brevo (lien vers page résultat)
```

## Fichiers à créer
- `quiz.html` ou section dans `index.html`
- `css/quiz.css` (styles dédiés)
- `js/quiz.js` (logique quiz + API Brevo)
- Templates de résultats (3-4 profils)

## Questions à clarifier avant implémentation

### 1. Contenu du quiz
- [ ] Nombre de questions (8-10 recommandé)
- [ ] Liste des questions
- [ ] Types de réponses (choix multiples, échelle...)

### 2. Profils/Résultats
- [ ] Combien de profils différents ? (3-4 recommandé)
- [ ] Noms des profils (ex: "Le Perfectionniste Silencieux")
- [ ] Description de chaque profil
- [ ] Conseils personnalisés par profil

### 3. Technique
- [ ] Clé API Brevo
- [ ] ID de la liste Brevo pour les contacts
- [ ] Template email (simple ou élaboré)

## Design prévu
- Couleurs : burgundy (#580017), crème (#FAF9F6)
- Typo titres : Forum
- Typo corps : Montserrat
- Animations : transitions douces, barre de progression
- Style : premium, minimaliste, chaleureux

## Prochaines étapes
1. Définir les questions du quiz
2. Créer les profils/archétypes
3. Configurer Brevo (API + liste)
4. Développer le quiz
5. Intégrer au site
6. Tester le parcours complet

---
*Créé le 09/02/2026 - À reprendre lors d'une prochaine session*
