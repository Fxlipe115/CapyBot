from ast import List
import json
import os
from typing import Literal, TypedDict
import openai

from functions.functions import Functions
from functions.weather_report import WeatherReport

Roles = Literal['system', 'user']
class OpenAi():
    class GptMessage(TypedDict):
        role: Roles
        content: str

    context: List[GptMessage]
    base_assumptions: List[str]
    functions: Functions

    def __init__(self) -> None:
        self.context = self._base_assumptions()
        self.functions = Functions()
        self.functions.register('get_weather_report', 'Return the weather report for a given city', WeatherReport)


    def get_answer(self, message: str, user_talking: str):
        openai.organization = os.getenv('OPENAI_ORGANIZATION')
        openai.api_key = os.getenv('OPENAI_API_KEY')

        self.base_assumptions.append(f'The name of the person talking to you is <@{user_talking}>!')
        
        self._add_message({'role': 'user', 'content': message})

        completion = self._call_chat_gpt()
        
        if completion.choices[0].finish_reason == 'function_call':
            function_call = completion.choices[0].message.function_call
            function_name = function_call.name
            arguments = json.loads(function_call.arguments)
            return self.functions.call_function(function_name, **arguments)
        else:
            return completion.choices[0].message.content
        

    def _base_assumptions(self) -> List[GptMessage]:
        return [
            'You are a helpful and friendly capybara assistant for Team Capybara.',
            'Your name is <@U05K30V08U9>.',
            'You are a Slack bot.',
            'Everytime someone makes a conversation, it is directed to you.',
            'You were created by Felipe Graeff.',
            'You are native to Rio Grande do Sul, Brazil',
            'When answering in portuguese you speak with the dialect of Rio Grande do Sul in Brazil',
            'You answer with capybara puns.'
        ]
    

    def _add_message(self, message: GptMessage):
        self.context.append(message)


    def _call_chat_gpt(self):
        return openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=self.context,
            functions=self.functions.get_functions()
        )
