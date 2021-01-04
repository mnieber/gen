from leap_mn.layer import LayerConfig
from moonleap import Resource, chop0, derive


def get_layer_config():
    return {"DOCKER_COMPOSE": {"name": "<INSERT NAME>"}}


class DockerCompose(Resource):
    def __init__(self, name, is_dev):
        super().__init__()
        self.name = name + (".docker-compose" if is_dev else ".docker-compose.dev")
        self.is_dev = is_dev
        self.services = []

    def describe(self):
        return dict(is_dev=self.is_dev, services=[x.name for x in self.services])

    def add_service(self, service):
        self.services.append(service)


def create(term, block):
    return [
        DockerCompose(name=term.data, is_dev=term.tag == "docker-compose-dev"),
    ]


@derive(resource=DockerCompose)
def create_layer_config(docker_compose):
    if docker_compose.term.tag == "docker-compose":
        return [LayerConfig("docker-compose", get_layer_config())]
    return []


tags = ["docker-compose", "docker-compose-dev"]
templates_by_resource_type = [(DockerCompose, "templates")]
