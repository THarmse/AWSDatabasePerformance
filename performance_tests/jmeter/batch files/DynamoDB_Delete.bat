@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean DynamoDB Delete results folder and run Apache JMeter Delete test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing DynamoDB Delete results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\DynamoDB\Delete"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\DynamoDB\Delete\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\DynamoDB_Delete.jmx"  -l "C:\code\performance_tests\jmeter\results\DynamoDB\Delete\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\DynamoDB\Delete\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
