$inputFile = "css/main.css"
$outputFile = "css/main.min.css"

if (Test-Path $inputFile) {
    Write-Host "Minification de $inputFile vers $outputFile..." -ForegroundColor Cyan
    
    $css = Get-Content -Path $inputFile -Raw
    
    # Suppression des commentaires /* ... */
    $css = [regex]::Replace($css, "/\*[\s\S]*?\*/", "")
    
    # Mise à plat (suppression des sauts de ligne)
    $css = $css.Replace("`r", "").Replace("`n", " ")
    
    # Suppression des espaces multiples
    $css = [regex]::Replace($css, "\s+", " ")
    
    # Optimisation des espaces autour des ponctuateurs
    $css = [regex]::Replace($css, "\s*{\s*", "{")
    $css = [regex]::Replace($css, "\s*}\s*", "}")
    $css = [regex]::Replace($css, "\s*:\s*", ":")
    $css = [regex]::Replace($css, "\s*;\s*", ";")
    $css = [regex]::Replace($css, "\s*,\s*", ",")
    
    # Nettoyage final
    $css = $css.Trim()
    
    Set-Content -Path $outputFile -Value $css -NoNewline -Encoding utf8
    
    $originalSize = (Get-Item $inputFile).Length / 1kb
    $minifiedSize = (Get-Item $outputFile).Length / 1kb
    
    Write-Host "Succès ! Taille réduite de $($originalSize.ToString('F2')) KB à $($minifiedSize.ToString('F2')) KB." -ForegroundColor Green
}
else {
    Write-Host "Erreur : Fichier $inputFile introuvable." -ForegroundColor Red
}
