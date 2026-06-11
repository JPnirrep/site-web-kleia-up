> Dernière action : v3.21.0-AUDIT-BLOG-TRACKING (11/06/2026) — Audit + P0 blog invisible + GTM/GA4 + BlogPosting + articles similaires
> 
> ## Session du 11/06/2026 — Audit + Tracking + SEO
> 
> ### Problème identifié
> - Blog invisible : aucun lien BLOG dans la navigation (7 pages sans lien)
> 
> ### Corrections P0
> - ✅ Lien BLOG ajouté dans nav de toutes les pages
> - ✅ Breadcrumb JSON-LD corrigé (journal.html → blog.html)
> - ✅ `index (1).html` (copie obsolète) supprimé
> 
> ### Tracking
> - ✅ GTM-5RP5FZR3 injecté sur 31+ pages
> - ✅ GA4 G-PBRNYXGCMC injecté sur 32+ pages
> - ✅ Newsletter link tracé avec `?utm_source=blog`
> 
> ### SEO Articles
> - ✅ Schema `Article` → `BlogPosting` (18 articles)
> - ✅ Articles similaires (3 par article, contexte différent)
> - ✅ `llms.txt` mis à jour (10 → 18 articles)
> 
> ### Tâches restantes
> - [ ] Google Search Console : soumettre sitemap `https://kleia-up.fr/sitemap.xml`
> - [ ] GA4 : vérifier les données après 48h
> - [ ] Configurer conversions newsletter + appels dans GTM (ouvrir GTM → GA4 event tag)
> 
# Notes de session — Projet KLEIA-UP

> ✅ Google Business Profile créé — `.agent/google-business-profile-setup.md` pour les données de la fiche



> Fin de session — tout commit + push + vérifié live sur kleia-up.fr ✅
> Prochaine action : Google Search Console (soumettre sitemap) + GA4 (vérifier données dans 48h) + configurer conversions newsletter dans GTM
## Pour reprendre le développement

Copie-colle ce message en début de session :

> Reprends le développement du site kleia-up.fr. Le projet est dans `C:\Users\JP\Documents\GitHub\KLEIA\site-web-kleia-up`. Consulte le `README.md` pour l'historique, puis vérifie l'état actuel des fichiers. Dernière version : v3.21.0-AUDIT-BLOG-TRACKING. GTM-5RP5FZR3 + GA4 G-PBRNYXGCMC déployés. Blog visible dans nav. 18 articles en BlogPosting avec articles similaires. Consulte `NOTES-SESSION.md` pour les points d'entrée et les tâches restantes.

## Contexte technique

- **Type** : Site statique HTML/CSS vanilla (0 framework, 0 JavaScript lourd)
- **Hébergement** : Hostinger (auto-pull depuis GitHub sur push `main`)
- **CI/CD** : GitHub Actions → GitHub Pages (aperçu) + Hostinger auto-pull
- **Domaine** : `https://kleia-up.fr`
- **GitHub** : `https://github.com/JPnirrep/site-web-kleia-up`
- **Aperçu GH Pages** : `https://jpnirrep.github.io/site-web-kleia-up/`

## Points d'entrée clés

| Ressource | Chemin |
|---|---|
| **README + Changelog** | `README.md` |
| **Audit SEO** | `G:\Mon Drive\KLEIA-UP\06_OPERATIONS_ET_TECHNIQUE\création du site web\rapport audit site kleia-up.json` |
| **Brevo API** | `php/config.php` (clé API incluse) |
| **Newsletters (source contenu blog)** | API Brevo → `GET https://api.brevo.com/v3/emailCampaigns` |
| **Témoignages clients** | `.agent/temoignages-clients.md` |
| **Script formation détaillé** | `C:\Users\JP\Documents\GitHub\KLEIA\formation-kleia-up\docs\doc formation kleia-up\formations en ligne Kleia-up\SCRIPT DE RÉFÉRENCE _ FORMATION LEADERSHIP ET AFFIRMATION DE SOI.docx` |
| **LinkedIn Sandrina** | sandrina.perrin2@gmail.com (mot de passe à demander à l'utilisateur) |

## Dernière version : v3.16.1 (08/06/2026)

### Ce qui a été fait
- **Blog** : 10 articles publiés depuis newsletters Brevo, pages individuelles dans `journal/`
- **JSON-LD E-E-A-T** : Person + hasCredential (9 certifs), alumniOf (8 org.), BreadcrumbList, Article schema
- **FAQPage** : 10 questions sur index.html
- **Review schema** : 4 témoignages clients
- **Performance** : Hero image 209→60 KB, logo 113→21 KB WebP, cache .htaccess
- **OG/Twitter cards** : sur toutes les pages (7 pages étaient sans)

### Tâches restantes (par priorité)

**🔵 P0 — Contenu blog**
- [ ] 8 newsletters Brevo restantes à transformer en articles
- [ ] Créer la page `journal/leadership-sensible.html` (placeholder existant)

### ✅ v3.18.0 réalisé (10/06/2026)
- [x] 8 newsletters Brevo transformées en articles (total : 18 articles dans le journal)
- [x] Nouveaux articles : Chaos ou Apaisement, De la joie de l'audace, Oser prendre sa place, Ce matin là j'ai pleuré, C'est le moment de muer, Communication relations, Écouter sans tes oreilles, Décider
- [x] Journal mis à jour avec 18 cartes classées par date
- [x] Sitemap enrichi (30 URLs) et cohérent
- [x] P0 complété — toutes les newsletters Brevo sont maintenant des articles de blog


### ✅ v3.19.0 réalisé (10/06/2026)
- [x] Page `coaching-vendee.html` créée : landing page SEO locale avec GEO meta, LocalBusiness schema, areaServed
- [x] Sitemap mis à jour (31 URLs)
- [x] Lien interne vers coaching-vendee dans le footer
- [x] P1 : page "Coaching Vendée" faite — reste Google Business Profile + vidéos YouTube

**🟡 P1 — SEO local**
- [x] Créer une page "Coaching Vendée" (`coaching-vendee.html`)
- [x] Créer un Google Business Profile
- [ ] Enregistrer 1-2 vidéos YouTube courtes et les embedder

**🟢 P2 — Technique (suite)**
- [x] Remplacer Tailwind CDN + Lucide sur `kit-survie.html` par CSS natif
- [ ] Backlinks (partenariats, podcast invité)

### ✅ v3.17.0 réalisé (10/06/2026)
- [x] 4 balises `<title>` cassées réparées (journal, contact, programmes, a-propos)
- [x] `og:image` + Twitter Cards ajoutés à `entreprises.html`
- [x] JSON-LD ajouté à `atelier-place.html`, `challenge-juin26.html`, `kit-survie.html` (harmonisé @graph)
- [x] Sitemap : priorité offres/signature corrigée, tous lastmod → 2026-06-10
- [x] llms.txt enrichi (10 articles, FAQ, témoignages, entités)
- [x] Meta GEO ajoutées à contact, atelier-place, challenge-juin26
- [x] CSS critique inline + deferred stylesheet sur 4 pages principales
```bash
# Récupérer les newsletters Brevo
python3 -c "
import httpx
api_key = open('php/config.php').read().split(\"'\")[1]  # extract key
headers = {'api-key': api_key}
resp = httpx.get('https://api.brevo.com/v3/emailCampaigns', headers=headers, params={'limit':50})
for c in resp.json()['campaigns']:
    print(f\"ID {c['id']:3d} | {c.get('name','?'):50s} | {c.get('status','?'):10s} | {c.get('sentDate','?'):25s}\")
"

# Vérifier le site en ligne
python3 -c "
import urllib.request
r = urllib.request.urlopen('https://kleia-up.fr/')
print(f\"Site OK: {r.status}\")
print(f\"JSON-LD blocks: {r.read().decode().count('application/ld+json')}\")
"
```

### 10 articles existants
1. `journal/dire-bonjour-cest-deja-prendre-la-parole.html` — 5 Juin 2026
2. `journal/croire-en-lautre.html` — 28 Mai 2026
3. `journal/tu-voulais-le-dire.html` — 27 Mai 2026
4. `journal/on-a-bien-ri.html` — 22 Mai 2026
5. `journal/prix-du-silence.html` — 8 Mai 2026
6. `journal/frontiere-limites.html` — 1er Mai 2026
7. `journal/humain-methode.html` — 13 Fev 2026
8. `journal/egoiste-talent.html` — 6 Fev 2026
9. `journal/etre-chaos.html` — 19 Jan 2026
10. `journal/corps-oublie.html` — 22 Oct 2025
