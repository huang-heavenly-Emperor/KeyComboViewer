@echo off
setlocal enabledelayedexpansion

:: 设置 Conda 安装路径
set CONDA_PATH=F:\soft\Anaconda
set ENV_NAME=myenv

echo ====================================
echo Checking Conda installation...

if not exist "%CONDA_PATH%\Scripts\conda.exe" (
    echo Error: Conda not found at %CONDA_PATH%
    pause
    exit /b 1
)

:: 初始化 conda
echo Initializing conda...
call "%CONDA_PATH%\Scripts\conda.exe" init cmd.exe

:: 重新加载环境变量
call "%CONDA_PATH%\condabin\conda.bat" activate base

:: 检查环境是否存在
echo Checking if environment exists...
"%CONDA_PATH%\Scripts\conda.exe" info --envs | find "%ENV_NAME%" > nul
if errorlevel 1 (
    echo Creating new environment: %ENV_NAME%
    call "%CONDA_PATH%\Scripts\conda.exe" create -n %ENV_NAME% python=3.8 -y
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
call "%CONDA_PATH%\Scripts\activate.bat" %ENV_NAME%

:: 验证环境激活
python --version

:: 使用conda安装所有依赖
echo ====================================
echo Installing dependencies with conda...
call conda install -y -c conda-forge ^
    tk ^
    pynput ^
    pip ^
    certifi
if errorlevel 1 (
    echo Error: Failed to install dependencies with conda
    pause
    exit /b 1
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
:: 安装依赖
echo ====================================
echo Installing dependencies...
call conda install -y tk -c conda-forge
if errorlevel 1 (
    echo Error: Failed to install tkinter
    pause
    exit /b 1
)

python -m pip install pynput --no-cache-dir
if errorlevel 1 (
    echo Error: Failed to install pynput
    pause
    exit /b 1
)

pause 