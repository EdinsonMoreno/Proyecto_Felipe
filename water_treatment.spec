# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

datas = [
    ('kv', 'kv'),
    ('animacion_practica1.kv', '.'),
    ('assets', 'assets'),
    ('animacion_practica1_pygame.py', '.'),
    ('animacion_practica2_pygame.py', '.'),
    ('animacion_practica3_pygame.py', '.'),
    ('animacion_practica4_pygame.py', '.'),
    ('animacion_practica5_pygame.py', '.'),
    ('animacion_practica1.py', '.'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'kivy.deps.sdl2',
        'kivy.deps.glew',
        'kivy.core.window.window_sdl2',
        'kivy.core.audio.audio_sdl2',
        'kivy.core.image.img_pil',
        'kivy.core.clipboard.clipboard_winapi',
        'kivy_garden.matplotlib',
        'matplotlib',
        'matplotlib.pyplot',
        'matplotlib.backends.backend_agg',
        'numpy',
        'PIL',
        'pygame',
        'backend',
        'backend.practica1_balance_energetico',
        'backend.practica2_filtrado_multicapa',
        'backend.practica3_intercambiador_calor',
        'backend.practica4_caldera',
        'backend.practica5_captacion_lluvia',
        'frontend',
        'frontend.main_screen',
        'frontend.screens.practica1_screen',
        'frontend.screens.practica2_screen',
        'frontend.screens.practica3_screen',
        'frontend.screens.practica4_screen',
        'frontend.screens.practica5_screen',
        'utils',
        'utils.helpers',
        'utils.sensores',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Water Treatment',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ico\\ico.ico',
)
