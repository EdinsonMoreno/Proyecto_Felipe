@echo off
echo ===============================================
echo    Compilando Water Treatment Application
echo ===============================================
echo.

echo Verificando dependencias...
pip install pyinstaller kivy kivy_garden.matplotlib matplotlib numpy pillow pygame

echo.
echo Iniciando compilacion con PyInstaller...
echo.

pyinstaller water_treatment.spec --clean --noconfirm

echo.
if exist "dist\Water Treatment.exe" (
    echo ===============================================
    echo    COMPILACION EXITOSA!
    echo ===============================================
    echo.
    echo El ejecutable se encuentra en:
    echo %CD%\dist\Water Treatment.exe
    echo.
    echo Tamano del archivo:
    dir "dist\Water Treatment.exe" | find "Water Treatment.exe"
) else (
    echo ===============================================
    echo    ERROR EN LA COMPILACION
    echo ===============================================
    echo.
    echo Revisa los mensajes de error arriba.
)

echo.
pause
