from slack_bolt import Ack, App, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from environs import Env
import requests

from assistant import Assistant
from functions.generate_image import GenerateImage
from functions.weather_report import WeatherReport
from handlers import handle_mention_event, handle_message_event
from slack_message.types import Message, Event

env = Env()
env.read_env()
SLACK_BOT_TOKEN = env('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = env('SLACK_APP_TOKEN')
PERSONALITY_TRAITS = env.list('PERSONALITY', subcast=lambda x: x.strip('\'"'), delimiter=':')
OPENAI_ORGANIZATION = env('OPENAI_ORGANIZATION')
OPENAI_API_KEY = env('OPENAI_API_KEY')


# Install the Slack app and get xoxb- token in advance
app = App(token=SLACK_BOT_TOKEN)
assistant = Assistant(OPENAI_ORGANIZATION, OPENAI_API_KEY)
assistant.functions.register(
    'get_weather_report',
    'Return the weather report for a given city',
    WeatherReport
)
assistant.functions.register(
    'generate_image',
    'Calls Dall-e with a detailed prompt and returns a generated image',
    GenerateImage
)

assistant.set_personality_traits(PERSONALITY_TRAITS)


@app.command('/capyoftheday')
def dailycapy_command(ack: Ack, say: Say):
    ack()

    url = 'https://api.capy.lol/v1/capyoftheday?json=true'
    response = requests.get(url, timeout=10)

    response.raise_for_status()  # raises exception when not a 2xx response
    response_json = {}
    if response.status_code != 204:
        response_json = response.json()

    response_json = response.json()
    if response_json != {} and response_json['success']:
        print('Sending capy of the day')
        data = response_json['data']
        say(
            blocks=[
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
def event_message(say: Say, client: WebClient, event):
    handle_message_event(say, Message.from_dict(event), client, assistant)


@app.event('app_mention')
def event_mention(say: Say, event):
    handle_mention_event(say, Event.from_dict(event), assistant)


if __name__ == '__main__':
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
