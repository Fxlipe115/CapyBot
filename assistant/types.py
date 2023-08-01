from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Union
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


class Roles(str, Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'
    FUNCTION = 'function'


@dataclass_json
@dataclass
class FunctionCall:
    name: str
    arguments: str

    @classmethod
    def from_dict(cls, other: Dict[str, Any]):
        return FunctionCall(
            name=other['name'],
            arguments=other['arguments']
        )


@dataclass
class Message:
    content: str
    role: Roles
    function_call: Optional[FunctionCall] = None

    @classmethod
    def from_dict(cls, other: Dict[str, Any]):
        return Message(
            content=other['content'],
            role=other['role'],
            function_call=FunctionCall.from_dict(other['function_call']) if other.get(
                'function_call') is not None else None
        )


class FinishReason(str, Enum):
    STOP = 'stop'
    LENGTH = 'length'
    FUNCTION_CALL = 'function_call'
    CONTENT_FILTER = 'content_filter'
    NULL = 'null'


@dataclass_json
@dataclass
class Choice:
    finish_reason: FinishReason
    index: int
    message: Message

    @classmethod
    def from_dict(cls, other: Dict[str, Any]):
        return Choice(
            finish_reason=other['finish_reason'],
            index=other['index'],
            message=Message.from_dict(other['message'])
        )


@dataclass_json
@dataclass
class Usage:
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


@dataclass
class ChatCompletionResponse:
    choices: List[Choice]
    created: int
    id: str
    model: str
    usage: Usage
    object: str = 'chat.completion'

    @classmethod
    def from_dict(cls, other: Dict[str, Any]):
        return ChatCompletionResponse(
            choices=list(map(Choice.from_dict, other['choices'])),
            created=other['created'],
            id=other['id'],
            model=other['model'],
            usage=other['usage'],
            object=other['object']
        )


@dataclass_json
@dataclass
class ContextMessage:
    content: str
    role: Roles


@dataclass_json
@dataclass
class Context:
    messages: List[ContextMessage]
    creation_ts: datetime = datetime.now()
    last_update_ts: datetime = datetime.now()
