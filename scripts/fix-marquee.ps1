$path = "css/main.css"
$lines = Get-Content $path
# On garde jusqu'à la ligne 2154 (0-index: 2153)
$lines[0..2153] | Set-Content $path -Encoding UTF8
$newStyles = @"

/* --- LOGO INFINITE MARQUEE (BLINDÉ) --- */

/* Conteneur principal - Forçage Horizontal Absolu */
.logo-marquee-wrapper {
    display: flex !important;
    flex-direction: row !important; /* Empêche le passage en colonne */
    flex-wrap: nowrap !important;   /* Interdit le retour à la ligne */
    overflow: hidden;
    user-select: none;
    width: 100%;
    padding: 3rem 0;
    position: relative;
}

/* La piste qui défile - Forçage Horizontal */
.logo-marquee-content {
    display: flex !important;
    flex-direction: row !important; /* Empêche le passage en colonne */
    flex-wrap: nowrap !important;
    align-items: center;
    justify-content: space-around;
    flex-shrink: 0;
    min-width: 100%;
    gap: 4rem;
    padding-right: 4rem; /* Compense le gap pour une boucle 100% invisible */
    animation: scroll-marquee 25s linear infinite;
}

/* Pause au survol */
.logo-marquee-wrapper:hover .logo-marquee-content {
    animation-play-state: paused;
}

/* Harmonisation des logos */
.logo-marquee-content img {
    max-height: 45px !important;
    width: auto !important;
    object-fit: contain;
    display: block; /* Empêche les marges fantômes inline */
    filter: none;
}

/* L'animation simplifiée et parfaite */
@keyframes scroll-marquee {
    from {
        transform: translateX(0);
    }
    to {
        transform: translateX(-100%);
    }
}
"@
Add-Content $path -Value $newStyles -Encoding UTF8
Write-Host "Correction appliquée."
