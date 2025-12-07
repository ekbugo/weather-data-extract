from datetime import date, timedelta
import os

# Automatically get yesterday's date
yesterday = date.today() - timedelta(days=1)

START_DATE = yesterday
END_DATE = yesterday

UNIT_SYSTEM = "imperial"
FIND_FIRST_DATE = False

# Output directory for JSON files (relative to this script)
# This should point to the weather-game/backend/data directory
OUTPUT_DIR = os.path.join('..', 'weather-game', 'backend', 'data')