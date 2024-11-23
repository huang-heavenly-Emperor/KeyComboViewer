# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import tkinter
import tkinter.ttk

# 获取 tcl/tk DLL 文件路径
tcl_dll = os.path.join(sys.prefix, 'DLLs', 'tcl86t.dll')
tk_dll = os.path.join(sys.prefix, 'DLLs', 'tk86t.dll')

# 获取 tkinter 库路径
tkinter_path = os.path.dirname(tkinter.__file__)

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        (tcl_dll, '.'),
        (tk_dll, '.'),
    ],
    datas=[
        (os.path.join(tkinter_path, '*.dll'), 'tkinter'),
        (os.path.join(sys.prefix, 'DLLs', '_tkinter.pyd'), '.'),
        (os.path.join(sys.prefix, 'tcl'), 'tcl'),
        (os.path.join(sys.prefix, 'tk'), 'tk'),
    ],
    hiddenimports=[
        'pynput.keyboard._win32',
        'pynput.mouse._win32',
        'tkinter',
        'tkinter.ttk',
        '_tkinter',
        'tkinter.messagebox'
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
    name='KeyboardListener',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为False以隐藏控制台窗口
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version='file_version_info.txt' if os.path.exists('file_version_info.txt') else None,
) 