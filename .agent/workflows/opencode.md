---
name: opencode
description: Délègue une tâche à OpenCode CLI ou Zed via le pont antigravity
trigger: /opencode
---

# Workflow /opencode

Délègue des tâches entre OpenCode, Zed et le cerveau antigravity.

## Usage

```
/opencode brain <question>
/opencode zed <fichier> [ligne] [col]
/opencode route <tâche>  → route automatiquement vers le bon outil
/opencode agents          → liste les agents disponibles
```

## Flux

1. Analyse de la requête → classification (brain / zed / opencode)
2. Exécution via `vagus_opencode_bridge.py`
3. Rapport du résultat

## Bridge

```bash
python "C:\Users\JP\Documents\GitHub\antigravity-brain\scripts\vagus_opencode_bridge.py" <cmd> <args>
```
