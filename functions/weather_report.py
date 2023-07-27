from typing import Literal
import requests
from functions.callable_function import CallableFunction

class WeatherReport(CallableFunction):
    city: str
    unit: Literal['°C', '°F']

    def call(self):
        self.city = self.city.replace(' ', '+')
        url = f'https://wttr.in/{self.city}'
        response = requests.get(url)
        # return f'report called with city={self.city} and unit={self.unit}'
        return f'{response.json()}'