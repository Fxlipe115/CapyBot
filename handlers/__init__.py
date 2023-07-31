
from dataclasses import asdict
from slack_bolt import Say
from slack_sdk import WebClient
from assistant import Assistant
from handlers.helpers import bot_is_part_of_thread, retrieve_thread

from slack_message.types import Event, Message

def handle_message_event(say: Say, event: Message, client: WebClient, assistant: Assistant):
    if event.thread_ts is not None and event.thread_ts != event.ts:
        if bot_is_part_of_thread(event, client):
            print('Event: message')
            _read_previous_conversation(event, client, assistant)
            answer = assistant.get_answer(event.text, event.thread_ts)
            answer.thread_ts = event.thread_ts
            say(**asdict(answer))
    elif event.channel_type == 'im':
        print('Event: message:im')
        if event.user not in assistant.contexts:
            assistant.add_system_message(
                f'The name of the person talking to you is <@{event.user}>!',
                event.ts
            )
        say(**asdict(assistant.get_answer(event.text, event.user)))

def _read_previous_conversation(event, client, assistant):
    if event.thread_ts not in assistant.contexts:
        for message in retrieve_thread(client, event.channel, event.thread_ts).messages:
            if message.user == 'U05K30V08U9':
                assistant.add_assistant_message(message.text, event.thread_ts)
            else:
                assistant.add_system_message(
                            f'The name of the person talking to you is <@{event.user}>!',
                            event.ts
                        )
                assistant.add_user_message(message.text, event.thread_ts)

def handle_mention_event(say: Say, event: Event, assistant: Assistant):
    print('Event: app_mention')
    if event.ts not in assistant.contexts:
        assistant.add_system_message(
            f'The name of the person talking to you is <@{event.user}>!',
            event.ts
        )
    answer = assistant.get_answer(event.text, event.ts)
    answer.thread_ts = event.ts
    say(**asdict(answer))
