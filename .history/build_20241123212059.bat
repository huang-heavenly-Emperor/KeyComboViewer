@echo off
echo Checking Python environment...

:: 检查 Python 是否在环境变量中
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python not found in PATH
    echo Please install Python and add it to PATH
    pause
    exit /b 1
)

:: 检查 PyInstaller 是否已安装，如果没有则安装
pip show pyinstaller >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install PyInstaller
        pause
        exit /b 1
    )
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
:: 使用完整的 Python 命令来运行 PyInstaller
python -m pyinstaller --clean keyboard_listener.spec

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo Build complete!
echo Executable can be found in the dist folder

:: 如果成功构建，尝试启动程序
if exist "dist\KeyboardListener.exe" (
    echo Starting application...
    start "" "dist\KeyboardListener.exe"
)

pause 