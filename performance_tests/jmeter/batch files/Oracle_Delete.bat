@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean Oracle Delete results folder and run Apache JMeter Delete test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing Oracle Delete results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\Oracle\Delete"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\Oracle\Delete\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\OracleDB_Delete.jmx"  -l "C:\code\performance_tests\jmeter\results\Oracle\Delete\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\Oracle\Delete\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
