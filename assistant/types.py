from dataclasses import dataclass
from typing import Dict, Optional, Sequence, Union
from slack_sdk.models.blocks import Block
from slack_sdk.models.attachments import Attachment
from slack_sdk.models.metadata import Metadata

@dataclass
class AssistantAnswer:
    text: Union[str, dict] = ""
    blocks: Optional[Sequence[Union[Dict, Block]]] = None
    attachments: Optional[Sequence[Union[Dict, Attachment]]] = None
    channel: Optional[str] = None
    as_user: Optional[bool] = None
    thread_ts: Optional[str] = None
    reply_broadcast: Optional[bool] = None
    unfurl_links: Optional[bool] = None
    unfurl_media: Optional[bool] = None
    icon_emoji: Optional[str] = None
    icon_url: Optional[str] = None
    username: Optional[str] = None
    mrkdwn: Optional[bool] = None
    link_names: Optional[bool] = None
    parse: Optional[str] = None  # none, full
    metadata: Optional[Union[Dict, Metadata]] = None
