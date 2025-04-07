# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('./resources/buttons/*', './resources/buttons/'),
    ('./resources/plant_cards/*', './resources/plant_cards/'),
    ('./resources/statics/*', './resources/statics/'), 
    ('./resources/texts/*', './resources/texts/'),
    ('./resources/zombies/*', './resources/zombies/'),
    ('./configs/buttons/*', './configs/buttons/'),
    ('./configs/plant_cards/*', './configs/plant_cards/'),
    ('./configs/statics/*', './configs/statics/'),
    ('./configs/texts/*', './configs/texts/'),
    ('./configs/zombies/*', './configs/zombies/'),
    ('./fonts/*', './fonts/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('v', None, 'OPTION')],
    name='pku-pvz',
    debug=True,
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
)
