@echo off
echo Checking Python environment...

:: 检查并激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found at venv\Scripts\activate.bat
    echo Using system Python...
)

:: 检查 Python 是否在环境变量中
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python not found in PATH
    echo Please install Python and add it to PATH
    pause
    exit /b 1
)

:: 确保 pip 是最新的
python -m pip install --upgrade pip

:: 强制重新安装 PyInstaller
echo Installing PyInstaller...
python -m pip uninstall -y pyinstaller
python -m pip install --no-cache-dir pyinstaller

:: 验证 PyInstaller 安装
python -m pip show pyinstaller
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install PyInstaller
    pause
    exit /b 1
)

echo Cleaning previous builds...
:: 尝试关闭可能正在运行的程序
taskkill /F /IM KeyboardListener.exe >nul 2>nul

:: 等待一会儿让系统释放文件
timeout /t 2 >nul

:: 使用 rd 命令删除目录，添加错误处理
if exist build (
    rd /s /q build >nul 2>nul
    if exist build (
        echo Warning: Could not delete build directory
    )
)

if exist dist (
    rd /s /q dist >nul 2>nul
    if exist dist (
        echo Warning: Could not delete dist directory
    )
)

echo Building application...
:: 使用 python -m 来运行 PyInstaller
python -m PyInstaller --clean keyboard_listener.spec

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    echo Trying alternative command...
    :: 尝试直接使用 pyinstaller 命令
    pyinstaller --clean keyboard_listener.spec
    if %ERRORLEVEL% NEQ 0 (
        echo Both build attempts failed!
        pause
        exit /b 1
    )
)

echo Build complete!
echo Executable can be found in the dist folder

:: 如果成功构建，尝试启动程序
if exist "dist\KeyboardListener.exe" (
    echo Starting application...
    start "" "dist\KeyboardListener.exe"
)

:: 如果在虚拟环境中，则退出虚拟环境
if defined VIRTUAL_ENV (
    echo Deactivating virtual environment...
    deactivate
)

pause 