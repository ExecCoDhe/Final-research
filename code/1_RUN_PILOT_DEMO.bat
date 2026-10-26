@echo off
cd /d "%~dp0"
echo Running the five rule-based verifiers on the 30 hand-checked pilot claims...
python run_rules.py pilot
echo.
pause
