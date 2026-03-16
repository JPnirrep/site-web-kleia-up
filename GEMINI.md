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

## ✅ Historique (Session v3.9-DEEP-PREMIUM)
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
- [ ] **Audit Indexation Réel** : Vérifier la remontée des nouvelles pages dans Google Search Console d'ici 48-72h.
- [ ] **Polissage Journal** : Ajouter des visuels d'en-tête pour les articles du blog pour augmenter le temps de rétention.
- [ ] **Formulaire Hostinger Reach** : Finaliser l'intégration et la stratégie d'envoi du formulaire modal (`#modal-contact` dans `entreprises.html`).
- [ ] **Audit Responsif Final** : Vérification minutieuse sur tablettes et petits smartphones.
