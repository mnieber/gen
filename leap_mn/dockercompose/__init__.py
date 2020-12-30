from moonleap.resource import Resource


class DockerCompose(Resource):
    def __init__(self, is_dev):
        self.is_dev = is_dev

    def describe(self):
        return {str(self): dict(is_dev=self.is_dev)}


def create(term, line, block):
    return [DockerCompose(is_dev=term.tag == "docker-compose-dev")]


tags = ["docker-compose", "docker-compose-dev"]
