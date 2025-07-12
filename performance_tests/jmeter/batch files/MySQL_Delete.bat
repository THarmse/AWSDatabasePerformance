@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean MySQL Delete results folder and run Apache JMeter Delete test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing MySQL Delete results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\MySQL\Delete"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\MySQL\Delete\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\MySQL_Delete.jmx"  -l "C:\code\performance_tests\jmeter\results\MySQL\Delete\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\MySQL\Delete\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
