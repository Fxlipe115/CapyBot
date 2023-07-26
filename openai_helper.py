import json
import os
import openai

from functions.functions import Functions
from functions.weather_report import WeatherReport

class OpenAi():
    context: str

    def get_answer(self, message: str, user_talking: str):
        openai.organization = os.getenv('OPENAI_ORGANIZATION')
        openai.api_key = os.getenv('OPENAI_API_KEY')
        openai.Model.list()

        base_assumptions = [
            'You are a helpful and friendly capybara assistant for Team Capybara.',
            'Your name is <@U05K30V08U9>.',
            'You are a Slack bot.',
            'Everytime someone makes a conversation, it is directed to you.',
            'You were created by Felipe Graeff.',
            'You are native to Rio Grande do Sul, Brazil',
            'When answering in portuguese you speak with the dialect of Rio Grande do Sul in Brazil',
            'You answer with capybara puns.'
            f'The name of the person talking to you is <@{user_talking}>!'
        ]

        functions = Functions()
        functions.register('get_weather_report', 'Return the weather report for a given city', WeatherReport)

        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=[
                {
                    'role': 'system', 
                    'content': ' '.join(base_assumptions)
                },
                {
                    'role': 'user', 
                    'content': message
                }
            ],
            functions=functions.get_functions()
        )
        
        if completion.choices[0].finish_reason == 'function_call':
            function_call = completion.choices[0].message.function_call
            function_name = function_call.name
            arguments = json.loads(function_call.arguments)
            return functions.call_function(function_name, **arguments)
        else:
            return completion.choices[0].message.content
