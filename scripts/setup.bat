@echo off

REM Check if the virtual environment exists
if not exist "venv" (
    echo Creating a new virtual environment...
    python -m venv venv
) else (
    echo Existing virtual environment found.
)

REM Activate the virtual environment
venv\Scripts\activate

REM Install requirements
pip install -r requirements.txt

REM Deactivate the virtual environment
deactivate

echo Setup complete. To run the dashboard, execute 'run.bat'.