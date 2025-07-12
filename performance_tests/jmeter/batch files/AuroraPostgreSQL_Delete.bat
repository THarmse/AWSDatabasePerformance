@echo off
REM -----------------------------------------------------------------------------
REM Theodor Harmse for the University of Liverpool
REM Batch file to clean Aurora PostgreSQL Delete results folder and run Apache JMeter Delete test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing Aurora PostgreSQL Delete results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\Aurora PostgreSQL\Delete"

echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\Aurora PostgreSQL\Delete\report"

echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\AuroraPostgreSQL_Delete.jmx"  -l "C:\code\performance_tests\jmeter\results\Aurora PostgreSQL\Delete\results.jtl"  -e -o "C:\code\performance_tests\jmeter\results\Aurora PostgreSQL\Delete\report"

echo === JMeter test completed ===

echo Press any key to exit...
cmd /k
