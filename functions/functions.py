import json
from typing import Any, List, Type
from functions.callable_function import CallableFunction
from typing import Dict, TypedDict

class FunctionDescription(TypedDict):
    name: str
    description: str
    parameters: dict[str, Any]

ClassReference = Type[CallableFunction]

class FunctionDescriptionAndClass(TypedDict):
    description: FunctionDescription
    callableFunction: CallableFunction

class Functions:
    functions: Dict[str, FunctionDescriptionAndClass]

    def __init__(self) -> None:
        self.functions = dict()

    def register(self, name: str, description: str, function: CallableFunction):
        self.functions[name] = {
            'description': {
                'name': name,
                'description': description,
                'parameters': function.model_json_schema()
            },
            'callableFunction': function
        }

    def get_functions(self) -> List[FunctionDescription]:
        return list(map(lambda x: x['description'], self.functions.values()))
    
    def call_function(self, function_name: str, **arguments: Any) -> str:
        completion_function = self.functions.get(function_name)
        return completion_function['callableFunction'](**arguments).call()
