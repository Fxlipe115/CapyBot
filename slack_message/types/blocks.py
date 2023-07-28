from typing import List, Literal, NotRequired, TypedDict

from slack_message.types.block_elements import _BlockElement, CheckBoxGroupsElement, DatePickerElement, ImageElement, MultiSelectMenuElement, PlaintTextInputElement, RadioButtonGroupElement, SelectMenuElement, Text



class _Block(TypedDict):
    type: Literal['actions', 'context', 'divider', 'file', 'header', 'image', 'input', 'section', 'video']
    block_id: NotRequired[str]


class ActionBlock(_Block):
    elements: List[_BlockElement]


class ContextBlock(_Block):
    elements: List[Text | ImageElement]


class DividerBlock(_Block):
    pass


class FileBlock(_Block):
    external_id: str
    source: str


class HeaderBlock(_Block):
    text: Text


class ImageBlock(_Block):
    image_url: str
    alt_text: str
    title: NotRequired[Text]


class InputBlock(_Block):
    label: Text
    element: PlaintTextInputElement | \
             CheckBoxGroupsElement | \
             RadioButtonGroupElement | \
             SelectMenuElement | \
             MultiSelectMenuElement | \
             DatePickerElement
    dispatch_action: NotRequired[bool]
    hint: NotRequired[Text]
    optional: NotRequired[bool]


class SectionBlock(_Block):
    text: NotRequired[Text] #if fields is filled
    fields: NotRequired[List[Text]] #if text is filled
    accessory: NotRequired[_BlockElement]

class VideoBlock(_Block):
    alt_text: str
    author_name: NotRequired[str]
    description: NotRequired[Text]
    provider_icon_url: NotRequired[str]
    provider_name: NotRequired[str]
    title: Text
    title_url: NotRequired[str]
    thumbnail_url: str
    video_url: str

Blocks = ActionBlock | \
         ContextBlock | \
         DividerBlock | \
         FileBlock | \
         HeaderBlock | \
         ImageBlock | \
         InputBlock | \
         SectionBlock | \
         VideoBlock
