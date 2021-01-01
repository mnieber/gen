from leap_mn.layer import LayerConfig
from moonleap import Always, Resource, chop0, reduce


def get_layer_config():
    return {"DOCKER_COMPOSE": {"name": "<INSERT NAME>"}}


class DockerCompose(Resource):
    def __init__(self, name, is_dev):
        self.name = name
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


@reduce(a_resource=DockerCompose, b_resource=Always)
def create_layer_config(docker_compose, always):
    if docker_compose.term.tag == "docker-compose":
        return [LayerConfig("docker-compose", get_layer_config())]


@reduce(a_resource=DockerCompose, b_resource="leap_mn.Service")
def add_service(docker_compose, service):
    if docker_compose.is_mentioned_in_same_line(service):
        docker_compose.add_service(service)


tags = ["docker-compose", "docker-compose-dev"]
render_function_by_resource_type = []
