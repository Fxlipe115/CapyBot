import time
from datetime import datetime, timedelta
from typing import Dict, TypedDict

from assistant.assistant import Assistant


class Contexts:
    class AssistantWithCreationTime(TypedDict):
        assistant: Assistant
        creationTimeStamp: datetime

    contexts: Dict[str, AssistantWithCreationTime]
    
    def __init__(self) -> None:
        self.contexts = {}

    def get_assistant(self, context: str) -> Assistant:
        self.__delete_obsolete_contexts()
        if context not in self.contexts:
            self.contexts[context] = {
                'assistant': Assistant(),
                'creationTimeStamp': datetime.now()
            }
        return self.contexts[context]['assistant']
    
    def __delete_obsolete_contexts(self) -> None:
        for context in self.contexts:
            if self.__is_obsolete(self.contexts[context]):
                self.contexts.pop(context)

    def __is_obsolete(self, context: AssistantWithCreationTime) -> bool:
        return (context['creationTimeStamp'] - datetime.now()).