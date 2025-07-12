@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean IBM DB2 Insert results folder and run Apache JMeter Insert test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing IBM DB2 Insert results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\IBM DB2\Insert"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\IBM DB2\Insert\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\IBMDB2_Insert.jmx"  -l "C:\code\performance_tests\jmeter\results\IBM DB2\Insert\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\IBM DB2\Insert\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
