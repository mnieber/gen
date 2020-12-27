from leap_mn.resource import Resource


class DockerCompose(Resource):
    def __init__(self, name):
        self.name = name

    def describe(self, indent=0):
        return " " * indent + f"DockerCompose: name={self.name}"


def create(term, line, block):
    return DockerCompose("default")


def create_dev(term, line, block):
    return DockerCompose("dev")
