from typing import List, NotRequired, Optional, TypedDict, Union

from slack_message.types.blocks import Blocks


class AssistantAnswer(TypedDict):
        text: Union[str, dict]
        blocks: NotRequired[Optional[List[Blocks]]]