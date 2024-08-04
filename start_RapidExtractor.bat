@echo off
REM Dynamically determine the drive letter of the USB stick
set USB_DRIVE=%~d0

REM Set the path to the portable Python interpreter
set "PYTHON_PATH=%USB_DRIVE%\WPy64-31241\python-3.12.4.amd64\python.exe"

REM Set the path to the main Python script
set "SCRIPT_PATH=%USB_DRIVE%\RapidExtractor\scripts\gui.py"

REM Debug output
echo Python Path: %PYTHON_PATH%
echo Script Path: %SCRIPT_PATH%

REM Check if the Python interpreter exists
if not exist "%PYTHON_PATH%" (
    echo The specified Python interpreter does not exist: %PYTHON_PATH%
    pause
    exit /b
)

REM Check if the main script exists
if not exist "%SCRIPT_PATH%" (
    echo The specified Python script does not exist: %SCRIPT_PATH%
    pause
    exit /b
)

REM Run the main script with selected modules
"%PYTHON_PATH%" "%SCRIPT_PATH%" %*

pause
