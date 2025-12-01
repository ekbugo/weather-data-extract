from datetime import date, timedelta

# Automatically get yesterday's date
yesterday = date.today() - timedelta(days=1)

START_DATE = yesterday
END_DATE = yesterday

UNIT_SYSTEM = "imperial"
FIND_FIRST_DATE = False