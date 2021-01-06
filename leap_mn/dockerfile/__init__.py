from leap_mn.service import Service
from moonleap import Resource, output_dir_from, tags


class Dockerfile(Resource):
    def __init__(self):
        super().__init__()
        self.install_command = "apt-get install -y"


@tags(["dockerfile"])
def create(term, block):
    return [Dockerfile()]


@tags(["dockerfile-dev"])
def create(term, block):
    return [DockerfileDev()]


class DockerfileDev(Dockerfile):
    pass


meta = {
    Dockerfile: dict(
        templates="templates",
        output_dir=output_dir_from("service"),
        parents={"service": Service},
    ),
    DockerfileDev: dict(
        templates="templates-dev",
        output_dir=output_dir_from("service"),
        parents={"service": Service},
    ),
}
