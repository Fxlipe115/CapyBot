from typing import Literal
from typing_extensions import override
from assistant.types import AssistantAnswer
from assistant.functions.callable_function import CallableFunction


class WeatherReport(CallableFunction):
    city: str
    unit: Literal['°C', '°F']

    @override
    def call(self) -> AssistantAnswer:
        return AssistantAnswer('Weather report function not implemented yet')
