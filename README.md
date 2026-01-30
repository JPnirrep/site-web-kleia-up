# 🏛️ KLEIA-UP - Site Web Officiel

## 🔒 VERSION STABLE - SITE STATIQUE HAUTE PERFORMANCE

![Status](https://img.shields.io/badge/status-PRODUCTION-success)
![Version](https://img.shields.io/badge/version-v2.0--CLEAN-blue)
![Architecture](https://img.shields.io/badge/architecture-VANILLA%20HTML%2FCSS-green)

---

## 🎯 ARCHITECTURE

**Site 100% statique** — Zéro dépendance, zéro framework, performance maximale.

### Structure des fichiers
```
site-web-kleia-up/
├── index.html          # FICHIER PRINCIPAL
├── css/
│   └── main.css        # Styles Vanilla (35 KB)
├── assets/
│   ├── logo_kleia.png
│   └── sandrina perrin photo site pepps.webp
├── .htaccess           # Configuration Apache
├── .gitignore          # Exclusions Git
├── .github/
│   └── workflows/
│       └── deploy.yml  # Déploiement automatique GitHub Pages
└── README.md           # Ce fichier
```

### Technologies utilisées
- **HTML5** : Structure sémantique
- **CSS3** : Styles et animations natives
- **JavaScript Vanilla** : Interactions minimales (inline)
- **Google Fonts** : Forum + Montserrat + Syne

---

## 🎨 RÈGLES TYPOGRAPHIQUES (GRAVÉES DANS LE MARBRE)

### 1. POLICES (FONTS)
*   **Titres (Hn)** : `Forum` (Serif).
*   **Interface / Corps** : `Montserrat` (Sans-serif).

### 2. HIÉRARCHIE VISUELLE (TITRES)
*   **H1 (Hero)** : Casse phrase obligatoire (sauf exception purement éditoriale type slogan).
*   **H2 / H3 (Sections)** : Uppercase (tout majuscule) **AUTORISÉ** pour les grands piliers :
    *   *PROGRAMME SIGNATURE*
    *   *L'INSTANT KLEIA*
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
3. **NE JAMAIS** ajouter de dépendances npm
4. **NE JAMAIS** supprimer les animations CSS natives
5. **NE JAMAIS** modifier la palette de couleurs burgundy (#580017)
6. **NE JAMAIS** toucher au fichier `index.html` sans backup préalable
7. **NE JAMAIS** utiliser d'IA pour "améliorer" le design

### ✅ CE QUI FONCTIONNE PARFAITEMENT

- ✨ **Animations CSS natives** : morph, waves, hover effects
- 🎨 **Design burgundy premium** : #580017, #D70040, #FAF9F6
- 📱 **Responsive design** : mobile, tablet, desktop
- 🚀 **Performance** : chargement ultra-rapide, zéro dépendance
- 🎯 **SEO** : balises meta complètes, schema.org
- 🔗 **GitHub Pages** : déploiement automatique activé

---

## 🖥️ TESTER LOCALEMENT

### Méthode 1 : Double-clic (le plus simple)
1. Ouvrir l'explorateur de fichiers
2. Double-cliquer sur `index.html`
3. Le site s'ouvre dans ton navigateur par défaut

### Méthode 2 : Live Server (recommandé pour le développement)
1. Installer l'extension **Live Server** dans VS Code
2. Clic droit sur `index.html` → **Open with Live Server**
3. La page se rafraîchit automatiquement à chaque modification

---

## 🛡️ SAUVEGARDES ET PROTECTION

### Branche principale
```
main (branch) - Version de production
```

### Branches de sauvegarde
```
STABLE-BACKUP-2026-01-08 - Backup du design original
pre-cleanup-2026-01-30   - Backup avant nettoyage des fichiers Vite
```

### Tag de version
```
v1.0-STABLE - Version stable tagée et protégée
```

---

## 🔧 PROCÉDURES DE MAINTENANCE

### 🚨 En cas de problème - RESTAURATION D'URGENCE

Si le site est cassé, suivre cette procédure **IMMÉDIATEMENT** :

```bash
# Option 1 : Restaurer depuis le tag
git checkout v1.0-STABLE
git push origin main --force

# Option 2 : Restaurer depuis la branche de backup
git checkout STABLE-BACKUP-2026-01-08
git checkout -b main-restored
git push origin main-restored:main --force
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

- Ne JAMAIS toucher au CSS sans backup
- Ne JAMAIS installer de dépendances npm
- Ne JAMAIS ajouter de frameworks CSS/JS
- Ne JAMAIS modifier la structure HTML sans backup

---

## 🌐 DÉPLOIEMENT

### GitHub Pages (actif)
- **URL** : https://jpnirrep.github.io/site-web-kleia-up/
- **Source** : Branch `main`
- **Build** : Automatique à chaque push

### Vérifier le déploiement
1. Aller sur Actions : https://github.com/JPnirrep/site-web-kleia-up/actions
2. Vérifier que "Deploy static content to Pages" est en succès (✅)
3. Tester le site en ligne

---

## 📝 HISTORIQUE DES VERSIONS

### v2.0-CLEAN (30/01/2026) - VERSION ACTUELLE
- ✅ Nettoyage des fichiers React/Vite/TypeScript parasites
- ✅ Architecture 100% Vanilla confirmée
- ✅ Documentation mise à jour
- ✅ Zéro dépendance npm

### v1.0-STABLE (08/01/2026)
- ✅ Design original restauré et protégé
- ✅ Animations CSS natives fonctionnelles
- ✅ Revert de la migration Tailwind ratée

---

## ❓ QUESTIONS FRÉQUENTES

### Q: Comment tester mes modifications ?
**R: Double-clic sur `index.html` ou utilise l'extension Live Server dans VS Code.**

### Q: Puis-je améliorer le design avec une IA ?
**R: NON. Le design actuel fonctionne parfaitement. Toute tentative d'\"amélioration\" a déjà cassé le site.**

### Q: Puis-je migrer vers Tailwind/React ?
**R: NON. JAMAIS. C'est déjà été tenté et a échoué. Les animations ne fonctionnent plus avec ces frameworks.**

### Q: Comment ajouter du contenu ?
**R: Modifier uniquement les TEXTES dans les balises HTML. Ne JAMAIS toucher au CSS ni à la structure.**

### Q: Le site est cassé, que faire ?
**R: Suivre la procédure de restauration d'urgence ci-dessus. Restaurer depuis v1.0-STABLE.**

---

## 👤 CONTACT

**Propriétaire** : KLEIA-UP  
**Site web** : https://jpnirrep.github.io/site-web-kleia-up/  
**GitHub** : https://github.com/JPnirrep

---

## 📜 LICENCE

Copyright © 2024-2026 KLEIA-UP - Tous droits réservés

---

> ⚠️ **RAPPEL FINAL** : Ce design est **IMMUABLE**. Toute tentative de modification majeure doit être précédée d'une sauvegarde complète et testée dans une branche séparée. En cas de doute, **NE RIEN MODIFIER**.
