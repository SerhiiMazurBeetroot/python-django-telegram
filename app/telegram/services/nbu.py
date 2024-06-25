import json
import requests
from datetime import datetime


class Nbu:
    char_format_date = "%Y%m%d"

    def __init__(self, date_cred: datetime, curr_code: str):
        self.status = False
        self.message = ""
        self.fetch_exchange_rate(date_cred, curr_code)

    def fetch_exchange_rate(self, date_cred: datetime, curr_code: str):
        try:
            formatted_url = (
                "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
                "?valcode={}&date={}&json".format(
                    curr_code, date_cred.strftime(self.char_format_date)
                )
            )

            response = requests.get(formatted_url)
            response.raise_for_status()

            json_object = response.json()

            if json_object:
                self.status = True
                row = json_object[0]
                self.message = f"1 {row['cc']} = {float(row['rate'])} UAH"
            else:
                self.message = f"Currency {curr_code} not found"

        except requests.RequestException as e:
            self.message = f"Request error: {str(e)}"
        except json.JSONDecodeError as e:
            self.message = f"JSON decode error: {str(e)}"
        except (KeyError, IndexError) as e:
            self.message = f"Data parsing error: {str(e)}"
        except Exception as e:
            self.message = f"An unexpected error occurred: {str(e)}"
