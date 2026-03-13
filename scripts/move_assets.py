import shutil
import os

files = [
    (r"C:\Users\JP\.gemini\antigravity\brain\d75f15c4-a641-4415-875c-f502e7272d92\k_incarnation_premium_1773420239005.png", "incarnation.png"),
    (r"C:\Users\JP\.gemini\antigravity\brain\d75f15c4-a641-4415-875c-f502e7272d92\k_enterprise_premium_1773420252897.png", "entreprise.png"),
    (r"C:\Users\JP\.gemini\antigravity\brain\d75f15c4-a641-4415-875c-f502e7272d92\k_leadership_auric_1773420268497.png", "conference.png")
]

dest_dir = r"c:\Users\JP\Documents\GitHub\site-web-kleia-up\assets\programmes"
os.makedirs(dest_dir, exist_ok=True)

for src, name in files:
    try:
        shutil.copy(src, os.path.join(dest_dir, name))
        print(f"Copied {name}")
    except Exception as e:
        print(f"Error copying {name}: {e}")
