@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean DynamoDB Insert results folder and run Apache JMeter Insert test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing DynamoDB Insert results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\DynamoDB\Insert"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\DynamoDB\Insert\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\DynamoDB_Insert.jmx"  -l "C:\code\performance_tests\jmeter\results\DynamoDB\Insert\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\DynamoDB\Insert\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
