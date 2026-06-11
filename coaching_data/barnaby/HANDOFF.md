# Barnaby Coaching Space — Handoff & Memory

## Session : 2026-06-11 — H4 + Dashboard upgrades

### Fichiers modifiés/créés

| Fichier | Action |
|---------|--------|
| `coaching_data/barnaby/barnaby_state.json` | Scores H2 ajoutés, H4 complété, assets + report_h4 |
| `coaching_data/barnaby/H4_report_premium.html` | **Nouveau** — 4 pages A4, design KLEIA |
| `coaching_data/barnaby/h4_transcript.json` | **Nouveau** — transcription brute 1116 segments |
| `coaching_data/barnaby/h4_transcript.txt` | **Nouveau** — texte brut transcription |
| `space/barnaby/index.html` | Section évolution H1→H4 ajoutée, baseline dynamique, cache buster `?v=3` |
| `space/barnaby/app.js` | `renderBaseline()`, `initEvolutionChart()` avec fallback H1 baseline |

### Architecture dashboard coaching

**Connexion** : Firebase Firestore token-based (`access_tokens/{secretcode}` → owner + role)
  - Prénom + code secret OU case "Visiteur"
  - Roles: `client` (accès total), `visitor` (H1 only)

**Données** : `coaching_data/barnaby/barnaby_state.json`
  - `baseline_scores` → utilisé pour H1 si absent de `sessions_content.1`
  - `sessions_content.{n}.scores` → session scores (optionnel; H1 n'en avait pas)
  - `content.roadmap[]` → statut "Upcoming"/"Completed"/"In Progress"
  - `assets.report_h{n}` → lien vers rapport premium HTML

**Dashboard dynamique** :
  - `renderBaseline(data)` → dernière session completed dans `roadmap` + `last_update`
  - `initEvolutionChart(data)` → line chart Chart.js, agrège H1→Hn, auto-extensible
  - `renderSessionView(n)` → vidéo + rapport + synthèse
  - `switchSession(n)` → met à jour radar + gauges selon scores de la session

### Template pour nouveau client coaching

1. Créer `coaching_data/{prenom}/barnaby_state.json` (copier structure)
2. Cloner `_template/` → `space/{prenom}/` (via clone.py)
3. Adapter auth.js + login.html (Firebase config)
4. Déployer sur Hostinger

### Scores H1→H4 Barnaby

| Session | Regard | Ancrage | Geste | Débit | Relief | Présence |
|---------|--------|---------|-------|-------|--------|----------|
| H1 (baseline) | 3 | 4 | 4 | 3 | 4 | 4 |
| H2 (estimé) | 4 | 5.5 | 4.5 | 3.5 | 4.5 | 5 |
| H3 | 5 | 6.5 | 5.5 | 4 | 5 | 6.5 |
| H4 | 6 | 7 | 6 | 5 | 6 | 7 |

### Hostinger upload

- Les vidéos (.mp4, .mov) sont dans `.gitignore` → upload manuel FTP
- Dossier : `public_html/coaching_data/{prenom}/`
- Nom = nom exact du fichier dans `assets.replay_h{n}`

### Prochaine session (H5)

Si nouvelles ressources arrivent :
1. `barnaby_state.json` : ajouter `sessions_content.5`, `assets.replay_h5`, roadmap H5
2. Updater la baseline auto (déjà fait par `renderBaseline`)
3. La courbe d'évolution inclura H5 automatiquement
4. Générer rapport H5 (suivre pattern H4)

### Prompts réutilisables

**Générer rapport coaching** :
"Génère H{n}_report_premium.html dans coaching_data/{prenom}/ suivant le template H3 (4 pages A4, CSS KLEIA bordeaux/or) avec sections : objectifs de la séance, bilan, exercices, observations coach, 3 forces actualisées, prises de conscience, messages clés, plan d'actions, prochaines étapes. Sources : transcription audio (h{n}_transcript.txt) et barnaby_state.json."

**Ajouter session coaching** :
"Ajoute session H{n} dans barnaby_state.json : sessions_content.{n}, assets.replay_h{n}, roadmap status Completed, update last_update et session_id. La vidéo est {nom_fichier}.mp4"
