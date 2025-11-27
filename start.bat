@echo off
echo ========================================
echo  Diabetic Retinopathy Detection System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [2/4] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created successfully!
    echo.
) else (
    echo [2/4] Virtual environment already exists
    echo.
)

REM Activate virtual environment
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Check if requirements are installed
echo [4/4] Installing/Checking dependencies...
pip install -r requirements.txt
echo.

REM Check if model file exists
if not exist "Retinal_blindness_detection_Pytorch-master\classifier.pt" (
    echo ========================================
    echo  WARNING: Model file not found!
    echo ========================================
    echo.
    echo The trained model file 'classifier.pt' is missing.
    echo.
    echo Please download it from:
    echo https://www.kaggle.com/souravs17031999/blindness-detection-pretrained-weights-pytorch
    echo.
    echo Place it in: Retinal_blindness_detection_Pytorch-master\classifier.pt
    echo.
    echo Press any key to continue anyway (server will start but predictions won't work)
    pause
)

echo ========================================
echo  Starting Flask Server...
echo ========================================
echo.
echo Server will be available at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask application
python app.py

pause
