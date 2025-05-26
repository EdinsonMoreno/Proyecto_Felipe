@echo off
REM Script para empaquetar automáticamente las 4 animaciones pygame con PyInstaller

setlocal
set PYINSTALLER=pyinstaller
set ICONO=ico\ico.ico
set COMMON_OPTS=--onefile --noconsole --icon %ICONO%

REM Empaquetar animacion_practica1_pygame.py
%PYINSTALLER% %COMMON_OPTS% animacion_practica1_pygame.py

REM Empaquetar animacion_practica2_pygame.py
%PYINSTALLER% %COMMON_OPTS% animacion_practica2_pygame.py

REM Empaquetar animacion_practica3_pygame.py
%PYINSTALLER% %COMMON_OPTS% animacion_practica3_pygame.py

REM Empaquetar animacion_practica4_pygame.py
%PYINSTALLER% %COMMON_OPTS% animacion_practica4_pygame.py

REM Mensaje final
@echo.
@echo Animaciones empaquetadas correctamente.
@echo Los ejecutables están en la carpeta dist\
endlocal
pause
