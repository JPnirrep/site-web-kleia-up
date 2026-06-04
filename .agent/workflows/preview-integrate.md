---
name: preview-integrate
description: Preview, edit, test, and integrate static sites on VPS before deployment
trigger: /preview
---

# Workflow /preview

Pipeline de preview visuelle sur VPS, boucle d'edition rapide, puis integration au depot local et deploiement.

## 1. VPS Sandbox Preview

Servir un dossier sur le VPS via Python HTTP server et creer un tunnel SSH vers localhost.

```bash
# Serveur HTTP sur le VPS (Python 3)
python3 -m http.server <port> --directory <path>

# Si Python est trop ancien (pas de --directory) :
cd <dir> && python3 -m http.server <port>

# Tunnel SSH vers localhost (mode background, sans shell interactif)
ssh -i <key> -f -N -L <local_port>:127.0.0.1:<vps_port> debian@135.125.53.215
```

Ouvrir `http://127.0.0.1:<local_port>` dans le navigateur pour verification visuelle.

### Conventions
- VPS IP : `135.125.53.215`
- SSH key : `~/.ssh/vagus_core_2026`
- Ports : choisir un port libre cote local et cote VPS (ex. 8080, 8081)

## 2. Rapid Editing Loop

Editer les fichiers directement sur le VPS, puis actualiser le navigateur.

```bash
# Remplacer rapidement une chaine dans index.html
sed -i 's|old|new|g' index.html
```

Modifier les fichiers statiques (HTML, CSS, JS) sur le VPS, recharger la page (`F5`) pour voir le rendu instantanement. Iterer jusqu'au resultat valide.

## 3. Finalize & Integrate

Copier les fichiers du VPS vers le depot local, ajouter la balise noindex, pusher sur GitHub.

```bash
# Copier depuis le VPS vers le depot local (scp recursif)
scp -i ~/.ssh/vagus_core_2026 -r debian@135.125.53.215:<vps_path>/* "C:\Users\JP\Documents\GitHub\KLEIA\site-web-kleia-up\"

# Ajouter la meta noindex pour les pages a duree limitee (time-limited landing pages)
# Dans <head> :
# <meta name="robots" content="noindex, nofollow">

# Commiter et pousser
git add .
git commit -m "feat: integrer preview <description>"
git push
```

Le push declenche le auto-deploy GitHub. Attendre la fin du build, puis verifier sur `https://kleia-up.fr`.

### Depot local
`C:\Users\JP\Documents\GitHub\KLEIA\site-web-kleia-up\`

## 4. Cleanup

Arreter le serveur HTTP sur le VPS et fermer le tunnel SSH.

```bash
# Trouver et tuer le serveur HTTP sur un port donne
kill $(ss -tlnp | grep <port> | grep -oP 'pid=\K[0-9]+')
```

Le tunnel SSH (`-f -N -L`) est un processus separe ; le tuer via `kill` avec le meme PID detecte par la commande ci-dessus, ou via `pkill -f "ssh.*<local_port>"`.
