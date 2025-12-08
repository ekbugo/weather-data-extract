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
            # Find the Temperature row
            temp_row = doc.xpath('//tr[.//span[contains(text(), "Temperature")] or .//*[contains(text(), "Temperature")]]')

            if temp_row:
                temp_tds = temp_row[0].xpath('.//td')

                if len(temp_tds) >= 2:
                    # td[0] = High, td[1] = Low, td[2] = Average
                    val1_text = temp_tds[0].text_content().strip()
                    val2_text = temp_tds[1].text_content().strip()

                    val1_match = re.search(r'([\d.]+)', val1_text)
                    val2_match = re.search(r'([\d.]+)', val2_text)

                    if val1_match and val2_match:
                        val1 = float(val1_match.group(1))
                        val2 = float(val2_match.group(1))

                        # Determine which is high and which is low by comparison
                        summary_data["MaxTemp"] = max(val1, val2)
                        summary_data["MinTemp"] = min(val1, val2)

            # Find the Wind Gust row
            gust_row = doc.xpath('//tr[.//span[contains(text(), "Wind Gust")] or .//*[contains(text(), "Wind Gust")]]')

            if gust_row:
                gust_tds = gust_row[0].xpath('.//td')

                if len(gust_tds) >= 1:
                    high_gust_text = gust_tds[0].text_content().strip()
                    gust_match = re.search(r'([\d.]+)', high_gust_text)

                    if gust_match:
                        summary_data["MaxGust"] = float(gust_match.group(1))

            # Find the Precipitation row
            precip_row = doc.xpath('//tr[.//span[contains(text(), "Precipitation")] or .//*[contains(text(), "Precipitation")]]')

            if precip_row:
                precip_tds = precip_row[0].xpath('.//td')

                if len(precip_tds) >= 1:
                    high_precip_text = precip_tds[0].text_content().strip()
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
