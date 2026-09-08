#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kleia-article-editorial.py — Article BLOG premium kleia-up.fr depuis un brief JSON
==================================================================================
Produit un article HTML de structure EXACTE quand-la-vie-chamboule-tout
(le gabarit validé Hermes/KLEIA) à partir d'un brief éditorial rempli par
Hermes (1 génération ciblée par newsletter = token-leger) :

  meta+og+twitter complètes  |  JSON-LD @graph complet (Person / Org /
  WebSite / Breadcrumb / BlogPosting / FAQPage)  |  hero promesse+byline  |
  sommaire ancré  |  chapeau answer-first  |  L'essentiel en 30s  |
  récit  |  sections H2(id)/H3  |  À retenir  |  FAQ (alignée FAQPage)  |
  CTA contextuel  |  À lire aussi  |  author box  |  retour  |  newsletter+footer

Vous ne DEVEZ PAS reconstruire la charpente : tout le head/CSS/JSON-LD/CTA/
footer est dans ce fichier. Hermes ne fournit que le contenu (brief JSON).

Usage:
  python kleia-article-editorial.py scaffold           # retoune le schéma brief vide
  python kleia-article-editorial.py brief <fichier.json>   # assemble + maj blog/llms/sitemap

Brief (voir build EMPTY en bas).
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JOURNAL_DIR = ROOT / "journal"

MONTHS_FR = {1:"Jan",2:"Fev",3:"Mar",4:"Avr",5:"Mai",6:"Juin",
             7:"Juil",8:"Aout",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
SITE = "https://www.kleia-up.fr"

# ---------------------------------------------------------------------------
# Invariant SEE (à copier tel quel, ne pas éditer sauf modification site)
# ---------------------------------------------------------------------------
PERSON = ('{"@type": "Person", "@id": "https://kleia-up.fr/#person",'
          ' "name": "Sandrina Perrin","givenName": "Sandrina","familyName": "Perrin",'
          ' "jobTitle": "Coach Prise de Parole & Leadership pour Profils Atypiques",'
          ' "url": "https://kleia-up.fr",'
          ' "sameAs": ["https://www.linkedin.com/in/sandrina-perrin-conference-formation/",'
          ' "https://www.instagram.com/sandrina_kleia_up/"],'
          ' "worksFor": {"@id":"https://kleia-up.fr/#organization"},'
          ' "alumniOf": [{"@type":"CollegeOrProgram","name":"LiveMentor"},'
          ' {"@type":"CollegeOrProgram","name":"L\'École française"},'
          ' {"@type":"CollegeOrProgram","name":"IFEDO"},'
          ' {"@type":"CollegeOrProgram","name":"Institut Neolys"},'
          ' {"@type":"CollegeOrProgram","name":"ZenPro"},'
          ' {"@type":"CollegeOrProgram","name":"Seve Association"},'
          ' {"@type":"CollegeOrProgram","name":"IFSAM"},'
          ' {"@type":"CollegeOrProgram","name":"Enseignement supérieur"}],'
          ' "knowsAbout": ["hypersensibilité","HPI","TDAH","prise de parole",'
          ' "leadership incarné","coaching","formation"]}')
ORGANIZATION = ('{"@type": "ProfessionalService", "@id": "https://kleia-up.fr/#organization",'
                ' "name": "KLEIA-UP","description": "Coaching scénique et leadership pour entrepreneurs'
                ' hypersensibles (HPI/HSP).","url": "https://kleia-up.fr",'
                ' "logo": "https://kleia-up.fr/assets/logo_kleia.webp",'
                ' "image": "https://kleia-up.fr/assets/sandrina-presence-scenique.webp",'
                ' "address": {"@type":"PostalAddress","addressLocality":"Poiroux",'
                ' "addressRegion":"Pays de la Loire","addressCountry":"FR"},'
                ' "founder": {"@id":"https://kleia-up.fr/#person"}}')
WEBSITE = ('{"@type": "WebSite", "@id": "https://kleia-up.fr/#website",'
           ' "url": "https://kleia-up.fr", "name": "KLEIA-UP",'
           ' "description": "Incarne ton autorité naturelle.",'
           ' "publisher": {"@id":"https://kleia-up.fr/#organization"}, "inLanguage": "fr-FR"}')

GTM = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PBRNYXGCMC"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-PBRNYXGCMC');
</script>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-5RP5FZR3');</script>
<!-- End Google Tag Manager -->"""

CID_INLINE = """<meta property="og:title" content="{ogtitle}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{ogimg}">
    <meta property="og:locale" content="fr_FR">
    <meta property="article:published_time" content="{date_iso}">
    <meta property="article:author" content="Sandrina Perrin">
    <meta property="article:section" content="{category}">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{ogtitle}">
    <meta name="twitter:description" content="{desc_tw}">
    <meta name="twitter:image" content="{ogimg}">"""

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://api.fontshare.com/v2/css?f[]=ranade@300,400,500,700,800,900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400..800&display=swap" rel="stylesheet">"""

HEAD_TAIL = """</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5RP5FZR3"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
"""

NAV = """<header class="header-corp" role="banner">
<div class="container header-container">
<a href="/" class="logo"><img src="../assets/logo_kleia.webp" alt="Logo KLEIA-UP"
width="140" height="100" loading="eager"></a>
<nav role="navigation" aria-label="Menu principal">
<button class="menu-burger" aria-label="Ouvrir le menu"><span class="burger-bar"></span><span class="burger-bar"></span><span class="burger-bar"></span></button>
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
<div class="header-cta"><a href="../individuel-groupe.html#kit-urgence" class="btn btn-primary pill-shape shine-effect">REJOINDRE LE MOUVEMENT</a></div>
</div>
</header>
"""

FOOTER = """</main>
<footer role="contentinfo" style="padding: 40px 0; background-color: var(--bg-cream); text-align: center;">
<div class="container"><div class="copyright" style="font-size: 0.8rem; opacity: 0.5;">© KLEIA-UP {year}</div></div>
</footer>
<script>
const burger = document.querySelector('.menu-burger');
const nav = document.querySelector('.nav-links');
if (burger) {{ burger.addEventListener('click', () => {{ burger.classList.toggle('active'); nav.classList.toggle('active'); }}); }}
</script>
</body>
</html>"""

NEWSLETTER = """<!-- NEWSLETTER SIGNUP -->
<section id="kit-urgence" class="section-padding" style="background-color: var(--color-burgundy); color: #fff; text-align: center;">
<div class="container">
<h2 style="font-family: var(--font-title); font-size: 2.5rem; color: #fff;">Ne manque aucun déclic.</h2>
<p style="margin-bottom: 30px; opacity: 0.9;">Inscris-toi pour recevoir le Journal directement dans ta boîte mail.</p>
<a href="https://tinyurl.com/kleia-kit" class="btn btn-kit-premium" style="background-color: #fff; color: var(--color-burgundy);">JE REÇOIS LE KIT AVANTAGES</a>
</div>
</section>"""

AUTHOR = """<hr style="border: none; border-top: 1px solid rgba(139, 29, 61, 0.15); margin: 50px 0;">
<div style="display: flex; align-items: center; gap: 20px; padding: 20px 0;">
<img src="../assets/sandrina-kleia-up.webp?v=2" alt="Sandrina Perrin" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; object-position: center 20%; border: 2px solid var(--color-burgundy);">
<div>
<strong style="color: var(--color-burgundy);">Sandrina Perrin</strong><br>
<span style="font-size: 0.9rem; opacity: 0.7;">Coach en leadership incarné — Fondatrice de KLEIA-UP</span>
</div>
</div>
<div style="margin-top: 30px; font-size: 0.9rem; opacity: 0.6;">
<a href="/blog" style="color: var(--color-burgundy);">← Retour au Blog</a>
</div>"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def esc(t):  # html escape (pas double-échapper les balises qu'on gère à l'unité)
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def bold(txt):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", str(txt))


def slugify(title):
    s = re.sub(r"[éèêë]", "e", title.lower())
    s = re.sub(r"[àâä]", "a", s); s = re.sub(r"[ùûü]", "u", s)
    s = re.sub(r"[ôö]", "o", s);  s = re.sub(r"[îï]", "i", s)
    s = re.sub(r"ç", "c", s)
    s = re.sub(r"[^a-z0-9\s-]", "", s).strip()
    s = re.sub(r"\s+", "-", s)
    return s[:60].strip("-")


def date_fr(iso):
    try:
        return f"{datetime.fromisoformat(iso[:10]).day} {MONTHS_FR[datetime.fromisoformat(iso[:10]).month]} {datetime.fromisoformat(iso[:10]).year}"
    except Exception:
        return iso[:10]


# ---------------------------------------------------------------------------
# Blocs éditoriaux
# ---------------------------------------------------------------------------
def sec_class(kind):
    return {"box": "#FAF9F6", "quote": "#FAF9F6"}.get(kind, "transparent")


def render_k(r):
    k = r.get("k", "p")
    if k == "h2":
        sid = r.get("id") or slugify(r["t"])
        return (f'<h2 id="{sid}" style="font-family: var(--font-title); color: var(--color-burgundy); '
                f'margin-top: 50px; font-size: 1.6rem;">{r["t"]}</h2>')
    if k == "h3":
        return (f'<h3 style="font-family: var(--font-title); color: var(--color-burgundy); '
                f'font-size: 1.25rem; margin-top: 35px;">{r["t"]}</h3>')
    if k == "blockquote":
        return (f'<blockquote style="border-left: 4px solid var(--color-burgundy); padding: 20px 25px; '
                f'margin: 30px 0; background: #FAF9F6; border-radius: 0 8px 8px 0; '
                f'font-style: italic; font-size: 1.1rem;">{r["t"]}</blockquote>')
    if k == "box":
        title = r.get("title")
        items = r.get("items")
        if items:
            lis = "\n".join(
                f'<li><strong>{esc(it.split(":",1)[0])}:</strong> ' + esc(":".join(it.split(":")[1:]).strip() if ":" in it else it) + "</li>"
                if ":" in it else f"<li>{esc(it)}</li>"
                for it in items)
            return (f'<div style="background: #FAF9F6; border-left: 4px solid var(--color-burgundy); '
                    f'border-radius: 0 8px 8px 0; padding: 20px 25px; margin: 30px 0;">'
                    f'<strong style="font-family: var(--font-title); color: var(--color-burgundy); '
                    f'font-size: 1.05rem;">{esc(title)}</strong>'
                    f'<ul style="margin: 12px 0 0 0; padding-left: 20px;">{lis}</ul></div>')
        return (f'<div style="background: #FAF9F6; border-left: 4px solid var(--color-burgundy); '
                f'border-radius: 0 8px 8px 0; padding: 20px 25px; margin: 30px 0;">{r["t"]}</div>')
    if k == "p":
        return f"<p>{bold(r['t'])}</p>"
    return f"<p>{bold(r.get('t',''))}</p>"


def render_body(rows, faq):
    out = []
    toc = []
    for r in rows:
        if r.get("k") == "h2":
            sid = r.get("id") or slugify(r["t"])
            toc.append((sid, r["t"]))
        out.append(render_k(r))
    # FAQ
    if faq:
        qids = []
        html = ['<h2 id="faq" style="font-family: var(--font-title); color: var(--color-burgundy); '
                'margin-top: 50px; font-size: 1.6rem;">FAQ : vos questions fréquentes</h2>']
        for q in faq:
            qids.append(json.dumps(q["q"], ensure_ascii=False))
            html.append(
                f'<div style="margin-bottom: 25px; padding: 20px; background: #FAF9F6; '
                f'border-radius: 8px; border-left: 4px solid var(--color-burgundy);">'
                f'<h3 style="font-family: var(--font-title); color: var(--color-burgundy); '
                f'font-size: 1.05rem; margin: 0 0 10px 0;">{esc(q["q"])}</h3>'
                f'<p style="margin: 0;">{esc(q["a"])}</p></div>')
        out.append("\n".join(html))
        toc.append(("faq", "FAQ : vos questions fréquentes"))
    return toc, "\n".join(out)


# ---------------------------------------------------------------------------
# Assembleur principal
# ---------------------------------------------------------------------------
def assemble(br):
    slug = slugify(br.get("slug") or br["title_seo"])
    url = f"{SITE}/journal/{slug}.html"
    date_iso = br["date_iso"]
    date_fr_v = date_fr(date_iso)
    desc = br["desc"]
    category = br.get("category", "Journal du Mouvement")
    ogimg = br.get("og_image", "https://www.kleia-up.fr/assets/sandrina-presence-scenique.webp")
    title_seo = esc(br["title_seo"])
    ogtitle = f"{title_seo} | KLEIA-UP"
    person = PERSON  # static
    org = ORGANIZATION
    website = WEBSITE

    breadcrumb = ('{"@type": "BreadcrumbList", "@id": "%s/journal/%s/#breadcrumb", '
                  '"itemListElement": [{"@type":"ListItem","position":1,"name":"Accueil","item":"%s/"},'
                  '{"@type":"ListItem","position":2,"name":"Blog","item":"%s/blog.html"},'
                  '{"@type":"ListItem","position":3,"name":%s,"item":"%s"}]}' % (
                      SITE, slug, SITE, SITE, json.dumps(br["title_seo"], ensure_ascii=False), url))

    blogpost = ('{"@type": "BlogPosting", "@id": "%s#article", "headline": %s, "description": %s, '
                '"author": {"@id": "https://kleia-up.fr/#person"}, '
                '"publisher": {"@id": "https://kleia-up.fr/#organization"}, '
                '"datePublished": "%s", "image": "%s", '
                '"mainEntityOfPage": {"@type":"WebPage","@id":"%s"}}' % (
                    url, json.dumps(br["title_seo"], ensure_ascii=False),
                    json.dumps(br["desc"], ensure_ascii=False), date_iso, ogimg, url))

    faq_json = ""
    if br.get("faq"):
        faq_content = []
        for q in br["faq"]:
            faq_content.append('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
                               % (json.dumps(q["q"], ensure_ascii=False),
                                  json.dumps(q["a"], ensure_ascii=False)))
        faq_json = ',{"@type": "FAQPage", "@id": "%s#faq", "mainEntity": [%s]}' % (
            url, ",".join(faq_content))

    jsonld = (
        f'<script type="application/ld+json">\n'
        f'{{"@context": "https://schema.org",\n"@graph": [\n'
        f'  {person},\n  {org},\n  {website},\n  {breadcrumb},\n  {blogpost}{faq_json}\n'
        f']}}\n</script>'
    )

    meta = (
        f'<meta name="description" content="{esc(br["desc"])}">\n'
        f'    <meta name="keywords" content="{esc(br.get("keywords", "hypersensibilité, prise de parole, leadership, neuroatypie, KLEIA"))}">\n'
        f'    <meta name="author" content="Sandrina Perrin - KLEIA-UP">\n'
        f'    <link rel="canonical" href="{url}" />'
    )

    # corps éditorial
    toc, body_html = render_body(br.get("rows", []), br.get("faq", []))

    # sommaire
    toc_html = ""
    if toc:
        lis = "\n".join(f'<li><a href="#{sid}" style="color: var(--color-burgundy);">→ {esc(t)}</a></li>'
                        for sid, t in toc)
        toc_html = f'''<!-- SOMMAIRE -->
<section class="section-padding" style="background-color: var(--bg-cream); padding-top: 0; padding-bottom: 0;">
<div class="container" style="max-width: 720px;">
<nav aria-label="Sommaire de l\'article" style="padding: 20px 0; border-bottom: 1px solid rgba(139, 29, 61, 0.1);">
<strong style="color: var(--color-burgundy); font-family: var(--font-title);">Au sommaire</strong>
<ul style="list-style: none; padding: 10px 0 0 0; margin: 0;">{lis}</ul>
</nav></div></section>'''

    # image d'en-tête (paramétrable : br["image"] = chemin relatif depuis journal/, ex "../assets/xxx.jpg")
    _img_src = br.get("image", "../assets/sandrina-presence-scenique.webp")
    img = (f'<img src="{esc(_img_src)}" alt="{esc(br.get("image_alt", "Sandrina Perrin — KLEIA-UP"))}" '
           f'style="width: 100%; height: auto; border-radius: 8px; margin-bottom: 30px;">')

    # CTA contextuel (par défaut après le body)
    cta = ""
    if br.get("cta"):
        c = br["cta"]
        cta = (f'<p style="margin: 35px 0; text-align: center;">'
               f'<a href="{esc(c["href"])}" class="btn btn-primary pill-shape shine-effect" '
               f'style="display: inline-block;">{esc(c["label"])}</a></p>')

    # À lire aussi
    ali = ""
    if br.get("ali"):
        cards = []
        for l in br["ali"]:
            cards.append(
                f'<article style="border: 1px solid rgba(139, 29, 61, 0.1); border-radius: 8px; padding: 20px; background: #fff;">'
                f'<span style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--color-burgundy);">{esc(l.get("tag","BLOG — KLEIA"))}</span>'
                f'<h4 style="margin-top: 10px; font-size: 1rem; font-family: var(--font-title); line-height: 1.3;">'
                f'<a href="{esc(l["href"])}" style="color: inherit;">{esc(l["title"])}</a></h4>'
                f'<a href="{esc(l["href"])}" style="display: inline-block; margin-top: 15px; color: var(--color-burgundy); font-size: 0.85rem;">Lire →</a></article>')
        grid = "\n".join(cards)
        ali = (f'<h2 id="ali" style="font-family: var(--font-title); color: var(--color-burgundy); '
               f'margin-top: 50px; font-size: 1.6rem;">À lire aussi</h2>'
               f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin: 35px 0;">{grid}</div>')

    content = f"""<main role="main">
<section class="section-padding" style="padding-top: 160px; background-color: var(--bg-cream);">
<div class="container" style="max-width: 720px;">
<span class="hero-eyebrow" style="margin-bottom: 20px; display: block;">{esc(br.get("eyebrow","BLOG — JOURNAL DU MOUVEMENT"))}</span>
<h1 class="hero-title" style="text-align: left; font-size: 2.8rem;">{esc(br["h1"])}</h1>
<p class="hero-subtitle" style="text-align: left; font-size: 0.95rem; line-height: 1.5; color: var(--color-text-light);">
Par <strong>Sandrina Perrin</strong> · <span class="hero-date">{esc(br.get("byline", date_fr_v))}</span> · Catégorie : {esc(category)}
</p>
</div>
</section>
{toc_html}
<!-- ARTICLE CONTENT -->
<section class="section-padding" style="background-color: #fff;">
<div class="container" style="max-width: 720px; font-size: 1.05rem; line-height: 1.8;">
{img}
{body_html}
{cta}
{ali}
{AUTHOR}
</div></section>
{NEWSLETTER}"""

    og_block = CID_INLINE.format(ogtitle=ogtitle, desc=esc(br["desc"]), url=url,
                                 ogimg=ogimg, date_iso=date_iso, category=esc(category),
                                 desc_tw=esc(br["desc"][:118]))
    head_block = (GTM + "\n"
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"<title>{ogtitle}</title>\n"
        '<link rel="icon" type="image/png" href="../assets/images/kleia-logoV12.png">\n'
        + meta + "\n    "
        + og_block + "\n\n    "
        + FONTS + "\n"
        + '<link rel="stylesheet" href="../css/main.css?v=3.7">\n'
        + jsonld + "\n"
        + HEAD_TAIL + NAV)

    footer_block = FOOTER.replace("{year}", str(datetime.now().year))

    # head_block contient déjà <head>…</head>, <body> + noscript et le header NAV.
    html_doc = (
        "<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n"
        + head_block
        + content
        + footer_block
    )
    return html_doc, slug


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _print_schema():
    print(json.dumps({
        "title_seo": "Titre SEO (<60 car., porte l'intention de recherche)",
        "slug": "URL slug (sinon dérivé)",
        "h1": "Titre visible H1 (promesse actionnable, peut différer du title)",
        "desc": "Meta description (~150 car., sans charabia)",
        "date_iso": "AAAA-MM-JJ",
        "eyebrow": "BLOG — <catégorie>",
        "byline": "Par Sandrina Perrin (optionnel date statique)",
        "category": "ex Hyperstress & Neuroatypie",
        "og_image": "URL partagée (sinon image d'en-tête ou sandrina-par défaut)",
        "image": "chemin relatif depuis journal/ de l image d en-tête (sinon sandrina-presence-scenique.webp)",
        "image_alt": "texte alternatif image d'en-tête",
        "keywords": "mots-clés (optionnel)",
        "rows": [
            {"k":"p","t":"**Chapeau answer-first** ... (1er mot = OUI/oui, réponse + bénéfice)"},
            {"k":"box","title":"L'essentiel en 30 secondes","items":["Point fort : détail", "..."]},
            {"k":"p","t":"récit authentique court Sandrina..."},
            {"k":"blockquote","t":"citation marquante"},
            {"k":"h2","id":"...","t":"Titre section réponse (1. ...)"},
            {"k":"h3","t":"Sous-point : question/action autonome"},
            {"k":"p","t":"texte + **phrase-clé en gras**"}
        ],
        "faq": [{"q":"Question fréquente","a":"Réponse alignée mot à mot dans FAQPage"}],
        "cta": {"label":"JE DÉCOUVRE LES ACCOMPAGNEMENTS","href":"/individuel-groupe"},
        "ali": [{"title":"Article lié réel","href":"/journal/slug.html","tag":"À LIRE AUSSI"}]
    }, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description="Générateur d'article premium KLEIA")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scaffold", help="affiche le schéma de brief JSON à remplir")
    p = sub.add_parser("brief", help="génère l'article depuis un fichier brief JSON")
    p.add_argument("brief")
    args = ap.parse_args()

    if args.cmd == "scaffold":
        _print_schema()
        return
    br = json.loads(Path(args.brief).read_text(encoding="utf-8"))
    html, slug = assemble(br)
    out = JOURNAL_DIR / f"{slug}.html"
    out.write_text(html, encoding="utf-8")
    print(f"✅ article créé : journal/{slug}.html")
    print("⚠️  Vous devez maintenant : (1) valider le rendu, "
          "(2) exécuter publish-blog-article.py sitemap (ou ajouter la carte sur blog.html "
          "et l'entrée llms.txt via la main du pipeline).")


if __name__ == "__main__":
    main()
