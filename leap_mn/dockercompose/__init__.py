from leap_mn.layerconfig import LayerConfig
from moonleap.resource import Resource
from moonleap.utils import chop0


def get_layer_config():
    return {"DOCKER_COMPOSE": {"name": "<INSERT NAME>"}}


class DockerCompose(Resource):
    def __init__(self, name, is_dev):
        self.name = name
        self.is_dev = is_dev

    def describe(self):
        return {str(self): dict(is_dev=self.is_dev)}


def create(term, line, block):
    return [
        DockerCompose(name=term.data, is_dev=term.tag == "docker-compose-dev"),
        term.tag == "docker-compose"
        and LayerConfig("docker-compose", get_layer_config()),
    ]


# TODO: create a reduce rule with parent=always that creates the layer config,
# such that the new layerconfig is itself also reduced.
# This allows us to decouple (if wanted) the creation of the layer config from the
# creation of the docker-compose


# TODO: let parent resource respond immediately to the creation of child resources
# Simplify by strictly requiring parent resources to exist before child resources


# TODO: publish a separate ontology that other vendors can support


tags = ["docker-compose", "docker-compose-dev"]
