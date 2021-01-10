import moonleap.props as props
from leap_mn.layer import LayerConfig
from leap_mn.service import Service
from moonleap import Resource, output_dir_from, tags


class Dockerfile(Resource):
    def __init__(self):
        super().__init__()
        self.install_command = "apt-get install -y"

    @property
    def name(self):
        return "Dockerfile"


class DockerfileDev(Dockerfile):
    @property
    def name(self):
        return "Dockerfile.dev"


class DockerImage(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name


def get_layer_config(docker_file):
    service = docker_file.service
    project = service.project

    return {"*": {"container": f"{project.name}_{service.name}_1"}}


@tags(["dockerfile"])
def create_dockerfile(term, block):
    docker_file = Dockerfile()
    return [
        docker_file,
        LayerConfig(lambda x: dict(DOCKER_OPTIONS=get_layer_config(docker_file))),
    ]


@tags(["dockerfile-dev"])
def create_dockerfile_dev(term, block):
    return [DockerfileDev()]


@tags(["docker-image"])
def create_docker_image(term, block):
    return [DockerImage(term.data)]


meta = {
    Dockerfile: dict(
        templates="templates",
        output_dir=output_dir_from("service"),
        props={
            "service": props.parent_of_type(Service),
            "image": props.child_of_type(DockerImage),
        },
    ),
    DockerfileDev: dict(
        templates="templates-dev",
        output_dir=output_dir_from("service"),
        props={
            "service": props.parent_of_type(Service),
            "image": props.child_of_type(DockerImage),
        },
    ),
    Service: dict(
        props={
            "dockerfile": props.child_of_type(Dockerfile),
            "dockerfile_dev": props.child_of_type(DockerfileDev),
        },
    ),
}
