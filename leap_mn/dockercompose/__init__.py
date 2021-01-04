from leap_mn.layer import LayerConfig
from moonleap import Resource, chop0, derive, tags


def get_layer_config():
    return {"DOCKER_COMPOSE": {"name": "<INSERT NAME>"}}


class DockerCompose(Resource):
    def __init__(self, name, is_dev):
        super().__init__()
        self.name = name + (".docker-compose" if is_dev else ".docker-compose.dev")
        self.is_dev = is_dev
        self.services = []

    def add_service(self, service):
        self.services.append(service)


@tags(["docker-compose"])
def create(term, block):
    return [
        DockerCompose(name=term.data),
    ]


@tags(["docker-compose-dev"])
def create(term, block):
    return [
        DockerComposeDev(name=term.data),
    ]


@derive(DockerCompose)
def create_layer_config(docker_compose):
    if docker_compose.term.tag == "docker-compose":
        return [LayerConfig("docker-compose", get_layer_config())]
    return []


meta = {
    DockerCompose: {"templates": "templates"},
    DockerComposeDev: {"templates": "templates-dev"},
}
