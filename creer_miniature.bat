@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Creation de l'environnement virtuel...
    py -3 -m venv .venv
    if errorlevel 1 goto :erreur
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto :erreur
)

".venv\Scripts\python.exe" miniaturiseur.py --sortie xx_miniature.png
if errorlevel 1 goto :erreur
echo Termine : xx_miniature.png
exit /b 0

:erreur
echo.
echo Une erreur est survenue.
pause
exit /b 1
