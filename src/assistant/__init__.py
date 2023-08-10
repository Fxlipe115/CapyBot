import dataclasses
from datetime import datetime
from functools import wraps
import json
from typing import Dict, List
import openai
from assistant.types import AssistantAnswer, ChatCompletionResponse, Context, ContextMessage, Roles

from assistant.functions import Functions


class Assistant():
    _contexts: Dict[str, Context]
    _functions: Functions
    _personality_traits: List[str]

    def __init__(self, openai_organization: str, openai_api_key: str) -> None:
        self._personality_traits = []
        self._functions = Functions()
        self._contexts = {}
        openai.organization = openai_organization
        openai.api_key = openai_api_key

    @property
    def model(self) -> str:
        return 'gpt-3.5-turbo-0613'

    @property
    def functions(self) -> Functions:
        return self._functions

    @property
    def contexts(self) -> Dict[str, Context]:
        return self._contexts

    def get_answer(self, message: str, context: str) -> AssistantAnswer:
        self.__add_message(Roles.USER, message, context)

        completion = self.__call_chat_gpt(context).choices[0]
        is_function_call = completion.finish_reason == 'function_call'
        if  is_function_call and completion.message.function_call is not None :
            function_call = completion.message.function_call
            function_name = function_call.name
            arguments = json.loads(function_call.arguments)
            self.__add_message(
                Roles.ASSISTANT,
                f'Function {function_name} called with arguments {function_call.arguments}',
                context
            )
            return self._functions.call_function(function_name, **arguments)
        else:
            content = completion.message.content
            self.__add_message(Roles.ASSISTANT, content, context)
            return AssistantAnswer(text=content)

    def set_personality_trait(self, personality_trait: str):
        print(f'Setting personality trait: {personality_trait}')
        self._personality_traits.append(personality_trait)

    def set_personality_traits(self, personality_traits: List[str]):
        list(map(self.set_personality_trait, personality_traits))

    def __get_context(self, context_key: str) -> Context:
        self.__delete_obsolete_contexts()
        if context_key not in self._contexts:
            print(f'Creating context {context_key}')
            self._contexts[context_key] = Context(
                messages=self.__personality())
        context = self._contexts[context_key]
        context.last_update_ts = datetime.now()
        return self._contexts[context_key]

    def __delete_obsolete_contexts(self) -> None:
        for context in self.__check_obsolete_contexts():
            print(f'Removing context {context}')
            self._contexts.pop(context)

    def __check_obsolete_contexts(self) -> List[str]:
        contexts = []
        for context in self._contexts:
            if self.__is_stale(context) or self.__is_obsolete(context):
                contexts.append(context)
        return contexts

    def __is_obsolete(self, context_key: str) -> bool:
        context = self._contexts[context_key]
        time_since_creation = datetime.now() - context.creation_ts
        print(
            f'Time since creation of context {context_key}: {time_since_creation}')
        return time_since_creation.days > 1

    def __is_stale(self, context_key: str) -> bool:
        context = self._contexts[context_key]
        time_since_update = datetime.now() - context.last_update_ts
        print(
            f'Time since context {context_key} was last used: {time_since_update}')
        return time_since_update.seconds > 60 * 30

    def __personality(self) -> List[ContextMessage]:
        personality_traits: List[ContextMessage] = []
        for personality_trait in self._personality_traits:
            personality_traits.append(
                ContextMessage(
                    role=Roles.SYSTEM,
                    content=personality_trait
                )
            )
        return personality_traits

    def __add_message(self, role: Roles, content: str, context: str):
        self.__get_context(context).messages.append(
            ContextMessage(role=role, content=content))

    def __call_chat_gpt(self, context: str) -> ChatCompletionResponse:
        return ChatCompletionResponse.from_dict(
            openai.ChatCompletion.create(
                model=self.model,
                messages=list(
                    map(dataclasses.asdict, self.__get_context(context).messages)),
                functions=self._functions.get_functions()
            )
        )

    def add_system_message(self, content: str, context: str):
        self.__add_message(Roles.SYSTEM, content, context)

    def add_user_message(self, content: str, context: str):
        self.__add_message(Roles.USER, content, context)

    def add_assistant_message(self, content: str, context: str):
        self.__add_message(Roles.ASSISTANT, content, context)
