# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['2B.py'],
    pathex=['C:\\Users\\canel\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages'],
    binaries=[],
    datas=[('templates', 'templates')],
    hiddenimports=['flask'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='2B',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir='.',
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
