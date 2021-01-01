from moonleap import Resource


class DockerfileDev(Resource):
    def __init__(self, name):
        self.name = name

    def describe(self):
        return dict(name=self.name)


def create(term, block):
    return [DockerfileDev(name=term.name)]


tags = ["dockerfile-dev"]
render_function_by_resource_type = []
