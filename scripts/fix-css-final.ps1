$path = "css/main.css"
$content = Get-Content -Path $path -Raw
# Handle the strange character spacing in the garbage if present
$content = $content -split "/ \*   D E B U G"[0]

# Replacement for the top block
$oldTop = 'html,
body {
    width: 100%;
    max-width: 100vw;
    /* Force la limite à la largeur de la fenêtre */
    overflow-x: hidden !important;
    /* INTERDIT tout dépassement horizontal */
    position: relative;
    /* Ancre la page */
    margin: 0;
    padding: 0;
}'

$newTop = '/* 1. Verrouillage du scroll horizontal sur le parent */
html, body {
    width: 100% !important;
    max-width: 100vw !important;
    overflow-x: hidden !important;
    position: relative;
    margin: 0;
    padding: 0;
    touch-action: pan-y; /* Interdit le scroll horizontal tactile, autorise vertical */
}'

$content = $content.Replace($oldTop, $newTop)

# Replacement for the nav-links block
$oldNav = '    .nav-links {
        position: fixed;
        top: 0;
        right: -100%;
        width: 100%;
        height: 100vh;
        background-color: var(--bg-cream);
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 30px;
        margin: 0;
        padding: 40px;
        z-index: 1000;
        transition: transform 0.5s cubic-bezier(0.77, 0, 0.175, 1), right 0s;
        box-shadow: -10px 0 30px rgba(88, 0, 23, 0.1);
        transform: translateX(100%);
        right: 0;
    }

    .nav-links.active {
        transform: translateX(0);
    }'

$newNav = '    .nav-links {
        position: fixed !important; /* Sort du flux du document */
        top: 0;
        right: 0;
        width: 100%;
        height: 100vh;
        
        /* LA CLEF : On le cache complètement quand il n'est pas actif */
        transform: translateX(100%);
        visibility: hidden; /* Le navigateur l'ignore totalement */
        transition: transform 0.3s ease-in-out, visibility 0.3s ease-in-out;
        
        z-index: 9999;
        background-color: var(--color-burgundy);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 30px;
        margin: 0;
        padding: 40px;
        box-shadow: -10px 0 30px rgba(88, 0, 23, 0.1);
    }

    .nav-links.active {
        transform: translateX(0);
        visibility: visible; /* On le rend visible uniquement maintenant */
    }'

$content = $content.Replace($oldNav, $newNav)

Set-Content -Path $path -Value $content -Encoding utf8
