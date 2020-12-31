from leap_mn.layerconfig import LayerConfig
from moonleap.config import reduce
from moonleap.resource import Always, Resource
from moonleap.utils import chop0


def get_layer_config():
    return {"DOCKER_COMPOSE": {"name": "<INSERT NAME>"}}


class DockerCompose(Resource):
    def __init__(self, name, is_dev):
        self.name = name
        self.is_dev = is_dev

    def describe(self):
        return {str(self): dict(is_dev=self.is_dev)}


def create(term, block):
    return [
        DockerCompose(name=term.data, is_dev=term.tag == "docker-compose-dev"),
    ]


@reduce(parent_resource=Always, resource=DockerCompose)
def create_layer_config(always, docker_compose):
    if docker_compose.term.tag == "docker-compose":
        return [LayerConfig("docker-compose", get_layer_config())]


# TODO: allow to add inferred terms to a block, based on the blocks contents
# From these inferred terms, resources can be created (e.g. root:layer is inferred from any other layer)


# TODO: publish a separate ontology that other vendors can support


tags = ["docker-compose", "docker-compose-dev"]
