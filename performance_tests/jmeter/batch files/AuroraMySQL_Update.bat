@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean Aurora MySQL Update results folder and run Apache JMeter Update test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing Aurora MySQL Update results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\Aurora MySQL\Update"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\Aurora MySQL\Update\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\AuroraMySQL_Update.jmx"  -l "C:\code\performance_tests\jmeter\results\Aurora MySQL\Update\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\Aurora MySQL\Update\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
