from leap_mn.service import Service
from moonleap import Resource, tags


class Dockerfile(Resource):
    def __init__(self, is_dev):
        super().__init__()


@tags(["docker-file"])
def create(term, block):
    return [Dockerfile()]


@tags(["docker-file-dev"])
def create(term, block):
    return [DockerfileDev()]


class DockerfileDev(Dockerfile):
    pass


meta = {
    Dockerfile: dict(templates="templates"),
    DockerfileDev: dict(templates="templates-dev"),
}
