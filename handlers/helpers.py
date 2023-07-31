from slack_sdk import WebClient

from slack_message.types import ConversationReplies, ThreadParent


def retrieve_message(client: WebClient, channel: str, ts: str):
    client.conversations_history(
        channel=channel,
        oldest=ts,
        inclusive=True,
        limit=1
    )

def retrieve_replies(client: WebClient, channel: str, thread_ts: str):
    replies = client.conversations_replies(channel=channel, ts=thread_ts)
    return ConversationReplies.from_dict(replies)

def bot_is_part_of_thread(event, client) -> bool:
    thread = retrieve_replies(client, event.channel, event.thread_ts)
    thread_parent: ThreadParent = thread.messages[0]
    if thread_parent.reply_count < 6:
        return 'U05K30V08U9' in thread_parent.reply_users
    return False
