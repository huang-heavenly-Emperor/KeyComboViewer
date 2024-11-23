@echo off
setlocal enabledelayedexpansion

set CONDA_PATH=F:\soft\Anaconda
set ENV_NAME=myenv

echo ====================================
echo Checking Conda installation...

if not exist "%CONDA_PATH%\Scripts\conda.exe" (
    echo Error: Conda not found at %CONDA_PATH%
    pause
    exit /b 1
)

echo Initializing conda...
call "%CONDA_PATH%\Scripts\conda.exe" init cmd.exe

call "%CONDA_PATH%\condabin\conda.bat" activate base

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

echo ====================================
echo Activating environment: %ENV_NAME%
call "%CONDA_PATH%\Scripts\activate.bat" %ENV_NAME%

python --version

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

echo ====================================
if not exist main.py (
    echo Error: main.py not found
    pause
    exit /b 1
)

echo Starting the program...
python main.py
if errorlevel 1 (
    echo Error: Program execution failed
    pause
    exit /b 1
)

pause 
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