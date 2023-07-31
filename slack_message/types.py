from typing import Any, Dict, List, NotRequired, Optional, TypedDict, Union
from dataclasses import dataclass
from slack_sdk.web import SlackResponse

from slack_sdk.models.blocks import Block


class Payload(TypedDict):
    text: str
    blocks: NotRequired[List[Block]]
    thread_ts: NotRequired[str]
    mrkdwn: NotRequired[bool]

@dataclass
class Event:
    type: str
    event_ts: str
    user: str
    text: str
    ts: str
    channel: Optional[str] = None
    channel_type: Optional[str] = None

    @classmethod
    def from_dict(cls, other: Dict[str, Any]):
        return Event(
            type=other['type'],
            event_ts=other['event_ts'],
            user=other['user'],
            text=other['text'],
            ts=other['ts'],
            channel=other.get('channel'),
            channel_type=other.get('channel_type')
        )


@dataclass
class Reply:
    user: str
    ts: str
    
    @classmethod
    def from_dict(cls, other: Dict[str, Any]):
        return Reply(
            user=other['user'],
            ts=other['ts']
        )

@dataclass
class Message:
    type: str
    user: str
    text: str
    event_ts: str
    channel: str
    ts: str
    thread_ts: Optional[str] = None
    reply_count: Optional[int] = None
    replies: Optional[List[Reply]] = None
    channel_type: Optional[str] = None

    @classmethod
    def from_dict(cls, other: Dict[str, Any]):
        return Message(
            type=other['type'],
            user=other['user'],
            text=other['text'],
            event_ts=other['event_ts'],
            channel=other['channel'],
            thread_ts=other.get('thread_ts'),
            reply_count=other.get('reply_count'),
            replies=None if other.get('replies') is None else list(map(Reply.from_dict, other['replies'])),
            ts=other['ts'],
            channel_type=other.get('channel_type')
        )


@dataclass
class ThreadParent:
    type: str
    user: str
    text: str
    thread_ts: str
    reply_count: int
    reply_users: List[str] #max 5
    reply_users_count: int
    latest_reply: str
    subscribed: bool
    ts: str
    unread_count: Optional[int] = None
    last_read: Optional[str] = None
    replies: Optional[List[Reply]] = None #deprecated

    @classmethod
    def from_dict(cls, other: Dict[str, Any]):
        return ThreadParent(
            type=other['type'],
            user=other['user'],
            text=other['text'],
            thread_ts=other['thread_ts'],
            reply_count=other['reply_count'],
            reply_users=other['reply_users'],
            reply_users_count=other['reply_users_count'],
            latest_reply=other['latest_reply'],
            subscribed=other['subscribed'],
            last_read=other.get('last_read'),
            unread_count=other.get('unread_count'),
            ts=other['ts'],
            replies=None if other.get('replies') is None else list(map(Reply.from_dict, other['replies']))
        )

@dataclass
class ThreadReply:
    type: str
    user: str
    text: str
    thread_ts: str
    parent_user_id: str
    ts: str

    @classmethod
    def from_dict(cls, other: Dict[str, Any]):
        return ThreadReply(
            type=other['type'],
            user=other['user'],
            text=other['text'],
            thread_ts=other['thread_ts'],
            parent_user_id=other['parent_user_id'],
            ts=other['ts']
        )

@dataclass
class ResponseMetadata:
    next_cursor: str

    @classmethod
    def from_dict(cls, other: Dict[str, Any]):
        return ResponseMetadata(
            next_cursor=other['next_cursor']
        )

@dataclass
class ConversationReplies:
    ok: bool
    messages: List[Union[ThreadParent, ThreadReply]]
    has_more: bool
    response_metadata: Optional[ResponseMetadata]

    @classmethod
    def from_dict(cls, other: Union[Dict[str, Any], SlackResponse]):
        return ConversationReplies(
            ok=other['ok'],
            messages=list(map(lambda x: ThreadParent.from_dict(x) if x.get('reply_count') is not None else ThreadReply.from_dict(x), other['messages'])),
            has_more=other['has_more'],
            response_metadata=None if other.get('response_metadata') is None else ResponseMetadata.from_dict(other['response_metadata'])
        )
