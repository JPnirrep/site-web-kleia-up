# KLEIA-UP — Instructions pour OpenCode

Tu es l'agent OpenCode dédié au projet **KLEIA-UP**. Tu travailles en synergie avec :
- **antigravity-brain** (le cerveau, mémoire perpétuelle)
- **Zed** (l'éditeur visuel pour les fichiers ouverts)
- **Le framework .agent/** (20 agents spécialisés)

## Architecture
```
site-web-kleia-up/
├── .agent/           # Framework agent (Antigravity Kit)
│   ├── agents/       # 20 spécialistes
│   ├── skills/       # 36 domaines
│   ├── rules/        # GEMINI.md (P0), supervisor.md
│   └── workflows/    # /create, /enhance, /opencode, etc.
├── .opencode/        # Config OpenCode (ce fichier)
├── .memory/          # Mémoire de session
├── GEMINI.md         # Règles workspace
└── *.html            # Pages du site
```

## Pont avec antigravity-brain
```bash
# Interroger le cerveau
python "C:\Users\JP\Documents\GitHub\antigravity-brain\scripts\vagus_opencode_bridge.py" brain "ma question"

# Router une requête
python "C:\Users\JP\Documents\GitHub\antigravity-brain\scripts\vagus_opencode_bridge.py" route . "ouvre le fichier X"

# Ouvrir dans Zed
python "C:\Users\JP\Documents\GitHub\antigravity-brain\scripts\vagus_opencode_bridge.py" open chemin/fichier.html 10 1

# Lister les agents disponibles
python "C:\Users\JP\Documents\GitHub\antigravity-brain\scripts\vagus_opencode_bridge.py" agents
```

## Principes FVP (Frugal, Vérifiable, Performant)
1. **Frugalité** — Économie de tokens. Pas de politesse inutile.
2. **Substance** — Priorise la densité d'information.
3. **Vérifiabilité** — Code commenté en anglais, rapports en français.
4. **Souveraineté** — Local-first, utilise le framework .agent/ intégré.

## Délégation Zed
Quand un fichier doit être édité visuellement, utilise le bridge :
```bash
vagus_opencode_bridge.py open individuel-groupe.html
```
Zed s'ouvre avec le fichier. Une fois fermé, l'édition est terminée.

## Règles du projet
- Site statique HTML/CSS vanilla
- Pas de frameworks JS
- Design KLEIA : bordeaux #8B1D3D, typo Ranade/Syne
- Priorité B2C (individuel-groupe.html)
