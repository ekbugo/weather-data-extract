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

            # Strategy 1: Look for elements containing the labels
            temp_elements = doc.xpath('//span[contains(text(), "Temperature")]/ancestor::tr[1]//td')
            print(f"DEBUG: Found {len(temp_elements)} temperature td elements (strategy 1)")

            # Strategy 2: Try looking in the entire document for Temperature labels
            if len(temp_elements) < 2:
                temp_elements = doc.xpath('//*[contains(text(), "Temperature")]/following::*//td')
                print(f"DEBUG: Found {len(temp_elements)} temperature td elements (strategy 2)")

            # Strategy 3: Look for the summary section specifically
            if len(temp_elements) < 2:
                # Try to find summary container
                summary_container = doc.xpath('//*[contains(@class, "summary") or contains(text(), "Summary")]')
                print(f"DEBUG: Found {len(summary_container)} summary containers")
                if summary_container:
                    temp_elements = summary_container[0].xpath('.//tr[contains(., "Temperature")]//td')
                    print(f"DEBUG: Found {len(temp_elements)} temperature td elements in summary (strategy 3)")

            if len(temp_elements) >= 2:
                high_temp_text = temp_elements[0].text_content().strip()
                low_temp_text = temp_elements[1].text_content().strip()
                print(f"DEBUG: Temperature texts: High='{high_temp_text}', Low='{low_temp_text}'")

                # Extract numeric value (remove °F, °C, etc.)
                high_match = re.search(r'([\d.]+)', high_temp_text)
                low_match = re.search(r'([\d.]+)', low_temp_text)

                if high_match:
                    summary_data["MaxTemp"] = float(high_match.group(1))
                    print(f"DEBUG: MaxTemp = {summary_data['MaxTemp']}")
                if low_match:
                    summary_data["MinTemp"] = float(low_match.group(1))
                    print(f"DEBUG: MinTemp = {summary_data['MinTemp']}")

            # Try to find Wind Gust High
            gust_elements = doc.xpath('//span[contains(text(), "Wind Gust")]/ancestor::tr[1]//td')
            print(f"DEBUG: Found {len(gust_elements)} wind gust td elements")

            if len(gust_elements) < 1:
                gust_elements = doc.xpath('//*[contains(text(), "Wind Gust")]/following::*//td')
                print(f"DEBUG: Found {len(gust_elements)} wind gust td elements (strategy 2)")

            if len(gust_elements) >= 1:
                high_gust_text = gust_elements[0].text_content().strip()
                print(f"DEBUG: Wind Gust text: '{high_gust_text}'")
                gust_match = re.search(r'([\d.]+)', high_gust_text)
                if gust_match:
                    summary_data["MaxGust"] = float(gust_match.group(1))
                    print(f"DEBUG: MaxGust = {summary_data['MaxGust']}")

            # Try to find Precipitation High
            precip_elements = doc.xpath('//span[contains(text(), "Precipitation")]/ancestor::tr[1]//td')
            print(f"DEBUG: Found {len(precip_elements)} precipitation td elements")

            if len(precip_elements) < 1:
                precip_elements = doc.xpath('//*[contains(text(), "Precipitation")]/following::*//td')
                print(f"DEBUG: Found {len(precip_elements)} precipitation td elements (strategy 2)")

            if len(precip_elements) >= 1:
                high_precip_text = precip_elements[0].text_content().strip()
                print(f"DEBUG: Precipitation text: '{high_precip_text}'")
                precip_match = re.search(r'([\d.]+)', high_precip_text)
                if precip_match:
                    summary_data["SumPrec"] = float(precip_match.group(1))
                    print(f"DEBUG: SumPrec = {summary_data['SumPrec']}")

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
