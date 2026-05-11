#!/usr/bin/env python3
"""
clone.py — Clone le template KLEIA-UP pour un nouveau client de coaching.

Usage:
    python _template/clone.py Barnaby
    python _template/clone.py "Jean Dupont"

Effet :
    Crée space/{prenom}/ et coaching_data/{prenom}/
    avec tous les fichiers renommés et les placeholders substitués.
"""

import sys
import os
import shutil
import re
import secrets
import string

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(ROOT, "_template")
SPACE_TEMPLATE = os.path.join(TEMPLATE_DIR, "space", "{prenom}")
DATA_TEMPLATE = os.path.join(TEMPLATE_DIR, "coaching_data", "{prenom}")


def normalize(prenom: str) -> tuple:
    """Retourne (lower, capitalized, upper)."""
    p = prenom.strip()
    lower = p.lower().replace(" ", "-")
    cap = p.title()
    upper = p.upper().replace(" ", "_")
    return lower, cap, upper


def replace_placeholders(content: str, lower: str, cap: str, upper: str) -> str:
    """Remplace tous les placeholders dans le contenu."""
    content = content.replace("{prenom}", lower)
    content = content.replace("{Prenom}", cap)
    content = content.replace("{PRENOM}", upper)
    return content


def replace_in_file(filepath: str, lower: str, cap: str, upper: str):
    """Remplace les placeholders dans un fichier sur place."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    content = replace_placeholders(content, lower, cap, upper)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def generate_secret_code() -> str:
    """Génère un code secret format: XXXX-XXXX-XX-XXXX"""

    def block(n):
        return "".join(
            secrets.choice(string.ascii_uppercase + string.digits) for _ in range(n)
        )

    return f"{block(4)}-{block(4)}-{block(2)}-{block(4)}"


def clone(src: str, dst: str, lower: str, cap: str, upper: str):
    """Copie un dossier template et remplace les placeholders (via robocopy)."""
    if os.path.exists(dst):
        print(f"⚠️  Le dossier {dst} existe déjà. Sauvegarde...")
        backup = dst + ".bak"
        if os.path.exists(backup):
            shutil.rmtree(backup)
        shutil.copytree(dst, backup)
        print(f"   → Sauvegardé dans {backup}")

    import subprocess

    subprocess.run(
        [
            "robocopy",
            os.path.abspath(src),
            os.path.abspath(dst),
            "/E",
            "/NFL",
            "/NDL",
            "/NJH",
            "/NJS",
            "/R:0",
        ],
        capture_output=True,
        shell=True,
    )

    for root, dirs, files in os.walk(dst):
        for fname in files:
            replace_in_file(os.path.join(root, fname), lower, cap, upper)

    old = os.path.join(dst, "{prenom}_state.json")
    new = os.path.join(dst, f"{lower}_state.json")
    if os.path.exists(old):
        if os.path.exists(new):
            os.remove(new)
        os.rename(old, new)

    for f in os.listdir(dst):
        if "{prenom}" in f:
            os.remove(os.path.join(dst, f))

    print(f"   ✅ {dst} — crée")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    raw = " ".join(sys.argv[1:])
    lower, cap, upper = normalize(raw)

    print(f"\n{'=' * 60}")
    print(f"  🧬 CLONAGE TEMPLATE KLEIA-UP POUR : {cap}")
    print(f"{'=' * 60}\n")

    # 1. Cloner space/{prenom}/
    space_dst = os.path.join(ROOT, "space", lower)
    print(f"  📁 Espace privé → space/{lower}/")
    clone(SPACE_TEMPLATE, space_dst, lower, cap, upper)

    # 2. Cloner coaching_data/{prenom}/
    data_dst = os.path.join(ROOT, "coaching_data", lower)
    print(f"  📁 Données → coaching_data/{lower}/")
    clone(DATA_TEMPLATE, data_dst, lower, cap, upper)

    # 3. Générer le code secret
    code = generate_secret_code()
    print(f"\n{'=' * 60}")
    print(f"  🔑 JETON FIREBASE À CRÉER")
    print(f"{'=' * 60}")
    print(f"""
    Prénom : {cap}
    Code   : {code}
    Rôle   : client

    → Console Firebase → Firestore → access_tokens/
    → Nouveau document avec :
        ID : {code}
        owner: "{lower}"
        role: "client"

    → Transmettre à {cap} :
        Lien : https://kleia-up.fr/space/{lower}/login.html
        Code : {code}
    """)

    # 4. Instructions vidéo
    print(f"{'=' * 60}")
    print(f"  🎥 VIDÉO À PLACER")
    print(f"{'=' * 60}")
    print(f"""
    → Copier la vidéo de session dans :
        coaching_data/{lower}/{lower}_session.mp4

    → Formats supportés : MP4 (H.264/AAC) — 1920x1080 recommandé
    """)

    # 5. Résumé
    print(f"{'=' * 60}")
    print(f"  ✅ CLONAGE TERMINÉ")
    print(f"{'=' * 60}")
    print(f"""
    space/{lower}/login.html    ← Accès client
    space/{lower}/index.html    ← Dashboard client
    coaching_data/{lower}/      ← Données à remplir

    Prochaine étape : éditer {lower}_state.json
    avec les scores, l'analyse et la roadmap.
    """)

    # 6. Ouvrir dans Zed si disponible
    try:
        import subprocess

        subprocess.Popen(["zed", space_dst], shell=True)
        print("  → Ouverture dans Zed...")
    except Exception:
        pass


if __name__ == "__main__":
    main()
