import typing as T
from dataclasses import dataclass

from moonleap import Resource


@dataclass
class SetupFile(Resource):
    pass


@dataclass
class SetupFileConfig(Resource):
    body: T.Union[dict, T.Callable]

    def get_body(self):
        return self.body() if callable(self.body) else self.body
