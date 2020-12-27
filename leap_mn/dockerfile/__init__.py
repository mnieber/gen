from leap_mn.resource import Resource


class Dockerfile(Resource):
    def __init__(self, name):
        self.name = name


def describe(self, indent=0):
    return " " * indent + f"Dockerfile: name={self.name}"


def create(term, line, block):
    return Dockerfile("default")


def create_dev(term, line, block):
    return Dockerfile("dev")


def pip_install_in_dockerfile(block, pip_package, try_resources):
    for resource_name in try_resources:
        dockerfile = block.resource_by_name.get(resource_name)
        if dockerfile:
            dockerfile.add_pip_install(pip_package)
            return
