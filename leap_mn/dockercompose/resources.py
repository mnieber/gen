import typing as T
from dataclasses import dataclass

from moonleap import Resource


@dataclass
class DockerCompose(Resource):
    is_dev: bool = False

    @property
    def name(self):
        return "docker-compose" + (".dev" if self.is_dev else "")

    def dockerfile_name(self, service):
        dockerfile = service.dockerfile_dev if self.is_dev else service.dockerfile
        return dockerfile.name if dockerfile else ""

    def config(self, service):
        volumes = dict(volumes=[f"./{service.name}:/app/src"])

        body = dict(
            depends_on=[],
            image=f"{service.project.name}_{service.name}",
            ports=["80:80"],
            **(volumes if self.is_dev else {}),
        )

        if service.dockerfile:
            body["build"] = dict(
                context=f"./{service.name}", dockerfile=self.dockerfile_name(service)
            )

        return {service.name: body}


@dataclass
class DockerComposeConfig(Resource):
    body: T.Union[dict, T.Callable]

    def get_body(self):
        return self.body(self) if callable(self.body) else self.body
