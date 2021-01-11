import moonleap.props as props
import moonleap.rules as rules
from leap_mn.layerconfig import LayerConfig
from leap_mn.project import Project
from leap_mn.service import Service
from moonleap import Resource, chop0, output_dir_from, tags


def get_layer_config():
    return {"name": "<INSERT NAME>"}


class DockerCompose(Resource):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return "docker-compose"

    def dockerfile_name(self, service):
        return service.dockerfile.name if service.dockerfile else ""

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


class DockerComposeDev(DockerCompose):
    @property
    def name(self):
        return "docker-compose.dev"

    def dockerfile_name(self, service):
        return service.dockerfile_dev.name if service.dockerfile_dev else ""


@tags(["docker-compose"])
def create_docker_compose(term, block):
    docker_compose = DockerCompose()
    docker_compose.add_child(LayerConfig(dict(DOCKER_COMPOSE=get_layer_config())))

    return docker_compose


@tags(["docker-compose-dev"])
def create_docker_compose_dev(term, block):
    docker_compose_dev = DockerCompose()
    docker_compose_dev.add_child(
        LayerConfig(dict(DOCKER_COMPOSE_DEV=get_layer_config()))
    )

    return docker_compose_dev


meta = {
    DockerCompose: dict(
        output_dir=output_dir_from("project"),
        templates="templates",
        props={
            "services": props.children_of_type(Service),
            "project": props.parent_of_type(Project),
            "layer_config": props.child_of_type(LayerConfig),
        },
    ),
    DockerComposeDev: dict(
        output_dir=output_dir_from("project"),
        templates="templates-dev",
        props={
            "services": props.children_of_type(Service),
            "project": props.parent_of_type(Project),
            "layer_config": props.child_of_type(LayerConfig),
        },
    ),
}


def add_docker_compose_to_project(project, docker_compose):
    if project.config_layer:
        project.config_layer.add_child(docker_compose.layer_config)


rules = {
    "project": {
        ("has", "docker-compose"): add_docker_compose_to_project,
        ("has", "docker-compose-dev"): add_docker_compose_to_project,
    },
}
