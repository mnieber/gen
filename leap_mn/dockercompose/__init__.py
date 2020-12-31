from leap_mn.layer import LayerConfig
from moonleap import Always, Resource, chop0, reduce


def get_layer_config():
    return {"DOCKER_COMPOSE": {"name": "<INSERT NAME>"}}


class DockerCompose(Resource):
    def __init__(self, name, is_dev):
        self.name = name
        self.is_dev = is_dev

    def describe(self):
        return dict(is_dev=self.is_dev)


def create(term, block):
    return [
        DockerCompose(name=term.data, is_dev=term.tag == "docker-compose-dev"),
    ]


@reduce(parent_resource=Always, resource=DockerCompose)
def create_layer_config(always, docker_compose):
    if docker_compose.term.tag == "docker-compose":
        return [LayerConfig("docker-compose", get_layer_config())]


tags = ["docker-compose", "docker-compose-dev"]
