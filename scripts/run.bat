@echo off

REM Check if the virtual environment directory exists
if not exist "venv" (
    echo Virtual environment not found. Please run 'setup.bat' first.
    exit /b
)

REM Activate the virtual environment
venv\Scripts\activate

REM Run the main Python program
python3 example_dashboard.py

REM Deactivate the virtual environment
deactivate