# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import tkinter
import tkinter.ttk

# 获取 Anaconda 的 DLL 路径
anaconda_path = r'F:\soft\Anaconda'  # 你的 Anaconda 安装路径

# 准备二进制文件列表
binaries = []

# 添加所有必要的 DLL 文件
dll_files = [
    'tcl86t.dll',
    'tk86t.dll',
    '_tkinter.pyd',
    'tcl86t.dll',
    'tk86t.dll',
    'sqlite3.dll',
    'libcrypto-1_1-x64.dll',
    'libssl-1_1-x64.dll',
]

for dll in dll_files:
    dll_path = os.path.join(anaconda_path, 'DLLs', dll)
    if os.path.exists(dll_path):
        binaries.append((dll_path, '.'))
    dll_path = os.path.join(anaconda_path, 'Library', 'bin', dll)
    if os.path.exists(dll_path):
        binaries.append((dll_path, '.'))

# 准备数据文件列表
datas = []

# 添加 tcl/tk 库文件
tcl_path = os.path.join(anaconda_path, 'tcl')
tk_path = os.path.join(anaconda_path, 'tk')
tcl_lib = os.path.join(anaconda_path, 'Library', 'lib', 'tcl8.6')
tk_lib = os.path.join(anaconda_path, 'Library', 'lib', 'tk8.6')

if os.path.exists(tcl_path):
    datas.append((tcl_path, 'tcl'))
if os.path.exists(tk_path):
    datas.append((tk_path, 'tk'))
if os.path.exists(tcl_lib):
    datas.append((tcl_lib, 'tcl8.6'))
if os.path.exists(tk_lib):
    datas.append((tk_lib, 'tk8.6'))

# 添加 tkinter 包
tkinter_path = os.path.dirname(tkinter.__file__)
if os.path.exists(tkinter_path):
    datas.append((tkinter_path, 'tkinter'))

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'pynput.keyboard._win32',
        'pynput.mouse._win32',
        'tkinter',
        'tkinter.ttk',
        '_tkinter',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.commondialog',
        'tkinter.colorchooser',
        'tkinter.constants',
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
    console=True,  # 临时设置为True以查看错误信息
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version='file_version_info.txt' if os.path.exists('file_version_info.txt') else None,
)

dll_path = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'dlls') 