from typing import List, NotRequired, Optional, TypedDict
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from slack_sdk.models.blocks import Block


class Payload(TypedDict):
    text: str
    blocks: NotRequired[List[Block]]
    thread_ts: NotRequired[str]
    mrkdwn: NotRequired[bool]

@dataclass_json
@dataclass
class Event:
    type: str
    event_ts: str
    user: str
    text: str
    ts: str
    channel: Optional[str] = None
    channel_type: Optional[str] = None


@dataclass
class Reply:
    user: str
    ts: str

@dataclass_json
@dataclass
class Message:
    type: str
    user: str
    text: str
    thread_ts: Optional[str]
    reply_count: Optional[int]
    replies: Optional[List[Reply]]
    ts: Optional[str]
    channel: Optional[str]
    event_ts: str
    channel_type: Optional[str]
