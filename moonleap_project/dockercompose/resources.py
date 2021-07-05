import typing as T
from dataclasses import dataclass

from moonleap import Resource


@dataclass
class DockerCompose(Resource):
    is_dev: bool = False

    @property
    def name(self):
        return "docker-compose" + (".dev" if self.is_dev else ".prod")


@dataclass
class DockerComposeConfig(Resource):
    get_service_body: T.Callable
    get_global_body: T.Callable
    is_dev: bool = False
