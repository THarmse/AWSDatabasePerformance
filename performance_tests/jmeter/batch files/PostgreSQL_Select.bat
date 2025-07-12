@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean PostgreSQL Select results folder and run Apache JMeter Select test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing PostgreSQL Select results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\PostgreSQL\Select"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\PostgreSQL\Select\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\PostgreSQL_Select.jmx"  -l "C:\code\performance_tests\jmeter\results\PostgreSQL\Select\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\PostgreSQL\Select\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
