# scripts/verify-visual.ps1
# Script de vérification visuelle du site KLEIA-UP
# Usage: powershell -File scripts/verify-visual.ps1

$root = "c:\Users\JP\Documents\GitHub\site-web-kleia-up"
Set-Location $root

Write-Host "📂 Répertoire: $root" -ForegroundColor Cyan
Write-Host ""

# 1. Afficher le statut git
Write-Host "🔍 Vérification du statut git..." -ForegroundColor Yellow
git status --short

# 2. Vérifier s'il y a des modifications
$changes = git status --porcelain

if ($changes) {
    Write-Host ""
    Write-Host "📝 Modifications détectées, préparation du push..." -ForegroundColor Green
    
    # Ajouter tous les fichiers
    git add .
    
    # Créer le commit
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "🔄 Update pour vérification visuelle - $timestamp"
    
    # Pousser sur GitHub
    Write-Host ""
    Write-Host "🚀 Push en cours..." -ForegroundColor Cyan
    git push
    
    Write-Host ""
    Write-Host "⏳ Attente de 45 secondes pour la build GitHub Pages..." -ForegroundColor Yellow
    Start-Sleep -Seconds 45
} else {
    Write-Host ""
    Write-Host "✅ Pas de modifications locales à pousser." -ForegroundColor Green
    Write-Host "⏳ Attente de 5 secondes avant ouverture..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
}

# 3. Ouvrir le site dans Chrome
Write-Host ""
Write-Host "🌐 Ouverture du site dans Chrome..." -ForegroundColor Cyan
Start-Process chrome "https://jpnirrep.github.io/site-web-kleia-up/"

Write-Host ""
Write-Host "✨ Vérification visuelle lancée!" -ForegroundColor Green
