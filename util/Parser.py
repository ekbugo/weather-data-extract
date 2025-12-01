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
            # The summary tables are typically in a specific section
            # Look for the summary data in the page

            # Try to find Temperature High/Low
            temp_elements = doc.xpath('//span[contains(text(), "Temperature")]/ancestor::tr[1]//td')
            if len(temp_elements) >= 2:
                high_temp_text = temp_elements[0].text_content().strip()
                low_temp_text = temp_elements[1].text_content().strip()

                # Extract numeric value (remove °F, °C, etc.)
                high_match = re.search(r'([\d.]+)', high_temp_text)
                low_match = re.search(r'([\d.]+)', low_temp_text)

                if high_match:
                    summary_data["MaxTemp"] = float(high_match.group(1))
                if low_match:
                    summary_data["MinTemp"] = float(low_match.group(1))

            # Try to find Wind Gust High
            gust_elements = doc.xpath('//span[contains(text(), "Wind Gust")]/ancestor::tr[1]//td')
            if len(gust_elements) >= 1:
                high_gust_text = gust_elements[0].text_content().strip()
                gust_match = re.search(r'([\d.]+)', high_gust_text)
                if gust_match:
                    summary_data["MaxGust"] = float(gust_match.group(1))

            # Try to find Precipitation High
            precip_elements = doc.xpath('//span[contains(text(), "Precipitation")]/ancestor::tr[1]//td')
            if len(precip_elements) >= 1:
                high_precip_text = precip_elements[0].text_content().strip()
                precip_match = re.search(r'([\d.]+)', high_precip_text)
                if precip_match:
                    summary_data["SumPrec"] = float(precip_match.group(1))

        except Exception as e:
            print(f"Error parsing summary table: {e}")

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
