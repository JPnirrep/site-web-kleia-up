# Rapport d'Audit — Site KLEIA-UP (kleia-up.fr)
**Date :** 11 Juin 2026  
**Objet :** Page blog invisible + audit connexions GitHub/Hostinger

---

## 🔴 PROBLÈME PRIORITAIRE — Pourquoi la page blog n'apparaît pas

### Diagnostic
**La page `blog.html` existe et est accessible depuis n'importe quelle URL directe :**
- `https://www.kleia-up.fr/blog.html` → 200 OK (18 articles listés)
- `https://kleia-up.fr/blog.html` → 301 → `https://www.kleia-up.fr/blog.html` → 200 OK

### Cause racine : AUCUN LIEN DE NAVIGATION vers le blog
**Aucune page du site ne contient de lien vers `blog.html` dans son menu de navigation :**

| Page | Lien BLOG dans nav ? |
|---|---|
| `index.html` (Accueil) | ❌ |
| `individuel-groupe.html` | ❌ |
| `entreprises.html` | ❌ |
| `manifeste.html` | ❌ |
| `programmes.html` | ❌ |
| `contact.html` | ❌ |
| `a-propos.html` | ❌ |
| `kit-survie.html` | ❌ |

**Seule `blog.html` elle-même** a le lien BLOG actif dans sa propre nav — mais l'utilisateur ne peut pas y accéder depuis la navigation.

### Gravité : **Critique**
- Un visiteur sur l'accueil ne peut **pas trouver le blog**
- Google crawl depuis l'accueil ne découvre pas `blog.html`
- Le blog existe mais est **invisible** sans URL directe

### Correction immédiate
Ajouter `<li><a href="blog.html" class="nav-link">BLOG</a></li>` dans la navigation de **TOUTES les pages** (index.html, individuel-groupe.html, entreprises.html, manifeste.html, programmes.html, contact.html, a-propos.html, kit-survie.html).

---

## 🟡 ANOMALIES CONNEXES

### 1. Breadcrumb JSON-LD incorrect (blog.html ligne 44)
```json
"item": "https://kleia-up.fr/journal.html"
```
`journal.html` n'existe pas → devrait être `https://kleia-up.fr/blog.html`.  
**Impact SEO :** Google ignore cette breadcrumb cassée.

### 2. Fichier orphelin `index (1).html`
Version antérieure de l'accueil (pre-Speculation Rules, pre-JSON-LD enrichi, sans blog).  
**Action :** Supprimer ce fichier.

### 3. Navigations non harmonisées
La nav de `index.html` utilise des classes CSS inline dans `<style>` (lignes 285-290), tandis que les pages blog/journal ont leur propre `<style>` inline. Les autres pages utilisent le `main.css` externe. **Cohérence :** toutes les pages devraient partager le même bloc de styles nav.

### 4. Blog titré "Journal" dans le contenu mais "Blog" dans l'URL
- URL : `blog.html`, menu : "BLOG"
- Contenu H1 : "Journal du Mouvement", héro eyebrow : "RÉFLEXIONS & COULISSES"
- Breadcrumb JSON-LD : référence à `journal.html`
- **Cohérence éditoriale :** choisir "Blog" ou "Journal" et uniformiser partout.

---

## 🔵 AUDIT DES CONNEXIONS GITHUB / HOSTINGER

### Chaîne de déploiement

```
Push main GitHub
  ├─► GitHub Actions deploy.yml → GitHub Pages (jpnirrep.github.io) — PREVIEW
  └─► Hostinger auto-pull depuis GitHub — PRODUCTION (www.kleia-up.fr)
```

| Composant | État | Notes |
|---|---|---|
| Dépôt GitHub | ✅ OK | `github.com/JPnirrep/site-web-kleia-up` |
| GitHub Actions | ✅ OK | 5 derniers runs : success |
| GitHub Pages preview | ✅ OK | `jpnirrep.github.io/site-web-kleia-up/` |
| DNS (www) | ✅ OK | CNAME → `www.kleia-up.fr.cdn.hstgr.net` (Hostinger CDN) |
| DNS (apex) | ✅ OK | Redirect 301 → www |
| Hostinger production | ✅ OK | Plate-forme hcdn, headers `platform: hostinger` |
| .htaccess | ✅ OK | Redirections, cache, anti-cache HTML |
| SSL | ✅ OK | Certificat actif |

### Constats
1. **Le workflow `deploy.yml` déploie vers GitHub Pages**, mais le site live est **servi par Hostinger** (auto-pull). Le GitHub Pages sert uniquement de preview/debug.
2. **Pas de CNAME file** dans le repo — le custom domain GH Pages n'est pas configuré côté repo. Si GH Pages devient la prod un jour, il faudra ajouter un CNAME.
3. **La config Hostinger (auto-pull)** n'est pas tracée dans le code — dépend de la configuration dans le panneau Hostinger. Risque si le repo change de nom ou si l'intégration est recréée.
4. **Pas de secret exposed** dans le code (les clés API Brevo sont dans `php/config.php` qui est dans `.gitignore` — uniquement `config.example.php` versionné).

---

## 🟢 PLAN D'ACTION

### P0 — Correction immédiate (30 min)
- [ ] Ajouter le lien BLOG dans la nav de **toutes les pages** (8 fichiers HTML)
- [ ] Corriger le breadcrumb JSON-LD dans `blog.html` : `journal.html` → `blog.html`
- [ ] Supprimer `index (1).html`

### P1 — Cohérence (1h)
- [ ] Uniformiser le bloc `<style>` de la nav sur toutes les pages (même CSS, même ordre des liens)
- [ ] Décider et appliquer : "Blog" ou "Journal" — titre, URL, breadcrumb, menu, H1

### P2 — Robustesse déploiement (2h)
- [ ] Ajouter un CNAME file dans le repo (`www.kleia-up.fr`) si GH Pages doit rester un preview fonctionnel
- [ ] Documenter dans README le pipeline exact : GitHub push → Hostinger auto-pull (avec URL du panneau de config)
- [ ] Ajouter un script de smoke-test post-déploiement (curl + vérification de contenu)
- [ ] Ajouter `.github/workflows/deploy.yml` une étape de vérification (crawl les URLs critiques)

### P3 — SEO & Contenu (planifiée)
- [ ] Vérifier que Google a bien indexé `blog.html` (GSC → vérification d'indexation)
- [ ] Ajouter les URLs articles au sitemap (déjà fait pour 18 articles — OK)
- [ ] Monitorer le trafic vers `/blog` vs `blog.html` (analytics)

---

## FICHIERS CONCERNÉS

| Fichier | Modifications |
|---|---|
| `index.html` | Ajouter BLOG dans nav |
| `individuel-groupe.html` | Ajouter BLOG dans nav |
| `entreprises.html` | Ajouter BLOG dans nav |
| `manifeste.html` | Ajouter BLOG dans nav |
| `programmes.html` | Ajouter BLOG dans nav |
| `contact.html` | Ajouter BLOG dans nav |
| `a-propos.html` | Ajouter BLOG dans nav |
| `kit-survie.html` | Ajouter BLOG dans nav |
| `blog.html` | Fix breadcrumb (journal.html → blog.html) |
| `index (1).html` | Supprimer |
