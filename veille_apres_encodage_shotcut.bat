@echo off
setlocal
title Veille apres export Shotcut

echo ==========================================
echo   Veille automatique apres export Shotcut
echo ==========================================
echo.
echo Lancez l'export dans Shotcut maintenant.
echo Attente du lancement de melt.exe ou qmelt.exe...
echo Fermez cette fenetre pour annuler.
echo.

:WAIT_START
call :EXPORT_RUNNING
if errorlevel 1 (
    timeout /t 5 /nobreak >NUL
    goto WAIT_START
)

echo Export detecte.
echo Attente de la fin de l'export...
echo.

:WAIT_END
call :EXPORT_RUNNING
if not errorlevel 1 (
    timeout /t 10 /nobreak >NUL
    goto WAIT_END
)

echo Export termine. Verification de la file...
echo Attente de 5 minutes sans nouvel export.
timeout /t 300 /nobreak >NUL

call :EXPORT_RUNNING
if not errorlevel 1 (
    echo Nouvel export detecte dans la file.
    goto WAIT_END
)

echo Tous les exports semblent termines.
echo Mise en veille dans 30 secondes...
echo Fermez cette fenetre maintenant pour annuler.
timeout /t 30 /nobreak >NUL

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState([System.Windows.Forms.PowerState]::Suspend,$false,$false)"

endlocal
exit /b 0

:EXPORT_RUNNING
tasklist /FI "IMAGENAME eq melt.exe" 2>NUL | find /I "melt.exe" >NUL
if not errorlevel 1 exit /b 0
tasklist /FI "IMAGENAME eq qmelt.exe" 2>NUL | find /I "qmelt.exe" >NUL
if not errorlevel 1 exit /b 0
exit /b 1
