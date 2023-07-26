import json
import os
import openai
from slack_bolt import App, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
from pydantic import BaseModel
from typing import Literal


# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ['SLACK_BOT_TOKEN'])

@app.command('/capyoftheday')
def dailycapy_command(ack, say: Say):
    ack()

    url = 'https://api.capy.lol/v1/capyoftheday?json=true'
    response = requests.get(url)

    response.raise_for_status()  # raises exception when not a 2xx response
    response_json = ''
    if response.status_code != 204:
        response_json = response.json()

    response_json = response.json()
    if response_json != '' and response_json['success']:
        print('Sending capy of the day')
        data = response_json['data']
        print(json.dumps(data, ident=2))
        say(
            blocks = [
                {
                    'type': 'section',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Here is your daily capybara :capybara2:',
                        'emoji': True
                    }
                },
                {
                'type': 'image',
                'image_url': data['url'],
                'alt_text': data['alt']
                }
            ]
        )
    else:
        say('Daily Capy failed. Try again later.')



@app.event('message')
def handle_message_events(say: Say, event):
    print(json.dumps(event))
    if 'thread_ts' in event and event['thread_ts'] != event['ts']:
        say(
            thread_ts = event['ts'],
            text = get_answer(event['text'], event['user'])
        )
    elif event['channel_type'] == 'im':
        say(get_answer(event['text'], event['user']))


@app.event('app_mention')
def event_mention(say: Say, event):
    print(json.dumps(event))
    say(
        thread_ts = event['ts'],
        text = get_answer(event['text'], event['user'])
    )


class WeatherReport(BaseModel):
    city: str
    unit: Literal['°C', '°F']

def get_weather_report(city, unit):
    return f'report called with city={self.city} and unit={self.unit}'

completion_functions = {
    'get_weather_report': {
        'description': {
            "name": "get_weather_report",
            "description": "Get weather report for given city",
            "parameters": WeatherReport.model_json_schema()
        },
        'function': get_weather_report
    }
}

def get_answer(message: str, user_talking: str):
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
        functions=list(map(lambda x: x['description'], completion_functions.values()))
    )
    if completion.choices[0].finish_reason == 'function_call':
        function_call = completion.choices[0].message.function_call
        completion_function = completion_functions.get(function_call.name)
        # arguments = json.dumps(function_call.arguments)
        print(function_call.arguments)
        return completion_function['function'](*function_call.arguments)
    else:
        return completion.choices[0].message.content


if __name__ == '__main__':
    SocketModeHandler(app, os.environ['SLACK_APP_TOKEN']).start()

