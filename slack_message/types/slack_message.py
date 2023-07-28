from typing import List, NotRequired, TypedDict

from slack_message.types.blocks import Blocks


class Payload(TypedDict):
    text: str
    blocks: NotRequired[List[Blocks]]
    thread_ts: NotRequired[str]
    mrkdwn: NotRequired[bool]
