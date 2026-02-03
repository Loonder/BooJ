@echo off
echo ========================================
echo  JobPulse - Python 3.11 Venv Setup
echo ========================================
echo.

REM Tentar encontrar Python 3.11 de várias formas
set PYTHON_CMD=

REM Opção 1: python311
where python311 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python311
    goto :found
)

REM Opção 2: py -3.11
py -3.11 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=py -3.11
    goto :found
)

REM Opção 3: Caminho padrão C:\Python311
if exist "C:\Python311\python.exe" (
    set PYTHON_CMD=C:\Python311\python.exe
    goto :found
)

REM Opção 4: python (verificar se é 3.11)
python --version 2>&1 | findstr /C:"3.11" >nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    goto :found
)

REM Não encontrou
echo [!] Python 3.11 NAO encontrado!
echo.
echo Opcoes:
echo  1. Download: https://www.python.org/downloads/release/python-3119/
echo  2. Durante instalacao, marque "Add Python to PATH"
echo  3. OU instale em: C:\Python311\
echo.
pause
exit /b 1

:found
echo [*] Python 3.11 encontrado: %PYTHON_CMD%
%PYTHON_CMD% --version

echo.
echo [*] Criando virtual environment...
%PYTHON_CMD% -m venv venv311

echo [*] Ativando venv311...
call venv311\Scripts\activate.bat

echo [*] Atualizando pip...
python -m pip install --upgrade pip

echo [*] Instalando dependencias do requirements.txt...
pip install -r requirements.txt

echo [*] Instalando JobSpy...
pip install -U python-jobspy

echo.
echo ========================================
echo  Setup Completo!
echo ========================================
echo.
echo Para usar:
echo   1. Ative o venv: venv311\Scripts\activate
echo   2. Rode: python src/hunter.py
echo.
echo Ou use: start_with_venv.bat
echo.
pause
