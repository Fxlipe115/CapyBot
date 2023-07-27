import time
from datetime import datetime, timedelta
from typing import Dict, TypedDict, List

from assistant.assistant import Assistant


class Contexts:
    class AssistantWithCreationTime(TypedDict):
        assistant: Assistant
        creationTimeStamp: datetime
        lastUpdatedTimeStamp: datetime


    contexts: Dict[str, AssistantWithCreationTime]
    

    def __init__(self) -> None:
        self.contexts = {}


    def get_assistant(self, context: str) -> Assistant:
        self.__delete_obsolete_contexts()
        if context not in self.contexts:
            print(f'Creating context {context}')
            self.contexts[context] = {
                'assistant': Assistant(),
                'creationTimeStamp': datetime.now()
            }
        assistant = self.contexts[context]
        assistant['lastUpdatedTimeStamp'] = datetime.now()
        return self.contexts[context]['assistant']
    
    
    def __delete_obsolete_contexts(self) -> None:
        for context in self.__check_obsolete_contexts():
            print(f'Removing context {context}')
            self.contexts.pop(context)


    def __check_obsolete_contexts(self) -> List[str]:
        contexts = []
        for context in self.contexts:
            if self.__is_stale(context) or self.__is_obsolete(context):
                contexts.append(context)
        return contexts
                
                
    def __is_obsolete(self, context: str) -> bool:
        assistant = self.contexts[context]
        time_since_creation = datetime.now() - assistant['creationTimeStamp']
        print(f'Time since creation of context {context}: {time_since_creation}')
        return time_since_creation.days > 1
    

    def __is_stale(self, context: str) -> bool:
        assistant = self.contexts[context]
        time_since_update = datetime.now() - assistant['lastUpdatedTimeStamp']
        print(f'Time context {context} was last used: {time_since_update}')
        return time_since_update.seconds > 60 * 30