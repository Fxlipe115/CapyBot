from typing import List, NotRequired, TypedDict, Union
from slack_sdk.models.blocks import Block


class AssistantAnswer(TypedDict):
    text: Union[str, dict]
    blocks: NotRequired[List[Block]]
