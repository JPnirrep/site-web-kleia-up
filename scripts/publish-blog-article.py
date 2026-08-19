#!/usr/bin/env python3
"""
Publish Blog Article — KLEIA-UP
================================
Pipeline : Newsletter Brevo → Article HTML blog → Update blog.html + llms.txt

Usage:
    python scripts/publish-blog-article.py <campaign_id>
    python scripts/publish-blog-article.py list          # Lister les newsletters récentes non bloguées
    python scripts/publish-blog-article.py status        # État du gap actuel

Prérequis :
    - Clé API Brevo dans php/config.php (lue automatiquement)
    - Exécuté depuis la racine de site-web-kleia-up/
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from html import escape

# --- Config ---
ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "php" / "config.php"
JOURNAL_DIR = ROOT / "journal"
BLOG_FILE = ROOT / "blog.html"
LLMS_FILE = ROOT / "llms.txt"

MONTHS_FR = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Avr", 5: "Mai", 6: "Juin",
    7: "Juil", 8: "Aout", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

# --- Helpers ---

def get_brevo_key():
    """Extract Brevo API key from PHP config."""
    text = CONFIG_FILE.read_text(encoding="utf-8")
    m = re.search(r"'brevo_api_key'\s*=>\s*'([^']+)'", text)
    if not m:
        sys.exit("ERROR: Brevo API key not found in php/config.php")
    return m.group(1)

def get_telegram_config():
    """Extract Telegram bot token and chat ID from PHP config."""
    text = CONFIG_FILE.read_text(encoding="utf-8")
    token = re.search(r"'telegram_bot_token'\s*=>\s*'([^']+)'", text)
    chat_id = re.search(r"'telegram_chat_id'\s*=>\s*'([^']+)'", text)
    if not token or not chat_id:
        return None, None
    return token.group(1), chat_id.group(1)

def send_telegram(message):
    """Send a Telegram message via bot API. Silent fail if config missing."""
    token, chat_id = get_telegram_config()
    if not token or not chat_id:
        return False
    try:
        import urllib.parse
        data = urllib.parse.urlencode({
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': 'true'
        }).encode()
        req = Request(f"https://api.telegram.org/bot{token}/sendMessage", data=data)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urlopen(req, timeout=10):
            pass
        return True
    except Exception as e:
        print(f"  ⚠️ Telegram notification failed: {e}")
        return False


def brevo_get(api_key, path):
    """Call Brevo API GET."""
    req = Request(f"https://api.brevo.com/v3/{path}")
    req.add_header("api-key", api_key)
    req.add_header("Accept", "application/json")
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def date_fr(iso_date):
    """Convert 2026-07-17 → '17 Juil 2026'."""
    dt = datetime.fromisoformat(iso_date[:10])
    return f"{dt.day} {MONTHS_FR[dt.month]} {dt.year}"


def slugify(text):
    """Generate URL slug from title."""
    s = text.lower()
    s = re.sub(r'[éèêë]', 'e', s)
    s = re.sub(r'[àâä]', 'a', s)
    s = re.sub(r'[ùûü]', 'u', s)
    s = re.sub(r'[ôö]', 'o', s)
    s = re.sub(r'[îï]', 'i', s)
    s = re.sub(r'[ç]', 'c', s)
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s[:60]


def extract_newsletter_text(html_content):
    """Extract readable text from Brevo email HTML."""
    # Remove head, style, script
    text = re.sub(r'<head>.*?</head>', '', html_content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    
    # Replace <br> with newlines
    text = re.sub(r'<br\s*/?>', '\n', text)
    
    # Replace block tags with newlines
    text = re.sub(r'</?(?:p|div|tr|td|li|h[1-6]|blockquote|section|table)[^>]*>', '\n', text)
    
    # Decode HTML entities
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    
    # Remove remaining tags and clean
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()
    
    # Take first 2000 chars as article body (newsletter intro)
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    return paragraphs


def generate_article_html(campaign, newsletter_paragraphs):
    """Generate full blog article HTML."""
    title = campaign['name'].replace('Mouvement Kleia-up', '').strip()
    subject = campaign.get('subject', title)
    sent_date = campaign['sentDate'][:10]
    sent_iso = sent_date
    sent_fr = date_fr(sent_date)

    url_slug = slugify(title)

    # Build description (first non-empty paragraph)
    desc = ""
    for p in newsletter_paragraphs:
        clean = re.sub(r'[«»""]', '', p).strip()
        if len(clean) > 30:
            desc = clean[:150]
            break
    if not desc:
        desc = subject[:150]

    keywords = "leadership, prise de parole, hypersensibilité, affirmation de soi, "
    keywords += ", ".join(title.lower().split()[:5])

    # Build body paragraphs
    body_html = []
    for p in newsletter_paragraphs[:15]:  # Limit to 15 paragraphs
        if len(p) < 15:
            continue
        body_html.append(f'                <p>{escape(p)}</p>')

    # Articles similaires (placeholder)
    similar_html = """
                    <article style="border: 1px solid rgba(139, 29, 61, 0.1); border-radius: 8px; padding: 20px; background: #fff;">
                        <span style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--color-burgundy);">DATE</span>
                        <h4 style="margin-top: 10px; font-size: 1rem; font-family: var(--font-title); line-height: 1.3;">TITRE</h4>
                        <a href="/journal/SLUG" style="display: inline-block; margin-top: 15px; color: var(--color-burgundy); font-size: 0.85rem;">Lire →</a>
                    </article>
"""
    html = f"""<!DOCTYPE html>
<html lang="fr">

<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PBRNYXGCMC"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-PBRNYXGCMC');
</script>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-5RP5FZR3');</script>
<!-- End Google Tag Manager -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)} | KLEIA-UP</title>
    <link rel="icon" type="image/png" href="../assets/images/kleia-logoV12.png">

    <meta name="description" content="{escape(desc)}">
    <meta name="keywords" content="{escape(keywords)}">
    <meta name="author" content="Sandrina Perrin - KLEIA-UP">
    <link rel="canonical" href="https://www.kleia-up.fr/journal/{url_slug}.html" />

    <!-- Open Graph -->
    <meta property="og:title" content="{escape(title)} | KLEIA-UP">
    <meta property="og:description" content="{escape(desc)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://www.kleia-up.fr/journal/{url_slug}.html">
    <meta property="og:image" content="https://www.kleia-up.fr/assets/sandrina-presence-scenique.webp">
    <meta property="og:locale" content="fr_FR">
    <meta property="article:published_time" content="{sent_iso}">
    <meta property="article:author" content="Sandrina Perrin">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape(title)} | KLEIA-UP">
    <meta name="twitter:description" content="{escape(desc[:120])}">
    <meta name="twitter:image" content="https://www.kleia-up.fr/assets/sandrina-presence-scenique.webp">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://api.fontshare.com/v2/css?f[]=ranade@300,400,500,700,800,900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400..800&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="../css/main.css?v=3.7">

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@graph": [
        {{ "@type": "Person", "@id": "https://kleia-up.fr/#person", "name": "Sandrina Perrin", "givenName": "Sandrina", "familyName": "Perrin", "jobTitle": "Coach Prise de Parole & Leadership pour Profils Atypiques", "url": "https://kleia-up.fr", "sameAs": ["https://www.linkedin.com/in/sandrina-perrin-conference-formation/","https://www.instagram.com/sandrina_kleia_up/"], "worksFor": {{"@id":"https://kleia-up.fr/#organization"}}, "alumniOf": [{{"@type":"CollegeOrProgram","name":"LiveMentor"}},{{"@type":"CollegeOrProgram","name":"L'École française"}},{{"@type":"CollegeOrProgram","name":"IFEDO"}},{{"@type":"CollegeOrProgram","name":"Institut Neolys"}},{{"@type":"CollegeOrProgram","name":"ZenPro"}},{{"@type":"CollegeOrProgram","name":"Seve Association"}},{{"@type":"CollegeOrProgram","name":"Université de Caroline du Nord"}},{{"@type":"CollegeOrProgram","name":"Unow"}}], "hasCredential": [{{"@type":"EducationalOccupationalCredential","name":"Prise de parole en public","credentialCategory":"certification","recognizedBy":{{"@type":"Organization","name":"LiveMentor","url":"https://www.livementor.com"}}}},{{"@type":"EducationalOccupationalCredential","name":"Cohérence cardiaque","credentialCategory":"certification","recognizedBy":{{"@type":"Organization","name":"IFEDO"}}}},{{"@type":"EducationalOccupationalCredential","name":"Relaxologue","credentialCategory":"certification","recognizedBy":{{"@type":"Organization","name":"Neolys"}}}},{{"@type":"EducationalOccupationalCredential","name":"Analyse transactionnelle","credentialCategory":"certification","recognizedBy":{{"@type":"Organization","name":"ZenPro"}}}},{{"@type":"EducationalOccupationalCredential","name":"Positive Psychology","credentialCategory":"certification","recognizedBy":{{"@type":"Organization","name":"Coursera"}}}},{{"@type":"EducationalOccupationalCredential","name":"Animatrice ateliers attention","credentialCategory":"certification","recognizedBy":{{"@type":"Organization","name":"Fondation SEVE"}}}},{{"@type":"EducationalOccupationalCredential","name":"Entreprise Agile","credentialCategory":"certification","recognizedBy":{{"@type":"Organization","name":"Unow"}}}}], "knowsAbout": ["Prise de parole en public","Leadership organique","Psychologie positive","Hypersensibilité HPI/HSP","Affirmation de soi","Cohérence cardiaque","Analyse transactionnelle","Rigologie","Communication non-violente","Management HPS"] }},
        {{ "@type": "ProfessionalService", "@id": "https://kleia-up.fr/#organization", "name": "KLEIA-UP", "description": "Coaching scénique et leadership pour entrepreneurs hypersensibles (HPI/HSP).", "url": "https://kleia-up.fr", "logo": "https://kleia-up.fr/assets/logo_kleia.webp", "image": "https://kleia-up.fr/assets/sandrina-presence-scenique.webp", "address": {{"@type":"PostalAddress","addressLocality":"Poiroux","addressRegion":"Pays de la Loire","addressCountry":"FR"}}, "founder": {{"@id":"https://kleia-up.fr/#person"}} }},
        {{ "@type": "WebSite", "@id": "https://kleia-up.fr/#website", "url": "https://kleia-up.fr", "name": "KLEIA-UP", "description": "Incarne ton autorité naturelle.", "publisher": {{"@id":"https://kleia-up.fr/#organization"}}, "inLanguage": "fr-FR" }},
        {{ "@type": "BreadcrumbList", "@id": "https://kleia-up.fr/journal/{url_slug}/#breadcrumb", "itemListElement": [{{"@type":"ListItem","position":1,"name":"Accueil","item":"https://kleia-up.fr/"}},{{"@type":"ListItem","position":2,"name":"Blog","item":"https://kleia-up.fr/blog.html"}},{{"@type":"ListItem","position":3,"name":"{escape(title)}","item":"https://kleia-up.fr/journal/{url_slug}.html"}}] }},
        {{
          "@type": "BlogPosting",
          "@id": "https://kleia-up.fr/journal/{url_slug}.html#article",
          "headline": "{escape(title)}",
          "description": "{escape(desc)}",
          "datePublished": "{sent_iso}",
          "author": {{ "@id": "https://kleia-up.fr/#person" }},
          "publisher": {{ "@id": "https://kleia-up.fr/#organization" }},
          "image": "https://www.kleia-up.fr/assets/sandrina-presence-scenique.webp",
          "mainEntityOfPage": {{ "@type": "WebPage", "@id": "https://kleia-up.fr/journal/{url_slug}.html" }},
          "articleBody": "ARTICLE_BODY_PLACEHOLDER"
        }}
      ]
    }}
    </script>
</head>

<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5RP5FZR3"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

    <header class="header-corp" role="banner">
        <div class="container header-container">
            <a href="/" class="logo">
                <img src="../assets/logo_kleia.webp" alt="Logo KLEIA-UP"
                    width="140" height="100" loading="eager">
            </a>

            <nav role="navigation" aria-label="Menu principal">
                <button class="menu-burger" aria-label="Ouvrir le menu">
                    <span class="burger-bar"></span>
                    <span class="burger-bar"></span>
                    <span class="burger-bar"></span>
                </button>

                <ul class="nav-links">
                    <li><a href="/" class="nav-link">ACCUEIL</a></li>
                    <li class="nav-separator">|</li>
                    <li><a href="/individuel-groupe" class="nav-link">POUR TOI</a></li>
                    <li><a href="/entreprises" class="nav-link">L'ENTREPRISE</a></li>
                    <li class="nav-separator">|</li>
                    <li><a href="/manifeste" class="nav-link">MANIFESTE</a></li>
                    <li><a href="/programmes" class="nav-link">PROGRAMMES</a></li>
                    <li><a href="/blog" class="nav-link active">BLOG</a></li>
                    <li><a href="/contact" class="nav-link">CONTACT</a></li>
                </ul>
            </nav>

            <div class="header-cta">
                <a href="../individuel-groupe.html#kit-urgence" class="btn btn-primary pill-shape shine-effect">
                    REJOINDRE LE MOUVEMENT
                </a>
            </div>
        </div>
    </header>

    <main role="main">

        <!-- HERO ARTICLE -->
        <section class="section-padding" style="padding-top: 160px; background-color: var(--bg-cream);">
            <div class="container" style="max-width: 720px;">
                <span class="hero-eyebrow" style="margin-bottom: 20px; display: block;">BLOG — {sent_fr.upper()}</span>
                <h1 class="hero-title" style="text-align: left; font-size: 2.8rem;">{escape(title)}</h1>
                <p class="hero-subtitle" style="text-align: left; font-size: 1.1rem; line-height: 1.7; margin-top: 20px; color: var(--color-text-light);">
                    Par <strong>Sandrina Perrin</strong> — Fondatrice de KLEIA-UP, coach en leadership incarné
                </p>
            </div>
        </section>

        <!-- ARTICLE CONTENT -->
        <section class="section-padding" style="background-color: #fff;">
            <div class="container" style="max-width: 720px; font-size: 1.05rem; line-height: 1.8;">

{chr(10).join(body_html)}

                <hr style="border: none; border-top: 1px solid rgba(139, 29, 61, 0.15); margin: 50px 0;">

                <div style="display: flex; align-items: center; gap: 20px; padding: 20px 0;">
                    <img src="../assets/sandrina-kleia-up.webp?v=2" alt="Sandrina Perrin" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; object-position: center 20%; border: 2px solid var(--color-burgundy);">
                    <div>
                        <strong style="color: var(--color-burgundy);">Sandrina Perrin</strong><br>
                        <span style="font-size: 0.9rem; opacity: 0.7;">Coach en leadership incarné — Fondatrice de KLEIA-UP</span>
                    </div>
                </div>

                <div style="margin-top: 30px; font-size: 0.9rem; opacity: 0.6;">
                    <a href="/blog" style="color: var(--color-burgundy);">← Retour au Blog</a>
                </div>

            </div>
        </section>

        <!-- NEWSLETTER SIGNUP -->
        <section id="kit-urgence" class="section-padding" style="background-color: var(--color-burgundy); color: #fff; text-align: center;">
            <div class="container">
                <h2 style="font-family: var(--font-title); font-size: 2.5rem; color: #fff;">Ne manque aucun déclic.</h2>
                <p style="margin-bottom: 30px; opacity: 0.9;">Inscris-toi pour recevoir le Journal directement dans ta boîte mail.</p>
                <a href="https://tinyurl.com/kleia-kit" class="btn btn-kit-premium" style="background-color: #fff; color: var(--color-burgundy);">JE REJOINS LE MOUVEMENT</a>
            </div>
        </section>
    </main>
    <footer role="contentinfo" style="padding: 40px 0; background-color: var(--bg-cream); text-align: center;">
        <div class="container">
            <div class="copyright" style="font-size: 0.8rem; opacity: 0.5;">
                © KLEIA-UP 2026
            </div>
        </div>
    </footer>

    <script>
        const burger = document.querySelector('.menu-burger');
        const nav = document.querySelector('.nav-links');
        if (burger) {{
            burger.addEventListener('click', () => {{
                burger.classList.toggle('active');
                nav.classList.toggle('active');
            }});
        }}
    </script>
</body>

</html>
"""
    return html, url_slug, title, sent_fr, desc


def update_blog_html(campaign, url_slug, title, sent_fr):
    """Add new article card at top of blog.html grid."""
    content = BLOG_FILE.read_text(encoding="utf-8")
    
    # Extract short desc from campaign
    subject = campaign.get('subject', '')
    short_desc = subject[:120] if subject else "Découvre mes dernières réflexions."
    
    card = f"""                    <!-- NOUVEAU -->
                    <article class="blog-post-card" style="border: 1px solid rgba(139, 29, 61, 0.1); border-radius: 8px; overflow: hidden; transition: transform 0.3s ease;">
                        <div class="post-content" style="padding: 30px;">
                            <span class="post-date" style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: var(--color-burgundy);">{sent_fr}</span>
                            <h3 style="margin-top: 15px; font-family: var(--font-title); color: var(--color-burgundy);">{title}</h3>
                            <p style="margin: 20px 0; font-size: 1rem; line-height: 1.6;">{escape(short_desc)}</p>
                            <a href="journal/{url_slug}" class="btn btn-subtle">Lire la suite →</a>
                        </div>
                    </article>
"""
    
    # Insert after <!-- ARTICLES LIST --> ... <div class="blog-grid"...>
    insert_point = '                <div class="blog-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 40px;">\n'
    idx = content.find(insert_point)
    if idx == -1:
        print("WARNING: Could not find blog-grid insertion point in blog.html")
        return False
    
    idx += len(insert_point)
    new_content = content[:idx] + '\n' + card + content[idx:]
    
    # Renumber existing comments <!-- N --> → <!-- N+1 -->
    def renumber(m):
        n = int(m.group(1))
        return f'<!-- {n + 1} -->'
    new_content = re.sub(r'<!-- (\d+) -->', renumber, new_content)
    
    BLOG_FILE.write_text(new_content, encoding="utf-8")
    print(f"✅ blog.html — card added for '{title}'")
    return True


def update_llms(title, url_slug, sent_fr, desc):
    """Add article entry to llms.txt."""
    content = LLMS_FILE.read_text(encoding="utf-8")
    
    entry = f"\n- [{escape(title)}](https://kleia-up.fr/journal/{url_slug}.html) — {sent_fr}. {escape(desc[:120])}"
    
    # Insert after "## Journal du Mouvement" section
    marker = "## Journal du Mouvement"
    idx = content.find(marker)
    if idx == -1:
        print("WARNING: Could not find Journal section in llms.txt")
        return False
    
    # Find the first article line after the header and insert before it
    section_start = idx + len(marker)
    next_article = content.find("\n- [", section_start)
    if next_article == -1:
        content += entry
    else:
        content = content[:next_article] + entry + content[next_article:]
    
    # Update article count in header
    article_count = len(re.findall(r'- \[.*?\]\(https://kleia-up.fr/journal/', content))
    content = re.sub(r'\((\d+) articles?\)', f'({article_count} articles)', content)
    
    LLMS_FILE.write_text(content, encoding="utf-8")
    print(f"✅ llms.txt — entry added (#{article_count} articles)")
    return True


def cmd_list(api_key):
    """List recent newsletters not yet on blog."""
    data = brevo_get(api_key, "emailCampaigns?status=sent&limit=50")
    campaigns = sorted(data.get('campaigns', []), key=lambda c: c.get('sentDate', ''), reverse=True)
    
    # Get existing article slugs
    existing_slugs = set()
    for f in JOURNAL_DIR.glob("*.html"):
        existing_slugs.add(f.stem)
    
    print("\n=== Newsletters récentes NON bloguées ===\n")
    count = 0
    for c in campaigns:
        name = c['name'].replace('Mouvement Kleia-up', '').strip()
        slug = slugify(name)
        sent = c['sentDate'][:10]
        if slug in existing_slugs or not name:
            continue
        if name.startswith('Prendre sa place sans forcer'):
            continue  # Skip event operational emails
        count += 1
        print(f"  #{c['id']:>4}  {sent}  {name[:60]}")
        print(f"         Objet: {c.get('subject','')[:80]}")
        print()
    
    print(f"Total: {count} newsletters à bloguer")
    print(f"Dernier article blog: 26 Juin 2026")
    print()
    print("Usage: python scripts/publish-blog-article.py <campaign_id>")


def cmd_status(api_key):
    """Show current gap status."""
    cmd_list(api_key)


def cmd_publish(api_key, campaign_id):
    """Publish a newsletter as blog article."""
    data = brevo_get(api_key, f"emailCampaigns/{campaign_id}")
    
    name = data['name'].replace('Mouvement Kleia-up', '').strip()
    if not name:
        sys.exit("ERROR: Empty campaign name")
    
    html_content = data.get('htmlContent', '')
    paragraphs = extract_newsletter_text(html_content)
    
    if len(paragraphs) < 3:
        sys.exit("ERROR: Not enough content extracted from newsletter")
    
    # Generate article
    article_html, url_slug, title, sent_fr, desc = generate_article_html(data, paragraphs)
    
    # Write article file
    article_file = JOURNAL_DIR / f"{url_slug}.html"
    if article_file.exists():
        print(f"⚠️  Article exists: {article_file.name}")
        resp = input("Overwrite? (y/N): ")
        if resp.lower() != 'y':
            print("Aborted.")
            return
    
    article_file.write_text(article_html, encoding="utf-8")
    print(f"✅ Created: journal/{url_slug}.html")
    
    # Update blog.html
    update_blog_html(data, url_slug, title, sent_fr)
    
    # Update llms.txt
    update_llms(title, url_slug, sent_fr, desc)
    
    print(f"\n📝 ARTICLE PUBLIÉ : {title}")
    print(f"   URL: https://www.kleia-up.fr/journal/{url_slug}")

    # Telegram notification
    msg = (
        f"✅ <b>Blog KLEIA-UP</b> — Article publié\n\n"
        f"📰 <b>{title}</b>\n"
        f"📅 {sent_fr}\n"
        f"🔗 kleia-up.fr/journal/{url_slug}"
    )
    if send_telegram(msg):
        print(f"   📱 Notification Telegram envoyée")


    # Cleanup pending flag
    gap_flag = ROOT / ".gap-pending"
    if gap_flag.exists():
        gap_flag.unlink()
        print(f"   🏁 Flag .gap-pending supprimé")

# --- Main ---

if __name__ == "__main__":
    os.chdir(ROOT)
    
    if not CONFIG_FILE.exists():
        sys.exit(f"ERROR: Config file not found at {CONFIG_FILE}")
    
    api_key = get_brevo_key()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/publish-blog-article.py list          # Lister les newsletters non bloguées")
        print("  python scripts/publish-blog-article.py status        # État du gap")
        print("  python scripts/publish-blog-article.py <campaign_id> # Publier une newsletter")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        cmd_list(api_key)
    elif cmd == "status":
        cmd_status(api_key)
    else:
        try:
            campaign_id = int(cmd)
        except ValueError:
            sys.exit(f"ERROR: Invalid campaign ID: {cmd}")
        cmd_publish(api_key, campaign_id)
