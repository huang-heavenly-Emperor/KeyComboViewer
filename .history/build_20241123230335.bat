@echo off
setlocal

:: 设置环境名称
set ENV_NAME=myenv

:: 检查环境是否存在
conda info --envs | find "%ENV_NAME%" > nul
if errorlevel 1 (
    echo Creating new environment: %ENV_NAME%
    conda create -n %ENV_NAME% python=3.8 -y
) else (
    echo Environment %ENV_NAME% already exists
)

:: 激活环境
echo Activating environment: %ENV_NAME%
call conda activate %ENV_NAME%

:: 检查requirements.txt是否存在并安装依赖
if exist requirements.txt (
    echo Installing dependencies from requirements.txt
    pip install -r requirements.txt
) else (
    echo Warning: requirements.txt not found
)

:: 运行Python程序
echo Starting the program...
python main.py

:: 保持窗口打开
pause 