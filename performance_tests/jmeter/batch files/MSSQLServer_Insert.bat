@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean MS SQL Server Insert results folder and run Apache JMeter Insert test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing MS SQL Server Insert results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\MS SQL Server\Insert"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\MS SQL Server\Insert\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\MSSQLServer_Insert.jmx"  -l "C:\code\performance_tests\jmeter\results\MS SQL Server\Insert\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\MS SQL Server\Insert\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
