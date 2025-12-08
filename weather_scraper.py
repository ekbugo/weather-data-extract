# Made with love by Karl
# Contact me on Telegram: @karlpy

import requests
import lxml.html as lh
import os

import config

from util.Parser import Parser
from util.Utils import Utils
from util.JsonExtractor import JsonExtractor
from util.GitHelper import GitHelper

# configuration
stations_file = open('stations.txt', 'r')
URLS = stations_file.readlines()
# Date format: YYYY-MM-DD
START_DATE = config.START_DATE
END_DATE = config.END_DATE
# find the first data entry automatically
FIND_FIRST_DATE = config.FIND_FIRST_DATE
# output directory for JSON files
OUTPUT_DIR = config.OUTPUT_DIR


def scrap_station(weather_station_url):
    """
    Scrapes weather summary statistics from a weather station URL.
    Extracts data directly from webpage summary tables and saves to JSON.
    """
    session = requests.Session()
    timeout = 5
    global START_DATE
    global END_DATE
    global FIND_FIRST_DATE

    if FIND_FIRST_DATE:
        # find first date
        first_date_with_data = Utils.find_first_data_entry(weather_station_url=weather_station_url, start_date=START_DATE)
        # if first date found
        if(first_date_with_data != -1):
            START_DATE = first_date_with_data

    url_gen = Utils.date_url_generator(weather_station_url, START_DATE, END_DATE)
    station_name = weather_station_url.split('/')[-1]

    # Track summary statistics across all dates
    aggregated_summary = {
        "MaxTemp": None,
        "MinTemp": None,
        "MaxGust": None,
        "SumPrec": None
    }

    for date_string, url in url_gen:
        try:
            print(f'Scraping data from {url}')

            # Fetch the webpage
            html_string = session.get(url, timeout=timeout)
            doc = lh.fromstring(html_string.content)

            # Extract summary statistics from the page
            daily_summary = Parser.parse_summary_table(doc)

            # Aggregate summary data across all dates
            if daily_summary["MaxTemp"] is not None:
                if aggregated_summary["MaxTemp"] is None or daily_summary["MaxTemp"] > aggregated_summary["MaxTemp"]:
                    aggregated_summary["MaxTemp"] = daily_summary["MaxTemp"]
            if daily_summary["MinTemp"] is not None:
                if aggregated_summary["MinTemp"] is None or daily_summary["MinTemp"] < aggregated_summary["MinTemp"]:
                    aggregated_summary["MinTemp"] = daily_summary["MinTemp"]
            if daily_summary["MaxGust"] is not None:
                if aggregated_summary["MaxGust"] is None or daily_summary["MaxGust"] > aggregated_summary["MaxGust"]:
                    aggregated_summary["MaxGust"] = daily_summary["MaxGust"]
            if daily_summary["SumPrec"] is not None:
                if aggregated_summary["SumPrec"] is None or daily_summary["SumPrec"] > aggregated_summary["SumPrec"]:
                    aggregated_summary["SumPrec"] = daily_summary["SumPrec"]

            print(f'Extracted summary: MaxTemp={daily_summary["MaxTemp"]}, MinTemp={daily_summary["MinTemp"]}, MaxGust={daily_summary["MaxGust"]}, SumPrec={daily_summary["SumPrec"]}')

        except Exception as e:
            print(f'Error scraping {url}: {e}')

    # Save aggregated summary statistics to JSON
    print(f'Saving summary statistics to JSON for {station_name}')
    json_file = JsonExtractor.save_summary_to_json(aggregated_summary, station_name, END_DATE, OUTPUT_DIR)
    return json_file


# Track created JSON files for git commit
created_json_files = []

for url in URLS:
    url = url.strip()
    print(url)
    json_file = scrap_station(url)
    if json_file:
        # Get just the filename (not the full path) for git add
        json_filename = os.path.basename(json_file)
        created_json_files.append(os.path.join('backend', 'data', json_filename))

# After all scraping is done, commit and push to weather-game repo
if created_json_files:
    print("\n" + "="*80)
    print("Committing and pushing to weather-game repository...")
    print("="*80)

    # Get the weather-game repo path (one level up from current dir, then weather-game)
    weather_game_repo = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'weather-game')

    success = GitHelper.commit_and_push(weather_game_repo, created_json_files, END_DATE)

    if success:
        print("\n✓ Successfully committed and pushed weather data!")
    else:
        print("\n✗ Failed to commit and push weather data. Please check errors above.")
else:
    print("\nNo JSON files were created.")