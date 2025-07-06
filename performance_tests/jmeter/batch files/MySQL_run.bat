@echo off
REM -----------------------------------------------------------------------------
REM Batch file to clean MySQL results folder and run Apache JMeter Insert test
REM -----------------------------------------------------------------------------

echo.
echo === Deleting existing MySQL results folder ===
rmdir /s /q "C:\code\performance_tests\jmeter\results\MySQL"

echo.
echo === Recreating required folders ===
mkdir "C:\code\performance_tests\jmeter\results\MySQL\Insert\report"

echo.
echo === Running JMeter Test ===
cd /d "C:\code\performance_tests\jmeter\bin"
jmeter -n -t "C:\code\performance_tests\jmeter\test plans\MySQL_Insert.jmx" ^
  -l "C:\code\performance_tests\jmeter\results\MySQL\Insert\results.jtl" ^
  -e -o "C:\code\performance_tests\jmeter\results\MySQL\Insert\report"

echo.
echo === JMeter test completed ===
echo.
echo Press any key to exit...
cmd /k
