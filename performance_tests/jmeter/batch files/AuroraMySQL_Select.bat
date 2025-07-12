@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean Aurora MySQL Select results folder and run Apache JMeter Select test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing Aurora MySQL Select results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\Aurora MySQL\Select"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\Aurora MySQL\Select\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\AuroraMySQL_Select.jmx"  -l "C:\code\performance_tests\jmeter\results\Aurora MySQL\Select\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\Aurora MySQL\Select\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
