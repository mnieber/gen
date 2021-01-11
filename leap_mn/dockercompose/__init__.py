from dataclasses import dataclass

import moonleap.props as props
from leap_mn.layerconfig import LayerConfig
from moonleap import Resource, extend, output_dir_from, rule, tags


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
        body = dict(
            depends_on=[],
            image=f"{service.project.name}_{service.name}",
            ports=["80:80"],
        )

        if service.dockerfile:
            body["build"] = dict(
                context=f"./{service.name}", dockerfile=self.dockerfile_name(service)
            )

        return {service.name: body}


def get_layer_config(docker_compose):
    project = docker_compose.project
    suffix = "_dev" if docker_compose.is_dev else ""
    name = (project.name if project else "<INSERT NAME>") + suffix
    return {"DOCKER_COMPOSE" + suffix.upper(): {"name": name}}


@tags(["docker-compose"])
def create_docker_compose(term, block):
    docker_compose = DockerCompose()
    return docker_compose


@tags(["dev:docker-compose"])
def create_docker_compose_dev(term, block):
    docker_compose_dev = DockerCompose(is_dev=True)
    return docker_compose_dev


@rule(
    "project",
    "has",
    "docker-compose",
    description="""
Add docker-compose settings to the root config layer in the dodo configuration.""",
)
def project_has_docker_compose(project, docker_compose):
    layer_config = LayerConfig(lambda: get_layer_config(docker_compose))
    project.config_layer.add_to_layer_configs(layer_config)


def meta():
    from leap_mn.project import Project

    @extend(DockerCompose)
    class ExtendDockerCompose:
        output_dir = output_dir_from("project")
        templates = "templates"
        services = props.children("run", "service")
        project = props.parent(Project, "has", "docker-compose")

    return [ExtendDockerCompose]
