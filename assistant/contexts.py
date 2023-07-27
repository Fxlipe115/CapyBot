from typing import Dict

from assistant.assistant import Assistant


class Contexts:
    contexts: Dict[str, Assistant]
    
    def __init__(self) -> None:
        self.contexts = {}

    def get_assistant(self, context: str) -> Assistant:
        self.__delete_obsolete_contexts()
        if context not in self.contexts:
            self.contexts[context] = Assistant()
        return self.contexts[context]
    
    def __delete_obsolete_contexts(self) -> None:
        for context in self.contexts:
            if self.__is_obsolete(self.contexts[context]):
                self.contexts.pop(context)

    def __is_obsolete(self, context: str) -> bool:
        return False