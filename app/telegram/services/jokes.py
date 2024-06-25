# https://jokeapi.dev/

from jokeapi import Jokes as JokeAPI
import requests
import requests


class Jokes:
    def __init__(self, lang):
        self.base_url = f"https://v2.jokeapi.dev/joke/Any?lang={lang}"

    def get_joke(self):
        try:
            response = requests.get(self.base_url)
            data = response.json()

            if data["error"] == False:
                return self.format_joke(data)
            else:
                return data["message"]

        except requests.RequestException as e:
            return f"Error fetching joke: {str(e)}"
        except (KeyError, ValueError) as e:
            return f"Error parsing joke data: {str(e)}"

    def format_joke(self, data):
        if data["type"] == "single":
            return data["joke"]
        elif data["type"] == "twopart":
            return f"{data['setup']}\n{data['delivery']}"
