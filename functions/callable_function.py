from abc import ABC, abstractmethod
from pydantic import BaseModel


class CallableFunction(ABC, BaseModel):
    @abstractmethod
    def call(self) -> str:
        pass
