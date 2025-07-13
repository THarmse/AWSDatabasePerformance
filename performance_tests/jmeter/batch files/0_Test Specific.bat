@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Master batch file to run Initialize.bat first (optional), then all DB batch files
REM -----------------------------------------------------------------------------

REM --- USER SETTING: 1 = run Initialize.bat, 0 = skip ---
set RunInitialize=0

REM --- USER SETTING: Wait time in seconds between scripts ---
set WaitSeconds=60

REM --- Capture the starting directory (this script's folder) ---
set "BatchDir=%~dp0"

echo =====================================================
echo JMeter Performance Test Master Batch Runner
echo =====================================================
echo.

REM --- Optional Initialize step ---
if "%RunInitialize%"=="1" (
    echo -----------------------------------------------------
    echo Running Initialize.bat
    echo -----------------------------------------------------
    if exist "%BatchDir%Initialize.bat" (
        pushd "%BatchDir%"
        call "Initialize.bat"
        popd
    ) else (
        echo [ERROR] Initialize.bat not found!
        pause
        exit /b
    )
    echo -----------------------------------------------------
    echo Initialize completed
    echo.
)

echo -----------------------------------------------------
echo Starting All Database Batch Files
echo Wait between scripts: %WaitSeconds% seconds
echo -----------------------------------------------------
echo.

REM === DATABASE TEST SEQUENCE ===



call "%BatchDir%DynamoDB_Insert.bat"
cd /d "%BatchDir%"
timeout /t %WaitSeconds% /nobreak
call "%BatchDir%DynamoDB_Select.bat"
cd /d "%BatchDir%"
timeout /t %WaitSeconds% /nobreak
call "%BatchDir%DynamoDB_Update.bat"
cd /d "%BatchDir%"
timeout /t %WaitSeconds% /nobreak
call "%BatchDir%DynamoDB_Delete.bat"
cd /d "%BatchDir%"
timeout /t %WaitSeconds% /nobreak

echo.
echo =====================================================
echo All Database Batch Files Have Completed
echo =====================================================
echo.
pause
