from resources.resource import Resource


class Dockerfile(Resource):
    def __init__(self, name):
        self.name = name


def describe(self, indent=0):
    return " " * indent + f"Dockerfile: name={self.name}"


class Builder:
    @staticmethod
    def create(term, line, block):
        return Dockerfile(term.data)


def pip_install_in_dockerfile(pip_package, try_resources):
    def action(term, line, block):
        for resource_name in try_resources:
            dockerfile = block.resource_by_name.get(resource_name)
            if dockerfile:
                dockerfile.add_pip_install(pip_package)
                return

    return action
