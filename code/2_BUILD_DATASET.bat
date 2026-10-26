@echo off
cd /d "%~dp0"
if not exist settings.txt copy settings.example.txt settings.txt >nul
echo Building the automatic dataset from free SEC data (takes about 5-15 minutes)...
python build_dataset.py --target 40
echo.
echo Running the rule-based verifiers on the new dataset...
python run_rules.py auto
python summarize.py
echo.
pause
