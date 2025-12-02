import json
from datetime import date


class JsonExtractor:
    """Saves weather summary statistics to JSON files"""

    @staticmethod
    def save_summary_to_json(summary_data, station_id, end_date):
        """
        Saves pre-extracted summary data directly to JSON file.

        Args:
            summary_data: Dictionary with MaxTemp, MinTemp, MaxGust, SumPrec
            station_id: Weather station ID (e.g., 'IAGUAD73')
            end_date: End date as date object or string (YYYY-MM-DD)

        Returns:
            Path to the created JSON file
        """
        # Convert date to string if needed
        if isinstance(end_date, date):
            end_date_str = end_date.strftime('%Y-%m-%d')
        else:
            end_date_str = str(end_date)

        # Create JSON filename
        json_filename = f"{station_id}_{end_date_str}.json"

        # Write JSON file
        try:
            with open(json_filename, 'w') as jsonfile:
                json.dump(summary_data, jsonfile, indent=4)
            print(f"JSON file created: {json_filename}")
            return json_filename
        except Exception as e:
            print(f"Error writing JSON file: {e}")
            return None
