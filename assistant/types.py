from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Literal, Optional, Sequence, Union
from dataclasses_json import dataclass_json
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

Roles = Literal['system', 'user', 'assistant', 'function']

@dataclass
class FunctionCall:
    name: str
    description: str
    arguments: str

@dataclass
class Message:
    content: str
    role: Roles
    function_call: Optional[FunctionCall] = None

FinishReason = Literal['stop', 'length', 'function_call', 'content_filter', 'null']

@dataclass
class Choice:
    finish_reason: FinishReason
    index: int
    message: Message

@dataclass
class Usage:
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

@dataclass_json
@dataclass
class ChatCompletionResponse:
    choices: List[Choice]
    created: int
    id: str
    model: str
    usage: Usage
    object: str = 'chat.completion'

@dataclass
class ContextMessage:
    content: str
    role: Roles

@dataclass
class Context:
    messages: List[ContextMessage]
    creation_ts: datetime = datetime.now()
    last_update_ts: datetime = datetime.now()