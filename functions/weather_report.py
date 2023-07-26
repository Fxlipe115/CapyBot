from typing import Literal
from gpt_function import CallableFunction

class WeatherReport(CallableFunction):
    city: str
    unit: Literal['°C', '°F']

    def call(self):
        return f'report called with city={self.city} and unit={self.unit}'