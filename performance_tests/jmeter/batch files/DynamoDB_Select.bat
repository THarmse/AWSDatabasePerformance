@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean DynamoDB Select results folder and run Apache JMeter Select test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing DynamoDB Select results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\DynamoDB\Select"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\DynamoDB\Select\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\DynamoDB_Select.jmx"  -l "C:\code\performance_tests\jmeter\results\DynamoDB\Select\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\DynamoDB\Select\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
