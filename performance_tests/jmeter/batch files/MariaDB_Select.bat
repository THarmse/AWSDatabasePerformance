@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean MariaDB Select results folder and run Apache JMeter Select test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing MariaDB Select results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\MariaDB\Select"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\MariaDB\Select\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\MariaDB_Select.jmx"  -l "C:\code\performance_tests\jmeter\results\MariaDB\Select\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\MariaDB\Select\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
