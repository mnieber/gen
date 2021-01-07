import moonleap.props as props
from leap_mn.layer import LayerConfig
from leap_mn.project import Project
from leap_mn.service import Service
from moonleap import Resource, chop0, derive, output_dir_from, tags


def get_layer_config():
    return {"DOCKER_COMPOSE": {"name": "<INSERT NAME>"}}


class DockerCompose(Resource):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return "docker-compose"

    def add_service(self, service):
        self.services.append(service)


class DockerComposeDev(DockerCompose):
    @property
    def name(self):
        return "docker-compose.dev"


@tags(["docker-compose"])
def create_docker_compose(term, block):
    return [
        DockerCompose(),
    ]


@tags(["docker-compose-dev"])
def create_docker_compose_dev(term, block):
    return [
        DockerComposeDev(),
    ]


@derive(DockerCompose)
def create_layer_config(docker_compose):
    return [LayerConfig("docker-compose", get_layer_config())]


meta = {
    DockerCompose: dict(
        output_dir=output_dir_from("project"),
        templates="templates",
        props={
            "services": props.children_of_type(Service),
            "project": props.parent_of_type(Project),
        },
    ),
    DockerComposeDev: dict(
        templates="templates-dev",
        props={"services": props.children_of_type(Service)},
    ),
}
