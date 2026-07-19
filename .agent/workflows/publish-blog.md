# Workflow : Publication d'article blog KLEIA-UP

Pipeline newsletter Brevo → article blog → déploiement.

## Prérequis
- Clé API Brevo dans `php/config.php`
- Python 3
- Exécution à la racine de `site-web-kleia-up/`

## Étapes

### 1. Lister les newsletters non bloguées
```bash
python scripts/publish-blog-article.py list
```
Affiche les newsletters récentes qui n'ont pas encore d'article sur le blog.

### 2. Publier une newsletter en article
```bash
python scripts/publish-blog-article.py <campaign_id>
```
Ce que fait le script :
- ✅ Récupère le contenu de la newsletter via API Brevo
- ✅ Crée `journal/<slug>.html` avec :
  - Meta/OG/Twitter cards
  - JSON-LD BlogPosting + BreadcrumbList
  - Navigation header complète
  - Newsletter SIGNUP section
  - Footer
- ✅ Ajoute la carte en tête de `blog.html`
- ✅ Ajoute l'entrée dans `llms.txt`

### 3. Éditer le contenu
Le texte extrait de la newsletter est un **brouillon**. Ouvre et affine :
```
journal/<slug>.html
```
- Reformule le contenu au format blog
- Ajoute des sous-titres (`<h2>`), citations (`<blockquote>`), listes
- Vérifie les liens

### 4. Déployer
```bash
git add .
git commit -m "blog: <titre de l'article>"
git push
```
Le déploiement GitHub Pages est automatique.

## Gap actuel (19 Juillet 2026)
**6 newsletters non bloguées :**
| Date | Campagne | Sujet |
|------|----------|-------|
| 17 Juil | #252 | Hypersensible et oser — Jongler avec 1000 vies |
| 10 Juil | #251 | Hypersensible et affirmation de soi — Coulisses ✨ |
| 3 Juil | #250 | Écrire un livre sur le lâcher-prise... 🙃 |
| 19 Juin | #248 | Prise de parole : le jour où j'ai refusé |
| 17 Juin | #244 | Tais toi Gigi |
| 12 Juin | #242 | Comment garder sa prestance |

## Maintenance
- Script : `scripts/publish-blog-article.py`
- La clé API Brevo est dans `php/config.php`
- Ne pas oublier de mettre à jour les articles similaires dans le bas de chaque article
