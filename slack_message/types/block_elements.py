from typing import List, Literal, NotRequired, TypedDict

from slack_message.types.composition_objects import ConfirmationDialog, DispatchActionConfiguration, FilterForConversationLists, Option, OptionGroup, Text, Workflow


class _BlockElement(TypedDict):
    type: Literal[
        'button',
        'checkboxes',
        'datepicker',
        'datetimepicker',
        'email_text_input',
        'image',
        'multi_static_select',
        'multi_external_select',
        'multi_users_select',
        'multi_conversations_select',
        'multi_channels_select',
        'number_input',
        'overflow',
        'plain_text_input',
        'radio_buttons',
        'static_select',
        'external_select',
        'users_select',
        'conversations_select',
        'channels_select',
        'timepicker',
        'url_text_input',
        'workflow_button'
    ]

class _Action(TypedDict):
    action_id: str

class _Confirmable(TypedDict):
    confirm: NotRequired[ConfirmationDialog]

class _Focusable(TypedDict):
    focus_on_load: NotRequired[bool]

class _HasPlaceholder(TypedDict):
    placeholder: NotRequired[Text]

class _Dispatchable(TypedDict):
    dispatch_action_config: NotRequired[DispatchActionConfiguration]

class _HasOptions(TypedDict):
    options: List[Option]

class _HasInitialOptions(TypedDict):
    initial_options: NotRequired[List[Option]]

class _HasOptionGroups(TypedDict):
    option_groups: NotRequired[List[OptionGroup]]

class _Button(
    _BlockElement):
    text: Text
    style: NotRequired[Literal['primary', 'danger']]
    accessibility_label: NotRequired[str]

class ButtonElement(
    _Button,
    _Action,
    _Confirmable):
    url: NotRequired[str]
    value: NotRequired[str]


class CheckBoxGroupsElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _Focusable,
    _HasOptions,
    _HasInitialOptions):
    pass

class DatePickerElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _Focusable,
    _HasPlaceholder):
    initial_date: NotRequired[str]

class DateTimePickerElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _Focusable):
    initial_date_time: NotRequired[int]

class EmailInputElement(
    _BlockElement,
    _Action,
    _Focusable,
    _HasPlaceholder,
    _Dispatchable):
    initial_value: NotRequired[str]

class ImageElement(_BlockElement):
    image_url: str
    alt_text: str

class MultiSelectMenuStaticElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _Focusable,
    _HasPlaceholder,
    _HasOptions,
    _HasInitialOptions,
    _HasOptionGroups):
    max_selected_items: NotRequired[int]

class MultiSelectMenuExternalElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _Focusable,
    _HasPlaceholder,
    _HasInitialOptions):
    min_query_length: NotRequired[int]
    max_selected_items: NotRequired[int]

class MultiSelectMenuUserListElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _Focusable,
    _HasPlaceholder):
    initial_users: NotRequired[List[str]]
    max_selected_items: NotRequired[int]

class MultiSelectMenuConversationListElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _Focusable,
    _HasPlaceholder):
    initial_conversations: NotRequired[List[str]]
    default_to_current_conversation: NotRequired[bool]
    max_selected_items: NotRequired[int]
    filter: NotRequired[FilterForConversationLists]

class MultiSelectMenuChannelsListElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _Focusable,
    _HasPlaceholder):
    initial_channels: NotRequired[List[str]]
    max_selected_items: NotRequired[int]

MultiSelectMenuElement = MultiSelectMenuStaticElement | \
                         MultiSelectMenuExternalElement | \
                         MultiSelectMenuUserListElement | \
                         MultiSelectMenuConversationListElement | \
                         MultiSelectMenuChannelsListElement

class NumberInputElement(_BlockElement,
                         _Action,
                         _Dispatchable,
                         _Focusable,
                         _HasPlaceholder):
    is_decimal_allowed: bool
    initial_value: NotRequired[str]
    min_value: NotRequired[str]
    max_value: NotRequired[str]

class OverflowMenuElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _HasOptions):
    pass

class PlaintTextInputElement(
    _BlockElement,
    _Action,
    _Dispatchable,
    _Focusable,
    _HasPlaceholder):
    initial_value: NotRequired[str]
    multiline: NotRequired[bool]
    min_length: NotRequired[int]
    max_length: NotRequired[int]

class RadioButtonGroupElement(
    _BlockElement,
    _Action,
    _HasOptions,
    _HasInitialOptions,
    _Confirmable,
    _Focusable):
    pass

class SelectMenuStaticElement(
    _BlockElement,
    _Action,
    _HasOptions,
    _HasOptionGroups,
    _HasInitialOptions,
    _Confirmable,
    _Focusable,
    _HasPlaceholder):
    pass

class SelectMenuExternalElement(
    _BlockElement,
    _Action,
    _HasInitialOptions,
    _Confirmable,
    _Focusable,
    _HasPlaceholder):
    min_query_length: NotRequired[int]

class SelectMenuUsersElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _Focusable,
    _HasPlaceholder):
    initial_user: NotRequired[str]

class SelectMenuConversationsElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _Focusable,
    _HasPlaceholder):
    initial_conversation: NotRequired[str]
    default_to_current_conversation: NotRequired[bool]
    response_url_enabled: NotRequired[bool]
    filter: NotRequired[FilterForConversationLists]

class SelectMenuChannelsElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _Focusable,
    _HasPlaceholder):
    initial_channel: NotRequired[str]
    response_url_enabled: NotRequired[bool]

SelectMenuElement = SelectMenuStaticElement | \
                    SelectMenuExternalElement | \
                    SelectMenuUsersElement | \
                    SelectMenuConversationsElement | \
                    SelectMenuChannelsElement

class TimePickerElement(
    _BlockElement,
    _Action,
    _Confirmable,
    _Focusable,
    _HasPlaceholder):
    initial_time: NotRequired[str]
    timezone: NotRequired[str]

class URLInputElement(
    _BlockElement,
    _Action,
    _Dispatchable,
    _Focusable,
    _HasPlaceholder):
    initial_value: NotRequired[str]

class WorkflowButtonElement(
    _Button):
    workflow: Workflow
