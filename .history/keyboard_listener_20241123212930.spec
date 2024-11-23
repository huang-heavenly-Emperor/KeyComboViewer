# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import tkinter
import tkinter.ttk

# 获取 Anaconda 的 DLL 路径
anaconda_path = r'F:\soft\Anaconda'  # 你的 Anaconda 安装路径

# 准备二进制文件列表
binaries = []
tcl_dll = os.path.join(anaconda_path, 'DLLs', 'tcl86t.dll')
tk_dll = os.path.join(anaconda_path, 'DLLs', 'tk86t.dll')

if os.path.exists(tcl_dll):
    binaries.append((tcl_dll, '.'))
if os.path.exists(tk_dll):
    binaries.append((tk_dll, '.'))

# 准备数据文件列表
datas = []
tkinter_dll = os.path.join(anaconda_path, 'DLLs', '_tkinter.pyd')
tcl_path = os.path.join(anaconda_path, 'tcl')
tk_path = os.path.join(anaconda_path, 'tk')

if os.path.exists(tkinter_dll):
    datas.append((tkinter_dll, '.'))
if os.path.exists(tcl_path):
    datas.append((tcl_path, 'tcl'))
if os.path.exists(tk_path):
    datas.append((tk_path, 'tk'))

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,  # 使用处理过的二进制文件列表
    datas=datas,        # 使用处理过的数据文件列表
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