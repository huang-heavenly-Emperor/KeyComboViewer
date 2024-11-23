@echo off
:: 检查并激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

:: 运行程序
python main.py

:: 如果在虚拟环境中，则退出虚拟环境
if defined VIRTUAL_ENV (
    deactivate
) 