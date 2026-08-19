# Workflow Hebdomadaire — Publication Blog KLEIA-UP

Pipeline newsletter Brevo → article blog → déploiement. Cycle hebdomadaire.

## Déclencheur
Tu dis « blog workflow hebdo » → je fais tout.

---

## Ce que je fais automatiquement

1. **Détection du gap** : `python publish-blog-article.py list` → newsletters Brevo non bloguées
2. **Génération** : `python publish-blog-article.py <id>` pour chaque newsletter (structure HTML + meta + JSON-LD)
3. **Réécriture** : contenu mis en forme (sous-titres, citations, listes, CTA) — comme les 6 articles de ce matin
4. **Mise à jour** : blog.html (carte en position chronologique) + llms.txt
5. **Déploiement** : `git add && git commit && git push` → GitHub Pages

Rien à faire de ton côté. Résultat en ligne sur `kleia-up.fr/blog`.
---

## 1. Détection du gap

```bash
cd C:\Users\JP\Documents\GitHub\KLEIA\site-web-kleia-up
python scripts/publish-blog-article.py list
```

Affiche les newsletters Brevo envoyées qui n'ont pas encore d'article sur le blog.  
⚠️ Ignorer les faux positifs (anciennes newsletters déjà bloguées mais avec un slug différent).

**Lecture du résultat :**
- Les lignes avec une date > dernier article blog = vrai gap
- Les lignes avec `Prendre sa place sans forcer` = opérationnelles (ateliers), pas du contenu → ignorer
- Les lignes avec une date < dernier article blog = déjà publiées sous un autre titre → ignorer

---

## 2. Publication assistée

Pour chaque newsletter à publier :

```bash
python scripts/publish-blog-article.py <campaign_id>
```

Ce que le script automatise :
- ✅ Crée `journal/<slug>.html` avec structure complète (meta, OG, JSON-LD, nav, footer)
- ✅ Ajoute la carte en tête de `blog.html`
- ✅ Met à jour `llms.txt`

---

## 3. Réécriture du contenu (ÉTAPE CRITIQUE)

Le script extrait le texte brut de l'email Brevo. **Tu dois réécrire le contenu** dans `journal/<slug>.html` avec :

### Structure attendue
```html
<!-- ARTICLE CONTENT -->
<section class="section-padding" style="background-color: #fff;">
    <div class="container" style="max-width: 720px; font-size: 1.05rem; line-height: 1.8;">

        <p>Paragraphe d'introduction...</p>

        <h2 style="font-family: var(--font-title); color: var(--color-burgundy); margin-top: 50px; font-size: 1.5rem;">Titre de section</h2>

        <p>Contenu...</p>

        <blockquote style="border-left: 4px solid var(--color-burgundy); padding: 20px 25px; margin: 30px 0; background: #FAF9F6; border-radius: 0 8px 8px 0; font-style: italic; font-size: 1.1rem;">
            Citation importante
        </blockquote>

        <ul style="margin: 25px 0; padding-left: 20px;">
            <li style="margin-bottom: 15px;">Élément 1</li>
            <li style="margin-bottom: 15px;">Élément 2</li>
        </ul>

        <div style="background: var(--bg-cream); border-radius: 12px; padding: 30px; margin: 40px 0;">
            <h3 style="font-family: var(--font-title); color: var(--color-burgundy); margin-bottom: 15px;">✨ Exercice / CTA</h3>
            <p>Contenu de l'encart...</p>
        </div>

        <!-- NE PAS SUPPRIMER -->
        <hr style="border: none; border-top: 1px solid rgba(139, 29, 61, 0.15); margin: 50px 0;">
        <!-- Signature Sandrina -->
        <!-- Retour au Blog -->
    </div>
</section>
```

### Règles d'écriture
- **Voix** : Sandrina — authentique, intime, parfois crue. Écrire comme elle parle.
- **Longueur** : 5-10 paragraphes + 2-3 sous-titres + 1 encart CTA
- **Liens** : vers `/individuel-groupe` (CTA), `/blog` (retour)
- **Ne pas toucher** au bloc signature Sandrina, au `hr`, au lien retour blog, à la section newsletter

---

## 4. Ordre chronologique

Le script insère toujours en tête de `blog.html`. Pour publier plusieurs articles :
1. Commencer par le **plus vieux**
2. Finir par le **plus récent**

Ainsi chaque nouvel article pousse le précédent vers le bas et l'ordre final est correct.

Exemple avec les 6 d'aujourd'hui :
```
#242 (12 Juin) → #244 (17 Juin) → #248 (19 Juin) → #250 (3 Juil) → #251 (10 Juil) → #252 (17 Juil)
```

---

## 5. Déploiement

```bash
git add .
git commit -m "blog: <titre des articles>"
git push
```

Déploiement automatique via GitHub Pages (~2 min).  
URL : `https://www.kleia-up.fr/blog`

---

## Scripts et fichiers

| Fichier | Rôle |
|---------|------|
| `scripts/publish-blog-article.py` | Génération article + update blog.html + llms.txt + sitemap.xml |
| `scripts/gsc.py` | Automatisation Google Search Console (sitemap, inspection, stats) — config `gsc-local.json` gitignorée |
| `.agent/workflows/publish-blog.md` | Documentation du workflow |
| `php/config.php` | Clé API Brevo |

---

## Améliorations prévues

- [ ] 🔧 Détection des doublons par objet/date plutôt que par slug
- [ ] 🔧 Insertion à la bonne position chronologique (pas seulement en tête)
- [ ] 🔧 Auto-génération des articles similaires en bas de page
- [x] 🔧 Mise à jour automatique du `sitemap.xml` (19/08/2026 : commande `sitemap` + hook dans publish)

---

## Trigger reprise

« blog workflow hebdo » ou « publication blog kleia-up »
