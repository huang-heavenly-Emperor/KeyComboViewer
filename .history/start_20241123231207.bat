@echo off
setlocal enabledelayedexpansion

:: 设置环境名称
set ENV_NAME=myenv

echo ====================================
echo Checking Conda installation...
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Conda is not installed or not in PATH
    pause
    exit /b 1
)

:: 检查环境是否存在
echo Checking if environment exists...
conda info --envs | find "%ENV_NAME%" > nul
if errorlevel 1 (
    echo Creating new environment: %ENV_NAME%
    call conda create -n %ENV_NAME% python=3.8 -y
    if errorlevel 1 (
        echo Error: Failed to create environment
        pause
        exit /b 1
    )
) else (
    echo Environment %ENV_NAME% already exists
)

:: 激活环境
echo ====================================
echo Activating environment: %ENV_NAME%
call conda activate %ENV_NAME%
if errorlevel 1 (
    echo Error: Failed to activate environment
    pause
    exit /b 1
)

:: 验证环境激活
python --version
if errorlevel 1 (
    echo Error: Python environment not properly activated
    pause
    exit /b 1
)

:: 检查requirements.txt并安装依赖
echo ====================================
if exist requirements.txt (
    echo Installing dependencies from requirements.txt
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Warning: requirements.txt not found
)

:: 检查main.py是否存在
echo ====================================
if not exist main.py (
    echo Error: main.py not found
    pause
    exit /b 1
)

:: 运行Python程序
echo Starting the program...
python main.py
if errorlevel 1 (
    echo Error: Program execution failed
    pause
    exit /b 1
)

pause 