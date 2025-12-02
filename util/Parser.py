import unicodedata
from datetime import datetime
import re


class Parser:
    @staticmethod
    def format_key(key: str) -> str:
        # Replace white space and delete dots
        return key.replace(' ', '_').replace('.', '')

    @staticmethod
    def parse_summary_table(doc) -> dict:
        """
        Extracts summary statistics from the Weather Underground summary tables.
        Returns a dictionary with MaxTemp, MinTemp, MaxGust, and SumPrec.
        """
        summary_data = {
            "MaxTemp": None,
            "MinTemp": None,
            "MaxGust": None,
            "SumPrec": None
        }

        try:
            print("DEBUG: Searching for summary data...")

            # More precise strategy: Find the row containing the label, then get td siblings
            # Look for Temperature row
            temp_row = doc.xpath('//tr[.//span[contains(text(), "Temperature")] or .//*[contains(text(), "Temperature")]]')
            print(f"DEBUG: Found {len(temp_row)} temperature rows")

            if temp_row:
                # Get all td elements in this row
                temp_tds = temp_row[0].xpath('.//td')
                print(f"DEBUG: Found {len(temp_tds)} td elements in temperature row")

                if len(temp_tds) >= 3:  # Should have: label, high, low, average
                    high_temp_text = temp_tds[1].text_content().strip()  # Index 1 is "High"
                    low_temp_text = temp_tds[2].text_content().strip()   # Index 2 is "Low"
                    print(f"DEBUG: Temperature texts: High='{high_temp_text}', Low='{low_temp_text}'")

                    high_match = re.search(r'([\d.]+)', high_temp_text)
                    low_match = re.search(r'([\d.]+)', low_temp_text)

                    if high_match:
                        summary_data["MaxTemp"] = float(high_match.group(1))
                        print(f"DEBUG: MaxTemp = {summary_data['MaxTemp']}")
                    if low_match:
                        summary_data["MinTemp"] = float(low_match.group(1))
                        print(f"DEBUG: MinTemp = {summary_data['MinTemp']}")

            # Look for Wind Gust row
            gust_row = doc.xpath('//tr[.//span[contains(text(), "Wind Gust")] or .//*[contains(text(), "Wind Gust")]]')
            print(f"DEBUG: Found {len(gust_row)} wind gust rows")

            if gust_row:
                gust_tds = gust_row[0].xpath('.//td')
                print(f"DEBUG: Found {len(gust_tds)} td elements in wind gust row")

                if len(gust_tds) >= 2:  # Should have: label, high, ...
                    high_gust_text = gust_tds[1].text_content().strip()  # Index 1 is "High"
                    print(f"DEBUG: Wind Gust text: '{high_gust_text}'")

                    gust_match = re.search(r'([\d.]+)', high_gust_text)
                    if gust_match:
                        summary_data["MaxGust"] = float(gust_match.group(1))
                        print(f"DEBUG: MaxGust = {summary_data['MaxGust']}")
                    else:
                        print(f"DEBUG: No numeric value found in wind gust (probably '--')")

            # Look for Precipitation row
            precip_row = doc.xpath('//tr[.//span[contains(text(), "Precipitation")] or .//*[contains(text(), "Precipitation")]]')
            print(f"DEBUG: Found {len(precip_row)} precipitation rows")

            if precip_row:
                precip_tds = precip_row[0].xpath('.//td')
                print(f"DEBUG: Found {len(precip_tds)} td elements in precipitation row")

                if len(precip_tds) >= 2:  # Should have: label, high, ...
                    high_precip_text = precip_tds[1].text_content().strip()  # Index 1 is "High"
                    print(f"DEBUG: Precipitation text: '{high_precip_text}'")

                    precip_match = re.search(r'([\d.]+)', high_precip_text)
                    if precip_match:
                        summary_data["SumPrec"] = float(precip_match.group(1))
                        print(f"DEBUG: SumPrec = {summary_data['SumPrec']}")
                    else:
                        print(f"DEBUG: No numeric value found in precipitation (probably '--')")

        except Exception as e:
            print(f"Error parsing summary table: {e}")
            import traceback
            traceback.print_exc()

        print(f"DEBUG: Final summary_data = {summary_data}")
        return summary_data

    @staticmethod
    def parse_html_table(date_string: str, history_table: list) -> dict:

        table_rows = [tr for tr in history_table[0].xpath('//tr') if len(tr) == 12]
        headers_list = []
        data_rows = []

        # set Table Headers
        for header in table_rows[0]:
            headers_list.append(header.text)

        for tr in table_rows[1:]:
            row_dict = {}
            for i, td in enumerate(tr.getchildren()):
                td_content = unicodedata.normalize("NFKD", td.text_content())

                # set date and time in the first 2 columns
                if i == 0:
                    date = datetime.strptime(date_string, "%Y-%m-%d")
                    time = datetime.strptime(td_content, "%I:%M %p")
                    row_dict['Date'] = date.strftime('%Y/%m/%d')
                    row_dict['Time'] = time.strftime('%I:%M %p')
                else:
                    row_dict[Parser.format_key(headers_list[i])] = td_content

            data_rows.append(row_dict)
        
        return data_rows
