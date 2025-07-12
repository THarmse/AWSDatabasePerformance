@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean MariaDB Insert results folder and run Apache JMeter Insert test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing MariaDB Insert results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\MariaDB\Insert"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\MariaDB\Insert\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\MariaDB_Insert.jmx"  -l "C:\code\performance_tests\jmeter\results\MariaDB\Insert\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\MariaDB\Insert\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
