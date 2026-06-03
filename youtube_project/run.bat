@echo off
title SmartTube AI
cd /d "%~dp0"

set DISABLE_SSL_VERIFY=1
set PYTHONHTTPSVERIFY=0
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

set PYTHON="C:\Users\Asus\AppData\Local\Programs\Python\Python311\python.exe"

if not exist %PYTHON% (
    echo ERROR: Python 3.11 not found.
    pause
    exit /b 1
)

echo.
echo  SmartTube AI starting...
echo  Open: http://localhost:8501
echo.

start http://localhost:8501
echo. | %PYTHON% -m streamlit run app.py --server.headless true

pause
