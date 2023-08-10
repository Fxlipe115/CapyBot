from abc import ABC, abstractmethod
from pydantic import BaseModel

from assistant.types import AssistantAnswer


class CallableFunction(ABC, BaseModel):
    @abstractmethod
    def call(self) -> AssistantAnswer:
        pass
