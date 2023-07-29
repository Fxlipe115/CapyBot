from typing import Dict, NotRequired, Sequence, TypedDict, Union
from slack_sdk.models.blocks import Block


class AssistantAnswer(TypedDict):
    text: Union[str, dict]
    blocks: NotRequired[Sequence[Dict | Block]]
