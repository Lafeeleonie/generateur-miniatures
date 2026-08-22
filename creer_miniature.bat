@echo off
setlocal
cd /d "%~dp0"

if not exist "programme\.venv\Scripts\pythonw.exe" (
    echo Creation de l'environnement virtuel...
    py -3 -m venv programme\.venv
    if errorlevel 1 goto :erreur
    "programme\.venv\Scripts\python.exe" -m pip install --upgrade pip
    "programme\.venv\Scripts\python.exe" -m pip install -r programme\requirements.txt
    if errorlevel 1 goto :erreur
)

start "" "programme\.venv\Scripts\pythonw.exe" "programme\miniaturiseur.py"
if errorlevel 1 goto :erreur
exit /b 0

:erreur
echo.
echo Une erreur est survenue.
pause
exit /b 1
