# Archive - Atelier "Prendre sa place sans forcer" (Mai-Juin 2026)

> Ce document archive l'integralite du dispositif deploye pour l'atelier visio du 2 juin 2026.

## Details Techniques
- **Offre** : Atelier visio 45 min "Prendre sa place sans forcer"
- **Periode** : 16 mai au 2 juin 2026 12h00
- **Design** : Identique a Paques (Blanc Perle Noble)
- **Formulaire** : Prenom, Nom, Email, Consentement RGPD
- **Inscription** : Mini-DB JSON locale + Brevo Sync

## Fichiers concernes

| Fichier | Role |
|---------|------|
| `js/atelier-popup.js` | Popup IIFE (injection CSS + HTML + logique) |
| `php/atelier-subscribe.php` | Endpoint POST (validation + stockage JSON) |
| `atelier-place.html` | Page de confirmation post-inscription |
| `php/brevo-sync.php` | Script sync vers Brevo (CLI ou HTTP) |
| `php/rollback-atelier.php` | Securite rollback (backup/restore/status) |
| `index.html` | Script tag ajoute en L266 |
| `data/atelier-inscriptions.json` | Mini-DB des inscrits (gitignored) |
| `data/rollback/index-backup.html` | Backup de index.html avant activation |

## Rollback

```bash
# Restaurer l'etat avant popup
php php/rollback-atelier.php restore

# Ou en HTTP
GET /php/rollback-atelier.php?token=kleia-bravo-2026&action=restore
```

## Sync Brevo

```bash
# Lancer la synchro
php php/brevo-sync.php

# Ou en HTTP
GET /php/brevo-sync.php?token=kleia-bravo-2026
```

**API Brevo**:
- Key: dans php/config.php (non commite)
- List ID: 14 (CHALLENGE-Juin-2026)
- Email SMTP: sandrina@kleia-up.fr (sender id:5, SPF a configurer pour delivrabilite optimale)

**Integration**:
- Firestore: Admin SDK via service account (php/firebase-credentials.json, non commite)
- Email confirmation: Brevo SMTP automatique (php/email-confirmation.php)
- Meet: https://meet.google.com/wbz-emxy-udw | Tel: +33 1 87 40 02 06 CODE: 996 704 367#
- v3.15.0-ATELIER-POPUP

## Design System
- Couleur Primaire : #8B1D3D (Bordeaux Noble)
- Couleur Secondaire : #FDFCF0 (Perle / Creme)
- Action : Gradient #8B1D3D vers #D70040
- Animation : blur(15px), translateY(30px) vers 0, cubic-bezier(0.19, 1, 0.22, 1)
- Police : Ranade (Fontshare)

## Date Logic
Le popup verifie automatiquement la date :
- Démarre le 16 mai 2026 00h00
- S'arrete le 2 juin 2026 12h00
- localStorage kleia_atelier_closed_2026 pour ne plus reapparaitre
