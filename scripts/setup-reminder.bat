@echo off
REM Setup Task Scheduler — Blog Reminder KLEIA-UP
REM À exécuter une seule fois en Administrateur

schtasks /create /tn "KLEIA-UP Blog Reminder" /tr "C:\Users\JP\Documents\GitHub\KLEIA\site-web-kleia-up\scripts\blog-reminder.bat" /sc weekly /d fri /st 17:00 /f

echo ✅ Tâche créée : KLEIA-UP Blog Reminder (Ven 17h)
echo.
schtasks /query /tn "KLEIA-UP Blog Reminder" /v /fo list | findstr /i "taskname schedule"
