from typing import Any, List, Type
from typing import Dict, TypedDict
from functions.callable_function import CallableFunction


class FunctionDescription(TypedDict):
    name: str
    description: str
    parameters: dict[str, Any]


class FunctionDescriptionAndClass(TypedDict):
    description: FunctionDescription
    callableFunction: Type[CallableFunction]


class Functions:
    functions: Dict[str, FunctionDescriptionAndClass]

    def __init__(self) -> None:
        self.functions = dict()

    def register(self, name: str, description: str, function: Type[CallableFunction]):
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
        if completion_function is not None:
            return completion_function['callableFunction'](**arguments).call()
        else:
            return ''
