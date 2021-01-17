import typing as T
from dataclasses import dataclass

from moonleap import Resource


@dataclass
class DockerCompose(Resource):
    is_dev: bool = False

    @property
    def name(self):
        return "docker-compose" + (".dev" if self.is_dev else "")


@dataclass
class DockerComposeConfig(Resource):
    body: T.Union[dict, T.Callable]
    is_dev: bool = False

    def get_body(self):
        return self.body(self) if callable(self.body) else self.body
