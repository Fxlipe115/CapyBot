import dataclasses
from datetime import datetime
from functools import wraps
import json
import os
from typing import Callable, Dict, List, Literal, TypedDict
import openai
from assistant.types import AssistantAnswer, ChatCompletionResponse, Context, ContextMessage, Message, Roles

from functions.functions import Functions
from functions.generate_image import GenerateImage
from functions.weather_report import WeatherReport

class Assistant():
    _contexts: Dict[str, Context]
    _functions: Functions
    _personality_traits: List[str]

    def __init__(self) -> None:
        self._personality_traits = []
        self._functions = Functions()
        self._contexts = {}

    @property
    def model(self) -> str:
        return 'gpt-3.5-turbo-0613'
    
    @property
    def functions(self) -> Functions:
        return self._functions

    def get_answer(self, message: str, user_talking: str, context: str) -> AssistantAnswer:
        openai.organization = os.getenv('OPENAI_ORGANIZATION')
        openai.api_key = os.getenv('OPENAI_API_KEY')

        self.__add_message(
            'system',
            f'The name of the person talking to you is <@{user_talking}>!',
            context)
        self.__add_message('user', message, context)

        completion = self.__call_chat_gpt(context).choices[0]

        if completion.finish_reason == 'function_call' and completion.message.function_call is not None:
            function_call = completion.message.function_call
            function_name = function_call.name
            arguments = json.loads(function_call.arguments)
            return self._functions.call_function(function_name, **arguments)
        else:
            content = completion.message.content
            self.__add_message('assistant', content, context)
            return AssistantAnswer(text=content)

    def set_personality_trait(self, personality_trait: str):
        self._personality_traits.append(personality_trait)
            
    def __get_context(self, context: str) -> Context:
        self.__delete_obsolete_contexts()
        if context not in self._contexts:
            print(f'Creating context {context}')
            self._contexts[context] = Context(messages=self.__personality())
        existing_context = self._contexts[context]
        existing_context.last_update_ts = datetime.now()
        return self._contexts[context]
    
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
        personality_traits: List[ContextMessage] = [
            ContextMessage(
                role='system',
                content='You are a helpful and friendly capybara assistant for Team Capybara.'
            ),
            ContextMessage(
                role='system',
                content='Your name is <@U05K30V08U9>.'
            ),
            ContextMessage(
                role='system',
                content='You are a Slack bot.'
            ),
            ContextMessage(
                role='system',
                content='Every time someone makes a conversation, it is directed to you.'
            ),
            ContextMessage(
                role='system',
                content='You were created by Felipe Graeff.'
            ),
            ContextMessage(
                role='system',
                content='You are native to Rio Grande do Sul, Brazil.'
            ),
            ContextMessage(
                role='system',
                content='When answering in portuguese you speak with the dialect of Rio Grande do Sul in Brazil.'
            ),
            ContextMessage(
                role='system',
                content='You answer with capybara puns.'
            ),
            ContextMessage(
                role='system',
                content='You use a lot of emojis in your answers.'
            )
        ]
        for personality_trait in self._personality_traits:
            personality_traits.append(
                ContextMessage(
                    role='system',
                    content=personality_trait
                )
            )
        return personality_traits

    def __add_message(self, role: Roles, content: str, context: str):
        self.__get_context(context).messages.append(ContextMessage(role=role, content=content))

    def __call_chat_gpt(self, context: str) -> ChatCompletionResponse:
        return ChatCompletionResponse.from_dict(
            openai.ChatCompletion.create(
                model=self.model,
                messages=list(map(dataclasses.asdict, self.__get_context(context).messages)),
                functions=self._functions.get_functions()
            )
        )
