
from dataclasses import asdict
from slack_bolt import Say
from assistant import Assistant

from slack_message.types.slack_message import Event, Message

def handle_message_event(say: Say, event: Message, assistant: Assistant):
    if event.thread_ts is not None and event.thread_ts != event.ts:
        print('message')
        answer = assistant.get_answer(event.text, event.user, event.thread_ts)
        answer.thread_ts = event.thread_ts
        say(**asdict(answer))
    elif event.channel_type == 'im':
        print('Event: message:im')
        say(**asdict(assistant.get_answer(event.text, event.user, event.user)))


def handle_mention_event(say: Say, event: Event, assistant: Assistant):
    print('Event: app_mention')
    answer = assistant.get_answer(event.text, event.user, event.ts)
    answer.thread_ts = event.ts
    say(**asdict(answer))
