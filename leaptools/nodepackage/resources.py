import typing as T
from dataclasses import dataclass

from moonleap.resource import Resource


@dataclass
class NodePackage(Resource):
    pass


@dataclass
class NodePackageConfig(Resource):
    body: T.Union[dict, T.Callable]

    def get_body(self):
        return self.body(self) if callable(self.body) else self.body
