# Templates de Coaching Premium KLEIA-UP

Ce dossier contient les modèles officiels pour les livrables de coaching.

## 📄 HTML Premium Template (`session_report_v2.html`)
C'est le modèle haute-couture utilisé pour l'affichage dans le Cockpit Barnaby et pour les exports PDF.

### Variables à remplacer :
- `{{CLIENT_NAME}}` : Nom complet du coaché.
- `{{SESSION_ID}}` : Identifiant (ex: H2, H3...).
- `{{DATE}}` : Date de la séance.
- `{{SESSION_NAME}}` : Thème de la session.
- `{{COACH_NAME}}` : Nom du coach (généralement Sandrina Perrin).
- `{{GLOBAL_OBJECTIVE}}` : Synthèse des objectifs.
- `{{OBJECTIVES_LIST}}` : Liste <li> des objectifs spécifiques.
- `{{COACH_NOTE}}` : Note importante mise en avant.
- `{{TOPICS_LIST}}` : Liste ordonnée <ol> des points abordés.
- `{{STRENGTHS}}` / `{{VIGILANCE}}` : Points d'appui et de vigilance.
- `{{INSIGHTS}}` : Prises de conscience du client.
- `{{KIT_FICHES}}` : Blocs `.fiche-exercice` détaillés.
- `{{ACTIONS}}` : Liste d'actions concrètes.
- `{{NEXT_SESSION}}` : Date et thèmes de la suite.

## ⚙️ Workflow de Publication
1. **Extraction** : Extraire les données du PDF ou des notes brutes.
2. **Génération** : Remplir le template HTML.
3. **Cockpit** : 
   - Enregistrer le fichier dans `coaching_data/[client]/H[X]_report_premium.html`.
   - Mettre à jour `[client]_state.json` (statut "Completed").
   - Vérifier le rendu dans `app.js` (fonction `renderSessionView`).
4. **Push** : Pousser sur GitHub pour déploiement immédiat.
