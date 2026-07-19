@echo off
REM Blog Reminder — KLEIA-UP
REM Vérifie le gap Brevo et crée un flag si des newsletters sont à publier
REM Déclenché par Windows Task Scheduler (Ven 17h)

cd /d "C:\Users\JP\Documents\GitHub\KLEIA\site-web-kleia-up"

REM Vérifier le gap
python scripts\publish-blog-article.py list > "%TEMP%\blog-gap-check.txt" 2>&1

REM Vérifier si le flag existe déjà, ou si le résultat indique un gap
findstr /C:"Total: 0 newsletter" "%TEMP%\blog-gap-check.txt" >nul
if %errorlevel% equ 0 (
    REM Pas de gap — nettoyer le flag si existant
    if exist ".gap-pending" del ".gap-pending"
    exit /b 0
)

REM Gap détecté — créer le flag
echo gap detected > ".gap-pending"

REM Notification Windows
powershell -Command "& {Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Des newsletters KLEIA-UP sont à publier sur le blog. Ouvre une session pour lancer : blog workflow hebdo', 'Blog KLEIA-UP', 'OK', 'Information')}"
