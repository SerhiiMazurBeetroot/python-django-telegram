import json
import requests
from django.conf import settings


class Weather:
    def __init__(self, city_name):
        self.status = False
        self.message = ""
        self.fetch_weather_data(city_name)

    def fetch_weather_data(self, city_name):
        try:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&lang=en&appid="
                f"{settings.OPENWEATHERMAP_TOKEN}"
            )
            response = requests.get(url)
            data = response.json()

            if data["cod"] == 200:
                self.status = True
                self.message = (
                    f"{data['name']} - {self.get_name_country(data['sys']['country'])}\n\n"
                    f"<b>Temperature:</b> {data['main']['temp']} °C\n"
                    f"(min: {data['main']['temp_min']} °C, max: {data['main']['temp_max']} °C)\n"
                    f"<b>Wind speed:</b> {data['wind']['speed']} m/s\n"
                    f"<b>Humidity:</b> {data['main']['humidity']} %"
                )
            elif data["cod"] == "404":
                self.message = f"Error: {city_name} {data['message']}"
            else:
                self.message = f"Error: {data['cod']} {data['message']}"

        except requests.RequestException as e:
            self.message = f"Request error: {str(e)}"
        except json.JSONDecodeError as e:
            self.message = f"JSON decode error: {str(e)}"
        except KeyError as e:
            self.message = f"Missing data in response: {str(e)}"
        except Exception as e:
            self.message = f"An unexpected error occurred: {str(e)}"

    @staticmethod
    def get_name_country(country_code):
        countries = {
            "AU": "Australia",
            "AT": "Austria",
            "AZ": "Azerbaijan",
            "AX": "Åland Islands",
            "AL": "Albania",
            "DZ": "Algeria",
            "AS": "American Samoa",
            "VI": "U.S. Virgin Islands",
            "AI": "Anguilla",
            "AO": "Angola",
            "AD": "Andorra",
            "AQ": "Antarctica",
            "AG": "Antigua and Barbuda",
            "AR": "Argentina",
            "AW": "Aruba",
            "AF": "Afghanistan",
            "BS": "Bahamas",
            "BD": "Bangladesh",
            "BB": "Barbados",
            "BH": "Bahrain",
            "BZ": "Belize",
            "BE": "Belgium",
            "BJ": "Benin",
            "BM": "Bermuda",
            "BY": "Belarus",
            "BG": "Bulgaria",
            "BO": "Bolivia",
            "BA": "Bosnia and Herzegovina",
            "BW": "Botswana",
            "BR": "Brazil",
            "IO": "British Indian Ocean Territory",
            "VG": "British Virgin Islands",
            "BN": "Brunei",
            "BF": "Burkina Faso",
            "BI": "Burundi",
            "BT": "Bhutan",
            "VU": "Vanuatu",
            "VA": "Vatican City",
            "GB": "United Kingdom",
            "VE": "Venezuela",
            "VN": "Vietnam",
            "AM": "Armenia",
            "WF": "Wallis and Futuna",
            "GA": "Gabon",
            "HT": "Haiti",
            "GY": "Guyana",
            "GM": "Gambia",
            "GH": "Ghana",
            "GP": "Guadeloupe",
            "GT": "Guatemala",
            "GN": "Guinea",
            "GW": "Guinea-Bissau",
            "GG": "Guernsey",
            "HN": "Honduras",
            "HK": "Hong Kong",
            "GD": "Grenada",
            "GR": "Greece",
            "GE": "Georgia",
            "GU": "Guam",
            "GI": "Gibraltar",
            "GL": "Greenland",
            "DK": "Denmark",
            "CD": "DR Congo",
            "JE": "Jersey",
            "DJ": "Djibouti",
            "DM": "Dominica",
            "DO": "Dominican Republic",
            "UM": "United States Minor Outlying Islands",
            "EC": "Ecuador",
            "GQ": "Equatorial Guinea",
            "ER": "Eritrea",
            "EE": "Estonia",
            "ET": "Ethiopia",
            "EG": "Egypt",
            "YE": "Yemen",
            "ZM": "Zambia",
            "EH": "Western Sahara",
            "ZW": "Zimbabwe",
            "IL": "Israel",
            "IN": "India",
            "ID": "Indonesia",
            "IQ": "Iraq",
            "IR": "Iran",
            "IE": "Ireland",
            "IS": "Iceland",
            "ES": "Spain",
            "IT": "Italy",
            "JO": "Jordan",
            "CV": "Cape Verde",
            "KZ": "Kazakhstan",
            "KY": "Cayman Islands",
            "KH": "Cambodia",
            "CM": "Cameroon",
            "CA": "Canada",
            "QA": "Qatar",
            "KE": "Kenya",
            "KG": "Kyrgyzstan",
            "CN": "China",
            "CY": "Cyprus",
            "KI": "Kiribati",
            "CC": "Cocos (Keeling) Islands",
            "CO": "Colombia",
            "KM": "Comoros",
            "CG": "Republic of the Congo",
            "CR": "Costa Rica",
            "CI": "Ivory Coast",
            "CU": "Cuba",
            "KW": "Kuwait",
            "CW": "Curaçao",
            "LA": "Laos",
            "LV": "Latvia",
            "LS": "Lesotho",
            "LT": "Lithuania",
            "LR": "Liberia",
            "LB": "Lebanon",
            "LY": "Libya",
            "LI": "Liechtenstein",
            "LU": "Luxembourg",
            "MU": "Mauritius",
            "MR": "Mauritania",
            "MG": "Madagascar",
            "YT": "Mayotte",
            "MO": "Macau",
            "MW": "Malawi",
            "MY": "Malaysia",
            "ML": "Mali",
            "MV": "Maldives",
            "MT": "Malta",
            "MA": "Morocco",
            "MQ": "Martinique",
            "MH": "Marshall Islands",
            "MX": "Mexico",
            "MZ": "Mozambique",
            "MD": "Moldova",
            "MC": "Monaco",
            "MN": "Mongolia",
            "MS": "Montserrat",
            "MM": "Myanmar",
            "NA": "Namibia",
            "NR": "Nauru",
            "NP": "Nepal",
            "NE": "Niger",
            "NG": "Nigeria",
            "NL": "Netherlands",
            "AN": "Netherlands Antilles",
            "BQ": "Caribbean Netherlands",
            "NI": "Nicaragua",
            "DE": "Germany",
            "NU": "Niue",
            "NZ": "New Zealand",
            "NC": "New Caledonia",
            "NO": "Norway",
            "AE": "United Arab Emirates",
            "OM": "Oman",
            "BV": "Bouvet Island",
            "IM": "Isle of Man",
            "NF": "Norfolk Island",
            "CX": "Christmas Island",
            "SH": "Saint Helena, Ascension and Tristan da Cunha",
            "HM": "Heard Island and McDonald Islands",
            "CK": "Cook Islands",
            "PK": "Pakistan",
            "PW": "Palau",
            "PS": "Palestine",
            "PA": "Panama",
            "PG": "Papua New Guinea",
            "PY": "Paraguay",
            "PE": "Peru",
            "ZA": "South Africa",
            "GS": "South Georgia and the South Sandwich Islands",
            "KR": "South Korea",
            "SS": "South Sudan",
            "KP": "North Korea",
            "MK": "North Macedonia",
            "MP": "Northern Mariana Islands",
            "PN": "Pitcairn Islands",
            "PL": "Poland",
            "PT": "Portugal",
            "PR": "Puerto Rico",
            "RE": "Réunion",
            "RU": "Russia",
            "RW": "Rwanda",
            "RO": "Romania",
            "SV": "El Salvador",
            "WS": "Samoa",
            "SM": "San Marino",
            "ST": "São Tomé and Príncipe",
            "SA": "Saudi Arabia",
            "SZ": "Eswatini",
            "SJ": "Svalbard and Jan Mayen",
            "SC": "Seychelles",
            "BL": "Saint Barthélemy",
            "SN": "Senegal",
            "MF": "Saint Martin",
            "PM": "Saint Pierre and Miquelon",
            "VC": "Saint Vincent and the Grenadines",
            "KN": "Saint Kitts and Nevis",
            "LC": "Saint Lucia",
            "RS": "Serbia",
            "SY": "Syria",
            "SG": "Singapore",
            "SX": "Sint Maarten",
            "SK": "Slovakia",
            "SI": "Slovenia",
            "SB": "Solomon Islands",
            "SO": "Somalia",
            "US": "United States",
            "SD": "Sudan",
            "SR": "Suriname",
            "TL": "East Timor",
            "SL": "Sierra Leone",
            "TJ": "Tajikistan",
            "TH": "Thailand",
            "TW": "Taiwan",
            "TZ": "Tanzania",
            "TC": "Turks and Caicos Islands",
            "TG": "Togo",
            "TK": "Tokelau",
            "TO": "Tonga",
            "TT": "Trinidad and Tobago",
            "TV": "Tuvalu",
            "TN": "Tunisia",
            "TR": "Turkey",
            "TM": "Turkmenistan",
            "UG": "Uganda",
            "HU": "Hungary",
            "UZ": "Uzbekistan",
            "UA": "Ukraine",
            "UY": "Uruguay",
            "FO": "Faroe Islands",
            "FM": "Federated States of Micronesia",
            "FJ": "Fiji",
            "PH": "Philippines",
            "FI": "Finland",
            "FK": "Falkland Islands",
            "FR": "France",
            "GF": "French Guiana",
            "PF": "French Polynesia",
            "TF": "French Southern and Antarctic Lands",
            "HR": "Croatia",
            "CF": "Central African Republic",
            "TD": "Chad",
            "CZ": "Czech Republic",
            "CL": "Chile",
            "ME": "Montenegro",
            "CH": "Switzerland",
            "SE": "Sweden",
            "LK": "Sri Lanka",
            "JM": "Jamaica",
            "JP": "Japan",
        }

        return countries.get(country_code, country_code)
