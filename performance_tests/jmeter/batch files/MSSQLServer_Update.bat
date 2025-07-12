@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean MS SQL Server Update results folder and run Apache JMeter Update test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing MS SQL Server Update results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\MS SQL Server\Update"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\MS SQL Server\Update\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\MSSQLServer_Update.jmx"  -l "C:\code\performance_tests\jmeter\results\MS SQL Server\Update\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\MS SQL Server\Update\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
