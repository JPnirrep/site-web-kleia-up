#!/usr/bin/env python3
"""
GSC Sync — kleia-up.fr
======================
Automatisation Google Search Console via API (OAuth Desktop, stdlib uniquement).

Commandes:
    python scripts/gsc.py auth                  # 1er run : consentement OAuth (navigateur)
    python scripts/gsc.py sitemap-status        # état du sitemap chez Google
    python scripts/gsc.py submit-sitemap        # (re)soumettre sitemap.xml
    python scripts/gsc.py inspect --all         # inspection des URLs du sitemap local
    python scripts/gsc.py inspect <url> [...]   # inspection ciblée
    python scripts/gsc.py report [--days 90]    # impressions/clics/position (par jour)

Config locale (GITIGNORÉE) — scripts/gsc-local.json:
    {"client_secret": "<chemin absolu client_secret_*.json>",
     "token": "<chemin du token> (défaut: à côté du client_secret)"}
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
SITEMAP = os.path.join(ROOT, "sitemap.xml")
LOCAL_CONFIG = os.path.join(SCRIPT_DIR, "gsc-local.json")

SCOPE = "https://www.googleapis.com/auth/webmasters"
REDIRECT_URI = "http://localhost"
SITE = "https://www.kleia-up.fr/"  # surchargeable dans gsc-local.json ("site")
AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
GSC_BASE = "https://www.googleapis.com/webmasters/v3/sites/"
INSPECT_URL = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"

# Libellés GSC FR pour les coverageState de l'API URL Inspection
COVERAGE_FR = {
    "InIndex": "Dans l'index",
    "NotInIndex": "Non inclus dans l'index",
    "PageWithRedirect": "Page avec redirection",
    "NotFound": "Introuvable (404)",
    "CrawledCurrentlyNotIndexed": "Détectée, actuellement non indexée",
    "DiscoveredCrawlScheduled": "Découverte, crawl programmé",
    "DuplicateWithoutUserSelectedCanonical": "Doublon, sans canonical choisi",
    "DuplicateGoogleChosenCanonical": "Doublon, Google a choisi un autre canonical",
    "BlockedByRobotsTxt": "Bloquée par robots.txt",
    "Soft404": "Soft 404",
    "URLIsUnknownRobotsFile": "URL pointant vers un robots.txt inconnu",
}


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_local():
    if not os.path.exists(LOCAL_CONFIG):
        die(f"Config locale absente: {LOCAL_CONFIG} (créer avec client_secret/token)")
    with open(LOCAL_CONFIG, encoding="utf-8") as f:
        return json.load(f)


def get_client_secret():
    cfg = load_local()
    path = cfg.get("client_secret")
    if not path or not os.path.exists(path):
        die(f"client_secret introuvable: {path}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["installed"]


def get_token_path():
    cfg = load_local()
    if cfg.get("token"):
        return cfg["token"]
    cs = cfg.get("client_secret", "")
    return os.path.join(os.path.dirname(cs), "gsc-token.json")


def load_token():
    p = get_token_path()
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save_token(token):
    p = get_token_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(token, f, indent=2)
    print(f"✅ Token sauvegardé: {p}")


def post_form(url, fields):
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        die(f"HTTP {e.code} sur {url}: {body[:500]}")


def refresh_token(client, token):
    fields = {
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "refresh_token": token["refresh_token"],
        "grant_type": "refresh_token",
    }
    new = post_form(TOKEN_URL, fields)
    token["access_token"] = new["access_token"]
    token["expires_at"] = time.time() + new.get("expires_in", 3600) - 60
    save_token(token)
    return token


def access_token():
    client = get_client_secret()
    token = load_token()
    if not token:
        die("Pas de token — lancer d'abord: python scripts/gsc.py auth")
    if token.get("expires_at", 0) < time.time():
        token = refresh_token(client, token)
    return token["access_token"]


def api(method, url, body=None):
    token = access_token()
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body_err = e.read().decode(errors="replace")
        die(f"API GSC HTTP {e.code}: {body_err[:600]}")


def site_url():
    cfg = load_local()
    return cfg.get("site", SITE)


def site_url_encoded():
    return urllib.parse.quote(site_url(), safe="")


# ---------------------------------------------------------------- auth
def cmd_auth():
    client = get_client_secret()
    params = {
        "client_id": client["client_id"],
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_link = AUTH_URL + "?" + urllib.parse.urlencode(params)
    code = None

    # Tente de capturer le code via serveur localhost:80 (redirect http://localhost)
    try:
        import http.server
        import threading

        captured = {}

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                if "code" in qs:
                    captured["code"] = qs["code"][0]
                    payload = "<html><body><h2>OK — tu peux fermer cette fenêtre.</h2></body></html>".encode("utf-8")
                else:
                    payload = "<html><body><h2>Paramètre manquant.</h2></body></html>".encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *a):
                pass

        srv = http.server.HTTPServer(("127.0.0.1", 80), Handler)
        timer = threading.Timer(240, srv.shutdown)
        timer.start()
        print("🌐 Ouvre ton navigateur pour autoriser l'accès Search Console")
        print(f"   URL: {auth_link}")
        try:
            import webbrowser
            webbrowser.open(auth_link)
        except Exception:
            pass
        srv.handle_request()  # bloque jusqu'au callback
        timer.cancel()
        code = captured.get("code")
    except OSError:
        # Port 80 occupé → mode manuel
        print("⚠️  Serveur localhost:80 indisponible → mode manuel")
        print(f"1. Ouvre cette URL dans ton navigateur (compte sandrina@kleia-up.fr):")
        print(f"   {auth_link}")
        print("2. Après autorisation, copie le paramètre 'code' de l'URL affichée")
        code = input("Code: ").strip()

    if not code:
        die("Aucun code reçu")

    fields = {
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token = post_form(TOKEN_URL, fields)
    token["expires_at"] = time.time() + token.get("expires_in", 3600) - 60
    save_token(token)
    print("✅ Authentification OK")


# ---------------------------------------------------------------- sitemap
def cmd_sitemap_status():
    entries = api("GET", f"{GSC_BASE}{site_url_encoded()}/sitemaps").get("sitemap", [])
    if not entries:
        print("Aucun sitemap soumis.")
        return
    for e in entries:
        print(f"- {e['path']}")
        print(f"    soumis: {e.get('lastSubmitted', '?')} | téléchargé: {e.get('lastDownloaded', '?')}")
        print(f"    errors: {e.get('errors', 0)} | warnings: {e.get('warnings', 0)} | isPending: {e.get('isPending')}")


def cmd_submit_sitemap():
    feed = urllib.parse.urljoin(site_url(), "sitemap.xml")
    url = f"{GSC_BASE}{site_url_encoded()}/sitemaps/{urllib.parse.quote(feed, safe='')}"
    api("PUT", url)
    print(f"✅ Sitemap soumis: {feed}")
    cmd_sitemap_status()


# ---------------------------------------------------------------- inspection
def cmd_inspect(urls):
    results = []
    for u in urls:
        res = api("POST", INSPECT_URL, {"inspectionUrl": u, "siteUrl": site_url()})
        ir = res.get("inspectionResult", {})
        ist = ir.get("indexStatusResult", {})
        coverage = ist.get("coverageState", "?")
        label = COVERAGE_FR.get(coverage, coverage)
        results.append((u, label, ist.get("indexingState", "?"), ir.get("pageFetchState", "?")))
        time.sleep(0.4)
    for u, label, idx, fetch in results:
        print(f"{label:42s} | idx={idx:18s} | fetch={fetch:12s} | {u}")
    from collections import Counter
    print("\nRésumé:")
    for label, n in Counter(r[1] for r in results).most_common():
        print(f"  {n:3d} × {label}")


def cmd_inspect_all():
    if not os.path.exists(SITEMAP):
        die(f"sitemap.xml absent: {SITEMAP}")
    with open(SITEMAP, encoding="utf-8") as f:
        content = f.read()
    urls = [part.split("</loc>")[0] for part in content.split("<loc>")[1:]]
    print(f"Inspection de {len(urls)} URLs (≈{len(urls) * 0.4:.0f}s + quota API)...")
    cmd_inspect(urls)


# ---------------------------------------------------------------- analytics
def cmd_report(days):
    end = time.strftime("%Y-%m-%d")
    start = time.strftime("%Y-%m-%d", time.localtime(time.time() - days * 86400))
    body = {
        "startDate": start,
        "endDate": end,
        "dimensions": ["date"],
    }
    res = api("POST", f"{GSC_BASE}{site_url_encoded()}/searchAnalytics/query", body)
    rows = res.get("rows", [])
    if not rows:
        print("Aucune donnée sur la période.")
        return
    total_c = sum(r["clicks"] for r in rows)
    total_i = sum(r["impressions"] for r in rows)
    print(f"Période {start} → {end} | clics: {total_c} | impressions: {total_i}")
    print(f"{'Date':12s} {'Clics':>6s} {'Impr.':>8s} {'CTR':>6s} {'Pos.':>6s}")
    for r in sorted(rows, key=lambda x: x["keys"][0]):
        print(f"{r['keys'][0]:12s} {r['clicks']:6d} {r['impressions']:8d} {r['ctr']:6.1%} {r['position']:6.1f}")


# ---------------------------------------------------------------- main
def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    cmd = args[0]

    if cmd == "auth":
        cmd_auth()
    elif cmd == "sitemap-status":
        cmd_sitemap_status()
    elif cmd == "submit-sitemap":
        cmd_submit_sitemap()
    elif cmd == "inspect":
        if "--all" in args:
            cmd_inspect_all()
        elif len(args) > 1:
            cmd_inspect(args[1:])
        else:
            print("usage: gsc.py inspect --all | <url> [...]")
    elif cmd == "report":
        days = 90
        if "--days" in args:
            i = args.index("--days")
            try:
                days = int(args[i + 1])
            except (IndexError, ValueError):
                pass
        cmd_report(days)
    else:
        print(f"Commande inconnue: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
