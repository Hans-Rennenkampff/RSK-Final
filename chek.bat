@echo off
:loop
tasklist /FI "IMAGENAME eq python.exe" | find /I "main.py" > nul
if errorlevel 1 (
    echo Starting main.py
    python main.py
)
timeout /t 30 > nul
goto loop
