import moonleap.props as props
from leap_mn.service import Service
from moonleap import Resource, output_dir_from, tags


class Dockerfile(Resource):
    def __init__(self):
        super().__init__()
        self.install_command = "apt-get install -y"


class DockerfileDev(Dockerfile):
    pass


class DockerImage(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name


@tags(["dockerfile"])
def create_dockerfile(term, block):
    return [Dockerfile()]


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
}
