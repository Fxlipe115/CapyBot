from typing import Any


class SlackEvent:
    event: str
    
    def __call__(self) -> Any:
        