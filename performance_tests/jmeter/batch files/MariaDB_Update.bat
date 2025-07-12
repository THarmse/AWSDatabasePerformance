@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean MariaDB Update results folder and run Apache JMeter Update test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing MariaDB Update results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\MariaDB\Update"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\MariaDB\Update\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\MariaDB_Update.jmx"  -l "C:\code\performance_tests\jmeter\results\MariaDB\Update\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\MariaDB\Update\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
