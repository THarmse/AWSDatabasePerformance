@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean Initialize results folder and run Apache JMeter Initialize test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing Initialize results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\Initialize"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\Initialize\report"

echo === Running JMeter Initialize Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\dbs_Initialize.jmx" ^
 -l "C:\code\performance_tests\jmeter\results\Initialize\results.jtl" ^
 -e -o "C:\code\performance_tests\jmeter\results\Initialize\report"

echo.
echo === JMeter Initialize test completed ===
echo.
echo Press any key to exit...
cmd /k
