@echo off
setlocal EnableDelayedExpansion

REM -------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM FINAL CORRECTED VERSION
REM Opens local JMeter HTML reports in browser
REM -------------------------------------------------------------------------

REM === USER SETTINGS ===
set "BasePath=C:\code\performance_tests\jmeter\results"

set "MySQL=1"
set "AuroraMySQL=1"
set "PostgreSQL=1"
set "AuroraPostgreSQL=1"
set "MariaDB=1"
set "MSSQLServer=1"
set "Oracle=1"
set "IBMDB2=1"
set "DynamoDB=1"

set "Operations=Insert Select Update Delete"

echo.
echo === OPENING JMETER HTML REPORTS ===
echo.

REM --- OPEN INITIALIZE REPORT FIRST ---
set "initPath=%BasePath%\Initialize\report\index.html"
if exist "%initPath%" (
    echo --------------------------------------------
    echo [INITIALIZE] Opening Initialization Report
    echo --------------------------------------------
    echo Opening: "%initPath%"
    start "" "%initPath%"
    timeout /t 2 >nul
) else (
    echo [WARN] Initialization Report not found: "%initPath%"
)
echo.

call :openReports "MySQL" !MySQL!
call :openReports "Aurora MySQL" !AuroraMySQL!
call :openReports "PostgreSQL" !PostgreSQL!
call :openReports "Aurora PostgreSQL" !AuroraPostgreSQL!
call :openReports "MariaDB" !MariaDB!
call :openReports "MS SQL Server" !MSSQLServer!
call :openReports "Oracle" !Oracle!
call :openReports "IBM DB2" !IBMDB2!
call :openReports "DynamoDB" !DynamoDB!

echo.
echo === DONE ===
pause
exit /b

:openReports
setlocal EnableDelayedExpansion
set "dbName=%~1"
set "enabled=%~2"

if "!enabled!"=="1" (
    echo --------------------------------------------
    echo [ENABLED] !dbName!
    echo --------------------------------------------
    for %%O in (%Operations%) do (
        set "thisPath=%BasePath%\!dbName!\%%O\report\index.html"
        if exist "!thisPath!" (
            echo Opening: "!thisPath!"
            start "" "!thisPath!"
            timeout /t 2 >nul
        ) else (
            echo [WARN] NOT FOUND: "!thisPath!"
        )
    )
) else (
    echo [SKIPPED] !dbName! (disabled)
)
echo.
exit /b
