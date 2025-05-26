@echo off
echo Compilando Water Treatment con PyInstaller...
echo.

pyinstaller ^
--onefile ^
--windowed ^
--name "Water Treatment" ^
--icon "ico\ico.ico" ^
--add-data "kv;kv" ^
--add-data "animacion_practica1.kv;." ^
--add-data "assets;assets" ^
--add-data "animacion_practica1_pygame.py;." ^
--add-data "animacion_practica2_pygame.py;." ^
--add-data "animacion_practica3_pygame.py;." ^
--add-data "animacion_practica4_pygame.py;." ^
--add-data "animacion_practica5_pygame.py;." ^
--add-data "animacion_practica1.py;." ^
--hidden-import kivy.deps.sdl2 ^
--hidden-import kivy.deps.glew ^
--hidden-import kivy.core.window.window_sdl2 ^
--hidden-import kivy.core.audio.audio_sdl2 ^
--hidden-import kivy.core.image.img_pil ^
--hidden-import kivy.core.clipboard.clipboard_winapi ^
--hidden-import kivy_garden.matplotlib ^
--hidden-import matplotlib ^
--hidden-import matplotlib.pyplot ^
--hidden-import matplotlib.backends.backend_agg ^
--hidden-import numpy ^
--hidden-import PIL ^
--hidden-import pygame ^
--collect-submodules kivy ^
--collect-submodules kivy_garden ^
main.py

echo.
echo Compilacion completada!
echo El ejecutable se encuentra en: dist\Water Treatment.exe
pause
