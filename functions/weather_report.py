from typing import Literal
from functions.callable_function import CallableFunction


class WeatherReport(CallableFunction):
    city: str
    unit: Literal['°C', '°F']

    def call(self):
        return 'Weather report function not implemented yet'
