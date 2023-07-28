import os
from slack_bolt import App, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
from assistant.contexts import Contexts


# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ['SLACK_BOT_TOKEN'])
contexts = Contexts()


@app.command('/capyoftheday')
def dailycapy_command(ack, say: Say):
    ack()

    url = 'https://api.capy.lol/v1/capyoftheday?json=true'
    response = requests.get(url, timeout=10)

    response.raise_for_status()  # raises exception when not a 2xx response
    response_json: str = ''
    if response.status_code != 204:
        response_json = response.json()

    response_json = response.json()
    if response_json != '' and response_json['success']:
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
def handle_message_events(say: Say, event):
    if 'thread_ts' in event and event['thread_ts'] != event['ts']:
        print('message')
        assistant = contexts.get_assistant(event['thread_ts'])
        say(
            thread_ts=event['thread_ts'],
            text=assistant.get_answer(event['text'], event['user'])
        )
    elif event['channel_type'] == 'im':
        print('Event: message:im')
        assistant = contexts.get_assistant(event['user'])
        say(assistant.get_answer(event['text'], event['user']))


@app.event('app_mention')
def event_mention(say: Say, event):
    print('Event: app_mention')
    assistant = contexts.get_assistant(event['ts'])
    say(
        thread_ts=event['ts'],
        text=assistant.get_answer(event['text'], event['user'])
    )


if __name__ == '__main__':
    SocketModeHandler(app, os.environ['SLACK_APP_TOKEN']).start()
