@echo off
echo ====================================
echo  Land Registry Management System
echo ====================================
echo.

REM Set database URL
set DATABASE_URL=mysql+pymysql://root:1234@localhost/land_registry_db

REM Activate virtual environment if exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo Running without virtual environment
)

echo.
echo Starting Flask application...
echo Open browser at: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py

pause
