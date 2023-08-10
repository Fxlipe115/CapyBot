from slack_sdk import WebClient

from slack_message.types import ConversationReplies, ThreadParent


def retrieve_message(client: WebClient, channel: str, ts: str):
    client.conversations_history(
        channel=channel,
        oldest=ts,
        inclusive=True,
        limit=1
    )


def retrieve_thread(client: WebClient, channel: str, thread_ts: str):
    replies = client.conversations_replies(channel=channel, ts=thread_ts)
    return ConversationReplies.from_dict(replies)


def bot_is_part_of_thread(event, client) -> bool:
    thread = retrieve_thread(client, event.channel, event.thread_ts)
    thread_parent: ThreadParent = thread.messages[0]
    print(thread.messages)
    bot_already_replied = False
    bot_was_mentioned = False
    bot_started_thread = thread_parent.user == 'U05K30V08U9'
    if thread_parent.reply_count < 6:
        bot_already_replied = 'U05K30V08U9' in thread_parent.reply_users
    if not bot_already_replied and not bot_started_thread:
        for message in thread.messages:
            if 'U05K30V08U9' in message.text:
                bot_already_replied = True
    return bot_already_replied or bot_was_mentioned or bot_started_thread
