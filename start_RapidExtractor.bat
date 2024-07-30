@echo off
REM Set the path to the portable Python interpreter
set "PYTHON_PATH=E:\WPy64-31241\python-3.12.4.amd64\python.exe"

REM Set the path to the GUI Python script
set "SCRIPT_PATH=E:\RapidExtractor\Scripts\gui.py"

REM Debug output
echo Python Path: %PYTHON_PATH%
echo Script Path: %SCRIPT_PATH%

REM Check if the Python interpreter exists
if not exist "%PYTHON_PATH%" (
    echo The specified Python interpreter does not exist: %PYTHON_PATH%
    pause
    exit /b
) else (
    echo Python interpreter found: %PYTHON_PATH%
)

REM Check if the GUI script exists
if not exist "%SCRIPT_PATH%" (
    echo The specified Python script does not exist: %SCRIPT_PATH%
    pause
    exit /b
) else (
    echo Python script found: %SCRIPT_PATH%
)

REM Run the GUI script
"%PYTHON_PATH%" "%SCRIPT_PATH%"
pause
