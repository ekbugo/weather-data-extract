@echo off
REM Weather Data Scraper - Automated Daily Run
REM This script runs the weather scraper and logs output

REM Set the working directory to the script location
cd /d "%~dp0"

REM Log file with timestamp
set LOGFILE=logs\scraper_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Run the Python script and log output
echo ============================================== >> %LOGFILE%
echo Weather Scraper Run: %date% %time% >> %LOGFILE%
echo ============================================== >> %LOGFILE%

python weather_scraper.py >> %LOGFILE% 2>&1

REM Log completion
echo. >> %LOGFILE%
echo Completed: %date% %time% >> %LOGFILE%
echo ============================================== >> %LOGFILE%
echo. >> %LOGFILE%

REM Exit
exit
