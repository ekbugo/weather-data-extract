import csv
import json
from datetime import date


class JsonExtractor:
    """Extracts summary statistics from weather data and saves to JSON"""

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
    """Extracts summary statistics from weather CSV files and saves to JSON"""

    @staticmethod
    def extract_to_json(csv_file_path, station_id, end_date):
        """
        Extracts weather statistics from CSV and saves to JSON file.

        Args:
            csv_file_path: Path to the CSV file
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

        # Initialize tracking variables
        max_temp = None
        min_temp = None
        sum_prec = None
        max_gust = None

        try:
            with open(csv_file_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    # Extract Temperature_F values
                    try:
                        temp_f = float(row.get('Temperature_F', '').strip())
                        if max_temp is None or temp_f > max_temp:
                            max_temp = temp_f
                        if min_temp is None or temp_f < min_temp:
                            min_temp = temp_f
                    except (ValueError, AttributeError):
                        pass  # Skip invalid values

                    # Extract Precip_Accum_in values (take the highest)
                    try:
                        precip_accum = float(row.get('Precip_Accum_in', '').strip())
                        if sum_prec is None or precip_accum > sum_prec:
                            sum_prec = precip_accum
                    except (ValueError, AttributeError):
                        pass  # Skip invalid values

                    # Extract Gust_mph values
                    try:
                        gust = float(row.get('Gust_mph', '').strip())
                        if max_gust is None or gust > max_gust:
                            max_gust = gust
                    except (ValueError, AttributeError):
                        pass  # Skip invalid values

        except FileNotFoundError:
            print(f"Error: CSV file not found at {csv_file_path}")
            return None
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None

        # Prepare JSON data structure
        json_data = {
            "MaxTemp": max_temp,
            "MinTemp": min_temp,
            "MaxGust": max_gust,
            "SumPrec": sum_prec
        }

        # Create JSON filename
        json_filename = f"{station_id}_{end_date_str}.json"

        # Write JSON file
        try:
            with open(json_filename, 'w') as jsonfile:
                json.dump(json_data, jsonfile, indent=4)
            print(f"JSON file created: {json_filename}")
            return json_filename
        except Exception as e:
            print(f"Error writing JSON file: {e}")
            return None
