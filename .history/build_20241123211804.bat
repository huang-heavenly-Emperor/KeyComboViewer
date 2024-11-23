@echo off
echo Cleaning previous builds...
rmdir /s /q build dist
echo Building application...
pyinstaller --clean keyboard_listener.spec
echo Build complete!
pause 