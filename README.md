# 🏛️ KLEIA-UP - Site Web Officiel

## 🔒 VERSION STABLE - DESIGN IMMUABLE

![Status](https://img.shields.io/badge/status-PRODUCTION-success)
![Version](https://img.shields.io/badge/version-v1.0--STABLE-blue)
![Maintenance](https://img.shields.io/badge/maintenance-PROT%C3%89G%C3%89-red)

---

## 🎨 RÈGLES TYPOGRAPHIQUES (GRAVÉES DANS LE MARBRE)

### 1. POLICES (FONTS)
*   **Titres (Hn)** : `Forum` (Serif).
*   **Interface / Corps** : `Montserrat` (Sans-serif).

### 2. HIÉRARCHIE VISUELLE (TITRES)
*   **H1 (Hero)** : Casse phrase obligatoire (sauf exception purement éditoriale type slogan).
*   **H2 / H3 (Sections)** : Uppercase (tout majuscule) **AUTORISÉ** pour les grands piliers :
    *   *PROGRAMME SIGNATURE*
    *   *L’INSTANT KLEIA*
    *   *ATELIERS FOCUS*
*   **Emphase** : Italique + Couleur Bordeaux (`#580017`). Jamais sur des blocs entiers, uniquement mots-clés.

### 3. INTERFACE (NAVIGATION, BOUTONS, LABELS)
*   **Style** : `UPPERCASE` (Tout majuscule).
*   **Propriétés techniques** :
    *   `letter-spacing: 1px`
    *   `font-weight: 600`
*   **Corps de texte / Formulaires** : Casse phrase (Sentence case) pour garder la chaleur et l'humain.

---

## ⚠️ AVERTISSEMENT CRITIQUE - LIRE AVANT TOUTE MODIFICATION

**CE DESIGN EST MAINTENANT IMMUABLE ET PROTÉGÉ**

### 🚫 INTERDICTIONS ABSOLUES

1. **NE JAMAIS** migrer vers Tailwind CSS
2. **NE JAMAIS** migrer vers React ou tout autre framework
3. **NE JAMAIS** supprimer les animations CSS natives
4. **NE JAMAIS** modifier la palette de couleurs burgundy (#580017)
5. **NE JAMAIS** toucher au fichier `index.html` sans backup préalable
6. **NE JAMAIS** utiliser d'IA pour "améliorer" le design

### ✅ CE QUI FONCTIONNE PARFAITEMENT

- ✨ **Animations CSS natives** : morph, waves, hover effects
- 🎨 **Design burgundy premium** : #580017, #D70040, #FAF9F6
- 📱 **Responsive design** : mobile, tablet, desktop
- 🚀 **Performance** : chargement ultra-rapide, aucune dépendance
- 🎯 **SEO** : balises meta complètes, schema.org
- 🔗 **GitHub Pages** : déploiement automatique activé

### 🛡️ SAUVEGARDES ET PROTECTION

#### Branche principale
```
main (branch) - Version de production
```

#### Branche de sauvegarde
```
STABLE-BACKUP-2026-01-08 - Backup immuable du 08/01/2026
```

#### Tag de version
```
v1.0-STABLE - Version stable tagée et protégée
```

#### Commit de référence
```
Hash: 2e743c3
Message: "revert: restore working version from yesterday (remove Tailwind)"
```

---

## 🔧 PROCÉDURES DE MAINTENANCE

### 🚨 En cas de problème - RESTAURATION D'URGENCE

Si le site est cassé, suivre cette procédure **IMMDIATEMENT** :

```bash
# Option 1 : Restaurer depuis le tag
git checkout v1.0-STABLE
git push origin main --force

# Option 2 : Restaurer depuis la branche de backup
git checkout STABLE-BACKUP-2026-01-08
git checkout -b main-restored
git push origin main-restored:main --force

# Option 3 : Restaurer depuis le commit spécifique
git checkout 2e743c3
git checkout -b main
git push origin main --force
```

### ✅ Modifications autorisées (avec précautions)

#### Textes et contenus
- Modifier les textes dans les balises HTML
- Mettre à jour les tarifs et offres
- Changer les images (conserver les mêmes dimensions)

#### Méthode sécurisée pour modifier
```bash
# 1. Créer une branche de test
git checkout -b test-modif-YYYY-MM-DD

# 2. Faire les modifications
# 3. Tester localement
# 4. Si OK, merger

git checkout main
git merge test-modif-YYYY-MM-DD
git push
```

### 🚫 Modifications INTERDITES

- Ne JAMAIS toucher au `<style>` dans l'index.html
- Ne JAMAIS installer de dépendances npm
- Ne JAMAIS ajouter de frameworks CSS/JS
- Ne JAMAIS modifier la structure HTML sans backup

---

## 📊 ARCHITECTURE DU SITE

### Structure des fichiers
```
site-web-la-fab-pepps/
├── index.html          # FICHIER PRINCIPAL - NE PAS TOUCHER SANS BACKUP
├── css/                 # Dossier vide (CSS intégré dans index.html)
├── README.md           # Ce fichier
└── .gitignore
```

### Technologies utilisées
- **HTML5** : Structure sémantique
- **CSS3** : Styles et animations natives
- **JavaScript Vanilla** : Interactions minimales
- **Google Fonts** : Playfair Display + Montserrat

### Ce qui N'est PAS utilisé (et ne doit JAMAIS l'être)
- ❌ Tailwind CSS
- ❌ React
- ❌ Vue.js
- ❌ Bootstrap
- ❌ jQuery
- ❌ Webpack/Vite/build tools

---

## 🌐 DÉPLOIEMENT

### GitHub Pages (actif)
- **URL** : https://jpnirrep.github.io/site-web-la-fab-pepps/
- **Source** : Branch `main`
- **Build** : Automatique à chaque push

### Vérifier le déploiement
1. Aller sur Actions : https://github.com/JPnirrep/site-web-la-fab-pepps/actions
2. Vérifier que "pages build and deployment" est en succès (✅)
3. Tester le site en ligne

---

## 📝 HISTORIQUE DES VERSIONS

### v1.0-STABLE (08/01/2026) - VERSION ACTUELLE
- ✅ Design original restauré et protégé
- ✅ Animations CSS natives fonctionnelles
- ✅ Revert de la migration Tailwind ratée
- ✅ Sauvegardes multiples créées
- ✅ GitHub Pages activé

### Versions précédentes (NON recommandées)
- Tentative de migration Tailwind : **❌ ÉCHOUÉE** (design cassé)

---

## ❓ QUESTIONS FRÉQUENTES

### Q: Puis-je améliorer le design avec une IA ?
**R: NON. Le design actuel fonctionne parfaitement. Toute tentative d'"amélioration" a déjà cassé le site.**

### Q: Puis-je migrer vers Tailwind/React ?
**R: NON. JAMAIS. C'est déjà été tenté et a échoué. Les animations ne fonctionnent plus avec ces frameworks.**

### Q: Comment ajouter du contenu ?
**R: Modifier uniquement les TEXTES dans les balises HTML. Ne JAMAIS toucher au CSS ni à la structure.**

### Q: Le site est cassé, que faire ?
**R: Suivre la procédure de restauration d'urgence ci-dessus. Restaurer depuis v1.0-STABLE.**

### Q: Puis-je supprimer les anciennes branches ?
**R: NON. JAMAIS supprimer STABLE-BACKUP-2026-01-08 ni le tag v1.0-STABLE.**

---

## 👤 CONTACT

**Propriétaire** : La Fabrique PEPPS  
**Site web** : https://jpnirrep.github.io/site-web-la-fab-pepps/  
**GitHub** : https://github.com/JPnirrep

---

## 📜 LICENCE

Copyright © 2024-2026 La Fabrique PEPPS - Tous droits réservés

---

> ⚠️ **RAPPEL FINAL** : Ce design est **IMMUABLE**. Toute tentative de modification majeure doit être précédée d'une sauvegarde complète et testée dans une branche séparée. En cas de doute, **NE RIEN MODIFIER**.
