from moonleap.resource import Resource


class DockerfileDev(Resource):
    def __init__(self, name):
        self.name = name

    def describe(self):
        return {str(self): dict(name=self.name)}


def create(term, block):
    return [DockerfileDev(name=term.name)]


tags = ["dockerfile-dev"]
