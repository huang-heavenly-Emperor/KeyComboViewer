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

:: 更新 pip 并安装证书
echo ====================================
echo Updating pip and installing certificates...
python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
python -m pip install certifi --trusted-host pypi.org --trusted-host files.pythonhosted.org

:: 设置国内镜像源
echo Setting pip mirror...
python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

:: 检查requirements.txt并安装依赖
echo ====================================
if exist requirements.txt (
    echo Installing dependencies from requirements.txt
    python -m pip install -r requirements.txt --trusted-host pypi.tuna.tsinghua.edu.cn
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