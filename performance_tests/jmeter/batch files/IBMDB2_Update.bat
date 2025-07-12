@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean IBM DB2 Update results folder and run Apache JMeter Update test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing IBM DB2 Update results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\IBM DB2\Update"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\IBM DB2\Update\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\IBMDB2_Update.jmx"  -l "C:\code\performance_tests\jmeter\results\IBM DB2\Update\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\IBM DB2\Update\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
