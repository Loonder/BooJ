@echo off
echo ========================================
echo  JobPulse - Starting with Python 3.11
echo ========================================
echo.

if not exist "venv311\Scripts\activate.bat" (
    echo [!] Venv nao encontrado!
    echo [!] Execute primeiro: setup_python311.bat
    pause
    exit /b 1
)

echo [*] Ativando venv311...
call venv311\Scripts\activate.bat

echo [*] Verificando versao do Python...
python --version

echo.
echo [*] Iniciando JobPulse Hunter...
echo.
python src\hunter.py

pause
