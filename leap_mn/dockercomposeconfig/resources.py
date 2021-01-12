import typing as T
from dataclasses import dataclass

from moonleap import Resource


@dataclass
class DockerComposeConfig(Resource):
    body: T.Union[dict, T.Callable]

    def __repr__(self):
        return f"DockerComposeConfig name={self.name}"

    @property
    def name(self):
        return "/".join(self.get_body().keys())

    def get_body(self):
        return self.body(self) if callable(self.body) else self.body
