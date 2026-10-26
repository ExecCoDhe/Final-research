@echo off
cd /d "%~dp0"
echo Rebuilding Midterm_Presentation.pptx from the latest results...
echo (Close the presentation in PowerPoint first, or saving will fail.)
python make_slides.py
pause
