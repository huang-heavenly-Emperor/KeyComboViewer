# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import tkinter
import tkinter.ttk

# 获取 Anaconda 的 DLL 路径
anaconda_path = r'F:\soft\Anaconda'  # 你的 Anaconda 安装路径
tcl_dll = os.path.join(anaconda_path, 'DLLs', 'tcl86t.dll')
tk_dll = os.path.join(anaconda_path, 'DLLs', 'tk86t.dll')

# 获取 tkinter 库路径
tkinter_path = os.path.dirname(tkinter.__file__)

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        (tcl_dll, '.') if os.path.exists(tcl_dll) else None,
        (tk_dll, '.') if os.path.exists(tk_dll) else None,
    ],
    datas=[
        (os.path.join(anaconda_path, 'DLLs', '_tkinter.pyd'), '.'),
        (os.path.join(anaconda_path, 'tcl'), 'tcl'),
        (os.path.join(anaconda_path, 'tk'), 'tk'),
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

# 过滤掉 None 值
a.binaries = [b for b in a.binaries if b is not None]

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