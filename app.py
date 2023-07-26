import json
import os
from slack_bolt import App, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests

from openai_helper import OpenAi


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
    ai = OpenAi()
    print(json.dumps(event))
    if 'thread_ts' in event and event['thread_ts'] != event['ts']:
        say(
            thread_ts = event['ts'],
            text = ai.get_answer(event['text'], event['user'])
        )
    elif event['channel_type'] == 'im':
        say(ai.get_answer(event['text'], event['user']))


@app.event('app_mention')
def event_mention(say: Say, event):
    ai = OpenAi()
    print(json.dumps(event))
    say(
        thread_ts = event['ts'],
        text = ai.get_answer(event['text'], event['user'])
    )




if __name__ == '__main__':
    SocketModeHandler(app, os.environ['SLACK_APP_TOKEN']).start()

