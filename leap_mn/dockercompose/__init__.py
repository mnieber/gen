import moonleap.props as props
from leap_mn.layerconfig import LayerConfig
from leap_mn.project import Project
from leap_mn.service import Service
from moonleap import Resource, chop0, derive, output_dir_from, tags


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
    return [LayerConfig(dict(DOCKER_COMPOSE=get_layer_config()))]


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
        output_dir=output_dir_from("project"),
        templates="templates-dev",
        props={
            "services": props.children_of_type(Service),
            "project": props.parent_of_type(Project),
        },
    ),
}
