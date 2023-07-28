from typing import List, NotRequired, TypedDict

from slack_sdk.models.blocks import Block


class Payload(TypedDict):
    text: str
    blocks: NotRequired[List[Block]]
    thread_ts: NotRequired[str]
    mrkdwn: NotRequired[bool]
