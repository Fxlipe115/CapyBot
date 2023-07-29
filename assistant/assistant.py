from functools import wraps
import json
import os
from typing import Callable, List, Literal, TypedDict
import openai
from assistant.types import AssistantAnswer

from functions.functions import Functions
from functions.generate_image import GenerateImage
from functions.weather_report import WeatherReport

Roles = Literal['system', 'user', 'assistant', 'function']

class Assistant():
    class GptMessage(TypedDict):
        role: Roles
        content: str

    context: List[GptMessage]
    base_assumptions: List[str]
    functions: Functions

    def __init__(self) -> None:
        self.__base_assumptions()
        self.functions = Functions()
        self.functions.register(
            'get_weather_report',
            'Return the weather report for a given city', 
            WeatherReport
        )
        self.functions.register(
            'generate_image', 
            'Calls Dall-e with a detailed prompt and returns a generated image', 
            GenerateImage
        )

    @property
    def model(self) -> str:
        return 'gpt-3.5-turbo-0613'

    def get_answer(self, message: str, user_talking: str) -> AssistantAnswer:
        openai.organization = os.getenv('OPENAI_ORGANIZATION')
        openai.api_key = os.getenv('OPENAI_API_KEY')

        self.__add_message(
            'system', f'The name of the person talking to you is <@{user_talking}>!')
        self.__add_message('user', message)

        completion = self.__call_chat_gpt()

        if completion.choices[0].finish_reason == 'function_call':
            function_call = completion.choices[0].message.function_call
            function_name = function_call.name
            arguments = json.loads(function_call.arguments)
            return self.functions.call_function(function_name, **arguments)
        else:
            content = completion.choices[0].message.content
            self.__add_message('assistant', content)
            return AssistantAnswer(text=content)

    def personality_trait(self, func: Callable[[], str]):
        @wraps
        def wrapper():
            self.__add_message('system', func())
        return wrapper
            

    def __base_assumptions(self) -> None:
        self.context = []
        self.__add_message(
            'system', 'You are a helpful and friendly capybara assistant for Team Capybara.')
        self.__add_message(
            'system', 'You are a helpful and friendly capybara assistant for Team Capybara.')
        self.__add_message('system', 'Your name is <@U05K30V08U9>.')
        self.__add_message('system', 'You are a Slack bot.')
        self.__add_message(
            'system', 'Every time someone makes a conversation, it is directed to you.')
        self.__add_message('system', 'You were created by Felipe Graeff.')
        self.__add_message(
            'system', 'You are native to Rio Grande do Sul, Brazil.')
        self.__add_message(
            'system', 'When answering in portuguese you speak with the dialect of Rio Grande do Sul in Brazil.')
        self.__add_message('system', 'You answer with capybara puns.')
        self.__add_message(
            'system', 'You use a lot of emojis in your answers.')

    def __add_message(self, role: Roles, content: str):
        self.context.append({"role": role, "content": content})

    def __call_chat_gpt(self):
        return openai.ChatCompletion.create(
            model=self.model,
            messages=self.context,
            functions=self.functions.get_functions()
        )
