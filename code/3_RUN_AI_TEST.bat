@echo off
cd /d "%~dp0"
if not exist settings.txt copy settings.example.txt settings.txt >nul
echo Which AI provider? Type gemini or groq and press Enter.
set /p PROVIDER=Provider [gemini]: 
if "%PROVIDER%"=="" set PROVIDER=gemini
echo Which dataset? Type pilot (30 claims) or auto (SEC dataset).
set /p DATASET=Dataset [pilot]: 
if "%DATASET%"=="" set DATASET=pilot
echo.
echo --- Condition 1 of 2: the model is told the policy and cutoff ---
python run_llm.py --provider %PROVIDER% --dataset %DATASET% --condition full
echo.
echo --- Condition 2 of 2: the model only sees the claim and documents ---
python run_llm.py --provider %PROVIDER% --dataset %DATASET% --condition bare
python summarize.py
echo.
pause
