import typing as T
from dataclasses import dataclass

from moonleap import Resource
from moonleap_tools.tool import Tool


@dataclass
class SetupFile(Tool):
    pass


@dataclass
class SetupFileConfig(Resource):
    body: T.Union[dict, T.Callable]

    def get_body(self):
        return self.body() if callable(self.body) else self.body
