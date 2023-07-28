from typing import List, Literal, NotRequired, TypedDict


class _CompositionObject(TypedDict):
    pass

class Text(_CompositionObject):
    type: Literal['plain_text', 'mrkdwn']
    text: str
    emoji: NotRequired[bool]
    verbatim: NotRequired[bool]

class ConfirmationDialog(_CompositionObject):
    title: Text
    text: Text
    confirm: Text
    deny: Text
    style: NotRequired[Literal['primary', 'danger']]

class Option(_CompositionObject):
    text: Text
    value: str
    description: NotRequired[Text]
    url: NotRequired[str]

class OptionGroup(_CompositionObject):
    label: Text
    options: List[Option]

class DispatchActionConfiguration(_CompositionObject):
    trigger_actions_on: NotRequired[List[Literal['on_enter_pressed', 
                                                 'on_character_entered']]]

class FilterForConversationLists(_CompositionObject):
    include: NotRequired[List[Literal['im',
                                      'mpim',
                                      'private',
                                      'public']]]
    exclude_external_shared_channels: NotRequired[bool]
    exclude_bot_users: NotRequired[bool]

class InputParameter(_CompositionObject):
    name: str
    value: str

class Trigger(_CompositionObject):
    url: str
    customizable_input_parameters: NotRequired[List[InputParameter]]

class Workflow(_CompositionObject):
    trigger: Trigger
