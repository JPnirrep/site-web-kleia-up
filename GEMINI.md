# KLEIA-UP - Règles du Workspace

## Contexte
Site web statique pour KLEIA-UP, hébergé sur GitHub Pages.
- **URL de production** : https://kleia-up.fr/
- **Statut SEO** : Validé Google Search Console (Mars 2026)
- **Hébergement** : GitHub Pages (déploiement automatique sur push)

## 🛠️ Configuration SEO & Indexation
Audit profond (13/03/2026) :
1. **Domaine d'Autorité** : kleia-up.fr.
2. **Page d'Accueil** : `index.html` est la landing page officielle.
3. **Validation Google** : Balise Meta Search Console active.
4. **Sitemap** : URLs harmonisées sur kleia-up.fr.

## 📐 Architecture

### Vérification visuelle (Push + Preview)
**NOUVELLE CONSIGNE GLOBALE** : À chaque fois que je fais une itération ou que je modifie le code, tu dois **OBLIGATOIREMENT** rafraîchir la page (lancer le workflow `/check-site`) pour que je puisse vérifier dans Chrome.

Quand je demande de :
- faire une itération, modifier le site
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
├── index.html           # Redirection vers individuel-groupe.html
├── individuel-groupe.html # Page Individuel / Groupe (ex-particuliers)
├── entreprises.html     # Page Entreprises
├── manifeste.html       # Le Manifeste
├── css/                 # Styles CSS
├── assets/              # Images et ressources
├── scripts/             # Scripts d'automatisation (PowerShell)
│   └── verify-visual.ps1
└── .agent/workflows/    # Workflows Antigravity
    └── check-site.md
```

### Supervision et cohérence (Mode Superviseur)
Quand je demande de :
- "vérifie la cohérence"
- "récap de session"
- "supervise"
- ou toute variante similaire

➡️ **Tu lances automatiquement le workflow `/supervise`** qui produit un rapport court (alertes, suggestions, todo).

**En fin de session** : tu me proposes automatiquement un récap et la mise à jour de la documentation.

### Documentation automatique
À chaque fin de session ou sauvegarde majeure :
- Mettre à jour `README.md` avec les changements
- Documenter les nouveaux workflows/scripts/règles

## Principes de développement
- ❌ Ne jamais casser le code existant
- ✅ Capitaliser sur l'existant
- ✅ Voies simples, efficaces, frugales
- ✅ Design moderne et premium

## Structure du projet
```
site-web-kleia-up/
├── index.html           # Redirection
├── individuel-groupe.html # Page Individuel / Groupe
├── entreprises.html     # Page Entreprises
├── manifeste.html       # Le Manifeste
├── css/                 # Styles CSS
├── assets/              # Images et ressources
├── scripts/             # Scripts d'automatisation (PowerShell)
│   └── verify-visual.ps1
├── GEMINI.md            # Règles du workspace
└── .agent/
    ├── workflows/       # Workflows Antigravity
    │   ├── check-site.md
    │   └── supervise.md
    └── rules/           # Règles agent
        └── supervisor.md
```

## Contraintes techniques
- Site statique (HTML/CSS/JS vanilla)
- Compatible Hostinger (si migration future)
- Pas de serveur backend requis
- Build GitHub Pages : ~45 secondes après push

## ✅ Historique (Session v3.9.3-RAYONNANCE-IMPACT)
- [x] **v3.12.0-SEO-GEO-PULSE (19/03/2026)** : Blindage total SEO et indexation IA.
- [x] **Meta-Data Pulse** : Injection des balises Open Graph et Twitter Card sur `kit-survie.html`.
- [x] **GEO AI Search** : Enrichissement du fichier `llms.txt` avec des métadonnées d'entités (Sandrina Perrin, Leadership Organique) et ajout de JSON-LD FAQ sur l'accueil pour les agents conversationnels.
- [x] **Sitemap Pulse** : Ajout du Kit de Survie dans le `sitemap.xml` et actualisation des dates d'indexation.

- [x] **v3.11.0-DUAL-SPACE (19/03/2026)** : Déploiement de la navigation duale et correction critique du CTA Header.
- [x] **Navigation Duale** : Implémentation du sélecteur `POUR TOI | L'ENTREPRISE` dans le header de toutes les pages pour clarifier instantanément les deux univers.
- [x] **Correction CTA Header** : Redirection globale du bouton "JE REJOINS LE MOUVEMENT" vers `#kit-urgence` (individuel) ou le modal contact (entreprise), assurant une conversion cohérente sur toutes les pages, y compris `index.html`.
- [x] **Style Actif** : Ajout d'un soulignement bordeaux dynamique pour marquer l'espace de navigation courant.

- [x] **v3.10.2-REDIRECT-B2B (19/03/2026)** : Correction de la redirection du bloc Conférence sur `programmes.html` vers `entreprises.html#conference`.
- [x] **v3.10.1-KIT-INTEGRATION (19/03/2026)** : Redirection de tous les CTA "Kit d'Urgence" vers la page interne `kit-survie.html` (suppression de TinyURL/Firebase).
- [x] **v3.10-KIT-SOUVERAIN (19/03/2026)** : Migration et souveraineté du "Kit de Survie".
- [x] **Fidélité Totale** : Reproduction exacte de la structure Firebase Studio (Bio, Témoignages, CTA intermédiaires).
- [x] **Design Organique** : Implémentation du Blob morphing vertical pour Sandrina (15s morphing) et boutons Shine.
- [x] **Micro-Interactions** : Ajout d'effets 3D au survol sur les modules et les promesses.
- [x] **Lead Capture** : Connexion au backend PHP (`contact-reach.php`) avec effet Caméléon (bouton vert + lien Drive) au succès.

- [x] **v3.9.5-PROPOS-REFINEMENT (16/03/2026)** : Refonte de l'autorité et du design "A Propos".
- [x] **Autorité Flash** : Remplacement de "Fabrique PEPPS" par le Podcast "Les Coulisses du Speaker" (80+ épisodes).
- [x] **Design Bijou** : Compression du bloc CTA final, boutons Or Royal avec effet balayage shine, et correction de la lisibilité/largeur.
- [x] **v3.9.4-SEO-PULSE (16/03/2026)** : Blindage SEO et indexation profonde.
- [x] **Meta Pulse** : Titres et descriptions uniques pour les 8 pages, injection de balises canoniques pour éviter le duplicate content.
- [x] **Sécurité Indexation** : Mise à jour de `robots.txt` pour exclure les dossiers techniques (`/scripts`, `/php`).
- [x] **v3.9.3-RAYONNANCE-IMPACT (16/03/2026)** : Optimisation finale de la rayonnance et sémantique.
- [x] **Rayonnance IMPACT** : `IMPACT` en majuscules, gras (900), sans italique, avec `text-shadow` doré pour un effet lumineux sur fond bordeaux.
- [x] **v3.9.2-GOLD-RESTORE (16/03/2026)** : Restauration de l'or brillant via la classe globale `.gold-shine-text`.
- [x] **v3.9.1-SEMANTIC-BOOST (16/03/2026)** : Remplacement de "transformation identitaire" par "libération de ton leadership" sur `individuel-groupe.html`.

- [x] **v3.9-SURGE-REFINEMENT (16/03/2026)** : Correction chirurgicale sur `programmes.html`.
- [x] **Harmonisation UX** : Suppression du style discordant sur le mot "Impact" pour une cohérence charte totale.
- [x] **Évolution Sémantique** : Remplacement de "ancrer" par "révéler" et "organique" par "authentique" dans les vignettes.
- [x] **Actualisation Offre** : Mise à jour de la promesse "Signature" (libération de l'essence et des talents).

- [x] **v3.9-DEEP-PREMIUM (13/03/2026)** : Refonte visuelle haute-couture et densification stratégique.
- [x] **Design Médaillon** : Implémentation de vignettes circulaires flottantes avec bordures Gold et effets de zoom sur la page `programmes.html`.
- [x] **Assets Premium** : Génération et intégration de 3 visuels abstraits haute qualité pour les offres Signature, Entreprise et Conférence.
- [x] **Header Dynamique** : Correction de la transparence du header sur `programmes.html` (transparence totale sur Hero bordeaux) pour une immersion parfaite.
- [x] **Densification Home** : Enrichissement de la section "Miroir de douleur" (Bento Grid 3 colonnes) et amélioration du Hero (double CTA, texte percutant).
- [x] **Polissage `a-propos.html`** : Réintégration du lien LinkedIn avec icône SVG, optimisation des marges organiques et du CTA final.

- [x] **v3.8-SEO-EXPANSION (13/03/2026)** : Déploiement de l'arborescence complète (5 nouvelles pages).
- [x] **Architecture Connectée** : Création de `a-propos.html`, `programmes.html`, `journal.html`, `contact.html`.
- [x] **Navigation Globale** : Unification du menu de navigation sur l'ensemble du site (8 pages).
- [x] **Optimisation AIO** : Mise à jour du `sitemap.xml` et du fichier `llms.txt` pour les agents IA.
- [x] **SEO Sémantique** : Injection de mots-clés stratégiques (leadership organique, rigologie, conférencière) dans les nouvelles routes.

- [x] **v3.7-STABLE-PREMIUM (13/03/2026)** : Version de référence finale. Activation du formulaire de contact PHP (Option B) avec double notification (Sandrina + JP).

## 🎯 TODO PROCHAINE SESSION
- [ ] **Audit Indexation Réel** : Vérifier la remontée de `kit-survie.html` dans Google Search Console.
- [ ] **Sitemap Update** : Ajouter manuellement le Kit dans `sitemap.xml`.
- [ ] **Polissage Journal** : Ajouter des visuels d'en-tête pour les articles du blog.
- [ ] **Audit Responsif Final** : Vérification minutieuse du Kit sur tablettes et mobiles.
