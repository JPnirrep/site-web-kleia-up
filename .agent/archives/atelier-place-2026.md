# Archive - Atelier "Prendre sa place sans forcer" (Mai-Juin 2026)

> Archive complete du dispositif. Version finale stable - 16 mai 2026.

## Details Techniques
- **Offre** : Atelier visio 45 min "Prendre sa place sans forcer"
- **Periode** : 16 mai au 2 juin 2026 12h00
- **Design popup** : Identique a Paques (Blanc Perle Noble)
- **Formulaire** : Prenom, Nom, Email, Consentement RGPD
- **Stockage** : 3 couches (Firestore + PHP JSON + localStorage)
- **Brevo** : Liste #14 (CHALLENGE-Juin-2026), push automatique
- **Email confirmation** : mail() Hostinger, texte brut, copie conforme contact-reach.php
- **Lien Meet** : https://meet.google.com/wbz-emxy-udw | Tel: +33 1 87 40 02 06 CODE: 996 704 367#

## Fichiers

| Fichier | Role |
|---------|------|
| `js/atelier-popup.js` | Popup IIFE, design Paques, 3 couches stockage |
| `php/atelier-subscribe.php` | Endpoint inscription (JSON + Firestore + email) |
| `php/email-confirmation.php` | Email texte brut via mail() Hostinger |
| `php/brevo-push.php` | Push contact vers liste Brevo #14 |
| `php/brevo-sync.php` | Batch sync Brevo |
| `php/firestore.php` | Firestore Admin REST helper |
| `php/rollback-atelier.php` | Rollback securise (backup/restore/status) |
| `atelier-place.html` | Page confirmation + lien Meet |
| `index.html` | +3 scripts (Firebase Compat + popup) |

## Secrets (hors Git)

| Fichier | Contenu |
|---------|---------|
| `php/config.php` | Cle API Brevo + list ID |
| `php/firebase-credentials.json` | Service account Firebase |

## Lecons apprises (email Hostinger)

1. **Reprendre le pattern existant** : contact-reach.php avait deja la recette qui marche. Ne pas reinventer.
2. **mail() Hostinger = hsendmail -t** : wrapper custom, exige destinataire meme-serveur + header To explicite.
3. **Pas de HTML** : Hostinger bloque ou mute les emails HTML sortants. Texte brut uniquement.
4. **Headers obligatoires** : Message-ID (<timestamp-md5@kleia-up.fr>), X-Mailer, Reply-To, -f$from.
5. **Curl et + dans les emails** : `-d` encode le `+` en espace. Utiliser `--data-urlencode` ou eviter `+alice` en test.
6. **Eviter Brevo SMTP pour l'envoi** : expediteur non verifie = adresse rewritee. Garder Brevo uniquement pour la liste contacts.

## Rollback
```bash
php php/rollback-atelier.php restore
# ou HTTP: GET /php/rollback-atelier.php?token=kleia-bravo-2026&action=restore
```

## Sync Brevo
```bash
php php/brevo-sync.php
# ou HTTP: GET /php/brevo-sync.php?token=kleia-bravo-2026
```

## Nettoyage post-challenge (apres le 2 juin 12h00)

Le popup s'arrete automatiquement via le date guard (js/atelier-popup.js L42).
Pour un nettoyage complet :

```bash
# 1. Desactiver le popup
php php/rollback-atelier.php restore

# 2. Supprimer les fichiers atelier (optionnel)
rm -f js/atelier-popup.js php/atelier-subscribe.php php/email-confirmation.php php/brevo-push.php atelier-place.html

# 3. Archiver la DB
cp data/atelier-inscriptions.json .agent/archives/atelier-db-2026-06-02.json

# 4. Commit
git add -A && git commit -m "cleanup: fin atelier juin 2026" && git push
```

## Historique Git (v3.15.0)

```
8cb0859 feat: email confirmation auto + lien Meet
55fcda6 feat: Firestore Admin via service account
c614116 feat: popup atelier (16 mai - 2 juin 2026)
dae99d2 fix: email From sandrina@kleia-up.fr via Brevo SMTP
854c163 docs: v3.15.0-ATELIER-POPUP
78205d9 fix: email headers renforces
bfb3874 fix: email via mail() Hostinger conforme contact-reach
```
