import typing as T
from dataclasses import dataclass

from moonleap import Resource, get_session


@dataclass
class DockerCompose(Resource):
    @property
    def override_fn(self):
        return get_session().get_setting_or(
            "docker-compose.dev.override.yml", ["project", "docker_compose_override_fn"]
        )


@dataclass
class DockerComposeConfig(Resource):
    get_service_body: T.Callable
    get_global_body: T.Callable
    target: str
    is_override: bool
