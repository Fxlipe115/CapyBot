import json
import os
from typing import List, Literal, TypedDict
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
        self._base_assumptions()
        self.functions = Functions()
        self.functions.register('get_weather_report', 'Return the weather report for a given city', WeatherReport)


    def get_answer(self, message: str, user_talking: str):
        openai.organization = os.getenv('OPENAI_ORGANIZATION')
        openai.api_key = os.getenv('OPENAI_API_KEY')

        self._add_message({'system', f'The name of the person talking to you is <@{user_talking}>!'})
        self._add_message({'user', message})

        completion = self._call_chat_gpt()
        
        if completion.choices[0].finish_reason == 'function_call':
            function_call = completion.choices[0].message.function_call
            function_name = function_call.name
            arguments = json.loads(function_call.arguments)
            return self.functions.call_function(function_name, **arguments)
        else:
            return completion.choices[0].message.content
        

    def _base_assumptions(self) -> List[GptMessage]:
        self.context = []
        self._add_message('system', 'You are a helpful and friendly capybara assistant for Team Capybara.')
        self._add_message('system', 'You are a helpful and friendly capybara assistant for Team Capybara.')
        self._add_message('system', 'Your name is <@U05K30V08U9>.')
        self._add_message('system', 'You are a Slack bot.')
        self._add_message('system', 'Everytime someone makes a conversation, it is directed to you.')
        self._add_message('system', 'You were created by Felipe Graeff.')
        self._add_message('system', 'You are native to Rio Grande do Sul, Brazil.')
        self._add_message('system', 'When answering in portuguese you speak with the dialect of Rio Grande do Sul in Brazil.')
        self._add_message('system', 'You answer with capybara puns.')
    

    def _add_message(self, role: Roles, content: str):
        self.context.append({"role":role, "content": content})


    def _call_chat_gpt(self):
        return openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=self.context,
            functions=self.functions.get_functions()
        )