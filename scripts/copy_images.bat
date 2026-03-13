@echo off
set SRC1="C:\Users\JP\.gemini\antigravity\brain\d75f15c4-a641-4415-875c-f502e7272d92\k_incarnation_premium_1773420239005.png"
set SRC2="C:\Users\JP\.gemini\antigravity\brain\d75f15c4-a641-4415-875c-f502e7272d92\k_enterprise_premium_1773420252897.png"
set SRC3="C:\Users\JP\.gemini\antigravity\brain\d75f15c4-a641-4415-875c-f502e7272d92\k_leadership_auric_1773420268497.png"

set DEST="c:\Users\JP\Documents\GitHub\site-web-kleia-up\assets\programmes"

if not exist %DEST% mkdir %DEST%

copy /Y %SRC1% %DEST%\incarnation.png
copy /Y %SRC2% %DEST%\entreprise.png
copy /Y %SRC3% %DEST%\conference.png
